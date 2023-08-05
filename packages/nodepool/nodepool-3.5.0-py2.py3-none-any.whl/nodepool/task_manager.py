#!/usr/bin/env python

# Copyright (C) 2011-2013 OpenStack Foundation
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#    http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or
# implied.
#
# See the License for the specific language governing permissions and
# limitations under the License.

import threading
import logging
import re
import queue
import time

from openstack import task_manager as openstack_task_manager

from nodepool import stats


def _transform_task_name(task_name):
    # Transform openstacksdk internal task name to something more
    # suitable for sending to statsd for tracking; e.g.
    #
    #  compute.DELETE.servers -> ComputeDeleteServers
    #  compute.POST.os-volumes_boot -> ComputePostOsVolumesBoot
    parts = re.split('[.\-_]', task_name)
    return "".join(
        [part.lower().capitalize() for part in parts]
    )


class TaskManager(openstack_task_manager.TaskManager):
    log = logging.getLogger("nodepool.TaskManager")

    def __init__(self, name, rate, workers=5):
        super(TaskManager, self).__init__(name=name, workers=workers)
        self.daemon = True
        self.queue = queue.Queue()
        self._running = True
        self.rate = float(rate)
        self.statsd = stats.get_client()
        self._thread = threading.Thread(name=name, target=self.run)
        self._thread.daemon = True

    def start(self):
        self._thread.start()

    def stop(self):
        self._running = False
        self.queue.put(None)

    def join(self):
        self._thread.join()

    def run(self):
        last_ts = 0
        try:
            while True:
                task = self.queue.get()
                if not task:
                    if not self._running:
                        break
                    continue
                while True:
                    delta = time.time() - last_ts
                    if delta >= self.rate:
                        break
                    time.sleep(self.rate - delta)
                self.log.debug("Manager %s running task %s (queue %s)" %
                               (self.name,
                                _transform_task_name(task.name),
                                self.queue.qsize()))
                self.run_task(task)
                self.queue.task_done()
        except Exception:
            self.log.exception("Task manager died.")
            raise

    def post_run_task(self, elapsed_time, task):
        task_name = _transform_task_name(task.name)
        self.log.debug(
            "Manager %s ran task %s in %ss" %
            (self.name, task_name, elapsed_time))

        if self.statsd:
            # nodepool.task.PROVIDER.TASK_NAME
            key = 'nodepool.task.%s.%s' % (self.name, task_name)
            self.statsd.timing(key, int(elapsed_time * 1000))
            self.statsd.incr(key)

import os
import os.path as osp
import time

import numpy as np
import tensorflow as tf
from tensorflow.core.util import event_pb2
from tensorflow.python import pywrap_tensorflow
from tensorflow.python.util import compat


class EventsFileWriterWrapper:
    """
    Rename EventsFileWriter's flush() and add_event() methods to be consistent
    with EventsWriter's methods.
    """

    def __init__(self, events_file_writer):
        self.writer = events_file_writer

    def WriteEvent(self, event):
        self.writer.add_event(event)

    def Flush(self):
        self.writer.flush()


class Logger(object):
    DEFAULT = None

    def __init__(self, log_dir=None, writer=None):
        self.key_steps = {}
        self.rate_values = {}

        if log_dir is None and writer is None:
            log_dir = 'logs'
            self.set_log_dir(log_dir)
        elif log_dir is not None and writer is None:
            self.set_log_dir(log_dir)
        elif log_dir is None and writer is not None:
            self.set_writer(writer)
        else:
            raise ValueError("Only one of log_dir or writer must be specified")

    def set_log_dir(self, log_dir):
        os.makedirs(log_dir, exist_ok=True)
        path = osp.join(log_dir, "events")
        # Why don't we just use an EventsFileWriter?
        # By default, we want to be fork-safe - we want to work even if we
        # create the writer in one process and try to use it in a forked
        # process. And because EventsFileWriter uses a subthread to do the
        # actual writing, EventsFileWriter /isn't/ fork-safe.
        self.writer = pywrap_tensorflow.EventsWriter(compat.as_bytes(path))

    def set_writer(self, writer):
        self.writer = EventsFileWriterWrapper(writer)

    def logkv(self, k, v, step=None):
        def summary_val(k, v):
            kwargs = {'tag': k, 'simple_value': float(v)}
            return tf.Summary.Value(**kwargs)

        summary = tf.Summary(value=[summary_val(k, v)])
        event = event_pb2.Event(wall_time=time.time(), summary=summary)
        # Use a separate step counter for each key
        if k not in self.key_steps:
            self.key_steps[k] = 0
        if step is not None:
            self.key_steps[k] = step
        event.step = self.key_steps[k]
        self.writer.WriteEvent(event)
        self.writer.Flush()
        self.key_steps[k] += 1

    def log_list_stats(self, k, l):
        for suffix, f in [('min', np.min), ('max', np.max), ('avg', np.mean), ('std', np.std)]:
            self.logkv(k + '_' + suffix, f(l))

    def measure_rate(self, k, v, tag=None):
        if k in self.rate_values:
            last_val, last_time = self.rate_values[k]
            interval = time.time() - last_time
            if tag is None:
                tag = k + '_rate'
            self.logkv(tag, (v - last_val) / interval)
        self.rate_values[k] = (v, time.time())

    def close(self):
        if self.writer:
            self.writer.Close()
            self.writer = None


def set_dir(log_dir):
    Logger.DEFAULT = Logger(log_dir=log_dir)


def set_writer(writer):
    Logger.DEFAULT = Logger(writer=writer)


def tflog(key, value, step=None):
    if not Logger.DEFAULT:
        set_dir('logs')
    Logger.DEFAULT.logkv(key, value, step)

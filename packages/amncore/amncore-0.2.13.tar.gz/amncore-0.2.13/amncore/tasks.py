from collections import Mapping
import kthread, time

class Task(object):
    def __init__(self, manager, tid, name, ctx, run_proc, clean_proc):
        self.manager = manager
        self.tid = tid
        self.name = name
        self.run_proc = run_proc
        self.clean_proc = clean_proc
        self.ctx = ctx
        self.start_time = None
        self.task_thread = None

    def async_func(self):
        try:
            self.run_proc(self.ctx)
        finally:
            if self.clean_proc is not None:
                self.clean_proc(self.ctx)
            self.manager.remove_task(self)

    def start(self, async = False):
        self.start_time = time.time()
        if (async):
            self.task_thread = kthread.KThread(target = self.async_func, name = "TaskID({}-{})".format(self.tid, self.name))
            self.task_thread.daemon = True
            time.sleep(0.01)
            self.task_thread.start()
        else:
            try:
                self.run_proc(self.ctx)
            except Exception as e:
                self.manager.stop_task(self.tid)
                raise e

    def stop(self):
        if (self.task_thread):
            self.task_thread.terminate()
            self.task_thread = None

        if self.clean_proc:
            self.clean_proc(self.ctx)

class TaskManager(Mapping):
    def __init__(self):
        self._dict = {}
        self.task_id_pool = 0

    def __iter__(self):
        return iter(self._dict)
        
    def __len__(self):
        return len(self._dict)
        
    def __getitem__(self, key):
        if key in self._dict:
            return self._dict[key]
        else:
            return None

    def __setitem__(self, key, value):
        self._dict.update({key: value})

    def __contains__(self, key):
        return key in self._dict

    def add_task(self, name, ctx, run_proc, clean_proc):
        real_name = name
        count = 0
        tid = self.task_id_pool

        self.task_id_pool += 1
        if real_name is None:
            real_name = '#' + str(tid)

        while real_name in self._dict:
            real_name = name + " {}".format(count)
            count += 1

        t = Task(self, tid, real_name, ctx, run_proc, clean_proc)

        self._dict.update({str(tid):t})

        return t

    def start_task(self, name, ctx, run_proc, clean_proc = None):
        t = self.add_task(name, ctx, run_proc, clean_proc)
        t.start()

        return t.tid

    def start_bg_task(self, name, ctx, run_proc, clean_proc = None, async = True):
        t = self.add_task(name, ctx, run_proc, clean_proc)
        t.start(async)

        return t.tid

    def stop_task(self, tid):
        if str(tid) in self._dict:
            t = self._dict[str(tid)]
            t.stop()
            self.remove_task(t)

    def remove_task(self, inst):
        self._dict.pop(str(inst.tid))
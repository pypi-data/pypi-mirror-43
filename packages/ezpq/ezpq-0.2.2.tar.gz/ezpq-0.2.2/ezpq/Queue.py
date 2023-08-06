import ezpq.Job
import multiprocessing as mp
import threading as thread
from heapq import heappush, heappop
import os
import csv
import time
import logging as log
from uuid import uuid4
import traceback

class Queue():

    class RepeatedTimer():
        """Runs a function using threads on a periodic schedule.
        Used internally to periodically process jobs in an EZPQ Queue.
        Borrowed from: https://stackoverflow.com/a/13151299
        """

        def __init__(self, interval, function, *args, **kwargs):
            self._timer     = None
            self._interval   = interval
            self.function   = function
            self.args       = args
            self.kwargs     = kwargs
            self.is_running = False
            # self.start()

        def _run(self):
            self.is_running = False
            self.start()
            self.function(*self.args, **self.kwargs)

        def start(self):
            if not self.is_running:
                self._timer = thread.Timer(self._interval, self._run)
                self._timer.start()
                self.is_running = True

        def stop(self):
            self.is_running = False
            self._timer.cancel()
            # self._timer.join()


    def __init__(self,
                 n_workers = mp.cpu_count(),
                 max_size = 0,
                 job_runner = mp.Process,
                 auto_remove = False,
                 auto_start = True,
                 auto_stop = False,
                 callback = None,
                 log_file = None,
                 poll = 0.1,
                 show_progress = False,
                 qid = None):
        """Implements a parallel queueing system.

        Args:
            n_workers: the max number of concurrent jobs.
                - Accepts: int
                - Default: cpu_count()
            max_size: when > 0, will throw an exception the number of enqueued jobs exceeds this value. Otherwise, no limit.
                - Accepts: int
                - Default: 0 (unlimited)
            job_runner: the class to use to invoke new jobs.
                - Accepts: multiprocessing.Process, threading.Thread
                - Default: multiprocessing.Process
            auto_remove: controls whether jobs are discarded of after completion.
                - Accepts: bool
                - Default: False
            auto_start: controls whether the queue system "pulse" is started upon instantiation (default), or manually.
                - Accepts: bool
                - Default: True
            auto_stop: controls whether the queue system "pulse" stops itself after all jobs are complete.
                - Accepts: bool
                - Default: False
            callback: optional function to execute synchronously immediately after a job completes.
                - Accepts: function object
                - Default: None
            log_file: if file path is specified, job data is written to this path in CSV format.
                - Accepts: str
                - Default: None
            poll: controls the pulse frequency; the amount of time slept between operations.
                - Accepts: float
                - Default: 0.1

        Returns:
            ezpq.Queue object.
        """

        assert(job_runner in (mp.Process, thread.Thread))
        assert(poll >= 0.01) # max 100 pulses per sec.

        if qid is None:
            self._qid = str(uuid4())[:8]
        else:
            self._qid = qid
        self.show_progress = show_progress
        self._max_size = max_size
        self._n_submitted = 0
        self._n_completed = 0
        self._n_workers = n_workers
        self._callback = callback
        self._log_file = log_file

        self._lock = thread.Lock() # https://opensource.com/article/17/4/grok-gil
        self._job_runner = job_runner

        self._q_waiting = list()
        self._q_waiting_lanes = dict()
        self._q_working = dict()
        self._q_completed = list()
        self._n_q_waiting = 0
        # self._n_q_working = 0
        # self._n_q_completed = 0

        self._auto_remove = auto_remove
        self._mpmanager = None

        if self._job_runner is mp.Process:
            self._mpmanager = mp.Manager()
            self._output = self._mpmanager.dict()
        else:
            self._output = dict()

        log.debug('Initialized queue with {} workers.'.format(self._n_workers))

        self._poll = poll
        self._ticker = Queue.RepeatedTimer(interval=self._poll, function=self._pulse)
        self.is_running = False
        if auto_start is True:
            self.start()
        self._auto_stop = auto_stop

        log.debug('Initialized pulse.')

    def __call__(self, fun, *args, **kwargs):
        '''Decorator guided by http://scottlobdell.me/2015/04/decorators-arguments-python/'''
        self.start()

        def wrapped_f(iterable, *args, **kwargs):
            for x in iterable:
                self.put(function=fun, args=[x]+list(args), kwargs=kwargs)
            self.wait(show_progress = self.show_progress)
            job_data = self.collect()
            self.dispose()
            return job_data
        return wrapped_f

    @staticmethod
    def log_csv(job, path='ezpq_log.csv', append=True):
        try:
            csv_exists = os.path.exists(path)

            mode = 'x' # create

            if csv_exists:
                if append:
                    mode = 'a' # append
                else:
                    mode = 'w' # write

            with open(path, mode) as csvfile:
                writer = None

                if isinstance(job, dict):
                    writer = csv.DictWriter(csvfile, fieldnames=list(job.keys()))

                    if not csv_exists:
                        writer.writeheader()

                    writer.writerow(job)

            return 0

        except IOError as ex:
            log.error("Logging error: {0}".format(str(ex)))

        return -1

    def __del__(self):
        if self.is_running:
            self.dispose()

    def start(self):
        '''Starts the queue system pulse.'''
        log.debug('Starting pulse.')
        self._ticker.start()
        self.is_running = True

    def _stop(self):
        '''Stops the queue system pulse.'''
        log.debug('Stopping pulse.')
        self._ticker.stop()
        self.is_running = False

    def dispose(self):
        '''Clears all output and stops the queue system pulse.'''
        log.debug('Disposing')

        self.stop_all(wait=True)

        self._stop()

        # self._q_working.clear()
        log.debug('Removed jobs.')
        self._output = None
        log.debug('Removed output.')
        self._q_completed.clear() # [:] = []
        log.debug('Removed completed.')
        # self._n_q_working = 0
        self._n_submitted = 0
        self._n_completed = 0
        log.debug('Reset counters.')
        
        if self._mpmanager is not None:
            self._mpmanager.shutdown()

    def clear_waiting(self):
        log.debug('Clearing waiting queue')
        with self._lock:
            for _ in range(len(self._q_waiting)):
                _, _, job = heappop(self._q_waiting)
                job._cancelled = True
                job._processed = time.time()
                if not self._auto_remove:
                    heappush(self._q_completed, (int(job.priority), job._submitted, job.to_dict()))
                self._n_q_waiting -= 1

            keys = list(self._q_waiting_lanes.keys())
            for k in keys:
                lane_jobs = self._q_waiting_lanes.get(k)
                for _ in range(len(lane_jobs)):
                    _, _, job = heappop(lane_jobs)
                    job._cancelled = True
                    job._processed = time.time()
                    if not self._auto_remove:
                        heappush(self._q_completed, (int(job.priority), job._submitted, job.to_dict()))
                    self._n_q_waiting -= 1
                del(self._q_waiting_lanes[k])

    def stop_all(self, wait=True):
        '''Stops working jobs and clears waiting jobs.'''

        self.clear_waiting()

        keys = list(self._q_working.keys())
        for k in keys:
            job = self._q_working.get(k)
            if job is not None:
                job._stop()

        if wait:
            self.wait()

    # def clear(self):
    #     '''Clears the queue system components: waiting, working, completed.
    #     Also resets the counters.
    #     '''
    #     self.clear_waiting()
    #     self.stop_all(wait=True)

    #     with self._lock:
    #         # self._q_working.clear()
    #         log.debug('Removed jobs.')
    #         self._output = None
    #         log.debug('Removed output.')
    #         self._q_completed.clear() # [:] = []
    #         log.debug('Removed completed.')
    #         # self._n_q_working = 0
    #         self._n_submitted = 0
    #         self._n_completed = 0
    #         log.debug('Reset counters.')

    def __enter__(self):
        log.debug('Entered context manager')
        return self

    def __exit__(self, *args):
        log.debug('Exiting context manager')
        self.dispose()

    def n_submitted(self):
        '''Returns the total number of jobs that have entered the queueing system.'''
        return self._n_submitted

    def n_completed(self):
        '''Returns the total number of jobs that have been completed.'''
        return self._n_completed

    def n_workers(self):
        '''Returns max concurrency limit.'''
        return self._n_workers

    def _pulse(self):
        '''Used internally; manages the queue system operations.'''

        # locked = self._lock.acquire(blocking=False)

        with self._lock:
            try:
                # if not locked: # self._lock.locked():
                #     log.debug('Thread already locked.') #' If you see this repeatedly, consider increasing the value of "poll", or removing a slow callback.')
                # else:
                if self._auto_stop and len(self._q_working) == 0 and self._n_q_waiting == 0: # self.size(waiting=True, working=True) == 0:
                    self._stop()
                else:
                    for job_id, job in self._q_working.items():
                        if job.is_expired():
                            job._stop()

                    for job_id in list(self._q_working.keys()):
                        job = self._q_working[job_id]

                        if not job.is_running() and not job.is_processed():
                            job._join()
                            if not job._cancelled:
                                try:
                                    job_data = self._output.pop(job._id)
                                    job._ended = job_data['_ended']
                                    job._output = job_data['_output']
                                    job._exitcode = job_data['_exitcode']
                                    job._exception = job_data['_exception']
                                except KeyError as ex:
                                    job._ended = time.time()
                                    job._output = None
                                    job._exitcode = 1
                                    job._exception = Exception('{}\n\nNo data for job; it may have exited unexpectedly.'.format(str(ex)))

                            if self._callback is not None:
                                try:
                                    job._callback = self._callback(job.to_dict())
                                except Exception as ex:
                                    job._callback = str(ex)

                            job._processed = time.time()

                            log.debug("Completed job: '{}'".format(job._id))
                            if not self._auto_remove:
                                heappush(self._q_completed, (int(job.priority), job._submitted, job.to_dict()))
                                # self._n_q_completed += 1

                            if self._log_file is not None:
                                Queue.log_csv(job=job.to_dict(), path=self._log_file)

                            del(self._q_working[job_id])
                            self._n_completed += 1
                            # self._n_q_working -= 1

                            if job.lane is not None:
                                lane = self._q_waiting_lanes.get(job.lane)
                                if lane is not None:
                                    next_job = None
                                    parent_exitcode = job.get_exitcode()
                                    while len(lane) > 0:
                                        _, _, next_job = heappop(lane)
                                        
                                        if parent_exitcode == 0 or not next_job._stop_on_lane_error:
                                            break
                                        else:
                                            next_job._cancelled = True
                                            next_job._exitcode = parent_exitcode
                                            next_job._exception = 'stop_on_lane_error = True and preceding job ({}) exit code is {}'.format(job._id, parent_exitcode)
                                            next_job._processed = time.time()
                                            if not self._auto_remove:
                                                heappush(self._q_completed, (int(next_job.priority), next_job._submitted, next_job.to_dict()))
                                            next_job = None
                                            self._n_q_waiting -= 1 # decrement after completed.
                                            continue

                                    if len(lane) == 0:
                                        del(self._q_waiting_lanes[job.lane])

                                    if next_job is not None:
                                        self._q_working[next_job._id] = next_job
                                        self._start_job(job=next_job)
                                        self._n_q_waiting -= 1 # decrement after started.

                    while len(self._q_waiting) > 0 and self.n_workers_free() > 0:
                        _, _, job = heappop(self._q_waiting)
                        # self._n_q_working += 1
                        self._q_working[job._id] = job
                        self._start_job(job=job)
                        self._n_q_waiting -= 1

            except Exception as ex:
                log.error(traceback.format_exc())
            finally:
                log.debug('Waiting={}; Working={}; Completed={}.'.format(self._n_q_waiting, len(self._q_working), len(self._q_completed)))
            #     if locked:
            #         self._lock.release()

    def size(self, waiting=False, working=False, completed=False):
        """Returns the number of jobs in the corresponding queue(s).

        Args:
            waiting: include jobs in the waiting queue?
                - Accepts: bool
                - Default: False
            working: include jobs in the working table?
                - Accepts: bool
                - Default: False
            completed: include jobs in the completed queue?
                - Accepts: bool
                - Default: False

        Note: when all are False, all jobs are counted (default).

        Returns:
            int
        """

        size = 0
        locked = False
        
        try:
            to_tally = sum([waiting, working, completed])
            if to_tally != 1:
                if to_tally == 0:
                    waiting, working, completed = True, True, True
                locked = self._lock.acquire() # must lock when more than 1 component included.

            if waiting:
                size += self._n_q_waiting
            if working:
                size += len(self._q_working)
            if completed:
                size += len(self._q_completed)
        finally:
            if locked:
                self._lock.release()

        return size

    def n_workers_free(self):
        '''Returns the number of available processes.'''
        return self._n_workers - len(self._q_working)

    def is_working(self):
        '''True if there are running jobs.'''
        return len(self._q_working) > 0

    def is_busy(self):
        '''True if max concurrent limit (n_workers) is reached or if there are waiting jobs.'''
        return self.n_workers_free() == 0 or self._n_q_waiting > 0

    # def is_running(self):
    #     '''True if the queue system pulse is running.'''
    #     return self.is_running

    def is_empty(self):
        '''True if there are no jobs in the queue system.'''
        return self.size() == 0

    def is_full(self):
        '''True if the number of jobs in the queue system is equal to max_size.'''
        return self._max_size > 0 and self.size() == self._max_size

    def remaining_jobs(self):
        '''The difference between the number of jobs submitted and the number completed.'''
        return self._n_submitted - self._n_completed

    def wait_worker(self, poll=0, timeout=0):
        """Waits for the number of running jobs to fall below the max concurrent limit (n_workers)

        Args:
            poll: the time, in seconds, between checks.
                - Accepts: float
                - Default: ezpq.Queue.poll
            timeout: when > 0, the maximum time to wait, in seconds. Otherwise, no limit.
                - Accepts: float
                - Default: 0 (unlimited)

        Returns:
            True if a worker is available; False otherwise.
        """
        if poll is None or poll <= 0:
            poll = self._poll
        else:
            assert poll >= self._poll

        start = time.time()
        while self.is_busy() and (timeout==0 or time.time() - start < timeout):
            time.sleep(poll)

        return not self.is_busy()

    def wait(self, poll=0, timeout=0, show_progress=False):
        """Waits for jobs to be completed by the queue system.

        Args:
            poll: the time, in seconds, between checks.
                - Accepts: float
                - Default: ezpq.Queue.poll
            timeout: when > 0, the maximum time to wait, in seconds. Otherwise, no limit.
                - Accepts: float
                - Default: 0 (unlimited)
            show_progress: show `tqdm` progress bar; (pass args to `waitpb`)
                - Accepts: bool
                - Default: False

        Returns:
            0 if the expected number of jobs completed. > 0 otherwise.
        """

        if poll is None or poll <= 0:
            poll = self._poll
        else:
            assert poll >= self._poll

        n_pending = 0

        if show_progress:
            n_pending = self.waitpb(poll=poll, timeout=timeout)
        else:
            n_pending = self.size(waiting=True, working=True)

            if n_pending > 0:
                start = time.time()

                while n_pending > 0 and (timeout==0 or time.time() - start < timeout):
                    time.sleep(poll)
                    n_pending = self.size(waiting=True, working=True)

        return n_pending

    def waitpb(self, poll=0, timeout=0):
        """Waits for jobs to be completed by the queue system.

        Args:
            poll: the time, in seconds, between checks.
                - Accepts: float
                - Default: ezpq.Queue.poll
            timeout: when > 0, the maximum time to wait, in seconds. Otherwise, no limit.
                - Accepts: float
                - Default: 0 (unlimited)

        Returns:
            0 if the expected number of jobs completed. > 0 otherwise.
        """

        if poll is None or poll <= 0:
            poll = self._poll
        else:
            assert poll >= self._poll

        n_pending = self.size(waiting=True, working=True)

        if n_pending > 0:
            
            from tqdm.auto import tqdm

            start = time.time()

            with tqdm(total=n_pending, unit='op') as pb:
                while n_pending > 0 and (timeout==0 or time.time() - start < timeout):
                    time.sleep(poll)
                    tmp = self.size(waiting=True, working=True)
                    diff = n_pending - tmp
                    if diff > 0:
                        n_pending = tmp
                        pb.update(diff)
                pb.close()

        return n_pending

    @staticmethod
    def _job_wrap(_job, _output, *args, **kwargs):
        '''Used internally to wrap a job, capture output and any exception.'''
        out = None
        ex_obj = None
        ex_msg = None
        code = 0

        try:
            out = _job.function(*args, **kwargs)
        except Exception as ex:
            ex_obj = ex
            ex_msg = traceback.format_exc()
            code = -1
        finally:
            _output.update({ _job._id: {'_ended':time.time(), '_output':out, '_exception': ex_msg, '_exitcode': code} })

        if not _job._suppress_errors and ex_obj is not None:
            raise ex_obj

    def _start_job(self, job):
        '''Internal; invokes jobs.'''

        job_args = dict()

        if job.args is not None:
            # if not isinstance(job.args, list):
            #     job_args['args'] = [job, self._output, job.args]
            # else:
            job_args['args'] = [job, self._output] + job.args

        if job.kwargs is None:
            job_args['kwargs'] = dict()
        else:
            job_args['kwargs'] = dict(job.kwargs)

        if job.args is None:
            job_args['kwargs'].update({'_job': job, '_output': self._output})

        j = self._job_runner(name=str(job._id),
                             target=Queue._job_wrap,
                             **job_args)
        j.start()

        job._started = time.time()
        job._inner_job = j

        log.debug("Started job '{}'".format(job._id))

    def submit(self, job):
        '''Submits a job into the ezpq.Queue system.

        Throws an exception if:
            1. the Queue uses a Thread job_runner and this job has a timeout (can't terminate Threads),
            2. the Queue max_size will be exceeded after adding this job.

        Returns:
            The number of jobs submitted to the queue.
        '''

        assert(not (self._job_runner is thread.Thread and job.timeout > 0))

        if self._max_size > 0 and self.size()+1 > self._max_size:
            raise Exception('Max size exceeded.')

        job._submitted = time.time()

        job._qid = self._qid
        self._n_submitted += 1
        job._id = self._n_submitted

        if job.name is None: job.name = job._id

        if job.lane is not None:
            lane = self._q_waiting_lanes.get(job.lane)
            if lane is None:
                lane = list()
                self._q_waiting_lanes[job.lane] = lane
                heappush(self._q_waiting, (int(job.priority), job._submitted, job))
            else:
                heappush(lane, (int(job.priority), job._submitted, job))
        else:
            heappush(self._q_waiting, (int(job.priority), job._submitted, job))

        self._n_q_waiting += 1
        log.debug("Queued job: '{}'".format(job._id))

        return job._id

    def put(self, *args, **kwargs): # function, args=None, kwargs=None, name=None, priority=100, lane=None, timeout=0):
        """Creates a job and submits it to an ezpq queue.
        see `help(ezpq.Job.__init__)`"""

        job = ezpq.Job(*args, **kwargs) #function=function, args=args, kwargs=kwargs, name=name, priority=priority, lane=lane, timeout=timeout)

        return self.submit(job)

    def map(self, function, iterable, args=None, kwargs=None, timeout=0, show_progress=False):
        
        assert hasattr(iterable, '__iter__')

        if args is None:
            args = [None]
        elif not hasattr(args, '__iter__'):
            args = [None] + [args]
        elif len(args) == 0:
            args = [None]
        else:
            args = [None] + list(args)

        for x in iterable:
            args[0] = x
            job = ezpq.Job(function=function, args=list(args), kwargs=kwargs, timeout=timeout)
            self.submit(job)

        self.wait(show_progress=show_progress)

        return self.collect()

    def starmap(self, function, iterable, args=None, kwargs=None, timeout=0, show_progress=False):
        
        assert hasattr(iterable, '__iter__')

        if args is None:
            args = []
        elif not isinstance(args, list):
            args = list(args)

        for x in iterable:
            job = ezpq.Job(function=function, args=list(x) + args, kwargs=kwargs, timeout=timeout)
            self.submit(job)

        self.wait(show_progress=show_progress)

        return self.collect()

    def starmapkw(self, function, iterable, args=None, kwargs=None, timeout=0, show_progress=False):
        
        assert hasattr(iterable, '__iter__')

        if kwargs is None:
            kwargs = {}
        elif not isinstance(kwargs, dict):
            kwargs = dict(kwargs)

        for x in iterable:
            job = ezpq.Job(function=function, args=args, kwargs={**x, **kwargs}, timeout=timeout)
            self.submit(job)

        self.wait(show_progress=show_progress)

        return self.collect()

    def get(self, wait=False, poll=0, timeout=0):
        """Pops the highest priority item from the completed queue.

        Args:
            poll: when > 0, time between checks
                - Accepts: float
                - Default: 0 (no wait)
            timeout: the maximum time, in seconds, to wait for a job to complete.
                - Accepts: float
                - Default: 0 (no wait/unlimited wait)

        Notes:
            - when both poll and timeout are 0, only one check is done;
            - when either is > 0, the method will block until output is available.

        Returns:
            Dictionary of the most recently completed, highest priority job.
        """

        assert (not self._auto_remove)

        if (wait or timeout > 0) and (poll is None or poll <= 0):
            poll = self._poll
            wait = True
        else:
            assert poll <= 0 or poll >= self._poll
            if not wait and (timeout > 0 or poll > 0):
                wait = True

        job = None

        start = time.time()

        while True:
            if len(self._q_completed) > 0:
                _,_,job = heappop(self._q_completed)
                # self._n_q_completed -= 1
                # job = x.to_dict()
            elif wait and self.size() > 0 and (timeout <= 0 or time.time() - start < timeout):
                time.sleep(poll)
                continue

            break

        return job

    def collect(self, n=0):
        """Repeatedly calls `get()` and returns a list of job data.

        Args:
            n: the number of jobs to pop from the completed queue.
                - Accepts: int
                - Default: 0 (all)

        Returns:
            a list of dictionary objects.
        """

        if n <= 0:
            n = len(self._q_completed)
        else:
            n = min(n, len(self._q_completed))

        return [self.get() for _ in range(n)]

    def set_workers(self, n):
        '''Allows adjusting max concurrency.'''
        diff = n - self._n_workers
        self._n_workers = n
        log.debug('Added {} workers to the queue.'.format(diff))

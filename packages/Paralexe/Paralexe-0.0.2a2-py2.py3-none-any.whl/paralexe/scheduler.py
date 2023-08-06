from multiprocessing.pool import ThreadPool
from tqdm import tqdm


class Scheduler(object):
    """The class to schedule multiple jobs.

    Args:
        workers (:obj:'dict' of :obj:'Worker', optional): list of the worker instances to be scheduled.
            if dict, key value indicate priority of the workers.
        n_threads (int, optional): Number of thread to use.

    Attributes:
        queues (dict): queued workers in dictionary form, the key value indicate priority.
        stderr (dict): collection of stderr from workers after execution.
        stdout (dict): collection of stdout from workers after execution.
    """
    def __init__(self, workers=None, n_threads=None):
        """
        Args:
            workers (dict or list): priority:list(workers)
            n_threads (int):
        """
        # Initiate counters
        self.__reset_counter()
        self.__queues = None
        self.__queues_labels = dict()
        self.__background_binder = None
        self.__n_threads = n_threads

        if workers is not None:
            self.queue(workers)

    def submit(self, mode='foreground', use_label=False):
        """Submit schedule

        Args:
            mode (str): run process on Thread if 'background', else running foreground.
        """

        def workflow():
            """Internal function that submitting jobs to Thread object
            The outputs from each worker are collected during running this function"""
            if self.__queues is not None:
                self.__num_steps = len(self.__queues)

                # initiate pool
                pool = ThreadPool(self.__n_threads)
                for order in sorted(self.__queues.keys()):
                    if order in self.__succeeded_steps:
                        pass
                    else:
                        if use_label is True:
                            label = self.__queues_labels[order]
                        else:
                            label = order
                        # Initiate counters
                        self.__incomplete_steps = []
                        self.__failed_steps = []
                        self.__succeeded_workers[order] = []
                        self.__failed_workers[order] = []
                        self.__stdout_collector[label] = dict()
                        self.__stderr_collector[label] = dict()
                        n_work = len(self.__queues[order])
                        self.__total_num_of_workers[order] = n_work
                        workers = self.__queues[order]

                        for id, rcode, output in pool.imap_unordered(self.request, workers):
                            # to catch the error related to the failed workers (when worker raise an exception)
                            if rcode == 1:
                                self.__failed_workers[order].append(id)
                            elif rcode == 0:
                                self.__succeeded_workers[order].append(id)
                            else:
                                raise Exception
                            if use_label is True:
                                label = self.__queues_labels[order]
                            else:
                                label = order
                            self.__stdout_collector[label][id] = output[0]
                            self.__stderr_collector[label][id] = output[1]

                        if self.__succeeded_workers[order] == 0:
                            self.__failed_steps.append(order)
                        else:
                            if self.__total_num_of_workers[order] > len(self.__succeeded_workers[order]):
                                self.__incomplete_steps.append(order)
                            else:
                                self.__succeeded_steps.append(order)

        # Pool will be staying on foreground
        if mode == 'foreground':
            workflow()

        # Pool will be staying on background
        elif mode == 'background':
            import threading
            self.__background_binder = threading.Thread(target=workflow, args=())
            self.__background_binder.daemon = True
            self.__background_binder.start()

    def request(self, worker):
        """Method for requesting execution to worker

        Args:
            worker (obj): single Worker object

        Returns:
            id (int): identifier code for worker instances.
            rcode (int): return code 0 if request is executed, 1 if not.
            output (list): stdout or stderr.
        """
        # if output file is exist
        rcode = worker.run()
        output = worker.output
        return worker.id, rcode, output

    def is_alive(self):
        """Check if the process is still alive if it running on background"""
        if self.__background_binder is not None:
            return self.__background_binder.is_alive()
        else:
            return None

    def join(self):
        """If running on background, attract out to foreground"""
        if self.is_alive():
            self.__background_binder.join()

    def check_progress(self):
        """Helper method to check overall progression"""

        if self.__queues is not None:
            total_bar = len(self.__succeeded_steps) + len(self.__failed_steps)
            tqdm(total=self.__num_steps, desc='__Total__', initial=total_bar, postfix=None)

            for priority in self.__queues.keys():
                if len(self.__queues_labels) != 0:
                    label = 'Step::{}'.format(self.__queues_labels[priority])
                else:
                    label = 'priority::{}'.format(str(priority + 1).zfill(3))
                if priority in self.__succeeded_workers.keys():
                    sub_bar = len(self.__succeeded_workers[priority])
                    tqdm(total=self.__total_num_of_workers[priority],
                         desc=label,
                         initial=sub_bar)
                else:
                    tqdm(total=len(self.__queues[priority]),
                         desc=label,
                         initial=0)
        else:
            print('[No scheduled jobs]')

    def summary(self):
        if self.__num_steps != 0:
            m = []
            zfill = len(str(self.__num_steps))
            m.append('outline')
            m.append('\t\tSummery')
            m.append('outline')
            m.append('Total number of steps:\t\t{}'.format(self.__num_steps))
            if len(self.__succeeded_steps) > 0:
                m.append('- Succeeded steps:\t\t\t{}'.format(len(self.__succeeded_steps)))
            if len(self.__incomplete_steps) > 0:
                m.append('- Incompleted steps:\t\t{}'.format(len(self.__incomplete_steps)))
            if len(self.__failed_steps) > 0:
                m.append('- Failed steps:\t\t\t{}'.format(len(self.__failed_steps)))
            # for s in range(self.__num_steps):
            for s in self.__queues.keys():
                if len(self.__queues_labels) == 0:
                    label = 'Step:'.format(str(s + 1).zfill(zfill))
                else:
                    label = 'Step::{}'.format(self.__queues_labels[s])
                if s in self.__total_num_of_workers.keys():
                    m.append('space')
                    m.append('{}\n\tNumber of workers: \t{}'.format(label,
                                                                    self.__total_num_of_workers[s]))
                    if len(self.__succeeded_workers[s]) > 0:
                        m.append('\t- Succeeded workers: \t{}'.format(len(self.__succeeded_workers[s])))
                    if len(self.__failed_workers[s]) > 0:
                        m.append('\t- Failed workers: \t\t{}'.format(len(self.__failed_workers[s])))
                else:
                    m.append('space')
                    m.append('{}\n- Not ready'.format(label))
            m.append('space')
            if self.__background_binder is not None:
                if self.is_alive() is True:
                    state = '\tActive'
                else:
                    if len(self.__succeeded_steps) == self.__num_steps:
                        state = '\tFinished'
                    elif len(self.__succeeded_steps) < self.__num_steps:
                        state = []
                        if len(self.__failed_steps) > 0:
                            state.append('\tFailed steps-{}'.format(self.__failed_steps))
                        if len(self.__incomplete_steps) > 0:
                            state.append('\tIncompleted steps-{}'.format(self.__incomplete_steps))
                        state = ''.join(state)
                    else:
                        state = '\tSubmission needed'
                m.append('Status:\n{}'.format(state))
            else:
                if len(self.__succeeded_steps) == self.__num_steps:
                    state = '\tFinished'
                elif len(self.__succeeded_steps) < self.__num_steps:
                    state = []
                    if len(self.__failed_steps) > 0:
                        state.append('\tFailed steps-{}'.format(self.__failed_steps))
                    if len(self.__incomplete_steps) > 0:
                        state.append('\tIncompleted steps-{}'.format(self.__incomplete_steps))
                    state = ''.join(state)
                else:
                    state = ('\tSubmission needed')
                m.append('Status:\n{}'.format(state))
            m.append('outline')

            spacer = '-' * (max(map(len, m)) + 1)
            outline = '=' * (max(map(len, m)) + 1)
            for i, line in enumerate(m):
                if line is 'space':
                    m[i] = spacer
                elif line is 'outline':
                    m[i] = outline
        else:
            m = ['Empty schedule...']
        return '\n'.join(m)

    def queue(self, workers, priority=None, label=None):
        """Queue the input list of workers"""

        # run inspection, if the input of worker instances is list, this step change it to dictionary.
        if self.__queues is None:
            self.__queues = self.__inspect_inputs(workers, priority=0, label=label)
        else:
            workers = self.__inspect_inputs(workers, priority)
            self.__update_queues(workers, label)

    def __inspect_inputs(self, workers, priority=None, label=None):
        """Inspect the integrity of the inputs.

        Args:
            workers (list or dict): The iterable set of pre-initiated Worker instances.
            priority (int): priority of the job of given workers.
            label (str): label

        Returns:
            workers (dict): corrected form of worker list.
        """
        label_index = None
        if label is not None:
            if label in self.__queues_labels.values():
                for order, l in self.__queues_labels.items():
                    if label is l:
                        label_index = order
            if label_index in self.__succeeded_steps:
                return {}
            elif label_index in self.__failed_steps or label_index in self.__incomplete_steps:
                priority = label_index
                try:
                    self.__failed_steps.remove(label_index)
                except:
                    pass
                try:
                    self.__incomplete_steps.remove(label_index)
                except:
                    pass
            else:
                pass

        if priority is None:
            if self.__queues is None:
                priority = 0
            else:
                priority = max(self.__queues.keys()) + 1

        from .worker import Worker

        # Check if the inputs has hierarchy works.
        if isinstance(workers, list):
            for ipt in workers:
                if not isinstance(ipt, Worker):
                    raise Exception
            self.__queues_labels[priority] = label
            return {priority:workers}

        # dictionary type of workers may have multiple workers list.
        elif isinstance(workers, dict):
            for p, w in workers.items():
                self.__queues_labels[p] = label
            return workers
        else:
            raise Exception

    def __update_queues(self, workers, label):
        """internal method to update workers into queue"""
        if len(workers) > 0:
            for priority, workers_in_priority in workers.items():
                if priority in self.__queues.keys():
                    if isinstance(workers_in_priority, list):
                        self.__queues[priority].extend(workers_in_priority)
                    else:
                        self.__queues[priority].append(workers_in_priority)
                else:
                    self.__queues[priority] = workers_in_priority
                    if label is not None:
                        self.__queues_labels[priority] = label

    def __reset_counter(self):
        # counter for steps
        self.__num_steps = 0
        self.__succeeded_steps = []
        self.__failed_steps = []
        self.__incomplete_steps = []

        # counter for workers
        self.__total_num_of_workers = {}
        self.__failed_workers = {}
        self.__succeeded_workers = {}

        # output collector
        self.__stdout_collector = {}
        self.__stderr_collector = {}

    @property
    def queues(self):
        return self.__queues

    @property
    def stdout(self):
        return self.__stdout_collector

    @property
    def stderr(self):
        return self.__stderr_collector

    def __repr__(self):
        return self.summary()
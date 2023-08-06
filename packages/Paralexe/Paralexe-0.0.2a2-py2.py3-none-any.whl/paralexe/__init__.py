# Parallel process Executor
from .scheduler import Scheduler
from .manager import Manager
from .worker import Worker
from .executor import Executor
from .rsubprocess import Ropen

__version__ = '0.0.2a2'
__all__ = ['Scheduler', 'Manager', 'Worker', 'Executor', 'Ropen']

# Worker execute Executor
# Manager allocate job to Worker and schedules it to Scheduler
# Scheduler run whole scheduled jobs with given priority

# License of the library - tqdm:: Mozilla Public Licence (MPL) v. 2.0 - Exhibit A, and MIT License (MIT)
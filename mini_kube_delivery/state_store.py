import threading
from typing import Dict, List
from .models import Depot, Job, DesiredState, JobStatus


class StateStore:
    """
    A simple in-memory state store that acts like etcd.
    Thread-safe to simulate concurrent controllers and agents.
    """

    def __init__(self):
        self._lock = threading.Lock()
        self.depots: Dict[str, Depot] = {}
        self.jobs: Dict[str, Job] = {}
        self.desired: Dict[str, DesiredState] = {}

    def add_depot(self, depot: Depot):
        with self._lock:
            self.depots[depot.id] = depot

    def upsert_desired_state(self, desired: DesiredState):
        with self._lock:
            self.desired[desired.region] = desired

    def create_job(self, job: Job):
        with self._lock:
            self.jobs[job.id] = job

    def update_job(self, job: Job):
        with self._lock:
            self.jobs[job.id] = job

    def list_unassigned_jobs(self) -> List[Job]:
        with self._lock:
            return [
                j for j in self.jobs.values()
                if j.assigned_depot_id is None and j.status == JobStatus.PENDING
            ]

    def list_jobs_for_region(self, region: str) -> List[Job]:
        with self._lock:
            return [j for j in self.jobs.values() if j.region == region]

    def list_depots(self) -> List[Depot]:
        with self._lock:
            return list(self.depots.values())

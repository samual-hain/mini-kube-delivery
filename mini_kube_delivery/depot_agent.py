import random
from .models import JobStatus
from .state_store import StateStore


class DepotAgent:
    """
    Simulates a kubelet running on a node.
    It transitions jobs through their lifecycle and introduces random failures.
    """

    def __init__(self, depot_id: str, store: StateStore, failure_rate=0.1):
        self.depot_id = depot_id
        self.store = store
        self.failure_rate = failure_rate

    def tick(self):
        jobs = self._jobs_for_depot()

        for job in jobs:
            if job.status == JobStatus.ASSIGNED:
                job.status = JobStatus.RUNNING

            elif job.status == JobStatus.RUNNING:
                r = random.random()
                if r < self.failure_rate:
                    job.status = JobStatus.FAILED
                elif r < self.failure_rate + 0.3:
                    job.status = JobStatus.COMPLETED

            self.store.update_job(job)

    def _jobs_for_depot(self):
        with self.store._lock:
            return [
                j for j in self.store.jobs.values()
                if j.assigned_depot_id == self.depot_id
            ]

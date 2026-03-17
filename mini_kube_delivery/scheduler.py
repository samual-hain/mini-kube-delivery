from .models import JobStatus
from .state_store import StateStore


class Scheduler:
    """
    A simplified scheduler that:
    - Filters depots by region, readiness, and capacity
    - Scores them by least active jobs
    - Binds jobs to depots
    """

    def __init__(self, store: StateStore):
        self.store = store

    def run_once(self):
        jobs = self.store.list_unassigned_jobs()
        depots = self.store.list_depots()

        for job in jobs:
            depot = self._pick_depot(job, depots)
            if depot is None:
                continue

            job.assigned_depot_id = depot.id
            job.status = JobStatus.ASSIGNED
            depot.active_jobs += 1

            self.store.update_job(job)
            self.store.add_depot(depot)

    def _pick_depot(self, job, depots):
        candidates = [
            d for d in depots
            if d.ready
            and d.region == job.region
            and d.active_jobs + job.required_capacity <= d.capacity
        ]

        if not candidates:
            return None

        candidates.sort(key=lambda d: d.active_jobs)
        return candidates[0]

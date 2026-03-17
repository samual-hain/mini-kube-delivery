import uuid
from .models import Job, JobStatus
from .state_store import StateStore


class RouteController:
    """
    Ensures that the number of jobs in each region matches the desired state.
    This mimics the behavior of the Kubernetes ReplicaSet/Deployment controller.
    """

    def __init__(self, store: StateStore):
        self.store = store

    def reconcile(self):
        for desired in self.store.desired.values():
            region = desired.region
            jobs = self.store.list_jobs_for_region(region)

            active = sum(
                1 for j in jobs
                if j.status in (JobStatus.PENDING, JobStatus.ASSIGNED, JobStatus.RUNNING)
            )

            missing = desired.desired_routes - active
            if missing <= 0:
                continue

            for _ in range(missing):
                job = Job(id=str(uuid.uuid4()), region=region)
                self.store.create_job(job)

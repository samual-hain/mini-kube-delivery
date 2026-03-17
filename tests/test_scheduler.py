from mini_kube_delivery.models import Depot, Job, JobStatus
from mini_kube_delivery.state_store import StateStore
from mini_kube_delivery.scheduler import Scheduler


def test_scheduler_assigns_jobs():
    store = StateStore()
    scheduler = Scheduler(store)

    store.add_depot(Depot(id="d1", region="north", capacity=2))
    job = Job(id="j1", region="north")
    store.create_job(job)

    scheduler.run_once()

    assert store.jobs["j1"].assigned_depot_id == "d1"
    assert store.jobs["j1"].status == JobStatus.ASSIGNED

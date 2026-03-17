from mini_kube_delivery.models import Depot, Job, JobStatus
from mini_kube_delivery.state_store import StateStore
from mini_kube_delivery.depot_agent import DepotAgent


def test_depot_agent_transitions_assigned_to_running():
    store = StateStore()
    store.add_depot(Depot(id="d1", region="north", capacity=2))

    job = Job(id="j1", region="north", assigned_depot_id="d1", status=JobStatus.ASSIGNED)
    store.create_job(job)

    agent = DepotAgent("d1", store, failure_rate=0)
    agent.tick()

    assert store.jobs["j1"].status == JobStatus.RUNNING

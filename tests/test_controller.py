from mini_kube_delivery.state_store import StateStore
from mini_kube_delivery.controllers import RouteController
from mini_kube_delivery.models import DesiredState


def test_controller_creates_missing_jobs():
    store = StateStore()
    controller = RouteController(store)

    store.upsert_desired_state(DesiredState(region="north", desired_routes=3))

    controller.reconcile()

    assert len(store.jobs) == 3

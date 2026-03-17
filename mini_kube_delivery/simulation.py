import time
import argparse
import logging
import threading

from .state_store import StateStore
from .controllers import RouteController
from .scheduler import Scheduler
from .depot_agent import DepotAgent
from .models import Depot, DesiredState

def setup_logging():
    logging.basicConfig(
        level=logging.INFO,
        format="%(asctime)s [%(levelname)s] %(message)s",
        datefmt="%H:%M:%S"
    )

def print_state(store):
    with store._lock:
        logging.info("=== CLUSTER STATE ===")
        for depot in store.depots.values():
            logging.info(f"Depot {depot.id}: active={depot.active_jobs}")
        for job in store.jobs.values():
            logging.info(
                f"Job {job.id[:6]} | {job.region} | {job.status.value} | depot={job.assigned_depot_id}"
            )


def run_simulation(runs=None, interval=1.0, dashboard=False):
    setup_logging()

    store = StateStore()

    # Seed depots
    store.add_depot(Depot(id="north-a", region="north", capacity=5))
    store.add_depot(Depot(id="south-a", region="south", capacity=5))

    # Desired state
    store.upsert_desired_state(DesiredState(region="north", desired_routes=3))
    store.upsert_desired_state(DesiredState(region="south", desired_routes=4))

    controller = RouteController(store)
    scheduler = Scheduler(store)
    agents = [
        DepotAgent("north-a", store),
        DepotAgent("south-a", store),
    ]

    # Optional dashboard
    if dashboard:
        try:
            from mini_kube_delivery.web.dashboard import start_dashboard
            threading.Thread(
                target=start_dashboard,
                args=(store,),
                daemon=True
            ).start()
            logging.info("Dashboard running at http://localhost:5000")
        except Exception as e:
            logging.error(f"Failed to start dashboard: {e}")

    logging.info("Starting simulation... Press Ctrl+C to stop.")

    try:
        step = 0
        while True:
            if runs is not None and step >= runs:
                logging.info(f"Completed {runs} runs. Exiting simulation.")
                break

            controller.reconcile()
            scheduler.run_once()

            for agent in agents:
                agent.tick()

            print_state(store)

            step += 1
            time.sleep(interval)

    except KeyboardInterrupt:
        logging.info("Received Ctrl+C. Shutting down simulation gracefully...")


def main():
    parser = argparse.ArgumentParser(
        description="Mini Kubernetes Delivery Simulator"
    )

    parser.add_argument(
        "--runs",
        type=int,
        default=None,
        help="Number of simulation cycles to run. If omitted, runs until Ctrl+C."
    )

    parser.add_argument(
        "--interval",
        type=float,
        default=1.0,
        help="Seconds between simulation ticks (default: 1.0)"
    )

    parser.add_argument(
        "--dashboard",
        action="store_true",
        help="Launch the web dashboard on port 5000"
    )

    args = parser.parse_args()
    run_simulation(runs=args.runs, interval=args.interval, dashboard=args.dashboard)

if __name__ == "__main__":
    main()

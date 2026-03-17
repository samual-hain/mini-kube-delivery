from flask import Flask, jsonify, render_template
from mini_kube_delivery.state_store import StateStore

app = Flask(__name__)
store: StateStore = None  # will be injected by simulation


@app.route("/")
def index():
    return render_template("index.html")


@app.route("/state")
def state():
    with store._lock:
        return jsonify({
            "depots": [
                {
                    "id": d.id,
                    "region": d.region,
                    "capacity": d.capacity,
                    "active_jobs": d.active_jobs,
                    "ready": d.ready,
                }
                for d in store.depots.values()
            ],
            "jobs": [
                {
                    "id": j.id,
                    "region": j.region,
                    "status": j.status.value,
                    "assigned_depot_id": j.assigned_depot_id,
                }
                for j in store.jobs.values()
            ]
        })


def start_dashboard(state_store: StateStore, port=5000):
    global store
    store = state_store
    app.run(port=port, debug=False, use_reloader=False)

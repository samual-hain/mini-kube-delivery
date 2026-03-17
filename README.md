📘 README.md
Mini Kubernetes Delivery Simulator
A Python learning project that models Kubernetes internals using a delivery‑company analogy.

📦 Overview
This project is a simplified, educational model of Kubernetes written in Python.
It simulates the core components of the Kubernetes control plane:

• A Route Controller (like a ReplicaSet/Deployment controller)
• A Scheduler (filter → score → bind)
• A State Store (similar to etcd)
• Depot Agents (simulated kubelets running on nodes)
• A simulation loop that ties everything together

I built this project as a way to learn Python and to understand how Kubernetes works under the hood.
Coming from a COBOL background, I wanted a hands‑on, conceptual way to explore modern distributed systems.

🧠 Architecture Overview
The system uses a delivery‑company analogy to make Kubernetes concepts intuitive:

• Depots = Kubernetes nodes
• Jobs = Pods
• RouteController = Deployment/ReplicaSet controller
• Scheduler = kube-scheduler
• DepotAgent = kubelet
• StateStore = etcd

The control plane continuously reconciles desired state with actual state, schedules work, and handles failures — just like a real Kubernetes cluster.

🚀 Features
• Declarative desired state (like Kubernetes Deployments)
• Reconciliation loop that maintains desired vs actual jobs
• Scheduler with filtering and scoring
• Node agents that simulate kubelet behavior
• Random job failures to model real distributed systems
• Self‑healing behavior through controllers
• Modular, readable Python code

🛠️ Installation
Clone the repository and install dependencies:

git clone https://github.com/<your-username>/mini-kube-delivery.git
cd mini-kube-delivery
pip install -r requirements.txt

▶️ Running the Simulation
Run the main simulation loop:

python -m mini_kube_delivery.simulation

Example output:

=== CLUSTER STATE ===
Depot north-a: active=2
Depot south-a: active=3
Job 1a2b3c | north | RUNNING | depot=north-a
Job 4d5e6f | south | COMPLETED | depot=south-a

This shows jobs being created, scheduled, run, failed, and replaced — just like a real Kubernetes cluster.

🎯 Learning Goals
This project helped me learn:

Python
• Classes and modules
• Dataclasses
• Enums
• Threading and locks
• Clean project structure

Kubernetes Internals
• Control plane architecture
• Reconciliation loops
• Scheduling algorithms
• Node‑local execution
• Failure handling
• Declarative vs imperative systems

Distributed Systems Concepts
• Event‑driven behavior
• State convergence
• Self‑healing
• Workload placement

🧩 Future Enhancements
• Taints & tolerations
• Topology spread constraints
• YAML loader (like kubectl apply)
• Web dashboard for cluster state
• Prometheus‑style metrics
• Custom scheduler plugins
• Node failure simulation

📄 License
MIT License — feel free to use, modify, and learn from this project.

🙌 Acknowledgements
This project was built as a personal learning tool to bridge the gap between COBOL and modern cloud‑native engineering.
It reflects my journey into Python, Kubernetes, and distributed systems.
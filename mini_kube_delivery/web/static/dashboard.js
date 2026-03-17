async function refresh() {
    const res = await fetch("/state");
    const data = await res.json();

    // Render depots
    document.getElementById("depots").innerHTML =
        "<h2>Depots</h2>" +
        data.depots.map(d => `
            <div class="depot">
                <strong>${d.id}</strong> (${d.region})<br>
                Active jobs: ${d.active_jobs} / ${d.capacity}<br>
                Status: ${d.ready ? "Ready" : "Not Ready"}
            </div>
        `).join("");

    // Render jobs
    document.getElementById("jobs").innerHTML =
        "<h2>Jobs</h2>" +
        data.jobs.map(j => `
            <div class="job job-${j.status.toLowerCase()}">
                <strong>${j.id.slice(0, 6)}</strong><br>
                Region: ${j.region}<br>
                Status: ${j.status}<br>
                Depot: ${j.assigned_depot_id || "Unassigned"}
            </div>
        `).join("");
}

setInterval(refresh, 1000);
refresh();

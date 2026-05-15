const API_URL = "http://127.0.0.1:5000";

async function addSession() {
    const subject = document.getElementById("subject").value;
    const hours = document.getElementById("hours").value;
    const notes = document.getElementById("notes").value;

    await fetch(`${API_URL}/sessions`, {
        method: "POST",
        headers: {
            "Content-Type": "application/json"
        },
        body: JSON.stringify({
            subject: subject,
            hours: parseFloat(hours),
            notes: notes
        })
    });

    document.getElementById("subject").value = "";
    document.getElementById("hours").value = "";
    document.getElementById("notes").value = "";

    loadSessions();
    loadStats();
}

async function loadSessions() {
    const response = await fetch(`${API_URL}/sessions`);
    const sessions = await response.json();

    const sessionsDiv = document.getElementById("sessions");
    sessionsDiv.innerHTML = "";

    sessions.forEach(session => {
        sessionsDiv.innerHTML += `
            <div class="session">
                <strong>${session.subject}</strong> - ${session.hours} hours
                <p>${session.notes}</p>
                <small>${session.date}</small>
            </div>
        `;
    });
}

async function loadStats() {
    const response = await fetch(`${API_URL}/stats`);
    const stats = await response.json();

    document.getElementById("totalHours").innerText = stats.total_hours;
}

loadSessions();
loadStats();
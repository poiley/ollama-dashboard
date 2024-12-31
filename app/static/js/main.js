function updateTimes() {
    const now = new Date();
    const timeStr = now.toLocaleTimeString(undefined, {
        hour: 'numeric',
        minute: '2-digit',
        hour12: true
    });
    const tzAbbr = document.getElementById('timezone').dataset.value;
    document.getElementById('lastUpdate').textContent = `${timeStr} ${tzAbbr}`;
    
    let seconds = 30;
    const countdown = setInterval(() => {
        seconds--;
        document.getElementById('nextRefresh').textContent = seconds;
        if (seconds <= 0) clearInterval(countdown);
    }, 1000);
}

function toggleSidebar() {
    const sidebar = document.getElementById('sidebar');
    const toggleButton = document.getElementById('toggleButton');
    sidebar.classList.toggle('show');
    toggleButton.innerHTML = sidebar.classList.contains('show') ? '✕' : '📋';
}

// Initialize timers when page loads
document.addEventListener('DOMContentLoaded', updateTimes); 
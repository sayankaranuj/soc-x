const API_URL = 'http://127.0.0.1:8000/api/dashboard';

const summaryEls = {
  totalLogs: document.getElementById('totalLogs'),
  totalAlerts: document.getElementById('totalAlerts'),
  openAlerts: document.getElementById('openAlerts'),
  criticalHighAlerts: document.getElementById('criticalHighAlerts'),
};

const alertsList = document.getElementById('alertsList');
const sourceIpsList = document.getElementById('sourceIpsList');
const eventsList = document.getElementById('eventsList');
const alertDetail = document.getElementById('alertDetail');
const refreshButton = document.getElementById('refreshButton');
const lastUpdated = document.getElementById('lastUpdated');

let selectedAlert = null;

function badgeClass(value) {
  return String(value).toLowerCase();
}

function formatTimestamp(value) {
  if (!value) return 'Unknown';
  const date = new Date(value);
  return Number.isNaN(date.getTime()) ? value : date.toLocaleString();
}

function renderSummary(summary) {
  summaryEls.totalLogs.textContent = summary.totalLogs ?? 0;
  summaryEls.totalAlerts.textContent = summary.totalAlerts ?? 0;
  summaryEls.openAlerts.textContent = summary.openAlerts ?? 0;
  summaryEls.criticalHighAlerts.textContent = summary.criticalHighAlerts ?? 0;
}

function renderAlertDetail(alert) {
  if (!alert) {
    alertDetail.innerHTML = '<div class="detail-card">No alert selected.</div>';
    return;
  }

  alertDetail.innerHTML = `
    <div class="detail-card">
      <div class="detail-row">
        <span class="detail-label">Alert ID</span>
        <strong>${alert.alertId || 'N/A'}</strong>
      </div>
      <div class="detail-row">
        <span class="detail-label">Type</span>
        <strong>${alert.alertType}</strong>
      </div>
      <div class="detail-row">
        <span class="detail-label">Source IP</span>
        <strong>${alert.sourceIp}</strong>
      </div>
      <div class="detail-row">
        <span class="detail-label">User</span>
        <strong>${alert.username || 'Unknown'}</strong>
      </div>
      <div class="detail-row">
        <span class="detail-label">Severity</span>
        <span class="badge ${badgeClass(alert.severity)}">${alert.severity}</span>
      </div>
      <div class="detail-row">
        <span class="detail-label">Status</span>
        <span class="badge ${badgeClass(alert.status)}">${alert.status}</span>
      </div>
      <div class="detail-row">
        <span class="detail-label">Time</span>
        <strong>${formatTimestamp(alert.timestamp)}</strong>
      </div>
      <div class="detail-row" style="display:block; margin-top: 12px;">
        <span class="detail-label">Description</span>
        <p style="margin:8px 0 0; line-height:1.5; color:#edf3ff;">${alert.description || 'No description available.'}</p>
      </div>
    </div>
  `;
}

function renderAlerts(alerts) {
  alertsList.innerHTML = alerts.map((alert, index) => `
    <button class="alert-row ${selectedAlert && selectedAlert.alertId === alert.alertId ? 'selected' : ''}" data-index="${index}">
      <div class="alert-meta">
        <span class="alert-type">${alert.alertType}</span>
        <span class="source-ip">${alert.sourceIp}</span>
      </div>
      <div class="alert-meta">
        <span class="badge ${badgeClass(alert.severity)}">${alert.severity}</span>
        <span class="badge ${badgeClass(alert.status)}">${alert.status}</span>
      </div>
    </button>
  `).join('');

  alertsList.querySelectorAll('.alert-row').forEach((button) => {
    button.addEventListener('click', () => {
      const index = Number(button.dataset.index);
      selectedAlert = alerts[index];
      renderAlertDetail(selectedAlert);
      renderAlerts(alerts);
    });
  });

  if (!selectedAlert && alerts.length) {
    selectedAlert = alerts[0];
  }

  renderAlertDetail(selectedAlert);
}

function renderSourceIps(sourceIps) {
  sourceIpsList.innerHTML = sourceIps.map((item) => `
    <div class="ip-row">
      <span>${item.sourceIp}</span>
      <strong>${item.count}</strong>
    </div>
  `).join('');
}

function renderEvents(events) {
  eventsList.innerHTML = events.map((event) => `
    <div class="event-row">
      <div class="event-meta">
        <span class="event-name">${event.event}</span>
        <span class="source-ip">${event.sourceIp}</span>
      </div>
      <div class="event-meta">
        <span class="badge ${badgeClass(event.severity)}">${event.severity}</span>
        <span class="timestamp">${formatTimestamp(event.timestamp)}</span>
      </div>
    </div>
  `).join('');
}

async function loadDashboard() {
  try {
    const response = await fetch(API_URL, { headers: { Accept: 'application/json' } });
    if (!response.ok) {
      throw new Error(`HTTP ${response.status}`);
    }

    const dashboard = await response.json();
    renderSummary(dashboard.summary || {});
    renderAlerts(dashboard.alerts || []);
    renderSourceIps(dashboard.sourceIps || []);
    renderEvents(dashboard.recentEvents || []);
    lastUpdated.textContent = `Last updated: ${formatTimestamp(dashboard.updatedAt)}`;
  } catch (error) {
    lastUpdated.textContent = 'Live endpoint unavailable, using last known data';
  }
}

refreshButton.addEventListener('click', loadDashboard);
loadDashboard();
setInterval(loadDashboard, 10000);

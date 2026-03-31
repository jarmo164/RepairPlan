(function (window) {
  const STATUS_VARIANTS = {
    'Alustamata': 'secondary',
    'Üle vaadatud': 'info',
    'Elektrooniline parandus': 'primary',
    'Töös': 'warning',
    'Ootel': 'dark',
    'Lõpetatud': 'success',
    'Tagastatud': 'danger',
  };

  const PRIORITY_VARIANTS = {
    'Kõrge': 'danger',
    'Keskmine': 'warning',
    'Madal': 'primary',
  };

  function electronicsIcon() {
    return '<span class="electronics-icon" title="Elektrooniline"><svg viewBox="0 0 16 16" width="14" height="14" aria-hidden="true"><path fill="currentColor" d="M6 1h4v2h2v2h2v6h-2v2h-2v2H6v-2H4v-2H2V5h2V3h2V1Zm1 1v2h2V2H7ZM4 4v2H3v4h1v2h2v1h4v-1h2v-2h1V6h-1V4h-2V3H6v1H4Zm3 3h2v2H7V7Z"/></svg></span>';
  }

  function statusBadge(label) {
    const variant = STATUS_VARIANTS[label] || 'secondary';
    return `<span class="badge rounded-pill text-bg-${variant}">${label}</span>`;
  }

  function priorityBadge(label) {
    const variant = PRIORITY_VARIANTS[label] || 'dark';
    return `<span class="badge rounded-pill text-bg-${variant}">${label}</span>`;
  }

  function trackBadge(label) {
    if (label === 'Elektrooniline') {
      return `<span class="badge rounded-pill repair-track-badge">${electronicsIcon()}<span>Elektrooniline</span></span>`;
    }
    return `<span class="badge rounded-pill text-bg-light border"><span>Üldine</span></span>`;
  }

  function assigneeLabel(name, specialty) {
    if (!name) return '<span class="text-warning-emphasis">Määramata</span>';
    return specialty === 'ELECTRONICS' ? `${electronicsIcon()}<span>${name}</span>` : `<span>${name}</span>`;
  }

  function emptyState(message, colSpan = 1) {
    return `<tr><td colspan="${colSpan}" class="text-center text-body-secondary py-5">${message}</td></tr>`;
  }

  function feedback(message, type = 'success') {
    return `<div class="alert alert-${type} shadow-sm">${message}</div>`;
  }

  function debounce(fn, wait = 250) {
    let timeout;
    return (...args) => {
      clearTimeout(timeout);
      timeout = setTimeout(() => fn(...args), wait);
    };
  }

  window.RepairPlanUi = {
    statusBadge,
    priorityBadge,
    trackBadge,
    assigneeLabel,
    electronicsIcon,
    emptyState,
    feedback,
    debounce,
  };
})(window);

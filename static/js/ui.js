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
    return '<span class="electronics-icon" title="Elektrooniline parandaja"><svg viewBox="0 0 24 24" width="15" height="15" aria-hidden="true"><path fill="currentColor" d="M4 5.5A2.5 2.5 0 0 1 6.5 3h11A2.5 2.5 0 0 1 20 5.5v8a2.5 2.5 0 0 1-2.5 2.5h-11A2.5 2.5 0 0 1 4 13.5v-8Zm2.5-1A1.5 1.5 0 0 0 5 5.5v8A1.5 1.5 0 0 0 6.5 15h11a1.5 1.5 0 0 0 1.5-1.5v-8A1.5 1.5 0 0 0 17.5 4.5h-11ZM6.5 18a.5.5 0 0 1 .5-.5h10a.5.5 0 0 1 0 1H7a.5.5 0 0 1-.5-.5Zm.766-8.142a.5.5 0 0 1 .702-.092l2.146 1.717 2.134-3.048a.5.5 0 0 1 .807.01l1.41 2.074 1.666-1.666a.5.5 0 1 1 .707.707l-2.09 2.09a.5.5 0 0 1-.777-.067l-1.289-1.897-2.091 2.987a.5.5 0 0 1-.729.105L7.358 10.56a.5.5 0 0 1-.092-.702Z"/></svg></span>';
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

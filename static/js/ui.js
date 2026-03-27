(function (window) {
  const STATUS_VARIANTS = {
    'Alustamata': 'secondary',
    'Üle vaadatud': 'info',
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

  function statusBadge(label) {
    const variant = STATUS_VARIANTS[label] || 'secondary';
    return `<span class="badge rounded-pill text-bg-${variant}">${label}</span>`;
  }

  function priorityBadge(label) {
    const variant = PRIORITY_VARIANTS[label] || 'dark';
    return `<span class="badge rounded-pill text-bg-${variant}">${label}</span>`;
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
    emptyState,
    feedback,
    debounce,
  };
})(window);

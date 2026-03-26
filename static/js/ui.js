(function (window) {
  function statusBadge(label, variant = 'secondary') {
    return `<span class="badge text-bg-${variant}">${label}</span>`;
  }

  function priorityBadge(label, variant = 'dark') {
    return `<span class="badge text-bg-${variant}">${label}</span>`;
  }

  function emptyState(message, colSpan = 1) {
    return `<tr><td colspan="${colSpan}" class="text-center text-body-secondary py-4">${message}</td></tr>`;
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
    debounce,
  };
})(window);

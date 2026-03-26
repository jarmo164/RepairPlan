(function (window) {
  const loadingIndicator = () => document.getElementById('global-loading-indicator');

  function setLoading(isLoading) {
    const indicator = loadingIndicator();
    if (!indicator) return;
    indicator.classList.toggle('d-none', !isLoading);
  }

  function getCsrfToken() {
    const metaToken = document.querySelector('meta[name="csrf-token"]');
    if (metaToken?.content && metaToken.content !== 'NOTPROVIDED') {
      return metaToken.content;
    }
    const cookie = document.cookie.split('; ').find((row) => row.startsWith('csrftoken='));
    return cookie ? decodeURIComponent(cookie.split('=')[1]) : '';
  }

  async function request(method, url, data) {
    const headers = {
      'Accept': 'application/json',
    };
    const options = {
      method,
      headers,
      credentials: 'same-origin',
    };

    if (data !== undefined) {
      headers['Content-Type'] = 'application/json';
      options.body = JSON.stringify(data);
    }

    if (!['GET', 'HEAD', 'OPTIONS', 'TRACE'].includes(method)) {
      headers['X-CSRFToken'] = getCsrfToken();
    }

    setLoading(true);
    try {
      const response = await fetch(url, options);
      const contentType = response.headers.get('content-type') || '';
      const payload = contentType.includes('application/json') ? await response.json() : await response.text();

      if (!response.ok) {
        const detail = typeof payload === 'object' ? (payload.detail || JSON.stringify(payload)) : payload;
        throw new Error(detail || `Request failed with status ${response.status}`);
      }

      return payload;
    } catch (error) {
      console.error('RepairPlan API error', error);
      throw error;
    } finally {
      setLoading(false);
    }
  }

  window.RepairPlanApi = {
    get(url) { return request('GET', url); },
    post(url, data) { return request('POST', url, data); },
    patch(url, data) { return request('PATCH', url, data); },
    delete(url) { return request('DELETE', url); },
  };
})(window);

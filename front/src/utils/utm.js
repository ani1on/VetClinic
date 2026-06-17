const UTM_KEYS = ['utm_source', 'utm_medium', 'utm_campaign', 'utm_term', 'utm_content'];
const UTM_STORAGE_KEY = 'utm_params';

export function parseUTMFromURL(url) {
  try {
    const parsed = new URL(url, window.location.origin);
    const params = {};
    let found = false;
    for (const key of UTM_KEYS) {
      const value = parsed.searchParams.get(key);
      if (value) {
        params[key] = value;
        found = true;
      }
    }
    return found ? params : null;
  } catch {
    return null;
  }
}

export function saveUTM(params) {
  if (params && Object.keys(params).length > 0) {
    localStorage.setItem(UTM_STORAGE_KEY, JSON.stringify(params));
  }
}

export function getUTM() {
  try {
    const raw = localStorage.getItem(UTM_STORAGE_KEY);
    return raw ? JSON.parse(raw) : {};
  } catch {
    return {};
  }
}

export function clearUTM() {
  localStorage.removeItem(UTM_STORAGE_KEY);
}

export function captureUTMFromCurrentURL() {
  const params = parseUTMFromURL(window.location.href);
  if (params) {
    saveUTM(params);
  }
}

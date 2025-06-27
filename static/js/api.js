import { showAppMessage } from './notif.js';

export async function apiRequest(url, { method = 'GET', body = null, headers = {} } = {}) {
  const config = {
    method: method.toUpperCase(),
    headers: {
      'Content-Type': 'application/json',
      'X-CSRFToken': window.CSRF_TOKEN,  // Use global token
      ...headers
    }
  };

  if (body) {
    config.body = JSON.stringify(body);
  }

  try {
    const response = await fetch(url, config);

    if (!response.ok) {
      throw new Error(`HTTP ${response.status}: ${response.statusText}`);
    }

    const result = await response.json()
    showAppMessage(result.message, result.status)
    
  } catch (error) {
    console.error('API Request Error:', error);
    throw error;
  }
}

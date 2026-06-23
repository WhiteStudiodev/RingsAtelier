const API_BASE = import.meta.env.VITE_API_URL || 'http://localhost:8000'
const API_URL = API_BASE.endsWith('/api') ? API_BASE : `${API_BASE}/api`

const fetchWithTimeout = (url, options, timeout = 10000) => {
  return Promise.race([
    fetch(url, options),
    new Promise((_, reject) =>
      setTimeout(() => reject(new Error('Request timeout')), timeout)
    )
  ])
}

export const submitLead = async (form) => {
  const response = await fetchWithTimeout(`${API_URL}/leads`, {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify({
      name: form.name,
      method: form.method,
      contact: form.contact,
      message: form.message
    })
  })

  if (!response.ok) {
    let errorMessage = 'Не удалось отправить заявку. Попробуйте ещё раз.'
    try {
      const data = await response.json()
      if (data.detail) {
        errorMessage = typeof data.detail === 'string'
          ? data.detail
          : 'Ошибка в данных заявки.'
      }
    } catch {
      // ignore JSON parse errors
    }
    throw new Error(errorMessage)
  }

  return response.json()
}

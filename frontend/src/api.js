const API_BASE_URL = import.meta.env.VITE_API_BASE_URL || "http://localhost:8000";

async function handleResponse(response) {
  if (!response.ok) {
    let message = `Request failed with status ${response.status}`;
    try {
      const data = await response.json();
      message = data.detail || message;
    } catch {
      // Keep default message when response is not JSON.
    }
    throw new Error(message);
  }
  return response.json();
}

export async function generateProject({ title, requirements }) {
  const response = await fetch(`${API_BASE_URL}/api/generate`, {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify({ title, requirements }),
  });
  return handleResponse(response);
}

export async function fetchProjects() {
  const response = await fetch(`${API_BASE_URL}/api/projects`);
  return handleResponse(response);
}

export async function fetchProjectById(id) {
  const response = await fetch(`${API_BASE_URL}/api/projects/${id}`);
  return handleResponse(response);
}

export async function deleteProject(id) {
  const response = await fetch(`${API_BASE_URL}/api/projects/${id}`, { method: "DELETE" });
  return handleResponse(response);
}

import { API_URL } from "../constants/Api";

export async function login(email: string, password: string) {
  const res = await fetch(`${API_URL}/login/`, {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify({ email, password }),
  });
  if (!res.ok) throw new Error("Błąd logowania");
  return res.json();
}

export async function getNotes(apiKey: string, userId: number) {
  const res = await fetch(`${API_URL}/notes/?user_id=${userId}`, {
    headers: { "api-key": apiKey },
  });
  if (!res.ok) throw new Error("Błąd pobierania notatek");
  return res.json();
}

export async function getNote(apiKey: string, noteId: number, userId: number) {
  const res = await fetch(`${API_URL}/notes/${noteId}?user_id=${userId}&api_key=${apiKey}`);
  if (!res.ok) {
    console.log("getNote error", res.status, await res.text());
    throw new Error("Błąd pobierania notatki");
  }
  return res.json();
}

export async function getTagsForNote(apiKey: string, noteId: number, userId: number) {
  const res = await fetch(
    `${API_URL}/tags/?note_id=${noteId}&user_id=${userId}`,
    {
      headers: { "api-key": apiKey },
    }
  );
  if (!res.ok) return [];
  return res.json();
}

// Utwórz nowy tag dla notatki
export async function createTag(apiKey: string, userId: number, noteId: number, name: string) {
  const res = await fetch(`${API_URL}/tags/?user_id=${userId}`, {
    method: "POST",
    headers: {
      "Content-Type": "application/json",
      "api-key": apiKey,
    },
    body: JSON.stringify({ name, note_id: noteId }),
  });
  if (!res.ok) {
    const err = await res.text();
    throw new Error(err || "Błąd tworzenia tagu");
  }
  return res.json();
}

// Edytuj tag
export async function updateTag(apiKey: string, userId: number, tagId: number, name: string) {
  const res = await fetch(`${API_URL}/tags/${tagId}?user_id=${userId}`, {
    method: "PUT",
    headers: {
      "Content-Type": "application/json",
      "api-key": apiKey,
    },
    body: JSON.stringify({ name }),
  });
  if (!res.ok) {
    const err = await res.text();
    throw new Error(err || "Błąd edycji tagu");
  }
  return res.json();
}

// Usuń tag
export async function deleteTag(apiKey: string, userId: number, tagId: number) {
  const res = await fetch(`${API_URL}/tags/${tagId}?user_id=${userId}`, {
    method: "DELETE",
    headers: {
      "api-key": apiKey,
    },
  });
  if (!res.ok) {
    const err = await res.text();
    throw new Error(err || "Błąd usuwania tagu");
  }
  return res.json();
}

export async function createNote(apiKey: string, userId: number, note: any) {
  const res = await fetch(`${API_URL}/notes/?user_id=${userId}&api_key=${apiKey}`, {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify(note),
  });
  if (!res.ok) {
    const err = await res.text();
    throw new Error(err || "Błąd tworzenia notatki");
  }
  return res.json();
}

export async function deleteNote(apiKey: string, userId: number, noteId: number) {
  const res = await fetch(`${API_URL}/notes/${noteId}?user_id=${userId}&api_key=${apiKey}`, {
    method: "DELETE",
  });
  if (!res.ok) {
    const err = await res.text();
    throw new Error(err || "Błąd usuwania notatki");
  }
  return res.json();
}

export async function getUserTags(apiKey: string, userId: number) {
  const res = await fetch(`${API_URL}/users/${userId}/tags/`, {
    headers: { Authorization: `Bearer ${apiKey}` },
  });
  if (!res.ok) throw new Error("Błąd pobierania tagów");
  return res.json();
}

export async function getUserData(apiKey: string, userId: number) {
  const res = await fetch(`${API_URL}/users/${userId}/`, {
    headers: { Authorization: `Bearer ${apiKey}` },
  });
  if (!res.ok) throw new Error("Błąd pobierania użytkownika");
  return res.json();
}

export async function exportUserData(apiKey: string, userId: number) {
  const res = await fetch(`${API_URL}/export_data?user_id=${userId}`, {
    headers: { "api-key": apiKey },
  });
  if (!res.ok) throw new Error("Błąd eksportu danych");
  return res.json();
}

export async function pingBackend() {
  try {
    const res = await fetch(`${API_URL}/ping`);
    if (!res.ok) return false;
    const data = await res.json();
    return data.status === "ok";
  } catch {
    return false;
  }
}
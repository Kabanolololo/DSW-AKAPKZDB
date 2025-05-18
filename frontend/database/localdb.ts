import * as SQLite from "expo-sqlite";

const db = SQLite.openDatabaseSync("localdb.db");

// Inicjalizacja bazy
export function initLocalDb() {
  db.execSync(`
    CREATE TABLE IF NOT EXISTS users (
      id INTEGER PRIMARY KEY AUTOINCREMENT,
      nick TEXT NOT NULL,
      email TEXT NOT NULL UNIQUE
    );
    CREATE TABLE IF NOT EXISTS notes (
      id INTEGER PRIMARY KEY AUTOINCREMENT,
      user_id INTEGER NOT NULL,
      title TEXT NOT NULL,
      content TEXT,
      created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
      updated_at DATETIME DEFAULT CURRENT_TIMESTAMP,
      FOREIGN KEY (user_id) REFERENCES users(id) ON DELETE CASCADE
    );
    CREATE TABLE IF NOT EXISTS tags (
      id INTEGER PRIMARY KEY AUTOINCREMENT,
      name TEXT NOT NULL
    );
    CREATE TABLE IF NOT EXISTS note_tags (
      note_id INTEGER NOT NULL,
      tag_id INTEGER NOT NULL,
      PRIMARY KEY (note_id, tag_id),
      FOREIGN KEY (note_id) REFERENCES notes(id) ON DELETE CASCADE,
      FOREIGN KEY (tag_id) REFERENCES tags(id) ON DELETE CASCADE
    );
  `);
}

export function getLocalNotes(userId: number): any[] {
  return db.getAllSync<any>(
    "SELECT * FROM notes WHERE user_id = ? ORDER BY updated_at DESC",
    [userId]
  );
}

export function getCurrentUser(userId: number): any | null {
  const users = db.getAllSync<any>("SELECT * FROM users WHERE id = ?", [userId]);
  return users.length > 0 ? users[0] : null;
}

export function getUserTags(userId: number): any[] {
  return db.getAllSync<any>(
    `SELECT DISTINCT t.* FROM tags t
     JOIN note_tags nt ON t.id = nt.tag_id
     JOIN notes n ON nt.note_id = n.id
     WHERE n.user_id = ?`,
    [userId]
  );
}

export function saveUsersToLocalDb(users: any[]) {
  for (const user of users) {
    try {
      db.runSync(
        "INSERT OR REPLACE INTO users (id, nick, email) VALUES (?, ?, ?)",
        [user.id, user.nick, user.email]
      );
    } catch (e) {
      console.log("Błąd zapisu usera:", user, e);
    }
  }
}

export function saveTagsToLocalDb(tags: any[]) {
  for (const tag of tags) {
    db.runSync(
      "INSERT OR REPLACE INTO tags (id, name) VALUES (?, ?)",
      [tag.id, tag.name]
    );
  }
}

export function saveNoteTagsToLocalDb(noteTags: any[]) {
  for (const nt of noteTags) {
    db.runSync(
      "INSERT OR REPLACE INTO note_tags (note_id, tag_id) VALUES (?, ?)",
      [nt.note_id, nt.tag_id]
    );
  }
}

export function saveNotesToLocalDb(userId: number, notes: any[]) {
  for (const note of notes) {
    db.runSync(
      "INSERT OR REPLACE INTO notes (id, user_id, title, content, created_at, updated_at) VALUES (?, ?, ?, ?, ?, ?)",
      [
        note.id,
        note.user_id,
        note.title,
        note.content,
        note.created_at,
        note.updated_at,
      ]
    );
  }
}

export function clearUserNotes(userId: number) {
  db.runSync("DELETE FROM notes WHERE user_id = ?", [userId]);
}

export function getAllUsers(): any[] {
  return db.getAllSync<any>("SELECT * FROM users", []);
}

export function getAllTags(): any[] {
  return db.getAllSync<any>("SELECT * FROM tags", []);
}


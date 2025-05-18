import React, { createContext, useState, useContext } from "react";
import { getNotes, getUserTags as getUserTagsApi, getUserData, login, exportUserData } from "../services/api";
import { saveNotesToLocalDb, saveTagsToLocalDb, saveUsersToLocalDb, clearUserNotes, getAllUsers, getAllTags, getLocalNotes, getCurrentUser, getUserTags as getUserTagsLocal } from "../database/localdb";

type AuthContextType = {
  apiKey: string | null;
  setApiKey: (key: string | null) => void;
  userId: number | null;
  setUserId: (id: number | null) => void;
  logout: () => void;
};

const AuthContext = createContext<AuthContextType | undefined>(undefined);

export const AuthProvider: React.FC<{ children: React.ReactNode }> = ({ children }) => {
  const [apiKey, setApiKey] = useState<string | null>(null);
  const [userId, setUserId] = useState<number | null>(null);

  const syncAllUserData = async (apiKey: string, userId: number) => {
    const data = await exportUserData(apiKey, userId);
    saveUsersToLocalDb(data.users);
    saveNotesToLocalDb(userId, data.notes);
    saveTagsToLocalDb(data.tags);

    // Logi po zapisie!
    console.log("Użytkownicy:", getAllUsers());
    console.log("Notatki:", getLocalNotes(userId));
    console.log("Tagi:", getAllTags());
    console.log("Aktualny użytkownik:", getCurrentUser(userId));
    console.log("Tagi użytkownika:", getUserTagsLocal(userId));
  };

  const handleLogin = async (email: string, password: string) => {
    const loginData = await login(email, password);
    setApiKey(loginData.api_key);
    setUserId(loginData.user_id);

    await syncAllUserData(loginData.api_key, loginData.user_id);
  };

  const logout = () => {
    if (userId) {
      clearUserNotes(userId);
    }
    setApiKey(null);
    setUserId(null);
  };

  return (
    <AuthContext.Provider value={{ apiKey, setApiKey, userId, setUserId, logout }}>
      {children}
    </AuthContext.Provider>
  );
};

export function useAuth() {
  const ctx = useContext(AuthContext);
  if (!ctx) throw new Error("useAuth must be used within AuthProvider");
  return ctx;
}
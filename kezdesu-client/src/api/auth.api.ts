import { User } from "../types/user";

const API_URL = "http://127.0.0.1:8000/auth";

export const getMe = async (): Promise<User | null> => {
  const res = await fetch(`${API_URL}/me`, { credentials: "include" });
  if (!res.ok) return null;
  return res.json();
};

export const logoutApi = async (): Promise<void> => {
  await fetch(`${API_URL}/logout`, { credentials: "include" });
};

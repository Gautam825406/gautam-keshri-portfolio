import type { Profile, Project, SkillGroup } from "./types";

// Same-origin by default: Vite proxies /api in dev, nginx proxies /api in
// Docker. Set VITE_API_URL only if the API lives on another origin.
const BASE = (import.meta.env.VITE_API_URL as string | undefined) || "";

export function adminKey(): string {
  return sessionStorage.getItem("portfolio_admin_key") || "";
}

export function setAdminKey(key: string) {
  if (key) sessionStorage.setItem("portfolio_admin_key", key);
  else sessionStorage.removeItem("portfolio_admin_key");
}

async function req<T>(path: string, init?: RequestInit): Promise<T> {
  const res = await fetch(`${BASE}${path}`, {
    ...init,
    headers: { "Content-Type": "application/json", ...(init?.headers || {}) },
  });
  if (!res.ok) {
    const body = await res.json().catch(() => ({}));
    throw new Error(body.detail || `Request failed: ${res.status}`);
  }
  return res.json() as Promise<T>;
}

export const api = {
  getProfile: () => req<Profile>("/api/profile"),
  getProjects: () => req<Project[]>("/api/projects"),
  getSkills: () => req<SkillGroup[]>("/api/skills"),
  updateProfile: (data: Omit<Profile, "id">) =>
    req<Profile>("/api/profile", {
      method: "PUT",
      headers: { "X-Admin-Key": adminKey() },
      body: JSON.stringify(data),
    }),
  createProject: (data: Omit<Project, "id">) =>
    req<Project>("/api/projects", {
      method: "POST",
      headers: { "X-Admin-Key": adminKey() },
      body: JSON.stringify(data),
    }),
  updateProject: (id: number, data: Omit<Project, "id">) =>
    req<Project>(`/api/projects/${id}`, {
      method: "PUT",
      headers: { "X-Admin-Key": adminKey() },
      body: JSON.stringify(data),
    }),
  deleteProject: (id: number) =>
    req<{ deleted: number }>(`/api/projects/${id}`, {
      method: "DELETE",
      headers: { "X-Admin-Key": adminKey() },
    }),
  updateSkills: (groups: SkillGroup[]) =>
    req<SkillGroup[]>("/api/skills", {
      method: "PUT",
      headers: { "X-Admin-Key": adminKey() },
      body: JSON.stringify({ groups }),
    }),
};

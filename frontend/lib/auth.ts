import type { AppRouterInstance } from "next/dist/shared/lib/app-router-context.shared-runtime";

const ACCESS_TOKEN_KEY = "access";
const REFRESH_TOKEN_KEY = "refresh";

/** Cookie max-age (seconds). Middleware only checks presence; align with refresh lifetime ~7d. */
const TOKEN_COOKIE_MAX_AGE = 60 * 60 * 24 * 7;

function setClientCookie(name: string, value: string, maxAge: number) {
  if (typeof document === "undefined") return;
  const encoded = encodeURIComponent(value);
  document.cookie = `${name}=${encoded}; path=/; max-age=${maxAge}; SameSite=Lax`;
}

function clearClientCookie(name: string) {
  if (typeof document === "undefined") return;
  document.cookie = `${name}=; path=/; max-age=0`;
}

export function setTokens(access: string, refresh: string) {
  localStorage.setItem(ACCESS_TOKEN_KEY, access);
  localStorage.setItem(REFRESH_TOKEN_KEY, refresh);
  // Middleware cannot read localStorage; mirror into cookies for /dashboard etc.
  setClientCookie(ACCESS_TOKEN_KEY, access, TOKEN_COOKIE_MAX_AGE);
  setClientCookie(REFRESH_TOKEN_KEY, refresh, TOKEN_COOKIE_MAX_AGE);
}

export function getAccessToken() {
  return localStorage.getItem(ACCESS_TOKEN_KEY);
}

export function logout() {
  localStorage.removeItem(ACCESS_TOKEN_KEY);
  localStorage.removeItem(REFRESH_TOKEN_KEY);
  clearClientCookie(ACCESS_TOKEN_KEY);
  clearClientCookie(REFRESH_TOKEN_KEY);
}

export function redirectIfNoToken(router: AppRouterInstance, target = "/login") {
  const token = getAccessToken();
  if (!token) {
    router.replace(target);
    return true;
  }
  return false;
}

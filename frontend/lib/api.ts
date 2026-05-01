import { getAccessToken } from "./auth";

export async function apiFetch(
  input: RequestInfo | URL,
  init: RequestInit = {},
) {
  const token = getAccessToken();
  if (!token) {
    if (typeof window !== "undefined") {
      window.location.href = "/login";
    }
    throw new Error("No access token");
  }

  const headers = new Headers(init.headers || {});
  headers.set("Authorization", `Bearer ${token}`);

  return fetch(input, {
    ...init,
    headers,
  });
}

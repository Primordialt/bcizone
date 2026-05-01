import { NextRequest, NextResponse } from "next/server";

const PUBLIC_ROUTES = new Set(["/", "/login", "/register"]);
const PROTECTED_PREFIXES = ["/dashboard", "/loan", "/profile"];

export function middleware(request: NextRequest) {
  const { pathname } = request.nextUrl;

  // Allow explicit public routes and registration subpaths.
  if (PUBLIC_ROUTES.has(pathname) || pathname.startsWith("/register/")) {
    return NextResponse.next();
  }

  const isProtected = PROTECTED_PREFIXES.some(
    (prefix) => pathname === prefix || pathname.startsWith(`${prefix}/`),
  );
  if (!isProtected) {
    return NextResponse.next();
  }

  // Middleware runs server-side; token must be available via cookie/header.
  const cookieToken = request.cookies.get("access")?.value;
  const authHeader = request.headers.get("authorization");
  const headerToken = authHeader?.startsWith("Bearer ")
    ? authHeader.slice("Bearer ".length).trim()
    : "";
  const token = cookieToken || headerToken;

  if (!token) {
    const loginUrl = new URL("/login", request.url);
    return NextResponse.redirect(loginUrl);
  }

  return NextResponse.next();
}

export const config = {
  matcher: [
    "/dashboard",
    "/dashboard/:path*",
    "/loan",
    "/loan/:path*",
    "/profile",
    "/profile/:path*",
    "/",
    "/login",
    "/register",
    "/register/:path*",
  ],
};

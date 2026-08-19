"use client";

import Link from "next/link";
import { useRouter } from "next/navigation";
import { FormEvent, useMemo, useState } from "react";
import { getApiBaseUrl } from "@/lib/api-base";
import { setTokens } from "@/lib/auth";

export default function LoginPage() {
  const router = useRouter();
  const [email, setEmail] = useState("");
  const [password, setPassword] = useState("");
  const [rememberMe, setRememberMe] = useState(true);
  const [showPassword, setShowPassword] = useState(false);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState("");

  const buttonText = useMemo(() => (loading ? "Signing In..." : "Sign In"), [loading]);

  function apiErrorMessage(data: Record<string, unknown>): string {
    const detail = data.detail;
    if (typeof detail === "string") return detail;
    if (Array.isArray(detail) && detail.length > 0) return String(detail[0]);
    const nfe = data.non_field_errors;
    if (Array.isArray(nfe) && typeof nfe[0] === "string") return nfe[0];
    for (const val of Object.values(data)) {
      if (Array.isArray(val) && val.length > 0) {
        const first = val[0];
        if (typeof first === "string") return first;
        if (first != null && typeof first === "object" && "string" in first) {
          return String((first as { string?: string }).string ?? first);
        }
      }
    }
    return "Invalid credentials";
  }

  const handleSubmit = async (event: FormEvent<HTMLFormElement>) => {
    event.preventDefault();
    event.stopPropagation();
    setError("");
    setLoading(true);
    try {
      const response = await fetch(`${getApiBaseUrl()}/api/auth/token/`, {
        method: "POST",
        headers: {
          "Content-Type": "application/json",
        },
        body: JSON.stringify({
          email,
          password,
        }),
      });

      let data: Record<string, unknown>;
      try {
        data = (await response.json()) as Record<string, unknown>;
      } catch {
        setError(
          response.ok
            ? "Invalid server response."
            : `Login failed (${response.status}). Check that the API is running.`,
        );
        return;
      }
      if (!response.ok) {
        setError(apiErrorMessage(data));
        return;
      }

      const access = typeof data.access === "string" ? data.access : "";
      const refresh = typeof data.refresh === "string" ? data.refresh : "";
      if (!access || !refresh) {
        setError("Invalid credentials");
        return;
      }

      setTokens(access, refresh);
      if (rememberMe) {
        localStorage.setItem("rememberMe", "true");
      } else {
        localStorage.removeItem("rememberMe");
      }
      router.push("/dashboard");
    } catch {
      setError(`Network error. Is the backend running at ${getApiBaseUrl()}?`);
    } finally {
      setLoading(false);
    }
  };

  return (
    <>
      <link rel="shortcut icon" href="/assets/images/favicon.png" />
      <link href="/assets/fonts/fontawesome/css/all.css" rel="stylesheet" type="text/css" />
      <link href="/css/plugins.bundle.css" rel="stylesheet" type="text/css" />
      <link href="/css/style.bundle.css" rel="stylesheet" type="text/css" />
      <link
        rel="stylesheet"
        href="https://cdn.jsdelivr.net/gh/lipis/flag-icons@6.6.6/css/flag-icons.min.css"
      />
      <link rel="stylesheet" href="/assets/filepond/css/filepond.css" />

      <style>{`
        .iti { position: relative; display: block; }
        body { font-family: "Graphik", sans-serif; }
      `}</style>

      <div
        id="kt_body"
        className="bg-light auth-bg header-fixed header-tablet-and-mobile-fixed toolbar-enabled aside-fixed aside-default-enabled"
      >
        <div className="row justify-content-center">
          <div className="col-md-6">
            <div className="py-10">
              <div className="p-10 p-lg-15 mx-auto">
                <div className="text-center">
                  <Link href="/" className="navbar-brand pe-3">
                    <img
                      className="mb-6 text-center"
                      src="/assets/images/logo.png"
                      width="200"
                      alt="Bespoke"
                      loading="lazy"
                    />
                  </Link>
                </div>
                <div className="card rounded-5">
                  <div className="card-body m-5">
                    <form className="form" onSubmit={handleSubmit}>
                      <div className="text-start mb-10">
                        <h1 className="text-dark mb-3 fs-2">Jump right back in</h1>
                        <div className="text-dark fw-bold fs-5">
                          New Here?{" "}
                          <Link href="/register/create_account" className="link-info fw-bolder">
                            Create an Account
                          </Link>
                        </div>
                      </div>
                      <div className="fv-row mb-10">
                        <label className="form-label fs-6 fw-bolder text-dark">Email</label>
                        <input
                          className="form-control form-control-lg form-control-solid border-light"
                          type="email"
                          autoComplete="email"
                          value={email}
                          onChange={(e) => setEmail(e.target.value)}
                          required
                          placeholder="name@email.com"
                        />
                      </div>
                      <div className="fv-row mb-10">
                        <div className="d-flex flex-stack mb-2">
                          <label className="form-label fw-bolder text-dark fs-6 mb-0">
                            Password
                          </label>
                          <span
                            className="text-muted fs-6 fw-bolder"
                            aria-disabled="true"
                            title="Password reset is not available"
                          >
                            Forgot Password ?
                          </span>
                        </div>
                        <div className="position-relative">
                          <input
                            className="form-control form-control-lg form-control-solid border-light"
                            type={showPassword ? "text" : "password"}
                            autoComplete="off"
                            required
                            id="password"
                            value={password}
                            onChange={(e) => setPassword(e.target.value)}
                            placeholder="XXXXXXXXX"
                          />
                          <span
                            className="btn btn-sm btn-icon position-absolute translate-middle top-50 end-0 me-n2 input-password"
                            onClick={() => setShowPassword((v) => !v)}
                            style={{ cursor: "pointer" }}
                          >
                            <i className={`bi fs-2 text-dark ${showPassword ? "bi-eye-slash" : "bi-eye"}`} />
                          </span>
                        </div>
                      </div>
                      <div className="form-check form-check-custom form-check-solid mb-6">
                        <input
                          className="form-check-input"
                          type="checkbox"
                          id="flexCheckDefault"
                          checked={rememberMe}
                          onChange={(e) => setRememberMe(e.target.checked)}
                        />
                        <label className="form-check-label" htmlFor="flexCheckDefault">
                          Stayed signed in for 30 days
                        </label>
                      </div>
                      {error ? (
                        <div className="alert alert-danger py-3 mb-6" role="alert">
                          {error}
                        </div>
                      ) : null}
                      <div className="text-center">
                        <button
                          type="submit"
                          className="btn btn-lg btn-info btn-block fw-bolder me-3 my-2"
                          disabled={loading}
                        >
                          <span>{buttonText}</span>
                        </button>
                      </div>
                    </form>
                  </div>
                </div>
              </div>
            </div>
            <div className="d-flex flex-center flex-wrap fs-6 p-5 pb-0">
              <div className="d-flex flex-center fw-bold fs-6">
                <span className="text-muted px-2" aria-disabled="true">
                  About
                </span>
                <Link href="/terms" className="text-dark text-hover-primary px-2">
                  Terms &amp; Conditions
                </Link>
                <Link href="/privacy" className="text-dark text-hover-primary px-2">
                  Privacy
                </Link>
              </div>
            </div>
          </div>
        </div>
      </div>
    </>
  );
}

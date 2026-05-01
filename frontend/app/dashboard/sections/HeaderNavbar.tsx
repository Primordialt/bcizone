"use client";

import Link from "next/link";
import { useRouter } from "next/navigation";
import { useEffect, useRef, useState } from "react";

import { logout } from "@/lib/auth";

type HeaderNavbarProps = {
  userLabel?: string;
  onMobileMenuClick: () => void;
};

export function HeaderNavbar({ userLabel, onMobileMenuClick }: HeaderNavbarProps) {
  const router = useRouter();
  const [userMenuOpen, setUserMenuOpen] = useState(false);
  const menuRef = useRef<HTMLDivElement>(null);

  useEffect(() => {
    if (!userMenuOpen) return;
    const close = (e: MouseEvent) => {
      if (menuRef.current && !menuRef.current.contains(e.target as Node)) {
        setUserMenuOpen(false);
      }
    };
    document.addEventListener("click", close);
    return () => document.removeEventListener("click", close);
  }, [userMenuOpen]);

  const handleSignOut = () => {
    logout();
    router.replace("/login");
  };

  return (
    <div id="kt_header" className="header align-items-stretch">
      <div className="container-fluid d-flex align-items-stretch justify-content-between">
        <div className="d-flex align-items-center d-lg-none ms-n2 me-2">
          <button
            type="button"
            className="btn btn-icon btn-active-color-primary w-35px h-35px border-0 bg-transparent"
            id="kt_aside_mobile_toggle"
            aria-label="Open menu"
            onClick={onMobileMenuClick}
          >
            <i className="bi bi-list fs-1" />
          </button>
        </div>
        <div className="d-flex align-items-stretch justify-content-between flex-lg-grow-1">
          <div className="d-flex align-items-stretch" id="kt_header_nav" />
          <div className="d-flex align-items-stretch flex-shrink-0">
            <div className="d-flex align-items-center ms-1 ms-lg-3" ref={menuRef}>
              <div className={`dropdown${userMenuOpen ? " show" : ""}`}>
                <button
                  type="button"
                  className="btn btn-flex btn-light-primary align-items-center rounded-pill px-3 py-2"
                  aria-expanded={userMenuOpen}
                  onClick={() => setUserMenuOpen((v) => !v)}
                >
                  <span className="symbol symbol-30px symbol-circle me-2 bg-light-primary text-primary fw-bold">
                    {(userLabel || "U").slice(0, 1).toUpperCase()}
                  </span>
                  <span className="text-gray-900 fw-semibold text-truncate max-w-125px">
                    {userLabel || "Account"}
                  </span>
                  <i className="bi bi-chevron-down fs-7 ms-2 text-gray-600" />
                </button>
                <div
                  className={`dropdown-menu dropdown-menu-end py-3 w-200px${userMenuOpen ? " show" : ""}`}
                  data-popper-placement="bottom-end"
                >
                  <div className="px-3 pb-3 border-bottom border-gray-200 mb-2">
                    <span className="fw-bold text-gray-900 text-truncate d-block">{userLabel || "Account"}</span>
                  </div>
                  <Link href="/" className="dropdown-item px-3 py-2" onClick={() => setUserMenuOpen(false)}>
                    Home
                  </Link>
                  <button
                    type="button"
                    className="dropdown-item px-3 py-2 text-start w-100"
                    onClick={() => {
                      setUserMenuOpen(false);
                      handleSignOut();
                    }}
                  >
                    Sign out
                  </button>
                </div>
              </div>
            </div>
          </div>
        </div>
      </div>
    </div>
  );
}

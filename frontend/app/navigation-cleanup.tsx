"use client";

import { usePathname } from "next/navigation";
import { useEffect, useLayoutEffect } from "react";

/**
 * Strip legacy / Bootstrap overlays that stay on document.body after SPA navigations
 * (offcanvas backdrops, modal backdrops, Metronic page loader divs, body.page-loading).
 * Without this, the UI stays dimmed and non-interactive.
 */
function stripBlockingOverlays() {
  document.querySelectorAll(".offcanvas-backdrop").forEach((el) => el.remove());
  document.querySelectorAll(".modal-backdrop").forEach((el) => el.remove());

  document.querySelectorAll(".offcanvas.show").forEach((el) => {
    el.classList.remove("show");
  });

  document.querySelectorAll(".page-loading").forEach((el) => {
    if (el !== document.body) el.remove();
  });

  document.body.classList.remove("modal-open", "page-loading");
  document.body.removeAttribute("data-kt-app-page-loading");
  document.body.style.overflow = "";
  document.body.style.removeProperty("padding-right");
  document.documentElement.style.overflow = "";
  document.documentElement.style.removeProperty("padding-right");
  document.documentElement.classList.remove("overflow-hidden");

  document.body.removeAttribute("data-kt-drawer");

  try {
    sessionStorage.removeItem("preloader");
  } catch {
    /* ignore */
  }
}

export function NavigationCleanup() {
  const pathname = usePathname();

  useLayoutEffect(() => {
    stripBlockingOverlays();
  }, [pathname]);

  useEffect(() => {
    stripBlockingOverlays();
    const t = window.setTimeout(stripBlockingOverlays, 0);
    const id = window.requestAnimationFrame(() => stripBlockingOverlays());
    return () => {
      window.clearTimeout(t);
      window.cancelAnimationFrame(id);
    };
  }, [pathname]);

  return null;
}

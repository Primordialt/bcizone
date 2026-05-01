"use client";

import { useSyncExternalStore } from "react";

const QUERY = "(min-width: 992px)";

function subscribe(onChange: () => void) {
  const mq = window.matchMedia(QUERY);
  mq.addEventListener("change", onChange);
  return () => mq.removeEventListener("change", onChange);
}

function getSnapshot() {
  return window.matchMedia(QUERY).matches;
}

/** SSR / first paint: assume desktop so we do not flash mobile drawer on wide screens */
function getServerSnapshot() {
  return true;
}

export function useMediaMinLg(): boolean {
  return useSyncExternalStore(subscribe, getSnapshot, getServerSnapshot);
}

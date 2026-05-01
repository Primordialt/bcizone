"use client";

import { usePathname } from "next/navigation";
import type { ReactNode } from "react";
import { useEffect, useState } from "react";

import { HeaderNavbar } from "./HeaderNavbar";
import { MainContent } from "./MainContent";
import { Sidebar } from "./Sidebar";
import { useMediaMinLg } from "./useMediaMinLg";

const KT_BODY_CLASSES =
  "header-fixed header-tablet-and-mobile-fixed toolbar-enabled aside-fixed aside-default-enabled bg-light";

type DashboardShellProps = {
  children: ReactNode;
  userLabel?: string;
  mainTitle?: string;
};

function DashboardShellInner({ children, userLabel, mainTitle }: DashboardShellProps) {
  const isLg = useMediaMinLg();
  const [mobileDrawerOpen, setMobileDrawerOpen] = useState(false);
  const showMobileDrawer = mobileDrawerOpen && !isLg;

  const closeDrawer = () => setMobileDrawerOpen(false);
  const toggleDrawer = () => setMobileDrawerOpen((v) => !v);

  useEffect(() => {
    if (!showMobileDrawer) return;
    const onKey = (e: KeyboardEvent) => {
      if (e.key === "Escape") setMobileDrawerOpen(false);
    };
    document.addEventListener("keydown", onKey);
    return () => document.removeEventListener("keydown", onKey);
  }, [showMobileDrawer]);

  return (
    <>
      <link rel="shortcut icon" href="/assets/images/favicon.png" />
      <link href="/assets/fonts/fontawesome/css/all.css" rel="stylesheet" type="text/css" />
      <link href="/css/plugins.bundle.css" rel="stylesheet" type="text/css" />
      <link href="/css/style.bundle.css" rel="stylesheet" type="text/css" />

      <style>{`
        @font-face {
          font-family: Graphik;
          font-weight: 400;
          src: url("/assets/fonts/Graphik/GraphikRegular.otf") format("opentype");
        }
        @font-face {
          font-family: Graphik;
          font-weight: 500;
          src: url("/assets/fonts/Graphik/GraphikMedium.otf") format("opentype");
        }
        @font-face {
          font-family: Graphik;
          font-weight: 700;
          src: url("/assets/fonts/Graphik/GraphikBold.otf") format("opentype");
        }
        .iti { position: relative; display: block; }
        #kt_body, #kt_body * { box-sizing: border-box; }
        #kt_body { font-family: Graphik, system-ui, -apple-system, sans-serif; }
      `}</style>

      <div
        id="kt_body"
        className={KT_BODY_CLASSES}
        {...(showMobileDrawer ? { "data-kt-drawer": "on" as const } : {})}
      >
        <div className="d-flex flex-column flex-root">
          <div className="page d-flex flex-row flex-column-fluid">
            <Sidebar isLg={isLg} mobileDrawerOpen={showMobileDrawer} onNavLinkClick={closeDrawer} />
            <div className="wrapper d-flex flex-column flex-row-fluid" id="kt_wrapper">
              <HeaderNavbar userLabel={userLabel} onMobileMenuClick={toggleDrawer} />
              <div className="content d-flex flex-column flex-column-fluid" id="kt_content">
                <MainContent title={mainTitle}>{children}</MainContent>
              </div>
            </div>
          </div>
        </div>
      </div>

      {showMobileDrawer ? (
        <button
          type="button"
          className="drawer-overlay border-0 p-0"
          style={{ cursor: "pointer" }}
          aria-label="Close menu"
          onClick={closeDrawer}
        />
      ) : null}
    </>
  );
}

export function DashboardShell(props: DashboardShellProps) {
  const pathname = usePathname();
  return <DashboardShellInner key={pathname} {...props} />;
}

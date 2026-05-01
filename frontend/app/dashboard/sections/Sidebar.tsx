import Link from "next/link";

type SidebarProps = {
  isLg: boolean;
  mobileDrawerOpen: boolean;
  onNavLinkClick?: () => void;
};

export function Sidebar({ isLg, mobileDrawerOpen, onNavLinkClick }: SidebarProps) {
  const drawerMod = !isLg
    ? ` drawer drawer-start${mobileDrawerOpen ? " drawer-on" : ""}`
    : "";

  return (
    <div
      id="kt_aside"
      className={`aside aside-default aside-hoverable${drawerMod}`}
      data-kt-drawer="true"
      data-kt-drawer-name="aside"
      data-kt-drawer-activate="{default: true, lg: false}"
      data-kt-drawer-overlay="true"
      data-kt-drawer-width="{default:'200px', '300px': '265px'}"
      data-kt-drawer-direction="start"
      data-kt-drawer-toggle="#kt_aside_mobile_toggle"
    >
      <div className="aside-logo flex-column-auto pt-10 pb-5 ps-5 pe-5" id="kt_aside_logo">
        <Link href="/dashboard" className="d-flex align-items-center" onClick={() => onNavLinkClick?.()}>
          <img alt="Logo" src="/assets/images/logo.png" className="h-25px theme-light-show" />
        </Link>
      </div>
      <div className="aside-menu flex-column-fluid px-5">
        <div className="hover-scroll-overlay-y my-5 my-lg-5 mx-n3" id="kt_aside_menu_wrapper">
          <div
            className="menu menu-column menu-rounded menu-sub-indention menu-title-gray-600 menu-state-primary menu-state-icon-primary menu-state-bullet-primary fw-semibold fs-6"
            id="kt_aside_menu"
            data-kt-menu="true"
          >
            <div className="menu-item">
              <Link href="/dashboard" className="menu-link active py-3" onClick={() => onNavLinkClick?.()}>
                <span className="menu-icon">
                  <i className="bi bi-speedometer2 fs-2" />
                </span>
                <span className="menu-title">Dashboard</span>
              </Link>
            </div>
            <div className="menu-item">
              <Link
                href="/dashboard#dashboard-loans"
                className="menu-link py-3"
                onClick={() => onNavLinkClick?.()}
              >
                <span className="menu-icon">
                  <i className="bi bi-cash-stack fs-2" />
                </span>
                <span className="menu-title">Loans</span>
              </Link>
            </div>
          </div>
        </div>
      </div>
    </div>
  );
}

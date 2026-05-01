import type { ReactNode } from "react";

type MainContentProps = {
  children: ReactNode;
  title?: string;
};

export function MainContent({ children, title = "Dashboard" }: MainContentProps) {
  return (
    <>
      <div className="toolbar" id="kt_toolbar">
        <div id="kt_toolbar_container" className="container-fluid d-flex flex-stack">
          <div className="page-title d-flex align-items-center flex-wrap me-3 mb-5 mb-lg-0 lh-1">
            <h1 className="d-flex align-items-center text-dark fw-bolder my-1 fs-3">{title}</h1>
          </div>
        </div>
      </div>
      <div id="kt_post" className="post d-flex flex-column-fluid">
        <div id="kt_content_container" className="container-xxl">
          {children}
        </div>
      </div>
    </>
  );
}

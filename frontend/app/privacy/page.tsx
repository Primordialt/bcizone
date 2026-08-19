import type { Metadata } from "next";

import { LegacyLegalBody } from "../legacy-legal-body";
import {
  PublicSiteAssets,
  PublicSiteFooter,
  PublicSiteHeader,
  PublicSiteScripts,
} from "../public-site-chrome";

export const metadata: Metadata = {
  title: "Privacy Policy",
  description: "Learn how BCI Zone collects, uses, and protects your personal information.",
};

export default function PrivacyPage() {
  return (
    <>
      <PublicSiteAssets />
      <main className="page-wrapper">
        <PublicSiteHeader variant="light" />
        <section
          className="position-relative py-lg-5 pt-5"
          style={{ backgroundImage: "url(/assets/images/auth.svg)" }}
          data-jarallax
          data-img-position="0% 100%"
          data-speed="0.5"
        >
          <div className="container position-relative zindex-2 pt-5 pb-2 pb-md-0 py-6">
            <div className="row justify-content-center pt-3 mt-3">
              <div className="col-xl-6 col-lg-7 col-md-8 col-sm-10 text-center">
                <h1 className="mb-4">Privacy policy</h1>
              </div>
            </div>
          </div>
        </section>
        <section className="container mb-5 pt-4 pb-2 py-mg-4">
          <div className="row gy-4">
            <div className="col-lg-12">
              <LegacyLegalBody />
            </div>
          </div>
        </section>
        <PublicSiteFooter />
      </main>
      <PublicSiteScripts />
    </>
  );
}

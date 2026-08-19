import Link from "next/link";
import Script from "next/script";
import type { ReactNode } from "react";

/** Visible but not clickable: keeps header/footer layout without 404 routes. */
function InactiveNavLabel({
  children,
  className,
}: {
  children: ReactNode;
  className: string;
}) {
  return (
    <span className={className} aria-disabled="true">
      {children}
    </span>
  );
}

export function PublicSiteHeader({ variant }: { variant: "dark" | "light" }) {
  const isDark = variant === "dark";
  return (
    <header
      className={`header navbar navbar-expand-lg position-absolute navbar-sticky  ${isDark ? "navbar-dark" : "navbar-light"} `}
    >
      <div className="container px-3">
        <a href="https://bajolcapital.com/" className="navbar-brand pe-3">
          <img
            src={isDark ? "/assets/images/dark_logo2.png" : "/assets/images/logo.png"}
            width="200"
            alt="Bajol Capital"
            loading="lazy"
          />
        </a>
        <div id="navbarNav" className="offcanvas offcanvas-end">
          <div className="offcanvas-header border-bottom">
            <h5 className="offcanvas-title">Menu</h5>
            <button type="button" className="btn-close" data-bs-dismiss="offcanvas" aria-label="Close"></button>
          </div>
          <div className="offcanvas-body">
            <ul className="navbar-nav me-auto mb-2 mb-lg-0">
              <li className="nav-item">
                <InactiveNavLabel className="nav-link fw-medium fs-sm">ABOUT</InactiveNavLabel>
              </li>
              <li className="nav-item">
                <InactiveNavLabel className="nav-link fw-medium fs-sm">BLOG</InactiveNavLabel>
              </li>
              <li className="nav-item">
                <InactiveNavLabel className="nav-link fw-medium fs-sm">FAQ</InactiveNavLabel>
              </li>
              <li className="nav-item d-md-none d-sm-block">
                <Link href="/login" className="nav-link fw-medium fs-sm">
                  Sign in
                </Link>
              </li>
            </ul>
          </div>
        </div>
        <button
          type="button"
          className="navbar-toggler"
          data-bs-toggle="offcanvas"
          data-bs-target="#navbarNav"
          aria-controls="navbarNav"
          aria-expanded="false"
          aria-label="Toggle navigation"
        >
          <span className="navbar-toggler-icon"></span>
        </button>
        <Link
          href="/login"
          className={`d-none d-lg-inline-flex me-4 text-decoration-none  ${isDark ? "text-white" : "text-dark"} `}
          rel="noopener"
        >
          Log In
        </Link>
        <Link href="/register" className="btn btn-info btn-sm fs-sm rounded-pill d-none d-lg-inline-flex" rel="noopener">
          Register <i className="fal fa-angle-right mx-2"></i>
        </Link>
      </div>
    </header>
  );
}

export function PublicSiteFooter() {
  return (
    <footer className="footer dark-mode border-top border-light py-5 bg-dark">
      <div className="container pt-lg-4">
        <div className="row pb-5">
          <div className="col-xl-12 col-lg-12 col-md-12 pt-4 pt-md-1 pt-lg-0">
            <div id="footer-links" className="row">
              <div className="col-xl-3 col-lg-3 col-6">
                <h6 className="mb-2">Company</h6>
                <ul className="nav flex-column mb-2 mb-lg-0">
                  <li className="nav-item">
                    <a href="https://google.com/" target="_blank" className="footer-link d-inline-block px-0 pt-1 pb-2">
                      Careers
                    </a>
                  </li>
                  <li className="nav-item">
                    <InactiveNavLabel className="footer-link d-inline-block px-0 pt-1 pb-2">About</InactiveNavLabel>
                  </li>
                  <li className="nav-item">
                    <InactiveNavLabel className="footer-link d-inline-block px-0 pt-1 pb-2">Contact Us</InactiveNavLabel>
                  </li>
                </ul>
              </div>
              <div className="col-xl-3 col-lg-3 col-6 pt-2 pt-lg-0">
                <h6 className="mb-2">Resources</h6>
                <ul className="nav flex-column mb-2 mb-lg-0 mb-3">
                  <li className="nav-item">
                    <InactiveNavLabel className="footer-link d-inline-block px-0 pt-1 pb-2">Help Centre</InactiveNavLabel>
                  </li>
                  <li className="nav-item">
                    <InactiveNavLabel className="footer-link d-inline-block px-0 pt-1 pb-2">Blog</InactiveNavLabel>
                  </li>
                </ul>
              </div>
              <div className="col-xl-3 col-lg-3 col-6 pt-2 pt-lg-0">
                <h6 className="mb-2">Legal</h6>
                <ul className="nav flex-column mb-2 mb-lg-0">
                  <li className="nav-item">
                    <Link href="/terms" className="footer-link d-inline-block px-0 pt-1 pb-2">
                      Terms &amp; Conditions
                    </Link>
                  </li>
                  <li className="nav-item">
                    <Link href="/privacy" className="footer-link d-inline-block px-0 pt-1 pb-2">
                      Privacy Policy
                    </Link>
                  </li>
                </ul>
              </div>
              <div className="col-xl-3 col-lg-3 col-6 pt-2 pt-lg-0">
                <h6 className="mb-2">Contact</h6>
                <p className="fs-sm pb-lg-3 mb-0 text-dark">
                  <a className="footer-link" href="#">
                    <i className="fal fa-envelope"></i> info@bajolcapital.com
                  </a>
                </p>
                <p className="fs-sm mb-3 text-dark">
                  <a className="footer-link" href="tel:+2349061499756">
                    <i className="fal fa-phone-volume"></i> +23490 6149 9756
                  </a>
                </p>
                <div className="d-flex mb-5">
                  <a href="https://facebook.com/" className="mx-2 text-white">
                    <i className="fab fa-facebook"></i>
                  </a>
                  <a href="https://instagram.com/" className="mx-2 text-white">
                    <i className="fab fa-instagram"></i>
                  </a>
                  <a href="https://twitter.com/" className="mx-2 text-white">
                    <i className="fab fa-twitter"></i>
                  </a>
                </div>
              </div>
            </div>
          </div>
        </div>
        <div className="space-1">
          <div className="w-md-75 text-lg-center mx-lg-auto">
            <p className="small text-dark">© Bajol Capital. 2025. All rights reserved.</p>
          </div>
        </div>
      </div>
    </footer>
  );
}

export function PublicSiteAssets() {
  return (
    <>
      <link rel="shortcut icon" href="/assets/images/favicon.png" />
      <link rel="stylesheet" href="/css/theme.css" type="text/css" media="all" />
      <link rel="stylesheet" href="/assets/vendor/boxicons/css/boxicons.css" />
      <link rel="stylesheet" href="/assets/vendor/lightgallery/css/lightgallery-bundle.min.css" />
      <link rel="stylesheet" href="/assets/vendor/swiper/swiper-bundle.min.css" />
      <link rel="stylesheet" href="/css/cookie.css" />
      <link rel="stylesheet" href="/css/toast.css" type="text/css" />
      <link href="/assets/fonts/fontawesome/css/all.css" rel="stylesheet" type="text/css" />
      <link
        rel="stylesheet"
        href="https://cdn.jsdelivr.net/gh/lipis/flag-icons@6.6.6/css/flag-icons.min.css"
      />
    </>
  );
}

export function PublicSiteScripts() {
  return (
    <>
      <Script src="/assets/vendor/jquery/dist/jquery.min.js" strategy="afterInteractive" />
      <Script src="/assets/vendor/bootstrap/dist/js/bootstrap.bundle.min.js" strategy="afterInteractive" />
      <Script src="/assets/vendor/smooth-scroll/dist/smooth-scroll.polyfills.min.js" strategy="afterInteractive" />
      <Script src="/assets/vendor/swiper/swiper-bundle.min.js" strategy="afterInteractive" />
      <Script src="/assets/vendor/jarallax/dist/jarallax.min.js" strategy="afterInteractive" />
      <Script src="/assets/vendor/cleave/dist/cleave.min.js" strategy="afterInteractive" />
      <Script src="/assets/vendor/imagesloaded/imagesloaded.pkgd.min.js" strategy="afterInteractive" />
      <Script src="/assets/vendor/parallax-js/dist/parallax.min.js" strategy="afterInteractive" />
      <Script src="/assets/vendor/rellax/rellax.min.js" strategy="afterInteractive" />
      <Script src="/assets/vendor/shufflejs/dist/shuffle.min.js" strategy="afterInteractive" />
      <Script src="/assets/vendor/lightgallery/lightgallery.min.js" strategy="afterInteractive" />
      <Script src="/assets/vendor/lightgallery/plugins/video/lg-video.min.js" strategy="afterInteractive" />
      <Script src="/assets/vendor/lottiefiles/lottie-player/dist/lottie-player.js" strategy="afterInteractive" />
      <Script src="/js/theme.min.js" strategy="afterInteractive" />
      <Script src="https://cdnjs.cloudflare.com/ajax/libs/lottie-web/5.7.6/lottie_svg.min.js" strategy="afterInteractive" />
      <Script src="/js/cookieconsent.js" strategy="afterInteractive" />
      <Script src="/js/cookie.js" strategy="afterInteractive" />
      <Script src="/js/toast.js" strategy="afterInteractive" />
    </>
  );
}

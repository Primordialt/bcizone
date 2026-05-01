import Link from "next/link";

export default function CreateAccountPage() {
  return (
    <>
      <link rel="shortcut icon" href="/assets/images/favicon.png" />
      <link href="/assets/fonts/fontawesome/css/all.css" rel="stylesheet" type="text/css" />
      <link href="/css/plugins.bundle.css" rel="stylesheet" type="text/css" />
      <link href="/css/style.bundle.css" rel="stylesheet" type="text/css" />
      <style>{`body { font-family: "Graphik", sans-serif; }`}</style>
      <div id="kt_body" className="bg-light auth-bg">
        <div className="row justify-content-center py-15">
          <div className="col-md-6">
            <div className="text-center mb-8">
              <Link href="/" className="navbar-brand">
                <img
                  className="mb-4"
                  src="/assets/images/logo.png"
                  width="200"
                  alt="BCI"
                  loading="lazy"
                />
              </Link>
            </div>
            <div className="card rounded-5">
              <div className="card-body m-8 text-center">
                <h1 className="fs-2 text-dark mb-4">Create an account</h1>
                <p className="text-muted mb-8">
                  Online registration is not available yet. Please contact support or sign in if you already have an account.
                </p>
                <Link href="/login" className="btn btn-lg btn-info fw-bolder me-3">
                  Sign in
                </Link>
                <Link href="/" className="btn btn-lg btn-light fw-bolder">
                  Home
                </Link>
              </div>
            </div>
          </div>
        </div>
      </div>
    </>
  );
}

import type { NextConfig } from "next";

const nextConfig: NextConfig = {
  async rewrites() {
    return [
      // theme CSS uses ../../asset/... → /asset/... but static files live under /assets/
      { source: "/asset/:path*", destination: "/assets/:path*" },
      // plugins.bundle.css resolves fonts relative to /css/ → /css/fonts/...
      { source: "/css/fonts/:path*", destination: "/plugins/global/fonts/:path*" },
    ];
  },
};

export default nextConfig;

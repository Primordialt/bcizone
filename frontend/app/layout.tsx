import type { Metadata } from "next";
import { Geist, Geist_Mono } from "next/font/google";

import { NavigationCleanup } from "./navigation-cleanup";
import "./globals.css";

const geistSans = Geist({
  variable: "--font-geist-sans",
  subsets: ["latin"],
});

const geistMono = Geist_Mono({
  variable: "--font-geist-mono",
  subsets: ["latin"],
});

export const metadata: Metadata = {
  metadataBase: new URL(process.env.NEXT_PUBLIC_SITE_URL ?? "https://bcizone.com"),
  title: {
    default: "BCI Zone — Smart Loans for Every Need",
    template: "%s | BCI Zone",
  },
  description:
    "BCI Zone makes financing simple and accessible. Apply for personal loans, business loans, and asset financing with flexible terms and quick approvals.",
  keywords: [
    "loans",
    "personal loans",
    "business loans",
    "asset financing",
    "quick loans",
    "BCI Zone",
    "Bajol Capital",
  ],
  authors: [{ name: "BCI Zone" }],
  openGraph: {
    type: "website",
    siteName: "BCI Zone",
    title: "BCI Zone — Smart Loans for Every Need",
    description:
      "Apply for personal loans, business loans, and asset financing with flexible terms and quick approvals.",
    images: [{ url: "/assets/images/dark_logo2.png", alt: "BCI Zone" }],
  },
  twitter: {
    card: "summary_large_image",
    title: "BCI Zone — Smart Loans for Every Need",
    description:
      "Apply for personal loans, business loans, and asset financing with flexible terms and quick approvals.",
    images: ["/assets/images/dark_logo2.png"],
  },
  robots: {
    index: true,
    follow: true,
  },
};

export default function RootLayout({
  children,
}: Readonly<{
  children: React.ReactNode;
}>) {
  return (
    <html
      lang="en"
      className={`${geistSans.variable} ${geistMono.variable} h-full antialiased`}
    >
      <body className="min-h-full flex flex-col">
        <NavigationCleanup />
        {children}
      </body>
    </html>
  );
}

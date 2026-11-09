import type { Metadata, Viewport } from "next";
import "./globals.css";

export const metadata: Metadata = {
  title: "PROJECT NOVA - Universal Autonomous AI Assistant & Operator",
  description:
    "Neural Operating & Virtual Assistant: A real-world JARVIS-inspired AI operator with continuous voice reasoning, dynamic desktop application control, and verified multi-step automation.",
  applicationName: "PROJECT NOVA",
  keywords: [
    "NOVA",
    "JARVIS",
    "AI Assistant",
    "Autonomous Agent",
    "Voice AI",
    "Desktop Automation",
    "Ollama",
    "FastAPI",
    "Next.js",
  ],
  authors: [{ name: "Project NOVA Team" }],
  creator: "Project NOVA",
  publisher: "Project NOVA",
  metadataBase: new URL(
    process.env.NEXT_PUBLIC_SITE_URL || "http://localhost:3000"
  ),
  alternates: {
    canonical: "/",
  },
  openGraph: {
    type: "website",
    locale: "en_US",
    url: "/",
    siteName: "PROJECT NOVA",
    title: "PROJECT NOVA — Real-World JARVIS AI Assistant & OS Operator",
    description:
      "Listen continuously, understand natural English, Hindi & Marathi, control real desktop applications, and autonomously execute multi-step workflows.",
    images: [
      {
        url: "/og-image.svg",
        width: 1200,
        height: 630,
        alt: "PROJECT NOVA - Neural Operating & Virtual Assistant",
        type: "image/svg+xml",
      },
    ],
  },
  twitter: {
    card: "summary_large_image",
    title: "PROJECT NOVA — Real-World JARVIS AI Assistant & OS Operator",
    description:
      "Listen continuously, understand natural English, Hindi & Marathi, control real desktop applications, and autonomously execute multi-step workflows.",
    images: ["/og-image.svg"],
    creator: "@ProjectNovaAI",
  },
  robots: {
    index: true,
    follow: true,
  },
  icons: {
    icon: "/og-image.svg",
    apple: "/og-image.svg",
  },
};

export const viewport: Viewport = {
  width: "device-width",
  initialScale: 1,
  maximumScale: 1,
  userScalable: false,
  viewportFit: "cover",
  themeColor: "#050811",
};

export default function RootLayout({
  children,
}: Readonly<{
  children: React.ReactNode;
}>) {
  return (
    <html lang="en">
      <body className="bg-nova-dark text-slate-100 min-h-screen antialiased selection:bg-cyan-500/30 selection:text-cyan-200">
        {children}
      </body>
    </html>
  );
}

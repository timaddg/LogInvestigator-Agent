import type { Metadata } from "next";
import "./globals.css";

export const metadata: Metadata = {
  title: "Log Investigator - AI-Powered Log Analysis",
  description: "AI-powered log analysis tool for cybersecurity and system administration. Upload log files or download from online sources for instant insights.",
};

export default function RootLayout({
  children,
}: Readonly<{
  children: React.ReactNode;
}>) {
  return (
    <html lang="en">
      <body className="antialiased">
        {children}
      </body>
    </html>
  );
}

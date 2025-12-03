import "./globals.css";
import type { ReactNode } from "react";

export const metadata = {
  title: "AI Multi-Agent Debate",
  description: "Review-driven multi-agent AI debate system with prompt advisor"
};

export default function RootLayout({ children }: { children: ReactNode }) {
  return (
    <html lang="en">
      <body>{children}</body>
    </html>
  );
}

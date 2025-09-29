// frontend/src/app/layout.tsx
"use client";

import "./globals.css";
import { ReactNode } from "react";
import Providers from "./providers";


const metadata = {
  title: "Dashboard Project",
  description: "Data visualization dashboard with Next.js + FastAPI",
}

export default function RootLayout({ children }: {children: ReactNode}) {
  return (
    <html lang="en">
      <body className="bg-gray-50 text-gray-900 min-h-screen">
        <div className="max-w-5xl mx-auto p-4">
          <header className="mb-6">
            <h1 className="text-3xl font-bold">My Dashboard</h1>
          </header>
          <Providers>{children}</Providers>
        </div>
      </body>
    </html>
  );
}

import type { Metadata } from "next";
import "./globals.css";
import './styles.css';

export const metadata: Metadata = {
  title: "Bias Lens",
  description: 'A modern news aggregator with sentiment analysis.',
};

export default function RootLayout({
  children,
}: Readonly<{
  children: React.ReactNode;
}>) {
  return (
    <html lang="en">
      <body>{children}</body>
    </html>
  );
}

import './globals.css'
import type { Metadata } from 'next'
import { Inter } from 'next/font/google'

const inter = Inter({ subsets: ['latin'] })

export const metadata: Metadata = {
  title: 'BiasLens - Uncovering Media Bias Through Data Analysis',
  description: 'Discover how different news sources cover the same topics. BiasLens analyzes political bias and sentiment across multiple media outlets to give you the full picture.',
  keywords: 'media bias, news analysis, political bias, sentiment analysis, news aggregator, media literacy',
  openGraph: {
    title: 'BiasLens - Uncovering Media Bias Through Data Analysis',
    description: 'Analyze political bias and sentiment across multiple news sources to get the full picture.',
    url: 'https://biaslens.com',
    siteName: 'BiasLens',
    images: [
      {
        url: '/BiasLens.jpg',
        width: 1200,
        height: 630,
        alt: 'BiasLens - Media Bias Analysis Tool',
      },
    ],
    locale: 'en_US',
    type: 'website',
  },
  twitter: {
    card: 'summary_large_image',
    title: 'BiasLens - Analyze Media Bias & Sentiment',
    description: 'See how different news sources cover the same topics with our bias and sentiment analysis tools.',
    images: ['/BiasLens.jpg'],
  },
  robots: {
    index: true,
    follow: true,
    googleBot: {
      index: true,
      follow: true,
      'max-video-preview': -1,
      'max-image-preview': 'large',
      'max-snippet': -1,
    },
  },
  verification: {
    google: 'verification_token',
  },
  alternates: {
    canonical: 'https://biaslens.com',
  },
}

export default function RootLayout({
  children,
}: {
  children: React.ReactNode
}) {
  return (
    <html lang="en">
      <body className={inter.className}>{children}</body>
    </html>
  )
}

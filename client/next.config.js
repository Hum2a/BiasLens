/** @type {import('next').NextConfig} */
const nextConfig = {
  reactStrictMode: true,
  poweredByHeader: false, // Removes the X-Powered-By header for security
  images: {
    domains: ['biaslens.com'],
    formats: ['image/avif', 'image/webp'],
  },
  compress: true, // Enable gzip compression
  // Add redirects for common URL patterns
  async redirects() {
    return [
      {
        source: '/home',
        destination: '/',
        permanent: true,
      },
      {
        source: '/news',
        destination: '/',
        permanent: true,
      },
    ]
  },
  // Add rewrites if needed
  async rewrites() {
    return []
  },
  // Add headers for security and SEO
  async headers() {
    return [
      {
        source: '/:path*',
        headers: [
          {
            key: 'X-Content-Type-Options',
            value: 'nosniff',
          },
          {
            key: 'X-Frame-Options',
            value: 'DENY',
          },
          {
            key: 'X-XSS-Protection',
            value: '1; mode=block',
          },
          {
            key: 'Referrer-Policy',
            value: 'strict-origin-when-cross-origin',
          },
          {
            key: 'Permissions-Policy',
            value: 'camera=(), microphone=(), geolocation=()',
          },
        ],
      },
    ]
  },
}

module.exports = nextConfig 
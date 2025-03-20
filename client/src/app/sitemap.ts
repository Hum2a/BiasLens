import { MetadataRoute } from 'next'

export default function sitemap(): MetadataRoute.Sitemap {
  const baseUrl = 'https://biaslens.com'
  
  // Define your main routes
  const routes = [
    '',                   // Home page
    '/about',             // About page (if you have one)
    '/methodology',       // Methodology page (if you have one)
    '/privacy',           // Privacy page (if you have one)
  ].map(route => ({
    url: `${baseUrl}${route}`,
    lastModified: new Date(),
    changeFrequency: 'daily' as const,
    priority: route === '' ? 1 : 0.8,
  }))

  return routes
} 
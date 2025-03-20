import fs from 'fs';
import path from 'path';
import { fileURLToPath } from 'url';

// Get the directory name in ESM
const __filename = fileURLToPath(import.meta.url);
const __dirname = path.dirname(__filename);

// Function to generate sitemap XML
async function generateSitemap() {
  const baseUrl = 'https://biaslens.com';
  
  // Define static routes
  const staticRoutes = [
    '',
    '/about',
    '/methodology',
    '/privacy',
  ];

  // In a real implementation, you would fetch articles from your database
  // For example:
  // import { initializeApp } from 'firebase/app';
  // import { getFirestore, collection, getDocs } from 'firebase/firestore';
  // Initialize Firebase and fetch articles
  // const articles = await fetchArticlesFromFirebase();
  
  // For now, we'll just create a placeholder
  const articleRoutes = [];
  
  // Combine all routes
  const allRoutes = [
    ...staticRoutes.map(route => ({
      url: `${baseUrl}${route}`,
      lastModified: new Date().toISOString(),
      changeFrequency: route === '' ? 'daily' : 'weekly',
      priority: route === '' ? 1.0 : 0.8
    })),
    ...articleRoutes.map(article => ({
      url: `${baseUrl}/article/${article.id}`,
      lastModified: article.lastModified || new Date().toISOString(),
      changeFrequency: 'weekly',
      priority: 0.7
    }))
  ];

  // Generate XML
  const sitemap = `<?xml version="1.0" encoding="UTF-8"?>
<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">
${allRoutes.map(route => `  <url>
    <loc>${route.url}</loc>
    <lastmod>${route.lastModified}</lastmod>
    <changefreq>${route.changeFrequency}</changefreq>
    <priority>${route.priority}</priority>
  </url>`).join('\n')}
</urlset>`;

  // Write to file
  const outputPath = path.join(__dirname, '../public/sitemap.xml');
  fs.writeFileSync(outputPath, sitemap);
  console.log(`Sitemap generated at ${outputPath}`);
}

// Run the generator
generateSitemap().catch(console.error); 
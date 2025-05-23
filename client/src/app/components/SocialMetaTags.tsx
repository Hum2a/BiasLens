import React from 'react';
import Head from 'next/head';

interface SocialMetaTagsProps {
  title: string;
  description: string;
  url: string;
  image: string;
}

export default function SocialMetaTags({ 
  title, 
  description, 
  url, 
  image 
}: SocialMetaTagsProps) {
  return (
    <Head>
      {/* Open Graph / Facebook */}
      <meta property="og:type" content="website" />
      <meta property="og:url" content={url} />
      <meta property="og:title" content={title} />
      <meta property="og:description" content={description} />
      <meta property="og:image" content={image} />

      {/* Twitter */}
      <meta property="twitter:card" content="summary_large_image" />
      <meta property="twitter:url" content={url} />
      <meta property="twitter:title" content={title} />
      <meta property="twitter:description" content={description} />
      <meta property="twitter:image" content={image} />
      
      {/* Canonical URL */}
      <link rel="canonical" href={url} />
    </Head>
  );
} 
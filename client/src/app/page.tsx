'use client'

import './styles.css';
import { useState, useEffect } from 'react';
import { getDocs, collection } from 'firebase/firestore';
import db from './lib/firebase';
import Image from 'next/image';
import { motion } from 'framer-motion';

interface Article {
  id: string;
  title: string;
  description: string;
  source: string;
  sentiment: string;
  sentiment_score: number;
  political_bias: string;
  url: string;
}

export default function Home() {
  const [articles, setArticles] = useState<Article[]>([]);
  const [expandedSources, setExpandedSources] = useState<Record<string, boolean>>({});
  const [searchTerm, setSearchTerm] = useState('');
  const [selectedBias, setSelectedBias] = useState('all');

  const fetchArticles = async (): Promise<Article[]> => {
    const querySnapshot = await getDocs(collection(db, 'Articles'));
    console.log("Query Snapshot:", querySnapshot.docs.map((doc) => doc.data())); // Log fetched data
    return querySnapshot.docs.map((doc) => ({ id: doc.id, ...doc.data() })) as Article[];
  };
  

  useEffect(() => {
    const loadArticles = async () => {
      try {
        const data = await fetchArticles();
        if (data.length === 0) {
          console.warn("No articles found in the database.");
        }
        setArticles(data);
      } catch (error) {
        console.error("Error fetching articles:", error);
        setArticles([]);
      }
    };
  
    loadArticles();
  }, []);
  

  const groupedArticles = articles.reduce((acc: Record<string, Article[]>, article: Article) => {
    const source = article.source || "Unknown Source";
    if (!acc[source]) {
      acc[source] = [];
    }
    acc[source].push(article);
    return acc;
  }, {});

  const toggleSource = (source: string) => {
    setExpandedSources((prev) => ({
      ...prev,
      [source]: !prev[source],
    }));
  };
   
  const getCardClass = (bias: "Left" | "Right" | "Center" | string) => {
    switch (bias) {
      case "Left":
        return "card left";
      case "Right":
        return "card right";
      case "Center":
        return "card center";
      default:
        return "card";
    }
  };

  const filteredArticles = articles.filter(article => {
    const matchesSearch = article.title.toLowerCase().includes(searchTerm.toLowerCase()) ||
                         article.description.toLowerCase().includes(searchTerm.toLowerCase());
    const matchesBias = selectedBias === 'all' || article.political_bias.toLowerCase() === selectedBias;
    return matchesSearch && matchesBias;
  });

  return (
    <motion.div
      initial={{ opacity: 0 }}
      animate={{ opacity: 1 }}
      transition={{ duration: 0.6 }}
    >
      <header className="header">
        <div className="container headerContent">
          <motion.div 
            className="headerTitle"
            initial={{ x: -20, opacity: 0 }}
            animate={{ x: 0, opacity: 1 }}
            transition={{ duration: 0.6, ease: "easeOut" }}
          >
            <Image 
              src="/BiasLens.jpg" 
              alt="BiasLens Logo" 
              width={40} 
              height={40}
              className="logo"
            />
            BiasLens
          </motion.div>
          
          <motion.div 
            className="searchBar"
            initial={{ y: -20, opacity: 0 }}
            animate={{ y: 0, opacity: 1 }}
            transition={{ delay: 0.2, duration: 0.6 }}
          >
            <input
              type="text"
              placeholder="Search for articles..."
              value={searchTerm}
              onChange={(e) => setSearchTerm(e.target.value)}
            />
            <select
              value={selectedBias}
              onChange={(e) => setSelectedBias(e.target.value)}
            >
              <option value="all">All Perspectives</option>
              <option value="left">Left-leaning</option>
              <option value="center">Centrist</option>
              <option value="right">Right-leaning</option>
            </select>
          </motion.div>
        </div>
      </header>

      <main className="container">
        <motion.h1 
          className="title"
          initial={{ y: 20, opacity: 0 }}
          animate={{ y: 0, opacity: 1 }}
          transition={{ delay: 0.4, duration: 0.6 }}
        >
          Discover Different Perspectives
        </motion.h1>

        {filteredArticles.length === 0 ? (
          <motion.div 
            className="noArticles"
            initial={{ opacity: 0 }}
            animate={{ opacity: 1 }}
            transition={{ delay: 0.6 }}
          >
            <h2>No articles found</h2>
            <p>Try adjusting your search criteria</p>
          </motion.div>
        ) : (
          <motion.div 
            className="grid"
            initial="hidden"
            animate="visible"
            variants={{
              visible: {
                transition: {
                  staggerChildren: 0.1
                }
              }
            }}
          >
            {filteredArticles.map((article, index) => (
              <motion.div
                key={article.id}
                className="card"
                variants={{
                  hidden: { y: 20, opacity: 0 },
                  visible: { y: 0, opacity: 1 }
                }}
                transition={{ duration: 0.6 }}
                whileHover={{ y: -8, transition: { duration: 0.2 } }}
              >
                <h2 className="cardTitle">{article.title}</h2>
                <p className="cardDescription">{article.description}</p>
                
                <div className="cardStats">
                  <div className="statRow">
                    <span className="statLabel">Sentiment</span>
                    <div className="sentimentBar">
                      <motion.div 
                        className="sentimentFill"
                        initial={{ scaleX: 0 }}
                        animate={{ scaleX: (article.sentiment_score + 1) / 2 }}
                        transition={{ delay: 0.2, duration: 0.8, ease: "easeOut" }}
                      />
                    </div>
                    <span>{article.sentiment}</span>
                  </div>
                  
                  <div className="statRow">
                    <span className="statLabel">Bias</span>
                    <motion.span 
                      className={`bias-tag ${article.political_bias.toLowerCase()}`}
                      whileHover={{ scale: 1.05 }}
                      whileTap={{ scale: 0.95 }}
                    >
                      {article.political_bias}
                    </motion.span>
                  </div>
                </div>

                <motion.a
                  href={article.url}
                  className="cardLink"
                  target="_blank"
                  rel="noopener noreferrer"
                  whileHover={{ scale: 1.02 }}
                  whileTap={{ scale: 0.98 }}
                >
                  Read Article
                  <svg width="16" height="16" viewBox="0 0 16 16" fill="none">
                    <path d="M4 12L12 4M12 4H6M12 4V10" stroke="currentColor" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round"/>
                  </svg>
                </motion.a>
              </motion.div>
            ))}
          </motion.div>
        )}
      </main>

      <footer className="footer">
        <div className="container footer-content">
          <div>
            <h3>BiasLens</h3>
            <p>Uncovering media bias through data analysis</p>
          </div>
          <div className="footer-links">
            <a href="#about">About</a>
            <a href="#methodology">Methodology</a>
            <a href="#privacy">Privacy</a>
          </div>
        </div>
      </footer>
    </motion.div>
  );
}

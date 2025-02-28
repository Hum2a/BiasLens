'use client'

import './styles.css';
import { useState, useEffect } from 'react';
import { getDocs, collection } from 'firebase/firestore';
import db from './lib/firebase';
import Image from 'next/image';

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
  const [viewMode, setViewMode] = useState<'grouped' | 'list'>('list');

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
    switch (bias.toLowerCase()) {
      case "left":
        return "card left";
      case "right":
        return "card right";
      case "center":
        return "card center";
      default:
        return "card";
    }
  };

  const filteredArticles = articles.filter(article => {
    const matchesSearch = (
      (article.title?.toLowerCase() || '').includes(searchTerm.toLowerCase()) ||
      (article.description?.toLowerCase() || '').includes(searchTerm.toLowerCase())
    );
    const matchesBias = selectedBias === 'all' || 
      (article.political_bias?.toLowerCase() || '') === selectedBias;
    return matchesSearch && matchesBias;
  });

  return (
    <div>
      <header className="header">
        <div className="container headerContent">
          <div className="headerTitle">
            <Image 
              src="/BiasLens.jpg" 
              alt="BiasLens Logo" 
              width={40} 
              height={40}
              className="logo"
            />
            BiasLens
          </div>
          
          <div className="searchBar">
            <input
              type="text"
              placeholder="Search for articles..."
              value={searchTerm}
              onChange={(e) => setSearchTerm(e.target.value)}
            />
            <select
              value={selectedBias}
              onChange={(e) => setSelectedBias(e.target.value)}
              aria-label="Filter by political bias"
            >
              <option value="all">All Perspectives</option>
              <option value="left">Left-leaning</option>
              <option value="center">Centrist</option>
              <option value="right">Right-leaning</option>
            </select>
            <div className="viewToggle">
              <button 
                className={viewMode === 'list' ? 'active' : ''} 
                onClick={() => setViewMode('list')}
              >
                List View
              </button>
              <button 
                className={viewMode === 'grouped' ? 'active' : ''} 
                onClick={() => setViewMode('grouped')}
              >
                Grouped View
              </button>
            </div>
          </div>
        </div>
      </header>

      <main className="container">
        <h1 className="title">
          Discover Different Perspectives
        </h1>

        {filteredArticles.length === 0 ? (
          <div className="noArticles">
            <h2>No articles found</h2>
            <p>Try adjusting your search criteria</p>
          </div>
        ) : viewMode === 'grouped' ? (
          // Grouped view - articles grouped by source
          <div className="groupedView">
            {Object.entries(groupedArticles).map(([source, sourceArticles]) => {
              // Filter source articles based on search and bias
              const filteredSourceArticles = sourceArticles.filter(article => {
                const matchesSearch = (
                  (article.title?.toLowerCase() || '').includes(searchTerm.toLowerCase()) ||
                  (article.description?.toLowerCase() || '').includes(searchTerm.toLowerCase())
                );
                const matchesBias = selectedBias === 'all' || 
                  (article.political_bias?.toLowerCase() || '') === selectedBias;
                return matchesSearch && matchesBias;
              });
              
              // Skip sources with no matching articles
              if (filteredSourceArticles.length === 0) return null;
              
              return (
                <div key={source} className="sourceGroup">
                  <div 
                    className="sourceHeader" 
                    onClick={() => toggleSource(source)}
                  >
                    <h2>{source}</h2>
                    <span>{expandedSources[source] ? '▼' : '►'}</span>
                  </div>
                  
                  {expandedSources[source] && (
                    <div className="sourceArticles">
                      {filteredSourceArticles.map((article) => (
                        <div
                          key={article.id}
                          className={getCardClass(article.political_bias || '')}
                        >
                          <h2 className="cardTitle">{article.title || 'Untitled'}</h2>
                          <p className="cardDescription">{article.description || 'No description available'}</p>
                          
                          <div className="cardStats">
                            <div className="statRow">
                              <span className="statLabel">Sentiment</span>
                              <div className="sentimentBar">
                                <div 
                                  className="sentimentFill"
                                  style={{ transform: `scaleX(${(article.sentiment_score + 1) / 2})` }}
                                />
                              </div>
                              <span>{article.sentiment}</span>
                            </div>
                            
                            <div className="statRow">
                              <span className="statLabel">Bias</span>
                              <span className={`bias-tag ${(article.political_bias?.toLowerCase() || 'unknown')}`}>
                                {article.political_bias || 'Unknown'}
                              </span>
                            </div>
                          </div>

                          <a
                            href={article.url}
                            className="cardLink"
                            target="_blank"
                            rel="noopener noreferrer"
                          >
                            Read Article
                            <svg width="16" height="16" viewBox="0 0 16 16" fill="none">
                              <path d="M4 12L12 4M12 4H6M12 4V10" stroke="currentColor" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round"/>
                            </svg>
                          </a>
                        </div>
                      ))}
                    </div>
                  )}
                </div>
              );
            })}
          </div>
        ) : (
          // List view (original grid)
          <div className="grid">
            {filteredArticles.map((article) => (
              <div
                key={article.id}
                className={getCardClass(article.political_bias || '')}
              >
                <h2 className="cardTitle">{article.title || 'Untitled'}</h2>
                <p className="cardDescription">{article.description || 'No description available'}</p>
                
                <div className="cardStats">
                  <div className="statRow">
                    <span className="statLabel">Sentiment</span>
                    <div className="sentimentBar">
                      <div 
                        className="sentimentFill"
                        style={{ transform: `scaleX(${(article.sentiment_score + 1) / 2})` }}
                      />
                    </div>
                    <span>{article.sentiment}</span>
                  </div>
                  
                  <div className="statRow">
                    <span className="statLabel">Bias</span>
                    <span className={`bias-tag ${(article.political_bias?.toLowerCase() || 'unknown')}`}>
                      {article.political_bias || 'Unknown'}
                    </span>
                  </div>
                </div>

                <a
                  href={article.url}
                  className="cardLink"
                  target="_blank"
                  rel="noopener noreferrer"
                >
                  Read Article
                  <svg width="16" height="16" viewBox="0 0 16 16" fill="none">
                    <path d="M4 12L12 4M12 4H6M12 4V10" stroke="currentColor" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round"/>
                  </svg>
                </a>
              </div>
            ))}
          </div>
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
    </div>
  );
}

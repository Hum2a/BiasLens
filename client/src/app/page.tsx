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

  return (
    <>
      <header className="header">
        <div className="container">
          <h1 className="headerTitle">
            <Image src="/BiasLens.jpg" alt="BiasLens Logo" className="logo" width={200} height={200} />
          </h1>
          <nav className="nav">
            <ul>
              <li><a href="#home">Home</a></li>
              <li><a href="#about">About</a></li>
              <li><a href="#contact">Contact</a></li>
            </ul>
          </nav>
        </div>
      </header>

      <main className="container">
        <h1 className="title">BiasLens News</h1>
        {articles.length === 0 ? (
          <p className="noArticles">No articles found. Please check your API or Firestore setup.</p>
        ) : (
          Object.keys(groupedArticles).map((source) => (
            <section key={source} className="sourceGroup">
              <h2
                className="sourceTitle"
                onClick={() => toggleSource(source)}
                style={{ cursor: 'pointer' }}
              >
                {source} {expandedSources[source] ? '▼' : '▶'}
              </h2>
              {expandedSources[source] && (
                <div className="grid">
                  {groupedArticles[source].map((article) => (
                    <div key={article.id} className={getCardClass(article.political_bias)}>
                      <h2 className="cardTitle">{article.title}</h2>
                      <p className="cardDescription">{article.description}</p>
                      <p className="cardSource">
                        <strong>Source:</strong> {article.source}
                      </p>
                      <p className="cardSentiment">
                        <strong>Sentiment:</strong> {article.sentiment} (Score: {article.sentiment_score})
                      </p>
                      <p className="cardBias">
                        <strong>Political Bias:</strong> {article.political_bias}
                      </p>
                      <a href={article.url} className="cardLink" target="_blank" rel="noopener noreferrer">
                        Read More
                      </a>
                    </div>
                  ))}
                </div>
              )}
            </section>
          ))
        )}
      </main>

      <footer className="footer">
        <div className="container">
          <p>© 2024 BiasLens. All rights reserved.</p>
          <p>
            <a href="#privacy">Privacy Policy</a> | <a href="#terms">Terms of Service</a>
          </p>
        </div>
      </footer>
    </>
  );
}

import db from "../../lib/firebase";
import { doc, getDoc } from "firebase/firestore";

export default async function ArticlePage({ params }) {
  const { id } = params;
  const docRef = doc(db, "Articles", id);
  const docSnap = await getDoc(docRef);

  if (!docSnap.exists()) {
    return <p>Article not found.</p>;
  }

  const article = docSnap.data();

  return (
    <div className="container mx-auto p-4">
      <h1 className="text-2xl font-bold">{article.title}</h1>
      <p>{article.description}</p>
      <p>Source: <strong>{article.source}</strong></p>
      <p>Sentiment: <span className="italic">{article.sentiment}</span> (Score: {article.sentiment_score})</p>
      <p>Political Bias: <strong>{article.political_bias}</strong></p>
      <a href={article.url} className="text-blue-500 underline" target="_blank" rel="noopener noreferrer">
        Read More
      </a>
    </div>
  );
}

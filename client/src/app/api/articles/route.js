import db from "../../lib/firebase";
import { collection, getDocs } from "firebase/firestore";
import { NextResponse } from "next/server";

export async function GET() {
  try {
    const querySnapshot = await getDocs(collection(db, "Articles"));
    const articles = [];
    querySnapshot.forEach((doc) => {
      articles.push({ id: doc.id, ...doc.data() });
    });
    console.log("Fetching articles from Firestore...");
    console.log("Articles fetched:", articles);
    return NextResponse.json(articles, { status: 200 });
  } catch (error) {
    console.error("Error in API route:", error);
    return NextResponse.json([], { status: 500 }); // Return an empty array on error
  }
}

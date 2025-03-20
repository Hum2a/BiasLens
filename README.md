# BiasLens

<div align="center">
  <img src="/client/public/BiasLens.jpg" alt="BiasLens Logo" width="200" />
  <h3>Uncovering media bias through data analysis</h3>
</div>

## Overview

BiasLens is a modern web application that helps users understand the political bias and sentiment of news articles across multiple sources. By aggregating content from various news outlets and applying natural language processing techniques, BiasLens provides users with insights into how different media sources cover the same topics from different perspectives.

## Features

- **Multi-source News Aggregation**: Collects articles from numerous news sources including NYT, The Guardian, CNN, Fox News, and more
- **Political Bias Analysis**: Automatically classifies articles as Left-leaning, Right-leaning, or Centrist
- **Sentiment Analysis**: Evaluates the emotional tone of each article (Positive, Negative, or Neutral)
- **Interactive UI**: Modern, animated interface with multiple viewing options
- **Search and Filter**: Find articles by keyword and filter by political orientation
- **Responsive Design**: Optimized for all devices from mobile to desktop

## Technology Stack

### Frontend
- **Framework**: Next.js with React
- **State Management**: React Hooks
- **Database Integration**: Firebase Firestore
- **Styling**: Custom CSS with animations
- **Deployment**: Vercel

### Backend
- **Language**: Python
- **Data Processing**: NLTK, spaCy for NLP
- **Article Sources**: Multiple API integrations (NewsAPI, NYT, The Guardian, MediaStack, GDELT, etc.)
- **Database**: Firebase Firestore
- **Sentiment Analysis**: VADER (Valence Aware Dictionary and sEntiment Reasoner)

## Project Structure

```
BiasLens/
│
├── client/                  # Frontend Next.js application
│   ├── public/              # Static assets
│   └── src/
│       ├── app/             # Next.js app directory
│       │   ├── lib/         # Firebase configuration
│       │   ├── page.tsx     # Main application page
│       │   └── styles.css   # Custom styling
│
├── server/                  # Python backend
│   ├── api_scripts/         # API integrations for news sources
│   ├── article_analyser.py  # NLP for sentiment and bias analysis
│   ├── firebase/            # Firebase integration
│   ├── data/                # JSON data storage
│   └── main.py              # Main backend script
│
└── README.md                # Documentation
```

## Setup and Installation

### Prerequisites
- Node.js (v14+)
- Python (v3.7+)
- Firebase account

### Frontend Setup
1. Navigate to the client directory:
   ```bash
   cd client
   ```

2. Install dependencies:
   ```bash
   npm install
   ```

3. Create a `.env.local` file with your Firebase configuration:
   ```
   NEXT_PUBLIC_FIREBASE_API_KEY=your_api_key
   NEXT_PUBLIC_FIREBASE_AUTH_DOMAIN=your_auth_domain
   NEXT_PUBLIC_FIREBASE_PROJECT_ID=your_project_id
   NEXT_PUBLIC_FIREBASE_STORAGE_BUCKET=your_storage_bucket
   NEXT_PUBLIC_FIREBASE_MESSAGING_SENDER_ID=your_messaging_sender_id
   NEXT_PUBLIC_FIREBASE_APP_ID=your_app_id
   ```

4. Start the development server:
   ```bash
   npm run dev
   ```

### Backend Setup
1. Navigate to the server directory:
   ```bash
   cd server
   ```

2. Install Python dependencies:
   ```bash
   pip install -r requirements.txt
   ```

3. Create a `.env` file with your API keys:
   ```
   NEWSAPI_KEY=your_news_api_key
   NYT_KEY=your_nyt_api_key
   GUARDIAN_KEY=your_guardian_api_key
   MEDIASTACK_KEY=your_mediastack_key
   CURRENTS_KEY=your_currents_api_key
   FIREBASE_SERVICE_ACCOUNT_KEY_PATH=path_to_your_firebase_service_account_key.json
   ```

4. Download required NLP models:
   ```bash
   python -m spacy download en_core_web_sm
   python -m nltk.downloader vader_lexicon punkt
   ```

5. Run the data collection and analysis script:
   ```bash
   python main.py
   ```

## Usage

1. **View Articles**: Browse the aggregated news articles on the home page
2. **Search**: Use the search bar to find articles by keyword
3. **Filter**: Select political orientation from the dropdown to filter articles
4. **View Modes**: 
   - List View: Traditional grid layout of all articles
   - Grouped View: Articles organized by news source

## Political Bias Analysis

BiasLens determines political bias through:

1. Source-based analysis (known political leanings of publications)
2. Content analysis (keyword detection for politically charged terms)
3. Contextual understanding (analyzing rhetoric and framing)

The system classifies content as:
- **Left**: Progressive/liberal perspective
- **Center**: Balanced/neutral perspective
- **Right**: Conservative perspective

## Sentiment Analysis

Article sentiment is rated on a scale from -1 (extremely negative) to +1 (extremely positive) and categorized as:
- **Positive**: Upbeat, optimistic, or favorable coverage
- **Negative**: Critical, pessimistic, or unfavorable coverage  
- **Neutral**: Balanced or factual reporting without strong emotion

## Development

### Building for Production

#### Frontend
```bash
cd client
npm run build
```

#### Deployment
The front-end can be deployed on Vercel, Netlify, or any other Next.js compatible hosting service.

The back-end is designed to run as a scheduled task to periodically update the article database.

## Contribution

Contributions are welcome! Please feel free to submit a Pull Request.

## License

This project is licensed under the MIT License - see the LICENSE file for details.

## Acknowledgments

- News data provided by various public APIs
- Sentiment analysis powered by NLTK's VADER
- Political bias detection using custom NLP techniques 
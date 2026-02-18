# Sakenny API - سكنّي

AI-powered real estate platform for the Egyptian market. Search properties using natural language in Arabic or English — the AI understands meaning, not just keywords.

## What It Does

- **Smart Property Search** — Type "affordable place for a student near university" and get relevant results, even if no listing uses those exact words
- **Similar Properties** — Find alternatives to any property you like
- **Full Property Management** — Create, read, update, delete listings
- **Experiment Tracking** — MLflow tracks AI model performance and search quality

## Tech Stack

- **Backend:** Python, FastAPI
- **Database:** PostgreSQL with pgvector (vector similarity search)
- **AI:** Sentence-Transformers (all-MiniLM-L6-v2) for semantic embeddings
- **Tracking:** MLflow for experiment monitoring
- **Dashboard:** Streamlit for property visualization
- **Infrastructure:** Docker, Docker Compose

## Architecture
```
┌──────────────┐     ┌──────────────────┐     ┌─────────┐
│   FastAPI    │────▶│  PostgreSQL +    │     │ MLflow  │
│   Backend    │     │  pgvector        │     │ Server  │
└──────────────┘     └──────────────────┘     └─────────┘
       │
       ▼
┌──────────────┐
│  Streamlit   │
│  Dashboard   │
└──────────────┘
```

## Quick Start

### Prerequisites
- Docker and Docker Compose installed

### Run
```bash
git clone https://github.com/fakhreldin001/sakenny-api.git
cd sakenny-api
docker-compose up --build -d
```

### Access

| Service    | URL                        |
|------------|----------------------------|
| API Docs   | http://localhost:8000/docs  |
| Dashboard  | http://localhost:8501       |
| MLflow     | http://localhost:5000       |

## API Endpoints

### Properties
- `POST /properties/` — Create a property (auto-generates AI embedding)
- `GET /properties/` — List all properties (with optional filters)
- `GET /properties/{id}` — Get a specific property
- `PUT /properties/{id}` — Update a property
- `DELETE /properties/{id}` — Delete a property

### AI-Powered Search
- `GET /properties/search/semantic?query=your search` — Search by meaning
- `GET /properties/{id}/similar` — Find similar properties

### Filters
- `location` — Filter by location name
- `min_price` / `max_price` — Filter by price range
- `bedrooms` — Filter by number of bedrooms
- `property_type` — Filter by type (apartment, villa, studio)

## How Semantic Search Works

1. When a property is created, its details are converted into a 384-dimension vector using a sentence-transformer model
2. This vector captures the semantic meaning of the property
3. When you search, your query is also converted to a vector
4. PostgreSQL (pgvector) finds properties with the most similar vectors
5. Results are ranked by similarity score

## Project Structure
```
sakenny-api/
├── src/
│   ├── main.py                    # FastAPI app entry point
│   ├── ai/
│   │   ├── embeddings.py          # AI embedding generation
│   │   └── tracking.py            # MLflow experiment tracking
│   ├── api/
│   │   ├── schemas.py             # Request/response models
│   │   └── routes/
│   │       └── properties.py      # All API endpoints
│   ├── core/
│   │   └── config.py              # App configuration
│   └── db/
│       ├── database.py            # Database connection
│       └── models/
│           └── property.py        # Property database model
├── dashboard/
│   └── app.py                     # Streamlit dashboard
├── docker-compose.yml             # Container orchestration
├── Dockerfile                     # API container
├── Dockerfile.dashboard           # Dashboard container
└── requirements.txt               # Python dependencies
```

## Author

**Fakhr** — [GitHub](https://github.com/fakhreldin001)
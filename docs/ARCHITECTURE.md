# Feedback System Architecture

## System Overview

```
┌─────────────────────────────────────────────────────────────────┐
│                         USER BROWSER                             │
│                                                                  │
│  ┌────────────────┐              ┌─────────────────┐           │
│  │  index.html    │              │ admin_dashboard │           │
│  │                │              │     .html       │           │
│  │  - Main page   │              │                 │           │
│  │  - Download    │              │  - View stats   │           │
│  │  - Feedback    │              │  - Charts       │           │
│  │    modal       │              │  - Export CSV   │           │
│  └───────┬────────┘              └────────┬────────┘           │
│          │                                 │                     │
└──────────┼─────────────────────────────────┼─────────────────────┘
           │                                 │
           │ HTTP POST/GET                   │ HTTP GET
           │ JSON                            │ JSON
           │                                 │
           ▼                                 ▼
    ┌─────────────────────────────────────────────────┐
    │            FLASK API SERVER                      │
    │         (feedback_api.py)                        │
    │                                                  │
    │  ┌──────────────────────────────────────────┐  │
    │  │  API Endpoints:                          │  │
    │  │                                          │  │
    │  │  POST /api/feedback                      │  │
    │  │    - Receive feedback submissions        │  │
    │  │    - Validate data                       │  │
    │  │    - Store in database                   │  │
    │  │                                          │  │
    │  │  GET /api/feedback                       │  │
    │  │    - Retrieve all feedback               │  │
    │  │                                          │  │
    │  │  GET /api/feedback/stats                 │  │
    │  │    - Calculate aggregated statistics     │  │
    │  │    - Group by provider, answers          │  │
    │  │                                          │  │
    │  │  GET /api/health                         │  │
    │  │    - Health check                        │  │
    │  └──────────────────────────────────────────┘  │
    │                      │                          │
    │                      │ SQL Queries              │
    │                      ▼                          │
    │  ┌──────────────────────────────────────────┐  │
    │  │         SQLite Database                  │  │
    │  │         (feedback.db)                    │  │
    │  │                                          │  │
    │  │  Table: feedback                         │  │
    │  │  - id (PRIMARY KEY)                      │  │
    │  │  - timestamp                             │  │
    │  │  - satisfaction (1-5)                    │  │
    │  │  - clarity (1-5)                         │  │
    │  │  - llm_provider                          │  │
    │  │  - questions_answered                    │  │
    │  │  - improvements (text)                   │  │
    │  │  - conversation (text)                   │  │
    │  │  - user_agent                            │  │
    │  │  - ip_address                            │  │
    │  └──────────────────────────────────────────┘  │
    └─────────────────────────────────────────────────┘
```

## Data Flow

### 1. User Downloads File
```
User clicks "Download" button
    ↓
localStorage stores:
    - llm_explorer_downloaded = true
    - llm_explorer_download_time = timestamp
```

### 2. Survey Trigger
```
User navigates away (changes tab/window)
    ↓
hasLeftPage = true
    ↓
User returns to page (5+ min after download)
    ↓
Check conditions:
    ✓ Has downloaded?
    ✓ Enough time passed (5+ min)?
    ✓ Not already submitted?
    ✓ Not already shown?
    ↓
Show feedback modal
```

### 3. Feedback Submission
```
User fills survey
    ↓
User clicks "Submit"
    ↓
JavaScript prepares JSON:
{
  satisfaction: 5,
  clarity: 4,
  llm_provider: "Claude (Anthropic)",
  questions_answered: "Yes",
  improvements: "...",
  conversation: "..."
}
    ↓
POST to http://localhost:5000/api/feedback
    ↓
Flask API validates data
    ↓
Stores in SQLite database
    ↓
Returns success response
    ↓
Show thank you message
    ↓
Set localStorage: feedback_submitted = true
```

### 4. Admin Views Data
```
Admin opens admin_dashboard.html
    ↓
JavaScript makes parallel requests:
    - GET /api/feedback/stats
    - GET /api/feedback
    ↓
Flask API queries database:
    - COUNT, AVG for stats
    - GROUP BY for distributions
    - ORDER BY timestamp for recent
    ↓
Returns JSON data
    ↓
Dashboard renders:
    - Statistics cards
    - Bar charts
    - Feedback table
    ↓
Auto-refreshes every 30 seconds
```

## Technology Stack

### Frontend
- **HTML5**: Semantic markup
- **CSS3**: Modern styling with animations
- **JavaScript (ES6+)**: Async/await, fetch API, localStorage
- **No frameworks**: Pure vanilla JavaScript for simplicity

### Backend
- **Flask**: Lightweight Python web framework
- **Flask-CORS**: Handle cross-origin requests
- **Python 3**: Modern Python features

### Database
- **SQLite**: Serverless, file-based SQL database
- **No ORM**: Direct SQL for simplicity and control

## Security Features

### Data Protection
- Anonymous collection (no PII)
- Input validation on server side
- SQL injection prevention (parameterized queries)
- XSS prevention (JSON API, no HTML rendering)

### Rate Limiting (Optional)
Can be added with Flask-Limiter:
```python
@limiter.limit("5 per hour")
def submit_feedback():
    ...
```

### CORS
Controlled by Flask-CORS:
```python
CORS(app)  # Allow all origins (dev)
# or
CORS(app, origins=["https://yourdomain.com"])  # Specific origin (prod)
```

## Scalability Considerations

### Current Implementation
- **Good for**: Small to medium traffic (< 1000 users/day)
- **SQLite**: Single file, no server needed
- **Simple deployment**: One Python script

### For Higher Scale
1. **Replace SQLite with PostgreSQL/MySQL**
   ```python
   # Use SQLAlchemy
   from flask_sqlalchemy import SQLAlchemy
   app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://...'
   ```

2. **Add Caching**
   ```python
   from flask_caching import Cache
   cache = Cache(app, config={'CACHE_TYPE': 'redis'})
   ```

3. **Load Balancing**
   - Deploy multiple API instances
   - Use nginx or cloud load balancer

4. **CDN for Static Files**
   - Serve index.html via CDN
   - API calls to separate backend domain

## Deployment Patterns

### Pattern 1: Single Server (Simple)
```
Nginx ──► Flask ──► SQLite
  │
  └─► Static files (index.html)
```

### Pattern 2: Serverless (Scalable)
```
CloudFront ──► S3 (index.html)
               ↓
           AWS Lambda ──► RDS (PostgreSQL)
           (Flask API)
```

### Pattern 3: Containerized (Portable)
```
Docker Compose:
  - nginx container
  - flask container
  - postgres container
```

## File Structure
```
docs/
├── index.html                    # Main page with feedback modal
├── admin_dashboard.html          # Admin panel (view-only)
├── feedback_api.py               # Flask backend
├── requirements.txt              # Python deps: Flask, flask-cors
├── start_feedback_server.sh      # Quick start (Unix)
├── start_feedback_server.bat     # Quick start (Windows)
├── README_FEEDBACK.md            # Quick reference
├── FEEDBACK_SETUP.md             # Detailed setup guide
├── ARCHITECTURE.md               # This file
└── feedback.db                   # SQLite database (created on run)
```

## API Contract

### Request/Response Examples

#### Submit Feedback
```http
POST /api/feedback
Content-Type: application/json

{
  "satisfaction": 5,
  "clarity": 4,
  "llm_provider": "Claude (Anthropic)",
  "questions_answered": "Yes",
  "improvements": "Great tool!",
  "conversation": ""
}

Response 201:
{
  "success": true,
  "message": "Feedback submitted successfully",
  "id": 123
}
```

#### Get Statistics
```http
GET /api/feedback/stats

Response 200:
{
  "success": true,
  "total_responses": 42,
  "average_satisfaction": 4.5,
  "average_clarity": 4.2,
  "llm_providers": [
    {"llm_provider": "Claude (Anthropic)", "count": 20},
    {"llm_provider": "ChatGPT (OpenAI)", "count": 15}
  ],
  "questions_answered": [
    {"questions_answered": "Yes", "count": 30},
    {"questions_answered": "Partially", "count": 10}
  ]
}
```

## Future Enhancements

### Potential Features
- [ ] Email notifications for new feedback
- [ ] Sentiment analysis on text responses
- [ ] Export to multiple formats (Excel, JSON, PDF)
- [ ] User segmentation (by LLM, by date, etc.)
- [ ] A/B testing different survey questions
- [ ] Integration with analytics platforms
- [ ] Real-time dashboard updates (WebSockets)
- [ ] Admin authentication for dashboard

### Implementation Priority
1. **High**: Add admin authentication
2. **High**: Email notifications
3. **Medium**: Better analytics/charts
4. **Low**: Real-time updates
5. **Low**: A/B testing

---

**Architecture designed for simplicity, reliability, and easy deployment.** 🏗️

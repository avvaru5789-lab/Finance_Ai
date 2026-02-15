# FastAPI Backend

Production-ready REST API for the AI Financial Coach system.

## Quick Start

### 1. Set Environment Variables
```bash
cp backend/.env.example backend/.env
# Edit backend/.env and add your OPENROUTER_API_KEY
```

### 2. Start the Server
```bash
# Development mode (with auto-reload)
conda run -n Finance_env uvicorn backend.main:app --reload --port 8000

# Or run directly
conda run -n Finance_env python backend/main.py
```

### 3. Access API Documentation
- **Swagger UI**: http://localhost:8000/docs
- **ReDoc**: http://localhost:8000/redoc

---

## API Endpoints

### Health Check
```bash
GET /health
```

### Main Analysis
```bash
POST /api/analyze
Content-Type: multipart/form-data

file: bank_statement.pdf
user_id: optional-user-id
```

### OCR Extraction
```bash
POST /api/ocr/extract
Content-Type: multipart/form-data

file: document.pdf
```

### Transaction Categorization
```bash
POST /api/transactions/categorize
Content-Type: application/json

{
  "transactions": [
    {
      "date": "2024-01-15T00:00:00",
      "description": "Amazon Prime",
      "amount": -14.99
    }
  ]
}
```

---

## Testing

```bash
# Run test suite
conda run -n Finance_env python backend/test_api.py

# Or use pytest
conda run -n Finance_env pytest backend/
```

---

## Architecture

```
backend/
├── main.py                  # FastAPI app
├── api/
│   ├── routes/             # API endpoints
│   │   ├── health.py
│   │   ├── analyze.py
│   │   ├── ocr.py
│   │   └── transactions.py
│   ├── schemas/            # Pydantic models
│   │   ├── requests.py
│   │   └── responses.py
│   └── middleware/         # CORS, error handling
│       └── error_handler.py
└── services/
    └── analysis_service.py  # Business logic
```

---

## Pipeline

1. **Upload** - Receive PDF via multipart/form-data
2. **OCR** - Extract text (Docker PaddleOCR or pdfplumber)
3. **Parse** - Extract transactions
4. **Categorize** - ML-based categorization
5. **Metrics** - Calculate financial metrics
6. **LangGraph** - Run 4 AI agents in parallel
7. **Response** - Return structured JSON

---

## Response Format

```json
{
  "analysis_id": "uuid",
  "timestamp": "2024-01-15T10:30:00Z",
  "status": "complete",
  "summary": {
    "total_income": 5000.00,
    "total_expenses": 3500.00,
    "net_income": 1500.00,
    "savings_rate": 30.0,
    "debt_to_income_ratio": 100.0
  },
  "analysis": {
    "debt": { ... },
    "savings": { ... },
    "budget": { ... },
    "risk": { ... }
  }
}
```

---

## Production Deployment

### Docker
```dockerfile
FROM python:3.11-slim

WORKDIR /app
COPY requirements.txt .
RUN pip install -r requirements.txt

COPY . .

CMD ["uvicorn", "backend.main:app", "--host", "0.0.0.0", "--port", "8000"]
```

### Environment Variables (Production)
- `OPENROUTER_API_KEY` - Required
- `MONGODB_URI` - For storing analyses
- `CORS_ORIGINS` - Frontend URLs
- `OCR_SERVICE_URL` - Docker OCR service

---

## Error Handling

All errors return consistent JSON format:
```json
{
  "error": "Error message",
  "status_code": 400,
  "detail": "Detailed information",
  "path": "/api/analyze"
}
```

---

## Development

### Add New Endpoint
1. Create route in `backend/api/routes/`
2. Add request/response schemas
3. Include router in `main.py`

### Add New Service
1. Create service in `backend/services/`
2. Inject dependencies in route handlers
3. Add error handling

---

## Features

✅ **Type-Safe** - Pydantic request/response validation  
✅ **Auto-Docs** - Swagger UI and ReDoc  
✅ **CORS** - Frontend integration ready  
✅ **Error Handling** - Consistent error responses  
✅ **File Upload** - Multipart form data support  
✅ **Async** - Full async/await support  
✅ **Testable** - FastAPI TestClient  

---

Production-ready API! 🚀

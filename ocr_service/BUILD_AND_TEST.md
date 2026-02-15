# Docker OCR Service - Build & Test Instructions

## ✅ Files Created

```
ocr_service/
├── Dockerfile              # Container definition
├── docker-compose.yml      # Service orchestration
├── requirements.txt        # Python dependencies (isolated)
├── app.py                  # FastAPI server
├── paddle_ocr_engine.py    # PaddleOCR wrapper
└── README.md               # Usage instructions
```

---

## 🚀 Build and Start Service

### Option 1: Using docker-compose (Recommended)

```bash
cd ocr_service
docker-compose up --build -d
```

**What this does:**
- Builds the Docker image
- Downloads PaddleOCR models (~50-100 MB)
- Starts service on http://localhost:8001
- Runs in background (`-d` flag)

**First build time:** 3-5 minutes (downloads and installs everything)
**Subsequent starts:** <10 seconds

---

### Option 2: Manual Docker commands

```bash
cd ocr_service

# Build image
docker build -t paddleocr-service .

# Run container
docker run -d -p 8001:8001 --name paddleocr paddleocr-service
```

---

## ✅ Verify Service is Running

### 1. Check health
```bash
curl http://localhost:8001/health
```

**Expected response:**
```json
{
  "status": "healthy",
  "service": "paddleocr",
  "version": "1.0.0"
}
```

### 2. Check logs
```bash
docker-compose logs -f
```

**Expected output:**
```
✅ PaddleOCR initialized successfully
✅ PaddleOCR service ready
INFO:     Application startup complete.
INFO:     Uvicorn running on http://0.0.0.0:8001
```

---

## 🧪 Test OCR Endpoint

### Using curl:
```bash
# Test with an image (create test.png first or use any image)
curl -X POST http://localhost:8001/ocr/image \
  -F "file=@test.png"
```

### Using Python:
```python
import requests

url = "http://localhost:8001/ocr/image"
files = {"file": open("test.png", "rb")}

response = requests.post(url, files=files)
print(response.json())
```

**Expected response:**
```json
{
  "text": "Extracted text from image",
  "confidence": 0.95,
  "detections": [...],
  "lines_found": 5
}
```

---

## 🛑 Stop Service

```bash
cd ocr_service
docker-compose down
```

---

## 🔧 Troubleshooting

### Service won't start
```bash
# Check logs
docker-compose logs

# Rebuild from scratch
docker-compose down
docker-compose build --no-cache
docker-compose up
```

### Port 8001 already in use
```bash
# Find what's using port 8001
lsof -i :8001

# Or change port in docker-compose.yml
ports:
  - "8002:8001"  # Use port 8002 instead
```

### Models not downloading
- Make sure you have internet connection
- First startup takes 3-5 minutes
- Models download automatically to `~/.paddleocr/` inside container

---

## ✅ Ready to Integrate

Once you see "✅ PaddleOCR service ready" in the logs, the service is running!

Next step: Update main OCR engine to call this Docker service via HTTP.

# PaddleOCR Microservice

Docker-based OCR service using PaddleOCR, isolated from main application dependencies.

## Quick Start

```bash
# Build and start the service
cd ocr_service
docker-compose up -d

# Check if service is healthy
curl http://localhost:8001/health

# Stop the service
docker-compose down
```

## API Endpoints

### Health Check
```bash
GET http://localhost:8001/health
```

### OCR from Image
```bash
POST http://localhost:8001/ocr/image
Content-Type: multipart/form-data

file: <image_file>
```

**Response:**
```json
{
  "text": "Extracted text here...",
  "confidence": 0.95,
  "detections": [...],
  "lines_found": 10
}
```

## Development

### Build image manually
```bash
docker build -t paddleocr-service .
```

### Run container manually
```bash
docker run -p 8001:8001 paddleocr-service
```

### View logs
```bash
docker-compose logs -f
```

## Architecture

- **Base Image:** Python 3.11-slim
- **Framework:** FastAPI + Uvicorn
- **OCR Engine:** PaddleOCR 2.7.3
- **Port:** 8001
- **Memory Limit:** 2GB
- **CPU Limit:** 2 cores

## Models

PaddleOCR downloads models automatically on first use (~50-100 MB).
Models are cached inside the container at `~/.paddleocr/`.

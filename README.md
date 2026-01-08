# 🤖 Chatbot API

FastAPI tabanlı AI chatbot API'si. Ollama ve LangChain kullanarak yerel LLM'lerle konuşma yapabilirsiniz.

## 🚀 Özellikler

- ✅ FastAPI ile hızlı ve modern API
- ✅ Ollama entegrasyonu (qwen3:1.7b)
- ✅ Rate limiting (60 saniyede 10 request)
- ✅ Structured logging
- ✅ Input validation
- ✅ Docker desteği

## 📋 Gereksinimler

- Python 3.12+
- Ollama (yerel olarak çalışıyor olmalı)
- uv veya pip

## 🛠️ Kurulum

1. Projeyi klonla:
```bash
git clone https://github.com/DenizOk20/chatbot-api.git
cd langgraph-chatbot-api
```

2. Bağımlılıkları kur:
```bash
uv pip install -r requirements.txt
```

3. Ollama'da modeli indir:
```bash
ollama pull qwen3:1.7b
```

4. API'yi çalıştır:
```bash
python main.py
```

## 🐳 Docker ile Çalıştırma
```bash
# Build
docker build -t chatbot-api .

# Run
docker run -d -p 8000:8000 --network host --name chatbot chatbot-api
```

## 📚 API Kullanımı

### Health Check
```bash
curl http://localhost:8000/health
```

### Chat Endpoint
```bash
curl -X POST http://localhost:8000/chat \
  -H "Content-Type: application/json" \
  -d '{"message": "Merhaba, nasılsın?"}'
```

**Response:**
```json
{
  "response": "İyiyim, teşekkür ederim!",
  "timestamp": "2026-01-02T16:30:00",
  "model": "qwen3:1.7b"
}
```

## 📖 API Dokümantasyonu

API çalıştıktan sonra:
- Swagger UI: http://localhost:8000/docs

## 🧪 Testler
```bash
pytest test_main.py -v
```

## 🔒 Rate Limiting

- **Limit:** 10 request / 60 saniye (IP bazlı)
- **Response:** 429 Too Many Requests

## 🛡️ Güvenlik

- Input validation (max 1000 karakter)
- Rate limiting
- Error handling
- Request logging

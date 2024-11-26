# Adjust .env

```
cp app/.env-sample  /app/.env
```

# Run Client to test

**Streaming Test**
```
python client.py
```

**Non Streaming Test**
```
curl -X POST http://127.0.0.1:5000/api/v1/chat/completions \
-H "Content-Type: application/json" \
-H "Authorization: Bearer xx" \
-d '{
    "messages": [
      {
        "role": "user",
        "content": "Skor terbaru liverpool"
      }
    ],
    "model": "perplexity/llama-3.1-sonar-large-128k-online"
}'
```

# Docker

```
pip freeze -l > requirements.txt
docker build -t my_flask_app .
docker run -p 5000:5000 my_flask_app
```
A simple python flask proxy to wrap add citation for Online Capable LLM like Perplexity.  

The citation will be add to the response 
```
Sources:
[1]. https://www.digitalocean.com/community/tutorials/how-to-configure-the-linux-firewall-for-docker-swarm-on-ubuntu-16-04
[2]. https://github.com/chaifeng/ufw-docker
[3]. https://blog.jarrousse.org/2023/03/18/how-to-use-ufw-firewall-with-docker-containers/
[4]. https://docs.docker.com/engine/network/packet-filtering-firewalls/
[5]. https://docs.docker.com/engine/install/ubuntu/
```

# Usage

## Run Docker Image as service

The proxy can be deployed as docker images using this command :
 
```
pip freeze -l > requirements.txt
docker build -t llm-citation-proxy .
docker run -p 5000:5000 llm-citation-proxy 
```

## Using docker COmpose

```
version: '3.4'
 
services:
  llm-citation-proxy:
    build:
      context: ./tonjoo-llm-citation-proxy
      dockerfile: Dockerfile
    environment:
      - DEBUG_LEVEL=INFO
      - BASE_URL=https://openrouter.ai/api/v1
    restart: unless-stopped
```

## Librechat Integration

```
endpoints:
  custom:
    - name: 'OnlineSearch'
      apiKey: 'xxxx'
      baseURL: 'http://llm-citation-proxy:5000/api/v1'
      models:
        default: [
          'perplexity/llama-3.1-sonar-huge-128k-online',
          'perplexity/llama-3.1-sonar-large-128k-online'
        ]
        fetch: false
      titleConvo: true
      titleModel: 'perplexity/llama-3.1-sonar-large-128k-online'
      modelDisplayLabel: 'OnlineSearch'
```


# Development

Adjust the env variable

```
cp app/.env-sample  /app/.env
```

Run python proxy
```
python app/app.py
```

Test using streaming client or curl

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


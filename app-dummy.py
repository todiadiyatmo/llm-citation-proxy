from flask import Flask, Response, request, jsonify
import json
import time

app = Flask(__name__)

def generate_dummy_chunks():
    # Simulate OpenAI ChatCompletionChunk format
    chunks = [
        {
            "id": "chatcmpl-123",
            "object": "chat.completion.chunk",
            "created": int(time.time()),
            "model": "gpt-3.5-turbo",
            "choices": [{
                "index": 0,
                "delta": {"content": "Hello"},
                "finish_reason": None
            }]
        },
        {
            "id": "chatcmpl-123",
            "object": "chat.completion.chunk",
            "created": int(time.time()),
            "model": "gpt-3.5-turbo",
            "choices": [{
                "index": 0,
                "delta": {"content": " world"},
                "finish_reason": None
            }]
        },
        {
            "id": "chatcmpl-123",
            "object": "chat.completion.chunk",
            "created": int(time.time()),
            "model": "gpt-3.5-turbo",
            "choices": [{
                "index": 0,
                "delta": {"content": "!"},
                "finish_reason": "stop"
            }]
        },
        # {
        #   "id": "gen-1732603149-NumRRGYMXXmEAbsnA06i",
        #   "choices": [
        #     {
        #       "delta": {
        #         "content": "-32",
        #         "function_call": null,
        #         "refusal": null,
        #         "role": "assistant",
        #         "tool_calls": null
        #       },
        #       "finish_reason": null,
        #       "index": 0,
        #       "logprobs": null
        #     }
        #   ],
        #   "created": 1732603149,
        #   "model": "perplexity/llama-3.1-sonar-large-128k-online",
        #   "object": "chat.completion.chunk",
        #   "service_tier": null,
        #   "system_fingerprint": null,
        #   "usage": null,
        #   "provider": "Perplexity",
        #   "citations": [
        #     "https://banjarmasin.tribunnews.com/2024/11/19/skor-2-0-hasil-akhir-pertandingan-timnas-indonesia-vs-arab-saudi-dan-klasemen-terbaru-grup-c",
        #     "https://tirto.id/hasil-timnas-indonesia-vs-arab-skor-akhir-update-klasemen-wcq-round-3-g5Uc",
        #     "https://www.tempo.co/sepakbola/hasil-kualifikasi-piala-dunia-2026-timnas-indonesia-kalah-0-4-dari-jepang-1168880",
        #     "https://www.sindonews.com/topic/142585/hasil-timnas-indonesia",
        #     "https://www.youtube.com/watch?v=ZjD26PYohtE"
        #   ]
        # }
    ]
    
    for chunk in chunks:
        yield f"data: {json.dumps(chunk)}\n\n"
        time.sleep(0.5)  # Simulate delay between chunks

@app.route('/api/v1/chat/completions', methods=['POST'])
def chat_completions():
    data = request.get_json()
    
    # Check if streaming is requested
    stream = data.get('stream', False)
    
    if not stream:
        # Return non-streaming response
        return jsonify({
            "id": "chatcmpl-123",
            "object": "chat.completion",
            "created": int(time.time()),
            "model": "gpt-3.5-turbo",
            "choices": [{
                "index": 0,
                "message": {"content": "Hello world!"},
                "finish_reason": "stop"
            }]
        })
    
    # Return streaming response
    return Response(
        generate_dummy_chunks(),
        mimetype='text/event-stream',
        headers={
            'Cache-Control': 'no-cache',
            'Connection': 'keep-alive',
        }
    )

if __name__ == '__main__':
    app.run(debug=True, port=5000)
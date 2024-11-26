import logging
from openai import OpenAI
from flask import Flask, request, Response, abort
import json
import os
from dotenv import load_dotenv

load_dotenv()

logging.basicConfig(level=os.getenv('DEBUG_LEVEL', 'INFO'))
# supress other debug
httpcore_logger = logging.getLogger('httpcore')
httpcore_logger.setLevel(logging.WARNING)
httpcore_logger = logging.getLogger('httpx')
httpcore_logger.setLevel(logging.WARNING)
app = Flask(__name__)

def generate(chunks):
    try:
        citations = []
        for chunk in chunks:
            logging.debug(f"Streaming event: {chunk.model_dump_json()}")
            
            if hasattr(chunk, 'citations') and chunk.citations:
                citations = chunk.citations

            if hasattr(chunk.choices[0], "finish_reason"):
                is_last_chunk = chunk.choices[0].finish_reason == "stop"
            else:
                is_last_chunk = False

            if is_last_chunk and citations:
                # Add citations to the last chunk
                citation_text = "\n\nSources:\n" + "\n".join([f"[{i}]. {citation}" for i, citation in enumerate(citations, 1)])
                
                chunk.choices[0].delta.content+=citation_text

                yield f"data: {chunk.model_dump_json()}\n\n"
            else:
                yield f"data: {chunk.model_dump_json()}\n\n"             

    except Exception as e:
        error_msg = f"An error occurred: {str(e)}"
        logging.error(error_msg)
        yield f"data: {json.dumps({'error': {'message': error_msg, 'type': 'internal_error', 'code': 500}})}\n\n"


@app.route('/api/v1/chat/completions', methods=['POST'])
def openai_completion():

    # Get API key from Authorization header
    auth_header = request.headers.get('Authorization', '')

    if not auth_header or not auth_header.startswith('Bearer '):
        abort(401, description="Unauthorized: Bearer token not found")

    api_key = auth_header.replace('Bearer ', '') if auth_header else None

    # Get request data with defaults
    request_data = request.json or {}
    
    logging.debug(json.dumps(request_data, indent=4))

    # Required parameters
    messages = request_data.get('messages')
    model = request_data.get('model', 'perplexity/llama-3.1-sonar-large-128k-online')

    if not messages:
        abort(400, description="Bad Request: 'messages' is required")

    if not api_key:
        abort(400, description="Bad Request: 'api_key' is required")

    # Optional parameters with defaults
    completion_params = {
        'messages': messages,
        'model': model,
        'max_tokens': request_data.get('max_tokens', 16000),
        'temperature': request_data.get('temperature', 1.0),
        'top_p': request_data.get('top_p', 1.0),
        'n': request_data.get('n', 1),
        'stream': True,  # Always true for streaming
        'presence_penalty': request_data.get('presence_penalty', 0),
        'frequency_penalty': request_data.get('frequency_penalty', 0),
        'stop': request_data.get('stop', None),
        'user': request_data.get('user', None),
    }

    # Remove None values
    completion_params = {k: v for k, v in completion_params.items() if v is not None}

    # Create client with provided API key
    client = OpenAI(
        base_url=os.getenv('BASE_URL', 'https://openrouter.ai/api/v1'),
        api_key=api_key,
        max_retries=1
    )

    chunks = client.chat.completions.create(**completion_params)

    # //suport non stream
    # stream = data.get('stream', False)
    
    return Response(
        generate(chunks),
        mimetype='text/event-stream',
        headers={
            'Cache-Control': 'no-cache',
            'Connection': 'keep-alive',
        }
    )

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)

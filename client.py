import logging
from openai import OpenAI

# Setup basic logging
logging.basicConfig(level=logging.INFO)
# Get the logger for 'httpcore' and set its level to WARNING
httpcore_logger = logging.getLogger('httpcore')
httpcore_logger.setLevel(logging.WARNING)
httpcore_logger = logging.getLogger('httpx')
httpcore_logger.setLevel(logging.WARNING)

client = OpenAI(
    # base_url="https://openrouter.ai/api/v1",
    base_url="http://127.0.0.1:5000/api/v1",
    api_key="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",
    max_retries=1
)

def stream_completion(message):
    try:
        response = client.chat.completions.create(
            model="perplexity/llama-3.1-sonar-large-128k-online",
            messages=[{"role": "user", "content": message}],
            max_tokens=16000,
            stream=True
        )
        
        # Stream the response
        for chunk in response:
            logging.debug(f"Received chunk: {chunk}")
            if chunk.choices and chunk.choices[0].delta.content:
                content = chunk.choices[0].delta.content
                print(content, end="", flush=True)
                logging.debug(f"Content chunk: {content}")
                
    except Exception as e:
        logging.error(f"An error occurred: {str(e)}")
        return f"An error occurred: {str(e)}"

if __name__ == "__main__":
    message = "skor liverpool terbaru"
    stream_completion(message)
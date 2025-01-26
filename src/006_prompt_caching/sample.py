from anthropic import Anthropic
from dotenv import load_dotenv
import time

load_dotenv()

client = Anthropic()
MODEL_NAME = "claude-3-5-sonnet-20241022"

with open('src/006_prompt_caching/frankenstein.txt', 'r') as file:
    book_content = file.read()

len(book_content)
book_content[100:200]


# def make_non_cached_api_call():
#     messages = [
#         {
#             "role": "user",
#             "content": [
#                 {
#                     "type": "text",
#                     "text": "<book>" + book_content + "</book>"
#                 },
#                 {
#                     "type": "text",
#                     "text": "チャプター3で何が起こっていますか？"
#                 }
#             ]
#         }
#     ]

#     start_time = time.time()
#     response = client.messages.create(
#         model=MODEL_NAME,
#         max_tokens=500,
#         messages=messages,
#     )
#     end_time = time.time()
#     return response, end_time - start_time


# non_cached_response, non_cached_time = make_non_cached_api_call()

# print(f"Non-cached time: {non_cached_time:.2f} seconds")

# print("\nOutput (non-cached):")
# print(non_cached_response.content)

# non_cached_response.usage


def make_cached_api_call():
    messages = [
        {
            "role": "user",
            "content": [
                {
                    "type": "text",
                    "text": "<book>" + book_content + "</book>",
                    "cache_control": {"type": "ephemeral"}
                },
                {
                    "type": "text",
                    "text": "チャプター5で何が起こっていますか？"
                }
            ]
        }
    ]

    start_time = time.time()
    response = client.messages.create(
        model=MODEL_NAME,
        max_tokens=500,
        messages=messages,
    )
    end_time = time.time()

    return response, end_time - start_time


response1, duration1 = make_cached_api_call()
response2, duration2 = make_cached_api_call()

print(response1)
print(response2)

print(f"Cached time: {duration1:.2f} seconds")
print(f"Cached time: {duration2:.2f} seconds")

print(response1.usage)
print(response2.usage)

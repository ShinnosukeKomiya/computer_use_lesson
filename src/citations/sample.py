from anthropic import Anthropic
from dotenv import load_dotenv
import base64
import httpx
import mimetypes
load_dotenv()

client = Anthropic()
MODEL_NAME = "claude-3-5-sonnet-20241022"


def create_image_message(image_path):
    with open(image_path, "rb") as image_file:
        binary_data = image_file.read()
    # Encode the binary data using Base64 encoding
    base64_encoded_data = base64.b64encode(binary_data)
    # Decode base64_encoded_data from bytes to a string
    base64_string = base64_encoded_data.decode('utf-8')
    # Get the MIME type of the image based on its file extension
    mime_type, _ = mimetypes.guess_type(image_path)
    # Create the image block
    image_block = {
        "type": "image",
        "source": {
            "type": "base64",
            "media_type": mime_type,
            "data": base64_string
        }
    }
    return image_block


messages = [
    {
        "role": "user",
        "content": [
            create_image_message("./src/citations/komiya.png"),
            {"type": "text", "text": "この画像の内容を説明してください。"}
        ]
    }
]

response = client.messages.create(
    model=MODEL_NAME,
    max_tokens=2048,
    messages=messages
)
print(response.content[0].text)


# def create_pdf_message(pdf_url):
#     return base64.standard_b64encode(httpx.get(pdf_url).content).decode("utf-8")


# messages = [
#     {
#         "role": "user",
#         "content": [
#             {
#                 "type": "document",
#                 "source": {
#                     "type": "base64",
#                     "media_type": "application/pdf",
#                     "data": create_pdf_message("https://www.stat.go.jp/data/jinsui/pdf/202404.pdf")
#                 },
#                 "citations": {"enabled": True}
#             },
#             {
#                 "type": "text",
#                 "text": "2015年の日本人人口の10月の人口を抽出してください。数値のみを回答してください。"
#             }
#         ]
#     }
# ]

# response = client.messages.create(
#     model=MODEL_NAME,
#     max_tokens=1024,
#     messages=messages
# )
# # 回答内容
# print(response.content[0].text)
# # 引用内容
# print(response.content[0].citations)

from anthropic import Anthropic
from dotenv import load_dotenv
import base64
import httpx

load_dotenv()

client = Anthropic()
MODEL_NAME = "claude-3-5-sonnet-20241022"


def create_pdf_message(pdf_url):
    return base64.standard_b64encode(httpx.get(pdf_url).content).decode("utf-8")


messages = [
    {
        "role": "user",
        "content": [
            {
                "type": "document",
                "source": {
                    "type": "base64",
                    "media_type": "application/pdf",
                    "data": create_pdf_message("https://www.stat.go.jp/data/jinsui/pdf/202404.pdf")
                },
                "citations": {"enabled": True}
            },
            {
                "type": "text",
                "text": "2015年の日本人人口の10月の人口を抽出してください。数値のみを回答してください。"
            }
        ]
    }
]

response = client.messages.create(
    model=MODEL_NAME,
    max_tokens=1024,
    messages=messages
)
print(response)

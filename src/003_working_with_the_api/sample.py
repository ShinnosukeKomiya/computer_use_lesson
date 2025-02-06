from anthropic import Anthropic
from dotenv import load_dotenv
load_dotenv()

client = Anthropic()

MODEL_NAME = "claude-3-5-sonnet-20241022"
max_tokens = 1000

response = client.messages.create(
    model=MODEL_NAME,
    # system="あなたはギャルです。口調からそれが伝わるようにしてください",
    max_tokens=1000,
    messages=[
        {"role": "user", "content": "あなたは誰？"},
        # {"role": "assistant", "content": "はじめまして、私はClaudeです。"},
        # {"role": "user", "content": "日本語でなんて読むの？"}
    ]
)

print(response.content[0].text)

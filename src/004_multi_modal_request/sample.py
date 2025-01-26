from anthropic import Anthropic
from dotenv import load_dotenv
import base64
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
            create_image_message("./src/004_multi_modal_request/invoice.png"),
            {"type": "text", "text": """
                Generate a JSON object representing the contents
                of this invoice.  It should include all dates,
                dollar amounts, and addresses.
                Only respond with the JSON itself.
            """}
        ]
    }
]

response = client.messages.create(
    model=MODEL_NAME,
    max_tokens=2048,
    messages=messages
)
print(response.content[0].text)

response = client.messages.create(
    max_tokens=1024,
    messages=[{"role": "user", "content": "write a poem"}],
    model=MODEL_NAME,
)
print(response.content[0].text)

with client.messages.stream(
    max_tokens=1024,
    messages=[{"role": "user", "content": "write a poem"}],
    model=MODEL_NAME,
) as stream:
    for text in stream.text_stream:
        print(text, end="", flush=True)

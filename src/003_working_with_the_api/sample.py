from anthropic import Anthropic
from dotenv import load_dotenv
load_dotenv()

client = Anthropic()

MODEL_NAME = "claude-3-5-sonnet-20241022"
max_tokens = 1000

response = client.messages.create(
    model=MODEL_NAME,
    max_tokens=1000,
    messages=[
        {"role": "user", "content": "Write a haiku"}
    ]
)

print(response.content[0].text)

# Here's a haiku:
#
# Autumn leaves falling
# Dancing softly in the breeze
# Nature's lullaby

response
# The Messages Format
response = client.messages.create(
    model=MODEL_NAME,
    max_tokens=1000,
    messages=[
        {"role": "user", "content": "Hello! Only speak to me in Spanish"},
        {"role": "assistant", "content": "Hola!"},
        {"role": "user", "content": "How are you?"}
    ]
)
print(response.content[0].text)
# Simple Chatbot
print("Simple Chatbot (type 'quit' to exit)")
# Store conversation history
messages = []
while True:
    # Get user input
    user_input = input("You: ")
    # Check for quit command
    if user_input.lower() == 'quit':
        print("Goodbye!")
        break
    # Add user message to history
    messages.append({"role": "user", "content": user_input})
    try:
        # Get response from Claude
        response = client.messages.create(
            model=MODEL_NAME,
            max_tokens=200,
            messages=messages
        )
        # Extract and print Claude's response
        asst_message = response.content[0].text
        print("Assistant:", asst_message)

        # Add assistant response to history
        messages.append({"role": "assistant", "content": asst_message})

    except Exception as e:
        print(f"An error occurred: {e}")
# Prefilling the Assistant Response
response = client.messages.create(
    model=MODEL_NAME,
    max_tokens=1000,
    messages=[
        {"role": "user", "content": "Write a short poem about pigs"},
        {"role": "assistant", "content": "Oink"}
    ]
)

print(response.content[0].text)
# Model Parameters
# Max Tokens
response = client.messages.create(
    model=MODEL_NAME,
    max_tokens=100,
    messages=[
        {"role": "user", "content": "Write me an essay on LLMs"},
    ]
)
print(response.content[0].text)
response
# Stop Sequences
prompt = """
Generate a numbered, ordered list of technical topics
I should learn if I want to work on LLMs
"""
response = client.messages.create(
    model=MODEL_NAME,
    max_tokens=500,
    messages=[{"role": "user", "content": prompt}],
)
print(response.content[0].text)
# In the follwong cell stop_sequences to ["4."].
# This will stop the output as soon as "4." is generated.

prompt = """
Generate a numbered, ordered list of technical topics
I should learn if I want to work on LLMs
"""
response = client.messages.create(
    model=MODEL_NAME,
    max_tokens=500,
    stop_sequences=["4."],
    messages=[{"role": "user", "content": prompt}],
)
print(response.content[0].text)
response
# Temperature


def demonstrate_temperature():
    temperatures = [0, 1]
    for temperature in temperatures:
        print(f"Prompting Claude three times with \
              temperature of {temperature}")
        print("================")
        for i in range(3):
            response = client.messages.create(
                model=MODEL_NAME,
                max_tokens=100,
                messages=[{"role": "user", "content": f"Prompt {i+1}: \
                          Come up with a name for an alien planet. \
                          Respond with a single word."}],
                temperature=temperature
            )
            print(f"Response {i+1}: {response.content[0].text}")


demonstrate_temperature()

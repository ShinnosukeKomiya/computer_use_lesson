from anthropic import Anthropic
from dotenv import load_dotenv
import re

load_dotenv()

MODEL_NAME = "claude-3-5-sonnet-20241022"
client = Anthropic()


class FakeDatabase:
    def __init__(self):
        self.customers = [
            {"id": "1213210", "name": "田中太郎", "email": "taro@example.com", "phone": "090-1234-5678", "username": "taro_t"},
            {"id": "2837622", "name": "鈴木花子", "email": "hanako@example.com", "phone": "080-8765-4321", "username": "hanako_s"},
            {"id": "3924156", "name": "佐藤健一", "email": "kenichi@example.com", "phone": "070-2345-6789", "username": "ken_sato"},
            {"id": "4782901", "name": "山田優子", "email": "yuko@example.com", "phone": "090-8901-2345", "username": "yuko_y"},
            {"id": "5190753", "name": "中村翔太", "email": "shota@example.com", "phone": "080-3456-7890", "username": "shota_n"},
            {"id": "6824095", "name": "小林美咲", "email": "misaki@example.com", "phone": "070-9012-3456", "username": "misaki_k"},
            {"id": "7135680", "name": "伊藤大輔", "email": "daisuke@example.com", "phone": "090-4567-8901", "username": "dai_ito"},
            {"id": "8259147", "name": "渡辺明子", "email": "akiko@example.com", "phone": "080-5678-9012", "username": "akiko_w"},
            {"id": "9603481", "name": "加藤裕太", "email": "yuta@example.com", "phone": "070-6789-0123", "username": "yuta_k"},
            {"id": "1057426", "name": "吉田さくら", "email": "sakura@example.com", "phone": "090-7890-1234", "username": "sakura_y"}
        ]

        self.orders = [
            {"id": "24601", "customer_id": "1213210", "product": "ワイヤレスイヤホン", "quantity": 1, "price": 15000, "status": "発送済み"},
            {"id": "13579", "customer_id": "1213210", "product": "スマホケース", "quantity": 2, "price": 2500, "status": "処理中"},
            {"id": "97531", "customer_id": "2837622", "product": "Bluetoothスピーカー", "quantity": 1, "price": 8000, "status": "発送済み"},
            {"id": "86420", "customer_id": "3924156", "product": "活動量計", "quantity": 1, "price": 12000, "status": "配達済み"},
            {"id": "54321", "customer_id": "4782901", "product": "ノートPCケース", "quantity": 3, "price": 3000, "status": "発送済み"},
            {"id": "19283", "customer_id": "5190753", "product": "ワイヤレスマウス", "quantity": 1, "price": 4500, "status": "処理中"},
            {"id": "74651", "customer_id": "6824095", "product": "ゲーミングキーボード", "quantity": 1, "price": 12000, "status": "配達済み"},
            {"id": "30298", "customer_id": "7135680", "product": "モバイルバッテリー", "quantity": 2, "price": 3500, "status": "発送済み"},
            {"id": "47652", "customer_id": "8259147", "product": "スマートウォッチ", "quantity": 1, "price": 25000, "status": "処理中"},
            {"id": "61984", "customer_id": "9603481", "product": "ノイズキャンセリングヘッドホン", "quantity": 1, "price": 28000, "status": "発送済み"},
            {"id": "58243", "customer_id": "1057426", "product": "完全ワイヤレスイヤホン", "quantity": 2, "price": 18000, "status": "配達済み"},
            {"id": "90357", "customer_id": "1213210", "product": "スマホケース", "quantity": 1, "price": 2500, "status": "発送済み"},
            {"id": "28164", "customer_id": "2837622", "product": "ワイヤレスイヤホン", "quantity": 2, "price": 15000, "status": "処理中"}
        ]

    def get_user(self, key, value):
        if key in {"email", "phone", "username"}:
            for customer in self.customers:
                if customer[key] == value:
                    return customer
            return f"Couldn't find a user with {key} of {value}"
        else:
            raise ValueError(f"Invalid key: {key}")

    def get_order_by_id(self, order_id):
        for order in self.orders:
            if order["id"] == order_id:
                return order
        return None

    def get_customer_orders(self, customer_id):
        return [order for order in self.orders if order["customer_id"] == customer_id]

    def cancel_order(self, order_id):
        order = self.get_order_by_id(order_id)
        if order:
            if order["status"] == "Processing":
                order["status"] = "Cancelled"
                return "Cancelled the order"
            else:
                return "Order has already shipped.  Can't cancel it."
        return "Can't find that order!"


db = FakeDatabase()
db.get_user("email", "taro@example.com")
db.get_customer_orders("1213210")
db.cancel_order("13579")

tools = [
    {
        "name": "get_user",
        "description": "Looks up a user by email, phone, or username.",
        "input_schema": {
            "type": "object",
            "properties": {
                "key": {
                    "type": "string",
                    "enum": ["email", "phone", "username"],
                    "description": "The attribute to search for a user by (email, phone, or username)."
                },
                "value": {
                    "type": "string",
                    "description": "The value to match for the specified attribute."
                }
            },
            "required": ["key", "value"]
        }
    },
    {
        "name": "get_order_by_id",
        "description": "Retrieves the details of a specific order based on the order ID. Returns the order ID, product name, quantity, price, and order status.",
        "input_schema": {
            "type": "object",
            "properties": {
                "order_id": {
                    "type": "string",
                    "description": "The unique identifier for the order."
                }
            },
            "required": ["order_id"]
        }
    },
    {
        "name": "get_customer_orders",
        "description": "Retrieves the list of orders belonging to a user based on a user's customer id.",
        "input_schema": {
            "type": "object",
            "properties": {
                "customer_id": {
                    "type": "string",
                    "description": "The customer_id belonging to the user"
                }
            },
            "required": ["customer_id"]
        }
    },
    {
        "name": "cancel_order",
        "description": "Cancels an order based on a provided order_id.  Only orders that are 'processing' can be cancelled",
        "input_schema": {
            "type": "object",
            "properties": {
                "order_id": {
                    "type": "string",
                    "description": "The order_id pertaining to a particular order"
                }
            },
            "required": ["order_id"]
        }
    }
]

messages = [
    {
        "role": "user",
        "content": "taro@example.comの注文履歴を教えてください。"
    }
]
response = client.messages.create(
    model=MODEL_NAME,
    max_tokens=4096,
    tools=tools,
    messages=messages
)
print(response.content)
print(response.content[-1])


# def process_tool_call(tool_name, tool_input):
#     if tool_name == "get_user":
#         return db.get_user(tool_input["key"], tool_input["value"])
#     elif tool_name == "get_order_by_id":
#         return db.get_order_by_id(tool_input["order_id"])
#     elif tool_name == "get_customer_orders":
#         return db.get_customer_orders(tool_input["customer_id"])
#     elif tool_name == "cancel_order":
#         return db.cancel_order(tool_input["order_id"])


# tool_use = response.content[-1]
# tool_name = tool_use.name
# tool_input = tool_use.input
# tool_result = process_tool_call(tool_name, tool_input)
# {
#     "role": "user",
#     "content": [
#         {
#             "type": "tool_result",
#             "tool_use_id": tool_use.id,
#             "content": str(tool_result),
#         }
#     ],
# }


# def extract_reply(text):
#     pattern = r'<reply>(.*?)</reply>'
#     match = re.search(pattern, text, re.DOTALL)
#     if match:
#         return match.group(1)
#     else:
#         return None


# def simple_chat():
#     system_prompt = """
#     You are a customer support chat bot for an online retailer
#     called Acme Co.Your job is to help users look up their account,
#     orders, and cancel orders.Be helpful and brief in your responses.
#     You have access to a set of tools, but only use them when needed.
#     If you do not have enough information to use a tool correctly,
#     ask a user follow up questions to get the required inputs.
#     Do not call any of the tools unless you have the required
#     data from a user.

#     In each conversational turn, you will begin by thinking about
#     your response. Once you're done, you will write a user-facing
#     response. It's important to place all user-facing conversational
#     responses in <reply></reply> XML tags to make them easy to parse.
#     """
#     user_message = input("\nUser: ")
#     messages = [{"role": "user", "content": user_message}]
#     while True:
#         if user_message == "quit":
#             break
#         # If the last message is from the assistant,
#         # get another input from the user
#         if messages[-1].get("role") == "assistant":
#             user_message = input("\nUser: ")
#             messages.append({"role": "user", "content": user_message})
#         # Send a request to Claude
#         response = client.messages.create(
#             model=MODEL_NAME,
#             system=system_prompt,
#             max_tokens=4096,
#             tools=tools,
#             messages=messages
#         )
#         # Update messages to include Claude's response
#         messages.append(
#             {"role": "assistant", "content": response.content}
#         )

#         # If Claude stops because it wants to use a tool:
#         if response.stop_reason == "tool_use":
#             # Naive approach assumes only 1 tool is called at a time
#             tool_use = response.content[-1]
#             tool_name = tool_use.name
#             tool_input = tool_use.input
#             print(f"=====Claude wants to use the {tool_name} tool=====")

#             # Actually run the underlying tool functionality on our db
#             tool_result = process_tool_call(tool_name, tool_input)

#             # Add our tool_result message:
#             messages.append(
#                 {
#                     "role": "user",
#                     "content": [
#                         {
#                             "type": "tool_result",
#                             "tool_use_id": tool_use.id,
#                             "content": str(tool_result),
#                         }
#                     ],
#                 },
#             )
#         else:
#             # If Claude does NOT want to use a tool,
#             # just print out the text reponse
#             model_reply = extract_reply(response.content[0].text)
#             print("\nAcme Co Support: " + f"{model_reply}")


# simple_chat()

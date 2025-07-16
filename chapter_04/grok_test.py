from xai_sdk import Client
from xai_sdk.chat import user, system

client = Client(api_key="xai-A61mZH2L2OnZO5KtwFB0a2cpfIk1zyMzUGekaQ4HM9jkKEOB3DoOa66FSVn4AY9COAwGKunCTch1dtU6")

chat = client.chat.create(model="grok-4-0709", temperature=0)
chat.append(system("You are a PhD-level mathematician."))
chat.append(user("What is 2 + 2?"))

response = chat.sample()
print(response.content)
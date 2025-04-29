from openai import AsyncOpenAI
import os

from dotenv import load_dotenv

class AIChatBot:
	def __init__(self, api_key, model):
		self.api_key = api_key
		self.model = model
		self.client = AsyncOpenAI(
                base_url="https://models.github.ai/inference",
				api_key=self.api_key,
			)
    
	async def ask(self, prompt):
		response = await self.client.chat.completions.create(
				model=self.model,
				messages=[
					{"role": "system", "content": "You are a helpful assistant for students. All your answers should be in Russian language."},
					{"role": "user", "content": f"{prompt}"}
					]
			)
		return response.choices[0].message.content

# import os
# from azure.ai.inference import ChatCompletionsClient
# from azure.ai.inference.models import SystemMessage, UserMessage
# from azure.core.credentials import AzureKeyCredential

# endpoint = "https://models.github.ai/inference"
# model = "openai/gpt-4.1"
# token = os.environ["GITHUB_TOKEN"]

# client = ChatCompletionsClient(
#     endpoint=endpoint,
#     credential=AzureKeyCredential(token),
# )

# response = client.complete(
#     messages=[
#         SystemMessage(""),
#         UserMessage("What is the capital of France?"),
#     ],
#     temperature=1,
#     top_p=1,
#     model=model
# )

# print(response.choices[0].message.content)
import openai
import os
import json


class OpenAI:

    def __init__(self):
        # Set the openapi key for OpenAI
        openai.api_key = os.getenv("OPENAI_API_KEY")

        # Load prompt json file into object
        with open('llm/openai_prompts.json', 'r') as f:
            self.prompts = json.loads(f.read())

    def get_system_prompt(self, prompt_name):
        return '\n'.join(self.prompts[prompt_name])

    @staticmethod
    def send_request(system_text, prompt_text):
        # Send the prompt to OpenAI
        response = openai.ChatCompletion.create(
            model="gpt-3.5-turbo-16k",
            messages=[
                {
                    'role': 'system',
                    'content': system_text
                },
                {
                    'role': 'user',
                    'content': prompt_text
                }
            ],
            temperature=0,
            n=1,
            frequency_penalty=1,
            presence_penalty=1
        )

        return response['choices'][0]['message']['content']

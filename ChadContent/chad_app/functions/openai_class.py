import openai
import requests

class OpenAIGPT:
    def __init__(self, model="gpt-3.5-turbo"):
        # Get environment variables
        self._API_KEY = None
        self._ORG_ID = None
        self._model = model
        self.last_prompt = None
        self.last_response = None
        self.last_response_insight = None
        self.last_prompt_insight = None

        # Load openAI
        self._openai = openai

    # Setup API data
    def setup_api(self, api_key: str, org_id: str):
        self._openai.organization = org_id
        self._openai.api_key = api_key


    # Generating a post
    def post_functions(self, topic: str, keywords: str, brand_voice: str, content_type: str):
        # Build the prompt strings keywords and voice
        prompt_string = ""
        if brand_voice != "":
            prompt_string += f"You using the voice styles of '{brand_voice}'."
        if keywords != "":
            prompt_string += f"Using as many of these words as possible '{keywords}'."

        # Set the prompt goal
        if content_type == "intro":
            prompt_string += f"Write 1 paragraph on `{topic}` that is 3-5 sentences long."

        elif content_type == "para":
            prompt_string += f"Write the introduction paragraph for a blog post on `{topic}` that is 3-5 sentences long."

        elif content_type == "tweet":
            prompt_string += f"Write 1-3 sentences on `{topic}` for social media."

        # Setup prompt
        self.last_prompt = [
            {"role": "user","content": prompt_string
            }]

        self.last_response = self._openai.ChatCompletion.create(
            model=self._model,
            messages=self.last_prompt)["choices"][0]["message"]["content"]

        return self.last_response, self.last_prompt[0]["content"]


    # Generate headings
    def generate_headings(self, content_info: str, keywords: str, brand_voice: str):
        # Build the prompt strings keywords and voice
        prompt_string = ""
        if brand_voice != "":
            prompt_string += f"You using the voice styles of '{brand_voice}'."
        if keywords != "":
            prompt_string += f"Using as many of these words as possible '{keywords}'."

        # Setup prompt
        self.last_prompt = [
            {"role": "user",
            "content": f"{prompt_string} Provide headings for a blog post on '{content_info}."
            }]

        self.last_response = self._openai.ChatCompletion.create(
            model=self._model,
            messages=self.last_prompt)["choices"][0]["message"]["content"]

        return self.last_response, self.last_prompt[0]["content"]


    # Reword a response
    def reword_response(self, brand_voice: str, input_prompt: str, keywords: str, 
        new_length: str, additional_prompt: str):
        # Build the prompt strings keywords and voice
        prompt_string = ""
        if brand_voice != "":
            prompt_string += f"You using the voice styles of '{brand_voice}'."
        if keywords != "":
            prompt_string += f"Using as many of these words as possible '{keywords}'."
        if new_length != "":
            prompt_string += f"Make the response {new_length} sentences long."
        if additional_prompt != "":
            prompt_string += f"{additional_prompt}"

        # Setup prompt
        self.last_prompt = [
            {"role": "user",
            "content": f"{prompt_string} Rephrase the following '{input_prompt}'."
            }]

        self.last_response = self._openai.ChatCompletion.create(
            model=self._model,
            messages=self.last_prompt)["choices"][0]["message"]["content"]

        return self.last_response, self.last_prompt[0]["content"]


    # Answer a question
    def answer_question(self, question: str, keywords: str, brand_voice: str, length_response: str):
        # Build the prompt strings keywords and voice
        prompt_string = ""
        if brand_voice != "":
            prompt_string += f"You using the voice styles of '{brand_voice}'."
        if keywords != "":
            prompt_string += f"Using as many of these words as possible '{keywords}'."
        if length_response != "":
            prompt_string += f"Make the response {length_response} sentences long."

        # Setup prompt
        self.last_prompt = [
                {"role": "user","content": f"{prompt_string} Answer `{question}?`."
                }]
       
        self.last_response = self._openai.ChatCompletion.create(
            model=self._model,
            messages=self.last_prompt)["choices"][0]["message"]["content"]

        return self.last_response, self.last_prompt[0]["content"]


    def make_embedding(self, response_in):
        model_id = "text-similarity-davinci-001"
        embedding_response = openai.Embedding.create(input=response_in, model=model_id)
        embedding_response = embedding_response["data"][0]["embedding"]

        return embedding_response
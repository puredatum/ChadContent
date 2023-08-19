import openai

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
    def setup_api(self, api_key, org_id):
        self._openai.organization = org_id
        self._openai.api_key = api_key

    # Make a chat request
    def make_paragraph(self, topic: str, keywords: str, brand_voice: str, content_type: str):
        if content_type == "intro":
            quote_prompt = [
                {"role": "user","content": f"You using the voice styles of '{brand_voice}' while using the keywords '{keywords}'' about a topic. Write the introduction paragraph of a blog post on `{topic}` that is 3-5 sentences long"
                }]
        elif content_type == "para":
            quote_prompt = [
                {"role": "user","content": f"You using the voice styles of '{brand_voice}' while using the keywords '{keywords}'' about a topic. Write 1 paragraph on `{topic}` that is 3-5 sentences long"
                }]

        elif content_type == "tweet":
            quote_prompt = [
                {"role": "user","content": f"You using the voice styles of '{brand_voice}' while using the keywords '{keywords}', write a post up to 3 sentences long on `{topic}`."
                }]

        self.last_prompt = quote_prompt
        self.last_response = self._openai.ChatCompletion.create(
            model=self._model,
            messages=quote_prompt)["choices"][0]["message"]["content"]

        return self.last_response, self.last_prompt[0]["content"]


    # Generate insight for a quote
    def generate_headings(self, content_info: str, keywords: str):
        headings_prompt = [
            {"role": "user",
            "content": f"Provide headings for a blog post on '{content_info}, aiming to include as many {keywords} as you can.'"
            }]

        self.last_prompt = headings_prompt
        self.last_response_insight = self._openai.ChatCompletion.create(
            model=self._model,
            messages=self.last_prompt)["choices"][0]["message"]["content"]

        return self.last_response, self.last_prompt[0]["content"]

    # Generate insight for a quote
    def regen(self, reword_response):
        self.last_prompt = [
            {"role": "user",
            "content": f"Reword the following '{reword_response}.'."
            }]

        self.last_response = self._openai.ChatCompletion.create(
            model=self._model,
            messages=self.last_prompt)["choices"][0]["message"]["content"]

        return self.last_response, self.last_prompt[0]["content"]

    # Make a chat request
    def answer_question(self, question: str, keywords: str, brand_voice: str):
        quote_prompt = [
            {"role": "user","content": f"Answer `{question}?` using the voice of '{brand_voice}' while using the as many of the following words as you can '{keywords}'."
            }]
       
        self.last_prompt = quote_prompt
        self.last_response = self._openai.ChatCompletion.create(
            model=self._model,
            messages=quote_prompt)["choices"][0]["message"]["content"]

        return self.last_response, self.last_prompt[0]["content"]
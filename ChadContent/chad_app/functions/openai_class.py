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
    def post_functions(self, topic: str, keywords: str, brand_voice: str, content_type: str):
        if content_type == "intro":
            if keywords != "":
                quote_prompt = [
                    {"role": "user","content": f"You using the voice styles of '{brand_voice}' while using the keywords '{keywords}'' about a topic. Write the introduction paragraph of a blog post on `{topic}` that is 3-5 sentences long"
                    }]
            else:
                quote_prompt = [
                    {"role": "user","content": f"You using the voice styles of '{brand_voice}'. Write the introduction paragraph of a blog post on `{topic}` that is 3-5 sentences long"
                    }]
        elif content_type == "para":
            if keywords != "":
                quote_prompt = [
                    {"role": "user","content": f"You using the voice styles of '{brand_voice}' while using the keywords '{keywords}'' about a topic. Write 1 paragraph on `{topic}` that is 3-5 sentences long"
                    }]
            else:
                quote_prompt = [
                    {"role": "user","content": f"You using the voice styles of '{brand_voice}'. Write 1 paragraph on `{topic}` that is 3-5 sentences long"
                    }]

        elif content_type == "tweet":
            if keywords != "":
                quote_prompt = [
                    {"role": "user","content": f"You using the voice styles of '{brand_voice}' while using the keywords '{keywords}', write a post up to 3 sentences long on `{topic}`."
                    }]
            else:
                quote_prompt = [
                    {"role": "user","content": f"You using the voice styles of '{brand_voice}'. Write a post up to 3 sentences long on `{topic}`."
                    }]

        self.last_prompt = quote_prompt
        self.last_response = self._openai.ChatCompletion.create(
            model=self._model,
            messages=quote_prompt)["choices"][0]["message"]["content"]

        return self.last_response, self.last_prompt[0]["content"]


    # Generate insight for a quote
    def generate_headings(self, content_info: str, keywords: str):
        if keywords != "":
            headings_prompt = [
                {"role": "user",
                "content": f"Provide headings for a blog post on '{content_info}, aiming to include as many {keywords} as you can.'"
                }]
        else:
            headings_prompt = [
                {"role": "user",
                "content": f"Provide headings for a blog post on '{content_info}.'"
                }]

        self.last_prompt = headings_prompt
        self.last_response_insight = self._openai.ChatCompletion.create(
            model=self._model,
            messages=self.last_prompt)["choices"][0]["message"]["content"]

        return self.last_response, self.last_prompt[0]["content"]

    # Generate insight for a quote
    def reword_response(self, input_prompt, keyword_list, new_length, additional_prompt):
        if keyword_list != "":
            keyword_list = f"Include the keywords '{keyword_list}'."

        if new_length != "":
            new_length = f"The response needs to be {new_length} sentences long."

        self.last_prompt = [
            {"role": "user",
            "content": f"Rephrase the following '{input_prompt}' with the following criteria. {keyword_list} {new_length} {additional_prompt}'."
            }]

        self.last_response = self._openai.ChatCompletion.create(
            model=self._model,
            messages=self.last_prompt)["choices"][0]["message"]["content"]

        return self.last_response, self.last_prompt[0]["content"]

    # Make a chat request
    def answer_question(self, question: str, keywords: str, brand_voice: str, length_response):
        if keywords != "":
            quote_prompt = [
                {"role": "user","content": f" In `{length_response}`, answer `{question}?` using the voice of '{brand_voice}' while using the as many of the following words as you can '{keywords}'."
                }]
        else:
            quote_prompt = [
                {"role": "user","content": f" In `{length_response}`, answer `{question}?` using the voice of '{brand_voice}'."
                }]
       
        self.last_prompt = quote_prompt
        self.last_response = self._openai.ChatCompletion.create(
            model=self._model,
            messages=quote_prompt)["choices"][0]["message"]["content"]

        return self.last_response, self.last_prompt[0]["content"]
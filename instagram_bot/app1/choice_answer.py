import openai
class text_with_gpt():
    def __init__(self, prompt):
        self.prompt = prompt
        self.model = "text-davinci-003"
        self.max_tokens = 200   
        self.top_p = 1
        self.frequency_penalty = 0
        self.presence_penalty = 0.6
        #self.stop = None,
        self.temperature = 0.9


    def get_response(self):
        response = openai.Completion.create(
            engine=self.model,
            prompt=self.prompt,
            max_tokens=self.max_tokens,
            top_p=self.top_p,
            frequency_penalty=self.frequency_penalty,
            presence_penalty=self.presence_penalty,
            #stop=self.stop,
            temperature=self.temperature,
        )
        return response.choices[0].text.strip()
    

class text():
    def __init__(self, prompt):
        self.prompt = prompt

    def get_response(self):
        prepared_text = self.prompt
        return prepared_text
    

model_map = {
    'text_with_gpt':text_with_gpt,
    'text':text
}
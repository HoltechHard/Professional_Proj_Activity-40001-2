from langchain_ollama import ChatOllama
from langchain_core.prompts import PromptTemplate

class WebSummarizer:
    def __init__(self):
        self.llm = ChatOllama(
            model = "deepseek-r1:1.5b",
            base_url = "http://localhost:11434",
            temperature = 0.3,
            max_tokens = 200
        )

        self.prompt_template =  """
                You are an AI assistant that is tasked with summarizing a web page.
                Your summary should be detailed and cover all key points mentioned in the web page.
                Below is the extracted content of the web page:
                {content}

                Please provide a comprehensive and detailed summary in Markdown format.
            """
        
    def summarize(self, content):
        summary_prompt = PromptTemplate(template = self.prompt_template, input_variables = ["content"])
        prompt_text = summary_prompt.format(content = content)
        messages = [{
            "role": "user",
            "content": prompt_text
        }]

        response = self.llm.invoke(messages)
        return response.content

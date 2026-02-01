import ollama

class AIService:
    @staticmethod
    def generate_response(prompt: str, model: str = 'llama3.2') -> str:
        """
        Responsibility: Execute the local LLM call and return the raw string.
        """
        response = ollama.generate(
            model=model, 
            prompt=prompt
        )
        return response['response']
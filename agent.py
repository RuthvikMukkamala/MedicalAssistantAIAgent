from langchain_openai import ChatOpenAI
from browser_use.agent.service import Agent
from browser_use.controller.service import Controller

controller = Controller()

@controller.action('Ask user for information')
def ask_human(question: str, display_question: bool) -> str:
    return input(f'\n{question}\nInput: ')

def create_prompt(city: str, state: str, country: str, medical_need: str) -> str:
    return f"""
    I want to find a {medical_need} doctor that lives close to {city}, {state}, {country}.
    Please return the best three options available.
    """

class MedicalAssistantAIAgent:
    def __init__(self, model_name: str = "gpt-4o"):
        self.model_name = model_name
        self.llm = ChatOpenAI(model=self.model_name)

    async def find_medical_provider(self, city: str, state: str, country: str, medical_need: str) -> str:
        prompt = create_prompt(city, state, country, medical_need)
        agent = Agent(
            task=prompt,
            llm=self.llm,
        )
        try:
            result = await agent.run()
            return result
        except Exception as e:
            return f"An error occurred: {e}"

    async def interactive_session(self):
        print("Medical Assistant: Find the highest rated doctor for your needs!")

        city = ask_human("Please enter the city:", True)
        state = ask_human("Please enter the state:", True)
        country = ask_human("Please enter the country:", True)
        medical_need = ask_human("What is your medical need? (e.g., LASIK)", True)

        print("\nFetching the best three options for you...")
        result = await self.find_medical_provider(city, state, country, medical_need)
        print("\nResult:")
        print(result)

if __name__ == "__main__":
    import asyncio

    agent = MedicalAssistantAIAgent()
    asyncio.run(agent.interactive_session())
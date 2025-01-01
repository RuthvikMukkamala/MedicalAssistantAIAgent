import asyncio
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

def extract_content(result):
    if result.all_results and result.all_results[0].is_done:
        return result.all_results[0].extracted_content
    else:
        return "Failed to retrieve results or no valid results found."

def display_result(result):
    content = extract_content(result)
    print("\n--- Recommended Doctors ---\n")
    if "failed" in content.lower():
        print("An error occurred while processing your request:")
    print(content)

class ParallelMedicalAssistantAIAgent:
    def __init__(self, model_name: str = "gpt-4o"):
        self.model_name = model_name
        self.llm = ChatOpenAI(model=self.model_name)

    async def validate_location(self, city: str, state: str, country: str):
        prompt = f"Validate the location: {city}, {state}, {country}."
        agent = Agent(task=prompt, llm=self.llm)
        try:
            return await agent.run()
        except Exception as e:
            return f"Location validation failed: {e}"

    async def find_doctors(self, city: str, state: str, country: str, medical_need: str):
        prompt = create_prompt(city, state, country, medical_need)
        agent = Agent(task=prompt, llm=self.llm)
        try:
            return await agent.run()
        except Exception as e:
            return f"Doctor search failed: {e}"

    async def filter_results(self, doctors):
        prompt = f"Filter the following doctor results to find the top three highly rated options: {doctors}"
        agent = Agent(task=prompt, llm=self.llm)
        try:
            return await agent.run()
        except Exception as e:
            return f"Filtering failed: {e}"

    async def find_medical_provider_parallel(self, city: str, state: str, country: str, medical_need: str):
        validate_task = self.validate_location(city, state, country)
        find_doctors_task = self.find_doctors(city, state, country, medical_need)

        validation_result, doctors_result = await asyncio.gather(validate_task, find_doctors_task)

        if isinstance(validation_result, str) and "failed" in validation_result.lower():
            return validation_result

        if isinstance(doctors_result, str) and "failed" in doctors_result.lower():
            return doctors_result

        return await self.filter_results(doctors_result)

    async def interactive_session(self):
        print("Medical Assistant: Find the highest rated doctors for your needs!")

        city = ask_human("Please enter the city:", True)
        state = ask_human("Please enter the state:", True)
        country = ask_human("Please enter the country:", True)
        medical_need = ask_human("What is your medical need? (e.g., LASIK)", True)

        print("\nFetching the best three options for you...")
        result = await self.find_medical_provider_parallel(city, state, country, medical_need)
        # display_result(result)

if __name__ == "__main__":
    agent = ParallelMedicalAssistantAIAgent()
    asyncio.run(agent.interactive_session())

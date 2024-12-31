from langchain_openai import ChatOpenAI
from browser_use.agent.service import Agent
from browser_use.browser.service import Browser
from browser_use.controller.service import Controller

controller = Controller()

@controller.action('Ask user for information')
def ask_human(question: str, display_question: bool) -> str:
    return input(f'\n{question}\nInput: ')

def create_prompt(city, state, country, medical_need, insurance_provider):
    return f"""
    I want to find a {medical_need} doctor that lives close to {city}, {state}, {country}. 
    I have {insurance_provider} as my insur›ance provider. Return me the best option.
    """

async def chat_interface():
    print("Welcome to the Medical Finder Chat!")

    city = ask_human("Please enter the city:", True)
    state = ask_human("Please enter the state:", True)
    country = ask_human("Please enter the country:", True)
    medical_need = ask_human("What is your medical need? (e.g., LASIK)", True)
    insurance_provider = ask_human("What is your insurance provider?", True)
    prompt = create_prompt(city, state, country, medical_need, insurance_provider)
    agent = Agent(
        task=prompt,
        llm=ChatOpenAI(model="gpt-4o"),
    )
    print("\nFetching the best option for you...")
    result = await agent.run()
    print("\nResult:")
    print(result)

if __name__ == "__main__":
    import asyncio
    asyncio.run(chat_interface())

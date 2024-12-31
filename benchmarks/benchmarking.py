import time
import asyncio
import pandas as pd
import matplotlib.pyplot as plt
from langchain_openai import ChatOpenAI
from browser_use.agent.service import Agent, AgentHistory

def create_prompt(city, state, country, medical_need):
    return f"""
    I want to find a {medical_need} doctor that lives close to {city}, {state}, {country}. Return me the best option.
    """

async def run_benchmark(test_cases):
    results = []

    for test in test_cases:
        city = test['city']
        state = test['state']
        country = test['country']
        medical_need = test['medical_need']

        prompt = create_prompt(city, state, country, medical_need)

        agent = Agent(
            task=prompt,
            llm=ChatOpenAI(model="gpt-4o"),
        )

        start_time = time.time()
        history: list[AgentHistory] = await agent.run()
        end_time = time.time()

        elapsed_time = end_time - start_time

        results.append({
            "test_case": f"{city}, {state}, {country} ({medical_need})",
            "history": history,
            "time_taken": elapsed_time
        })

    return results

async def evaluate_results(results):
    data = []

    for res in results:
        data.append({
            "Test Case": res['test_case'],
            "Time Taken (s)": res['time_taken'],
        })

    df = pd.DataFrame(data)

    print(df)

    plt.figure(figsize=(10, 6))
    plt.bar(df["Test Case"], df["Time Taken (s)"])
    plt.xlabel("Test Cases")
    plt.ylabel("Time Taken (seconds)")
    plt.title("Benchmark Results")
    plt.xticks(rotation=45, ha="right")
    plt.tight_layout()
    plt.show()

async def main():
    test_cases = [
        {"city": "Princeton", "state": "New Jersey", "country": "United States", "medical_need": "LASIK"},
        {"city": "New York", "state": "New York", "country": "United States", "medical_need": "Orthodontics"},
        {"city": "San Francisco", "state": "California", "country": "United States", "medical_need": "Dermatology"},
    ]

    results = await run_benchmark(test_cases)
    await evaluate_results(results)
    print(results)


if __name__ == "__main__":
    loop = asyncio.get_event_loop()
    if loop.is_running():
        asyncio.ensure_future(main())
    else:
        asyncio.run(main())


import asyncio
import pandas as pd
import matplotlib.pyplot as plt
from typing import List, Dict, Any
from dataclasses import dataclass
from browser_use.agent.service import Agent
from langchain_openai import ChatOpenAI
from langchain_anthropic import ChatAnthropic
import logging

logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)

@dataclass
class TestCase:
    city: str
    state: str
    country: str
    medical_need: str

    def __str__(self) -> str:
        return f"{self.city}, {self.state}, {self.country} ({self.medical_need})"

class BenchmarkRunner:
    def __init__(self, test_cases: List[Dict[str, str]], model_name: str = "gpt-4o"):
        self.test_cases = [TestCase(**case) for case in test_cases]
        self.model_name = model_name
        self.results = []
        self.llm = self.get_model_instance(model_name)

    def get_model_instance(self, model_name: str):

        if model_name.startswith("gpt"):
            logging.info(f"Using OpenAI model: {model_name}")
            return ChatOpenAI(model=model_name)

        elif model_name.startswith("claude"):

            logging.info(f"Using Anthropic model: {model_name}")
            return ChatAnthropic(model=model_name)
            
        else:
            raise ValueError(f"Unsupported model name: {model_name}")

    def create_prompt(self, test_case: TestCase) -> str:
        return f"Find the best three {test_case.medical_need} doctors near {test_case.city}, {test_case.state}, {test_case.country}."

    async def run_single_test(self, test_case: TestCase) -> Dict[str, Any]:
        prompt = self.create_prompt(test_case)
        agent = Agent(task=prompt, llm=self.llm)

        try:
            start_time = asyncio.get_event_loop().time()
            history = await agent.run()
            elapsed_time = asyncio.get_event_loop().time() - start_time

            return {
                "test_case": str(test_case),
                "history": history,
                "time_taken": elapsed_time,
                "status": "success"
            }
        except Exception as e:
            logging.error(f"Error running test case {test_case}: {str(e)}")
            return {
                "test_case": str(test_case),
                "history": [],
                "time_taken": 0,
                "status": "failed",
                "error": str(e)
            }

    async def run_benchmark(self) -> List[Dict[str, Any]]:
        tasks = [self.run_single_test(test_case) for test_case in self.test_cases]
        self.results = await asyncio.gather(*tasks)
        return self.results

    def visualize_results(self):
        if not self.results:
            logging.warning("No results to visualize.")
            return

        df = pd.DataFrame([
            {
                "Test Case": r["test_case"],
                "Time Taken (s)": r["time_taken"],
                "Status": r["status"]
            }
            for r in self.results
        ])

        if df.empty:
            logging.warning("No results to display.")
            return

        print("\n--- Benchmark Results ---")
        print(df.to_string(index=False))

async def main():
    test_cases = [
        {"city": "Princeton", "state": "New Jersey", "country": "United States", "medical_need": "LASIK"},
        {"city": "New York", "state": "New York", "country": "United States", "medical_need": "Orthodontics"},
        {"city": "San Francisco", "state": "California", "country": "United States", "medical_need": "Dermatology"},
    ]

    logging.info("Starting benchmark run with OpenAI model 'gpt-4o'...")
    runner_gpt = BenchmarkRunner(test_cases, model_name="gpt-4o")
    results_gpt = await runner_gpt.run_benchmark()
    logging.info("Benchmark run with OpenAI model 'gpt-4o' completed.")
    runner_gpt.visualize_results()

    logging.info("Starting benchmark run with Anthropic model 'claude-3-5-sonnet-20240620'...")
    runner_claude = BenchmarkRunner(test_cases, model_name="claude-3-5-sonnet-20240620")
    results_claude = await runner_claude.run_benchmark()
    logging.info("Benchmark run with Anthropic model 'claude-3-5-sonnet-20240620' completed.")
    runner_claude.visualize_results()

if __name__ == "__main__":
    asyncio.run(main())

import asyncio
import pandas as pd
import matplotlib.pyplot as plt
from typing import List, Dict, Any
from dataclasses import dataclass
from browser_use.agent.service import Agent
from langchain_openai import ChatOpenAI
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
        self.llm = ChatOpenAI(model=model_name)

    def create_prompt(self, test_case: TestCase) -> str:
        return f"Find a {test_case.medical_need} doctor near {test_case.city}, {test_case.state}, {test_case.country}."

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

        df_success = df[df["Status"] == "success"]
        if df_success.empty:
            logging.warning("No successful test cases to visualize.")
            return

        plt.figure(figsize=(10, 6))
        plt.bar(df_success["Test Case"], df_success["Time Taken (s)"])
        plt.title("Benchmark Results")
        plt.xlabel("Test Cases")
        plt.ylabel("Time (seconds)")
        plt.xticks(rotation=45, ha="right")
        plt.tight_layout()

async def main():
    test_cases = [
        {"city": "Princeton", "state": "New Jersey", "country": "United States", "medical_need": "LASIK"},
        {"city": "New York", "state": "New York", "country": "United States", "medical_need": "Orthodontics"},
        {"city": "San Francisco", "state": "California", "country": "United States", "medical_need": "Dermatology"},
    ]
    
    runner = BenchmarkRunner(test_cases)
    
    logging.info("Starting benchmark run...")
    results = await runner.run_benchmark()
    
    runner.visualize_results()
    plt.show()
    
    df_results = pd.DataFrame([
        {
            "Test Case": r["test_case"],
            "Time (s)": round(r["time_taken"], 2),
            "Status": r["status"]
        }
        for r in results
    ])
    
    print("\nBenchmark Summary:")
    print(df_results)

if __name__ == "__main__":
    asyncio.run(main())

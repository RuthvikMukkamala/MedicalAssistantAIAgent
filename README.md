# MedicalAssistantAIAgent


For the project, we hope to build an agent to find the best doctor given some geographic restrictions and the medical requirement (ex. LASIK surgery, dentists, etc). 


To interpret the best standard for the performance of a medical assistant AI agent, we
check if the AI is able to provide the "highest rated" doctor per our criteria. Since, "the best" doctor is difficult to determine, we choose the highest rated based in Google. 

How can we improve the quantifiable measure of being the best doctor for our client? We can select the doctor that is covered through our insurance provider, in close proximity to our client, years of experience, etc. As the project progresses, we hope to add more complexity variables such as doctors that accept a specific insurance provider, and the number of doctors to return to user so they can correctly assess who to choose from. However, as we will find from benchmarks and testing that certain complexity variables may not achieve the results we desire. Simple is better in many cases, and we can leverge simplicity within the model. 


For the AI Agent architecture, we use Browser-Use to help with interacting with the browser and implementing the desired model.




## Project Set-Up

1. Clone the repository:
   ```bash
   git clone https://github.com/your-username/MedicalAssistantAIAgent.git
   cd MedicalAssistantAIAgent

        ```python
        python -m venv env
        source env/bin/activate  # On Windows, use `env\Scripts\activate`
        pip install -r requirements.txt

To run the main agent:

python agent.py


To run the parallelized agent:

python parallel_agent.py






Agentic Architecture:


Using Anthropic's guide to model building, I realized the most optimal workflow would have parallel agents that build upon the context of the prompt - especially if we want to build a prompt that includes more complex variable patterns. 


Included in the workflow is the basic agent in agent.py, and the parallel workflow in the parallel_agent.py. The benchmarks are presented below using the same test cases. 



Architecture Details:

1) Parallelization
2) 









Benchmarking:


We had three test cases that we passed to the AI Agent: 

test_cases = [
        {"city": "Princeton", "state": "New Jersey", "country": "United States", "medical_need": "LASIK"},
        {"city": "New York", "state": "New York", "country": "United States", "medical_need": "Orthodontics"},
        {"city": "San Francisco", "state": "California", "country": "United States", "medical_need": "Dermatology"},
    ]

We run this with GPT-4o (Free) and Claude. We find how long the model takes to complete each task and present the data in a visual format. Based on this information, we extend the task to run a parallel agent architecture to break down LLM tasks to attempt the performance of the model. 


Benchmark Presentation:






Video Presentation:








Oservations and notes about the agents performance throughout the iteration and development

    1. Where is the agent performant?
The agent is perfomant given strict geographic locations and a precise medical requirement i.e the prompt is flush with information for the agent to precisely act upon. This can be judged through 

    2. Where does it struggle?
The agent struggles with typos in the input string, as well as asking for a large magnitude of output (> 5 doctors for example). This is because the web scrolling of the Browser-Use is limited, and the model is lazy - once it completes a goal it will submit. 

    3. Do certain LLMs perform better with this task?



    4. How would you improve the agent in the future?





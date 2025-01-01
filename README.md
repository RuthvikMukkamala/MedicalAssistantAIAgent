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

2. Run the code

   ```python
   python -m venv env
   source env/bin/activate  # On Windows, use `env\Scripts\activate`
   pip install -r requirements.txt

3. Create a .env file in the root directory
   ```bash
   OPENAI_API_KEY=
   ANTHROPIC_API_KEY=

5. To run the main agent:

   ```python
   python agent.py


6. To run the parallelized agent:
   
   ```python
   python parallel_agent.py

7. To run the benchmarks:
   
   ```python
   python benchmarks/benchmarking.py


Agentic Architecture:


Using Anthropic's guide to model building, I realized the most optimal workflow would have parallel agents that build upon the context of the prompt - especially if we want to build a prompt that includes more complex variable patterns. 


Included in the workflow is the basic agent in agent.py, and the parallel workflow in the parallel_agent.py. The benchmarks are presented below using the same test cases. 



Architecture Details:

1) Parallelization (breakdown the location, doctor, and result filtering into different LLM prompts)
2) Optimize the precision of the prompts
3) Use different LLMs (in this case GPT and Claude)
4) The code was implemented into three files, agent.py, parallel_agent.py, and benchmarks/benchmarking.py





Benchmarking:


1) We had three test cases that we passed to the AI Agent: 

   ```python
   test_cases = [
           {"city": "Princeton", "state": "New Jersey", "country": "United States", "medical_need": "LASIK"},
           {"city": "New York", "state": "New York", "country": "United States", "medical_need": "Orthodontics"},
           {"city": "San Francisco", "state": "California", "country": "United States", "medical_need": "Dermatology"},
       ]


2) We run this with GPT-4o (Free) and Claude. We find how long the model takes to complete each task and present the data in a visual format. Based on this information, we extend the task to run a parallel agent architecture to break down LLM tasks to attempt the performance of the model. 


3) Benchmark Presentation:

Broken down into Task Completion Time and Quality of Results (> 4.8 average rating w/ over atleast 10 ratings)

Here are the results of the GPT-4o model with the Task Completion Time
<img width="986" alt="Screenshot 2024-12-31 at 5 20 24 PM" src="https://github.com/user-attachments/assets/837d3de1-dbbf-4794-b177-f430ddded801" />


Here are the results of Claude's Task Completion Time
<img width="762" alt="Screenshot 2025-01-01 at 12 09 16 AM" src="https://github.com/user-attachments/assets/b9bd9093-840e-4aa9-ba9b-7ce32a76325b" />


Here are the Quality of Results of the GPT-4o model (looking for average rating and institutions)

<img width="659" alt="Screenshot 2025-01-01 at 9 14 13 AM" src="https://github.com/user-attachments/assets/572bb6a8-1a1e-4340-957a-8d90836d5958" />


Here are the Quality of Results of Claude 3.5 (looking for average rating and institutions)


<img width="764" alt="Screenshot 2025-01-01 at 12 10 00 AM" src="https://github.com/user-attachments/assets/0741a189-4f35-4d54-9ed5-bf78ec458bde" />



Observations from Benchmarks: 

We notice that GPT-4o takes less time to complete the task, with the average rating (from the Google API + web browsing) is approximately 4.8 - 5 stars. The drawback is that the model chooses doctors from the same medical institution. 
For Claude, we notice that the model takes more time (approx. 3x times) to complete the task, with the average rating (from the Google API + web browsing) is also approximately 4.8 - 5 stars. The benefit from Claude however is that the model chooses doctors from the a diverse group of medical institutions providing a higher quality of results. When testing a simple agentic workflow (LLM Prompt --> Web) achieves similar results in the benchmarking with the parallelized architecture i.e same ratings and same institutions. As we build more complexity into the agent workflow however (adding more client restrictions), the parallelized architecture poses to have better quality of results due to filtering based on a group of subtasks. 





Oservations and notes about the agents performance throughout the iteration and development

    1. Where is the agent performant?
The agent is perfomant given strict geographic locations and a precise medical requirement i.e the prompt is flush with information for the agent to precisely act upon. This can be judged through the benchmarking shown above. 

    2. Where does it struggle?
The agent struggles with typos in the input string, as well as asking for a large magnitude of output (> 5 doctors for example). This is because the web scrolling of the Browser-Use is limited, and the model is lazy - once it completes a goal it will submit. 

    3. Do certain LLMs perform better with this task?
To get better results, we can use a more token heavy model such as Claude 3.5 over GPT-4o for result improvement - meaning the quality of the results with higher average rating and a larger distribution over medical institutions. 


    4. How would you improve the agent in the future?
I would implement a typo correction for user inputs so the parallelized model does not get stuck on incorrect geographics for example. Furthermore, build onto the model complexity by adding insurance, years of experience, and distance from client, 
and finally improve the "retry" mechanism of continuing till a proper distribution of results is achieved. 




# MedicalAssistantAIAgent


For the project, we hope to build an agent to find the best doctor given some geographic restrictions and the medical requirement (ex. LASIK surgery, dentists, etc). 


To interpret the best standard for the performance of a medical assistant AI agent, we
check if the AI is able to provide the "highest rated" doctor per our criteria. Since, "the best" doctor is difficult to determine, we choose the highest rated based in Google. 

How can we improve the quantifiable measure of being the best doctor for our client? We can select the doctor that is covered through our insurance provider, in close proximity to our client, years of experience, etc. As the project progresses, we hope to add more complexity variables such as doctors that accept a specific insurance provider, and the number of doctors to return to user so they can correctly assess who to choose from. However, as we will find from benchmarks and testing that certain complexity variables may not achieve the results we desire. Simple is better in many cases, and we can leverge simplicity within the model. 


For the AI Agent architecture, we use Browser-Use to help with interacting with the 
browser and implementing the desired model. We also extend the project with Magentic-One as a multi-modal agent to read the desired 




Project Set-Up: 







Agentic Architecture:







Benchmarking:


We had three test cases that we passed to the AI Agent: 

test_cases = [
        {"city": "Princeton", "state": "New Jersey", "country": "United States", "medical_need": "LASIK"},
        {"city": "New York", "state": "New York", "country": "United States", "medical_need": "Orthodontics"},
        {"city": "San Francisco", "state": "California", "country": "United States", "medical_need": "Dermatology"},
    ]

We run this with GPT-4o, Claude, and Gemini. We find how long the model takes to complete each task and present the data in a visual format. Based on this information, we extend the task to run a parallel agent architecture to break down LLM tasks to attempt the performance of the model. 


Benchmark Presentation:






Video Presentation:






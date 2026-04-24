import os
from dotenv import load_dotenv
from crewai import Agent, Task, Crew, LLM
from crewai_tools import FileReadTool
import yaml
from IPython.display import Markdown, display

# Load environment variables from the .env file at project root.
# Uncomment if tracing enabeld or Options B (Gemini) is used.
#load_dotenv()

FILE_PATH = 'inputs/messy_agenda.txt'

# LLM Setup (GitHub Models / Gemini Backup)

#Option A: GitHub (Default)
def create_llm(temperature):
    return LLM(
        model="github/gpt-4o-mini",
        temperature=temperature,
        api_key=os.environ.get("GITHUB_TOKEN")
    )

# Option B: Gemini (Backup)
# To switch, just comment (CTRL + /) out Option A and uncomment these lines (CTRL + /):

# def create_llm(temperature):
#     return LLM(
#         model="gemini-flash-latest",
#         temperature=temperature,
#         api_key=os.environ.get("GEMINI_API_KEY")
#     )

# Read input file
file_tool = FileReadTool(file_path=FILE_PATH)

# Load Agents Config & Build Agents
with open('configs/agents.yaml', 'r') as f:
    agents_config = yaml.safe_load(f)

analyzer_agent = Agent(config=agents_config['analyzer_agent'], tools=[file_tool], llm=create_llm(agents_config['analyzer_agent']['temperature']))
scheduler_agent = Agent(config=agents_config['scheduler_agent'], llm=create_llm(agents_config['scheduler_agent']['temperature']))
funky_agent = Agent(config=agents_config['funky_agent'], llm=create_llm(agents_config['funky_agent']['temperature']))
#custom_agent = Agent(config=agents_config['custom_agent'], llm=create_llm(agents_config['custom_agent']['temperature'])) 

# Load Tasks Config & Build Tasks
with open('configs/tasks.yaml', 'r') as f:
    tasks_config = yaml.safe_load(f)

agent_map = {
    'analyzer_agent': analyzer_agent,
    'scheduler_agent': scheduler_agent,
    'funky_agent': funky_agent
    #'custom_agent': custom_agent
}

# Build sequential tasks based on the config
tasks = []
for task_name, task_config in tasks_config.items():
    task_kwargs = {
        'description': task_config['description'].format(FILE_PATH=FILE_PATH),
        'expected_output': task_config['expected_output'],
        'agent': agent_map[task_config['agent']]
    }
    if 'output_file' in task_config:
        task_kwargs['output_file'] = task_config['output_file']
    task = Task(**task_kwargs)
    tasks.append(task)



# Run the crew
# Add verbose=True to the Crew constructor to see detailed logs of each agent's actions and thoughts in the console.
crew = Crew(agents=[analyzer_agent, scheduler_agent, funky_agent], tasks=tasks)
result = crew.kickoff()

# Display results
print("--- output saved to outputs/final_schedule.md ---")
# print(str(result))
# In notebook environments this will render nicely:
display(Markdown(str(result)))

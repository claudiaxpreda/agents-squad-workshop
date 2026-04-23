import os
from crewai import Agent, Task, Crew, LLM
from crewai_tools import FileReadTool
import yaml
from IPython.display import Markdown, display

# 1. SETUP: Student tweaks these!
FILE_PATH = 'inputs/messy_agenda.txt'

# 2. LLM Setup (GitHub Models / Gemini Backup)
# Agents now use individual temperatures from their config
# Defaults to GitHub, can be swapped easily

# Option A: GitHub (Default)
def create_llm(temperature):
    return LLM(
        model="github/gpt-4o-mini",
        temperature=temperature,
        api_key=os.environ.get("GITHUB_TOKEN")
    )

# Option B: Gemini (Backup)
# To switch, just comment out Option A and uncomment these lines:
# def create_llm(temperature):
#     return LLM(
#         model="gemini/gemini-1.5-flash",
#         temperature=temperature,
#         api_key=os.environ.get("GEMINI_API_KEY")
#     )

# 3. TOOL: Ability to read the student's file
file_tool = FileReadTool(file_path=FILE_PATH)

# 4. LOAD CONFIG & BUILD AGENTS
with open('configs/agents.yaml', 'r') as f:
    agents_config = yaml.safe_load(f)

intake_agent = Agent(config=agents_config['intake_agent'], tools=[file_tool], llm=create_llm(agents_config['intake_agent']['temperature']))
scheduler_agent = Agent(config=agents_config['scheduler_agent'], llm=create_llm(agents_config['scheduler_agent']['temperature']))
funky_agent = Agent(config=agents_config['funky_agent'], llm=create_llm(agents_config['funky_agent']['temperature']))

# 5. LOAD TASKS CONFIG & BUILD TASKS
with open('configs/tasks.yaml', 'r') as f:
    tasks_config = yaml.safe_load(f)

agent_map = {
    'intake_agent': intake_agent,
    'scheduler_agent': scheduler_agent,
    'funky_agent': funky_agent
}

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



# 6. RUN THE CREW
crew = Crew(agents=[intake_agent, scheduler_agent, funky_agent], tasks=tasks)
result = crew.kickoff()

# 7. VISUAL EXPERIENCE: Render the output
print("--- RAW OUTPUT SAVED TO final_schedule.md ---")
display(Markdown(str(result)))

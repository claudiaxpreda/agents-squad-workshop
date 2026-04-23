from crewai.flow.flow import Flow, start, listen

class PlannerFlow(Flow):
    @start()
    def extract_notes(self):
        # Logic to trigger Intake Agent
        return "Notes Processed"

    @listen(extract_notes)
    def create_calendar(self):
        # Logic to trigger Scheduler Agent
        return "Final Schedule Ready"

# 1. Generate the map
flow = PlannerFlow()
flow.plot("my_agent_blueprint") # This creates 'my_agent_blueprint.html'

# 2. Display it in the Workspace
from IPython.display import IFrame
IFrame(src='my_agent_blueprint.html', width=700, height=500)

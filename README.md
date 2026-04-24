# Agents Squad Workshop

This repository demonstrates a simple multi-agent workflow using the `crewai` library.

The project reads a messy agenda from `inputs/messy_agenda.txt`, runs a set of configured agents to extract events, create a clean schedule, and then transform that schedule into a final, motivational markdown output.

## Project structure

- `main.py` - Main orchestrator script that loads agent and task configuration, builds agents, and runs the workflow.
- `configs/agents.yaml` - Agent definitions and behavior settings.
- `configs/tasks.yaml` - Task pipeline definitions and output targets.
- `blueprints/flow_diagram.md` - A diagram file showing the task flow in Mermaid format for dark-friendly viewing.
- `inputs/messy_agenda.txt` - Raw agenda input used by the intake agent.
- `outputs/intermediate_schedule.md` - Generated schedule produced by the scheduler agent.
- `outputs/final_schedule.md` - Final schedule with motivational and astral-style enhancements.

## Diagram details

- `blueprints/flow_diagram.md` contains a Mermaid diagram showing the task flow for the schedule workflow.
- It is an illustrative visualization of the intake, scheduler, and funky agents working together.
- The diagram is separate from the main `Crew`-based task execution in `main.py`.

## Prerequisites

- Python 3.10+ or compatible Python environment
- Access to the required AI model API credentials in environment variables (for example `GITHUB_TOKEN` or `GEMINI_API_KEY` depending on the chosen model)
- Optionally, a `.env` file in the project root for local environment variables

## Install

```bash
pip install -r requirements.txt
```

## Run

```bash
python main.py
```

The script will run the configured agents and print the result. The final output is also saved to `outputs/final_schedule.md`.

## Previewing markdown files

- Open `outputs/intermediate_schedule.md` or `outputs/final_schedule.md` in VS Code.
- Use the editor action **Open Preview** or press `Ctrl+Shift+V` to view the rendered Markdown.
- You can also use **Open Preview to the Side** (`Ctrl+K V`) for side-by-side editing and preview.

## Notes

- By default, `main.py` uses the GitHub model configuration defined in `create_llm()`.
- If you want to use a different model, swap the commented Gemini block in `main.py` and provide the corresponding API key.
- The agent/task pipeline is sequential: the intake agent extracts events first, the scheduler agent creates the schedule next, and the funky agent adds the final styling.

import datetime

from aris_engines.aris_research_agent import research_query
from aris_planner_agent import planner_agent
from aris_engines.aris_creation_agent import creation_agent
from aris_analyzer_agent import analyzer_agent
from aris_brain import ask_ai


def executor_agent(task):

    print("Executing task:", task)

    task_text = task.lower()

    # AGENT SELECTION
    if "research" in task_text:
        result = research_agent(task)

    elif "plan" in task_text or "strategy" in task_text:
        result = planner_agent(task)

    elif "create" in task_text or "generate" in task_text:
        result = creation_agent(task)

    elif "analyze" in task_text:
        result = analyzer_agent(task)

    else:
        result = ask_ai(task)

    report = f"""
ARIS EXECUTION REPORT
Time: {datetime.datetime.now()}

Task:
{task}

Result:
{result}

Status: COMPLETED
"""

    return report
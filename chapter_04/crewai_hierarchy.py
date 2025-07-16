from textwrap import dedent

import agentops
from crewai import Agent, Crew, Process, Task
from dotenv import load_dotenv
from langchain_openai import ChatOpenAI
from pydantic import SecretStr

load_dotenv()

import os
os.environ["OPENAI_API_KEY"] = os.getenv("OPENAI_API_KEY", "").replace("\n", "").strip()
os.environ["GROK_API_KEY"] = os.getenv("GROK_API_KEY", "").replace("\n", "").strip()

import argparse
import sys

# Parse command-line arguments
parser = argparse.ArgumentParser(description="Game Crew Script")

# Mutually exclusive group for LLM provider
group = parser.add_mutually_exclusive_group()
group.add_argument("--grok", action="store_true", help="Use Grok API instead of OpenAI")
group.add_argument("--openai", action="store_true", help="Use OpenAI (default)")

args = parser.parse_args()

if args.grok:
    llm_provider = "grok"
else:
    llm_provider = "openai"

agentops.init()

print("## Welcome to the Game Crew")
print("-------------------------------")
game = input("What is the game you would like to build? What will be the mechanics?\n")


senior_engineer_agent = Agent(
    role="Senior Software Engineer",
    goal="Create software as needed",
    backstory=dedent(
        """
        You are a Senior Software Engineer at a leading tech think tank.
        Your expertise in programming in python. and do your best to
        produce perfect code
        """
    ),
    allow_delegation=False,
    verbose=True,
)

qa_engineer_agent = Agent(
    role="Software Quality Control Engineer",
    goal="create prefect code, by analizing the code that is given for errors",
    backstory=dedent(
        """
        You are a software engineer that specializes in checking code
        for errors. You have an eye for detail and a knack for finding
        hidden bugs.
        You check for missing imports, variable declarations, mismatched
        brackets and syntax errors.
        You also check for security vulnerabilities, and logic errors
        """
    ),
    allow_delegation=False,
    verbose=True,
)

chief_qa_engineer_agent = Agent(
    role="Chief Software Quality Control Engineer",
    goal="Ensure that the code does the job that it is supposed to do",
    backstory=dedent(
        """
        You are a Chief Software Quality Control Engineer at a leading
        tech think tank. You are responsible for ensuring that the code
        that is written does the job that it is supposed to do.
        You are responsible for checking the code for errors and ensuring
        that it is of the highest quality.
        """
    ),
    allow_delegation=True,
    verbose=True,
)

code_task = Task(
    description=f"""You will create a game using python, these are the instructions:
        Instructions
        ------------
        {game}        
        You will write the code for the game using python.""",
    expected_output="Your Final answer must be the full python code, only the python code and nothing else.",
    agent=senior_engineer_agent,
)

qa_task = Task(
    description=f"""You are helping create a game using python, these are the instructions:
        Instructions
        ------------
        {game}
        Using the code you got, check for errors. Check for logic errors,
        syntax errors, missing imports, variable declarations, mismatched brackets,
        and security vulnerabilities.""",
    expected_output="Output a list of issues you found in the code.",
    agent=qa_engineer_agent,
)

evaluate_task = Task(
    description=f"""You are helping create a game using python, these are the instructions:
        Instructions
        ------------
        {game}
        You will look over the code to insure that it is complete and
        does the job that it is supposed to do. """,
    expected_output="Your Final answer must be the corrected a full python code, only the python code and nothing else.",
    agent=chief_qa_engineer_agent,
)

if llm_provider == "openai":
    manager_llm = ChatOpenAI(temperature=0, model="gpt-4o")
else:
    manager_llm = ChatOpenAI(
        temperature=0,
        model="grok-4-0709",
        base_url="https://api.x.ai/v1",
        api_key=SecretStr(value) if (value := os.getenv("GROK_API_KEY")) else None
    )

# Instantiate your crew with a sequential process
crew = Crew(
    agents=[senior_engineer_agent, qa_engineer_agent, chief_qa_engineer_agent],
    tasks=[code_task, qa_task, evaluate_task],
    verbose=True,
    process=Process.hierarchical,
    manager_llm=manager_llm,  # Mandatory: Use a language model for manager
)

# Get your crew to work!
result = crew.kickoff()

print("######################")
print(result)

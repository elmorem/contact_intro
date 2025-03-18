import os
from dotenv import load_dotenv


from langchain import hub
from langchain.agents import (
    create_react_agent,
    AgentExecutor,
)
from langchain_core.tools import Tool
from langchain_openai import ChatOpenAI
from langchain_core.prompts import PromptTemplate

from tools.tools import get_profile_url_tavily

load_dotenv(override=True)


def lookup(name: str) -> str:
    llm = ChatOpenAI(
        temperature=0,
        model_name="gpt-4o-mini",
        openai_api_key=os.environ["OPENAI_API_KEY"]),

    template = """given the full name {name_of_person} I want you to get it me a link to their Linkedin profile page.
                          Your answer should contain only a URL"""

    prompt_template = PromptTemplate(
        template=template, input_variables=["name_of_person"]
    )

    tools_for_agent = [
        Tool(
            name="linkedin_lookup",
            func=get_profile_url_tavily,
            description="use this tool to lookup a linkedin profile of a person",
        )
    ]

    react_prompt = hub.pull("hwchase17/react")
    agent = create_react_agent(llm, react_prompt, tools=tools_for_agent, verbose=True)
    agent_executor = AgentExecutor(agent=agent, tools=tools_for_agent, verbose=True)

    result = agent_executor.invoke(
        input={prompt_template.format_prompt(name_of_person=name)}
    )

    linkedin_url = result["output"]

    return linkedin_url

# ReAct Reasoning and Acting

from langchain import hub
from langchain.agents import AgentExecutor, create_react_agent
from langchain_openai import OpenAI
# from langchain_community.llms import HuggingFaceHub
# from langchain_community.chat_models.huggingface import ChatHuggingFace
from langchain.agents.load_tools import load_tools

# https://smith.langchain.com/hub/hwchase17/react
# """
# Answer the following questions as best you can. You have access to the following tools:

# {tools}

# Use the following format:

# Question: the input question you must answer
# Thought: you should always think about what to do
# Action: the action to take, should be one of [{tool_names}]
# Action Input: the input to the action
# Observation: the result of the action
# ... (this Thought/Action/Action Input/Observation can repeat N times)
# Thought: I now know the final answer
# Final Answer: the final answer to the original input question

# Begin!

# Question: {input}
# Thought:{agent_scratchpad}
# """
prompt = hub.pull("hwchase17/react")

# Choose the LLM to use
llm = OpenAI()
# llm = HuggingFaceHub(repo_id="google/gemma-7b")

# Google Search API (https://serpapi.com/dashboard) (pip install google-search-results)
# LLMMathChain (pip install numexpr)
tools = load_tools(["serpapi", "llm-math"], llm=llm)

# Construct the ReAct agent
agent = create_react_agent(llm, tools, prompt)
# Create an agent executor by passing in the agent and tools
agent_executor = AgentExecutor(agent=agent, tools=tools, verbose=True)
agent_executor.invoke({"input": "How many seconds are in 1:23:45"})

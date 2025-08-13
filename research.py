import os
import json
from dotenv import load_dotenv
import letta_client
from rich import print
from rich.markdown import Markdown
from research_tools import register_tools, setup_exa_mcp_server

# Load environment variables from .env file
load_dotenv()

# Register tools and set up MCP server
register_tools()
exa_tool_ids = setup_exa_mcp_server()

# Initialize the Letta client
base_url = os.getenv("LETTA_BASE_URL")
token = os.getenv("LETTA_API_KEY")
print(f"Connecting to Letta server at {base_url}")
client = letta_client.Letta(base_url=base_url, token=token)
exit()

TASK = """
Please write a research report on postgres and its ecosystem.
"""

# Block definitions
persona_value = """You are a research agent assisting a human in doing 
deep research by pulling many sources from online by composing search tools. 
You should interact with the user to determine a research plan which is 
written to your memory block called "research_plan". Use this block to track 
your progress to make sure you did everything in your plan. You can use your 
memory tools (e.g. memory_replace) to make updates to the plan as needed. 

Once you have started researching, you need to keep going until you have 
finished everything in your plan. Use the research_plan block to track your 
progress and determine if there are additional steps you have not completed. 
The final report should be written to research_report. 

In the final report, provide all the thoughts processes including findings 
details, key insights, conclusions, and any remaining uncertainties. Include 
citations to sources where appropriate. You must include citations for any sources 
that you use. 

This analysis should be very comprehensive and full of details. It is expected 
to be very long, detailed and comprehensive.

Make sure to include relevant citations in your report! Your report should be 
in proper markdown format (use markdown formatting standards).

Don't stop until you have finished the report. You may use the send_message tool
to update the human on your progress. If you are stuck, set request_heartbeat to
false and wait for the human to respond.
"""

# Create a new agent
lead_agent = client.agents.create(
    name="Lead Researcher Agent",
    description="A research agent that creates research tasks for the swarm",
    model="openai/gpt-4o-mini",
    embedding="openai/text-embedding-3-small",
    memory_blocks=[
        {
            "label":"persona",
            "value": persona_value,
            "description": "The persona block: Stores details about your current persona, guiding how you behave and respond. This helps you to maintain consistency and personality in your interactions."
        },
        {
            "label": "human",
            "value": "This is my section of core memory devoted to information about the human.",
            "description": "The human block: Stores key details about the person you are conversing with, allowing for more personalized and friend-like conversation."
        },
        { "label":"research_plan",
          "value": "", # initially empty
          "description": "Scratchpad to store the current research plan and progress. Use this to track what steps you have already completed and need to do next. "
        },
        { "label":"research_report",
          "value": "", # initially empty
          "description": "Contains the final research report. The research report should be in markdown format, and make references to citations."
        }
    ],
    tools=[
        "create_research_plan",
        "reset_research",
        "memory_replace",
        "memory_insert", 
        "memory_rethink",
        "send_message",
        "conversation_search",
    ],
    tool_ids=exa_tool_ids  # Add Exa MCP tool IDs
)

# Ask the agent to create a research plan
response = client.agents.messages.create_stream(
    agent_id = lead_agent.id,
    messages = [
        {
            "role": "user",
            "content": TASK
        }
    ]
)

for chunk in response:
    print(chunk, end="", flush=True)

    # Check if we have the message_type field in the chunk
    if hasattr(chunk, "message_type"):
        if chunk.message_type == "reasoning":
            print(chunk.reasoning)
        elif chunk.message_type == "tool_call_message":
            print("Calling tool: ", chunk.tool_call.name)
            print(json.dumps(chunk.tool_call.arguments, indent=2))
        elif chunk.message_type == "assistant_message":
            print(chunk.content)

#
# When the agent is done, get the research report and pretty-print it
# using rich markdown
#

# Get the research report
report = client.agents.blocks.retrieve(
    agent_id = lead_agent.id,
    block_label = "research_report"
)

md = Markdown(report.value)
print(md)

from llama_index.core.agent.workflow import AgentWorkflow
from llama_index.core import Settings


# workflow = AgentWorkflow.from_tools_or_functions(
#     tools_or_functions=[],
#     llm = Settings.llm,
#     system_prompt="You are an assistant. You have access to a database tool. If you need information, use that tool. If the user says they are done with a task, use the delete tool."
# )
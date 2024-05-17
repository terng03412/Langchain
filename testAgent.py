from langchain_openai import ChatOpenAI
from langchain_core.messages import HumanMessage
from langgraph.graph import END, MessageGraph

# Initialize the model with desired parameters
model = ChatOpenAI(temperature=0)

# Create a message graph
graph = MessageGraph()

# Add a node to the graph and set up the edge to the end node
graph.add_node("oracle", model)
graph.add_edge("oracle", END)

# Set the entry point of the graph
graph.set_entry_point("oracle")

# Compile the graph to make it runnable
runnable = graph.compile()

# Invoke the graph with a human message and print the result
result = runnable.invoke(HumanMessage("What is 1 + 1?"))
print(result)

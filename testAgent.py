from langchain_openai import ChatOpenAI
from langchain_core.messages import HumanMessage
from langgraph.graph import END, MessageGraph
from langchain.memory import ConversationBufferMemory
from langchain.chains import ConversationChain

# Initialize the language model
model = ChatOpenAI(temperature=0)

# Initialize memory
memory = ConversationBufferMemory()

# Define the conversation chain with memory
conversation_chain = ConversationChain(llm=model, memory=memory)

# Define a function to run the conversation
def run_conversation():
    # Start the conversation
    user_input = "Hi"
    response = conversation_chain.run(user_input)
    print(f"User: {user_input}")
    print(f"Bot: {response}")

    # Ask for the user's name
    user_input = "My name is Terng."
    response = conversation_chain.run(user_input)
    print(f"User: {user_input}")
    print(f"Bot: {response}")

    # Ask for the user's age
    user_input = "I am 25 years old."
    response = conversation_chain.run(user_input)
    print(f"User: {user_input}")
    print(f"Bot: {response}")

    # Ask for the user's gender
    user_input = "I am male."
    response = conversation_chain.run(user_input)
    print(f"User: {user_input}")
    print(f"Bot: {response}")

    # Continue the conversation
    user_input = "Tell me what you know about me. like name/age or something that I have told you"
    response = conversation_chain.run(user_input)
    print(f"User: {user_input}")
    print(f"Bot: {response}")

# Run the conversation
run_conversation()

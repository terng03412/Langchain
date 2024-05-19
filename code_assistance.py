from langchain import OpenAI
from graphviz import Digraph
import os

# Retrieve the environment variable
openai_api_key = os.getenv('OPENAI_API_KEY')

class ProgrammerAgent:
    def __init__(self, model):
        self.model = model

    def generate_code(self, requirements):
        try:
            prompt = f"Write a Python function based on these requirements:\n{requirements}"
            response = self.model.generate([prompt], max_tokens=150)
            
            if response.generations and response.generations[0]:
                code = response.generations[0][0].text.strip()
                return code
            return "Error: No code generated."
        except Exception as e:
            return f"An error occurred: {str(e)}"


import re

class TesterAgent:
    def __init__(self, model):
        self.model = model

    def generate_tests(self, code):
        try:
            prompt = f"Generate comprehensive test cases for this Python function to validate its input and output:\n{code}"
            response = self.model.generate([prompt], max_tokens=150)
            if response.generations and response.generations[0]:
                tests = response.generations[0][0].text.strip()
                return tests
            return "Error: No test cases generated."
        except Exception as e:
            return f"An error occurred while generating test cases: {str(e)}"

    def run_tests(self, code, tests):
        try:
            # Create a safe namespace to execute the code and tests
            local_namespace = {}
            exec(code, globals(), local_namespace)
            
            results = []
            test_cases = tests.strip().split('\n')
            pattern = r"Input: num1 = ([-\d.]+), num2 = ([-\d.]+)\n   Expected output: ([-\d.]+)"
            
            for test_case in test_cases:
                match = re.search(pattern, test_case)
                if match:
                    num1 = float(match.group(1))
                    num2 = float(match.group(2))
                    expected_output = float(match.group(3))
                    
                    # Execute the function with the parsed inputs
                    actual_output = local_namespace['add_numbers'](num1, num2)
                    
                    if actual_output == expected_output:
                        results.append((test_case, "Pass"))
                    else:
                        results.append((test_case, f"Fail: Expected {expected_output}, got {actual_output}"))
            return results
        except Exception as e:
            return f"An error occurred while running the tests: {str(e)}"


class ExecutorAgent:
    def execute_code(self, code):
        try:
            local_vars = {}
            exec(code, globals(), local_vars)
            return "Execution successful", local_vars.get('result')
        except Exception as e:
            return f"Execution failed: {str(e)}", None


class DebuggerAgent:
    def __init__(self, model):
        self.model = model

    def debug_code(self, code, error):
        try:
            prompt = f"Debug and fix this Python code:\n{code}\nError detected: {error}"
            response = self.model.generate([prompt], max_tokens=150)
            if response.generations and response.generations[0]:
                fix = response.generations[0][0].text.strip()
                return fix
            return "Error: No debug suggestions generated."
        except Exception as e:
            return f"An error occurred while debugging the code: {str(e)}"

# Initialize the agents
model = OpenAI(model="gpt-3.5-turbo-instruct", openai_api_key=openai_api_key)
programmer_agent = ProgrammerAgent(model)
tester_agent = TesterAgent(model)
executor_agent = ExecutorAgent()
debugger_agent = DebuggerAgent(model)

class CodeAssistant:
    def __init__(self, programmer_agent, tester_agent, executor_agent, debugger_agent):
        self.programmer_agent = programmer_agent
        self.tester_agent = tester_agent
        self.executor_agent = executor_agent
        self.debugger_agent = debugger_agent

    def review_and_improve_code(self, requirements):
        code = self.programmer_agent.generate_code(requirements)
        print(f"Generated Code:\n{code}\n")

        tests = self.tester_agent.generate_tests(code)
        if "Error" in tests:
            print(tests)
            return

        print(f"Generated Tests:\n{tests}\n")
        test_results = self.tester_agent.run_tests(code, tests)
        print(test_results)
        for test, result in test_results:
            print(f"Test: {test} - Result: {result}")

        if all(result == "Pass" for _, result in test_results):
            print("All tests passed. Code is ready for deployment.")
        else:
            print("Some tests failed. Debugging needed.")
            for test, result in test_results:
                if "Fail" in result:
                    error_description = result.split("Fail: ")[1]
                    fix = self.debugger_agent.debug_code(code, error_description)
                    print(f"Debugging Suggestion for {test}:\n{fix}\n")

# Initialize the CodeAssistant
code_assistant = CodeAssistant(programmer_agent, tester_agent, executor_agent, debugger_agent)
requirements = "Create a function to add three numbers."
code_assistant.review_and_improve_code(requirements)

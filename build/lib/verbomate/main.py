import argparse
import json
import subprocess
import sys
from openai import OpenAI
import os

def generate_script(task, max_attempts=5):
    config_path = os.path.join(os.path.expanduser("~"), ".verbomate", "config.json")

    for attempt in range(max_attempts):
        with open(config_path, "r") as file:
            config = json.load(file)

        client = OpenAI(api_key=config["api_key"])
        assistant = client.beta.assistants.create(
            name="verbomate",
            instructions="""Generate python code to acomplish a task. Always surround code contents with triple backticks (```).""",
            tools=[],
            model="gpt-4-1106-preview"
        )
        thread = client.beta.threads.create()
        message = client.beta.threads.messages.create(
            thread_id=thread.id,
            role="user",
            content=task
        )
        ls_output = subprocess.check_output(['ls']).decode('utf-8')
        run = client.beta.threads.runs.create(
            thread_id=thread.id,
            assistant_id=assistant.id,
            instructions=f"Generate a single block of python code surrounded by triple backticks (```) to acomplish the task[{task}]. Context: ls_output[{ls_output}]",
        )
        while True:
            run = client.beta.threads.runs.retrieve(
                thread_id=thread.id,
                run_id=run.id
            )
            if run.status == "completed":
                break
        messages = client.beta.threads.messages.list(
            thread_id=thread.id
        )
        thread_messages = messages.data

        # Filter messages to get only those sent by the assistant
        assistant_messages = [msg for msg in thread_messages if msg.role == "assistant"]

        # Check if there are any assistant messages
        if not assistant_messages:
            raise ValueError("No assistant messages found in the thread")

        # Get the last assistant message
        last_assistant_message = assistant_messages[-1]
        last_message_text = last_assistant_message.content[0].text.value

        start = last_message_text.find("```python")
        end = last_message_text.find("```", start + 9)
        if start != -1 and end != -1:
            script_text = last_message_text[start+9:end].strip()  # +9 to skip past ```python
            print('\n\n')
            print('------------------------')
            print('START OF SCRIPT')
            print(script_text)
            print('END OF SCRIPT')
            print('------------------------')
            print('\n\n')
            return script_text

    # If we've reached this point, we've failed to generate a valid script after max_attempts
    raise ValueError("Script not found between ```python and ``` after {} attempts".format(max_attempts))

def execute_script(script_text):
    with open("temp_script.py", "w") as file:
        file.write(script_text)
    subprocess.run(["python3", "temp_script.py"], check=True)

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("-key", help="API key for OpenAI")
    parser.add_argument("task", nargs="?", default="", help="Task for the script to perform")
    args = parser.parse_args()

    # Define the path to the config file
    config_path = os.path.join(os.path.expanduser("~"), ".verbomate", "config.json")

    if args.key:
        # Ensure the directory for the config file exists
        os.makedirs(os.path.dirname(config_path), exist_ok=True)

        with open(config_path, "w") as file:
            json.dump({"api_key": args.key}, file)
        print("API key stored.")
        return

    try:
        if args.task:
            script = generate_script(args.task)
            execute_script(script)
        else:
            print("""Please provide a task as a command-line argument. e.g. verbomate "create helloworld.txt" """)
    except subprocess.CalledProcessError as e:
        print(f"Error executing script: {e}")

if __name__ == "__main__":
    main()
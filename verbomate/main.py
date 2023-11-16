import subprocess
import sys
from openai import OpenAI

#yes | pip uninstall verbomate && pip install . && verbomate

def generate_script(task):

    client = OpenAI(
    # Defaults to os.environ.get("OPENAI_API_KEY")
    # Otherwise use: api_key="Your_API_Key",
    api_key="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"
    )
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
    run = client.beta.threads.runs.create(
        thread_id=thread.id,
        assistant_id=assistant.id,
        instructions=f"Generate a single block of python code surrounded by triple backticks (```) to acomplish the task[{task}]"
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
    else:
        raise ValueError("Script not found between ```python and ```")

    print('\n\n')
    print('------------------------')
    print('START OF SCRIPT')
    print(script_text)
    print('END OF SCRIPT')
    print('------------------------')
    print('\n\n')
    return script_text

def execute_script(script_text):
    with open("temp_script.py", "w") as file:
        file.write(script_text)
    subprocess.run(["python3", "temp_script.py"], check=True)

def main():
    try:
        if len(sys.argv) > 1:
                    task = sys.argv[1]
                    script = generate_script(task)
                    execute_script(script)
        else:
            print("""Please provide a task as a command-line argument. e.g. verbomate "create helloworld.txt" """)
    except subprocess.CalledProcessError as e:
        print(f"Error executing script: {e}")

if __name__ == "__main__":
    main()


import subprocess
import sys
from openai import OpenAI

#yes | pip uninstall verbomate && pip install . && verbomate

def generate_script():

    client = OpenAI(
    # Defaults to os.environ.get("OPENAI_API_KEY")
    # Otherwise use: api_key="Your_API_Key",
    api_key="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"
    )
    assistant = client.beta.assistants.create(
        name="verbomate",
        instructions="You generate python code AND ONLY PYTHON CODE based on user prompt and (optional) context. \n The text you generate will be run as a python script and should be a valid python file. \n It will be run in the directory in which the user wrote their prompt.",
        tools=[],
        model="gpt-4-1106-preview"
    )
    thread = client.beta.threads.create()
    message = client.beta.threads.messages.create(
        thread_id=thread.id,
        role="user",
        content="create a file hello_world.txt"
    )
    run = client.beta.threads.runs.create(
        thread_id=thread.id,
        assistant_id=assistant.id,
        instructions="Please address the user as Jane Doe. The user has a premium account."
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
    print(messages)
    last_message_text = messages[-1]['content'][0]['text']['value']
    return last_message_text

def execute_script(script_text):
    with open("temp_script.py", "w") as file:
        file.write(script_text)
    subprocess.run([sys.executable, "temp_script.py"], check=True)

def main():
    try:
        script = generate_script()
        execute_script(script)
    except subprocess.CalledProcessError as e:
        print(f"Error executing script: {e}")

if __name__ == "__main__":
    main()


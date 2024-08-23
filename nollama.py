import argparse
import sys
from rich.console import Console
from rich.markdown import Markdown
from rich.text import Text
import inquirer
from g4f.client import Client
from yaspin import yaspin

# Initialize the rich console
console = Console()
    
# Models dictionary
models = {
    'gpt-4o-mini': 'gpt-4o-mini',
    'claude-3-haiku' : 'claude-3-haiku',
    'gpt-4o': 'gpt-4o',
    'gpt-4': 'gpt-4',
    'gpt-4-turbo': 'gpt-4-turbo',
    'llama-3-70b-instruct': 'llama-3-70b-instruct',
    'llama-3.1-70b': 'llama-3.1-70b',
    'llama-3.1-70b-instruct': 'llama-3.1-70b-instruct',
    'mixtral-8x7b': 'mixtral-8x7b',
    'Nous-Hermes-2-Mixtral-8x7B-DPO': 'Nous-Hermes-2-Mixtral-8x7B-DPO',
    'Yi-1.5-34b-chat': 'Yi-1.5-34b-chat',
    'Phi-3-mini-4k-instruct': 'Phi-3-mini-4k-instruct',
    'blackbox' : 'blackbox',
    'Qwen2-7b-instruct' : 'Qwen2-7b-instruct',
    'command-r+' : 'command-r+',
    'SparkDesk-v1.1' : 'SparkDesk-v1.1',
    'glm4-9b-chat' : 'glm4-9b-chat',
    'chatglm3-6b' : 'chatglm3-6b',
}

# Initialize the g4f client
client = Client()

# Function to display the title and model
def display_title_and_model(selected_model):
    title = Text("nollama", style="bold red underline")
    model_text = Text(f"Model: {selected_model}", style="bold yellow")
    console.print(title, justify="center")
    console.print(model_text, justify="right")

# Function to select a model using inquirer
def select_model():
    questions = [
        inquirer.List('model',
                      message="Select a model",
                      choices=list(models.keys()))
    ]
    answer = inquirer.prompt(questions)
    return models[answer['model']]

# Function to handle asking a question
def ask_question(selected_model, stream):
    # Prompt the user for input
    question = input(">>> ").strip()

    if not question:
        console.print("[bold red]Error: Input is empty. Please type something.[/bold red]")
        return selected_model

    if question.lower() in ["quit", "exit", "q"]:
        console.print("[bold red]Exiting the prompt...[/bold red]")
        sys.exit()
    
    if question.lower() == "clear":
        console.clear()
        display_title_and_model(selected_model)
        return selected_model

    if question.lower() == "model":
        return select_model()

    # Initialize a variable to collect the markdown content
    markdown_content = ""

    # Show spinner while waiting for response to start streaming
    with yaspin(text="Waiting for response...", color="yellow") as spinner:
        try:
            chat_completion = client.chat.completions.create(
                model=selected_model,
                messages=[{"role": "user", "content": question}],
                stream=stream
            )

            if stream:
                # Process each chunk of the streamed response
                first_chunk_received = False
                for completion in chat_completion:
                    if not first_chunk_received:
                        spinner.stop()  # Stop the spinner once the first chunk arrives
                        first_chunk_received = True

                    # Get the new text from the stream
                    chunk = completion.choices[0].delta.content or ""

                    # Append the new chunk to the markdown content
                    markdown_content += chunk

                    # Clear the console but preserve the prompt and question
                    console.clear()
                    display_title_and_model(selected_model)  # Display the title and selected model
                    console.print(f">>> {question}")  # Reprint the prompt and question
                    console.print(Markdown(markdown_content), end="")  # Render the markdown content

            else:
                # If not streaming, get the complete response and print it at once
                markdown_content = chat_completion.choices[0].message.content or ""
                spinner.stop()
                console.print(Markdown(markdown_content))

        except Exception as e:
            spinner.fail("Error occurred!")
            console.print(f"[bold red]An error occurred: {e}[/bold red]")
            return selected_model

        # After response is complete, print a newline for separation
        console.print()
    return selected_model

# Main loop to keep asking questions
def main():
    # Parse command-line arguments
    parser = argparse.ArgumentParser(description="Run nollama with or without streaming output.")
    parser.add_argument("--stream", action="store_true", help="Enable live streaming of the output.")
    args = parser.parse_args()

    selected_model = select_model()
    console.clear()
    display_title_and_model(selected_model)

    try:
        while True:
            selected_model = ask_question(selected_model, stream=args.stream)
    except KeyboardInterrupt:
        console.print("\n[bold red]Exiting the prompt...[/bold red]")
        sys.exit()

if __name__ == "__main__":
    main()

import argparse
import sys
import os
from pathlib import Path
from rich.console import Console
from rich.markdown import Markdown
from rich.text import Text
from rich.live import Live
from rich.status import Status
import inquirer
from google import genai
from google.genai import types
import time

# Initialize the rich console
console = Console()
    
# Models dictionary
models = {
    'gemini-2.0-flash': 'gemini-2.0-flash',
    'gemini-2.5-flash-preview-04-17': 'gemini-2.5-flash-preview-04-17',
    'gemini-2.5-pro-preview-03-25': 'gemini-2.5-pro-preview-03-25',
}

# Function to read the API key from ~/.nollama
def get_api_key():
    nollama_file = Path.home() / ".nollama"
    if not nollama_file.exists():
        console.print("[bold red]Error: ~/.nollama file not found.[/bold red]")
        console.print("[yellow]Please create a file at ~/.nollama with your Gemini API key:[/yellow]")
        console.print("[yellow]GEMINI=your_api_key_here[/yellow]")
        sys.exit(1)
    
    with open(nollama_file, "r") as f:
        for line in f:
            if line.startswith("GEMINI="):
                api_key = line.strip().split("=")[1]
                return api_key
    
    console.print("[bold red]Error: GEMINI API key not found in ~/.nollama file.[/bold red]")
    console.print("[yellow]Please add a line with GEMINI=your_api_key_here[/yellow]")
    sys.exit(1)

# Initialize Gemini client
def initialize_client():
    api_key = get_api_key()
    client = genai.Client(api_key=api_key)
    return client

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
def ask_question(client, chat, selected_model, stream):
    # Prompt the user for input
    try:
        question = input(">>> ").strip()
    except EOFError:
        # Handle Ctrl+D
        console.print("\n[bold red]Exiting the prompt...[/bold red]")
        sys.exit()

    if not question:
        console.print("[bold red]Error: Input is empty. Please type something.[/bold red]")
        return selected_model, chat

    if question.lower() in ["quit", "exit", "q"]:
        console.print("[bold red]Exiting the prompt...[/bold red]")
        sys.exit()
    
    if question.lower() == "clear":
        console.clear()
        display_title_and_model(selected_model)
        # Create a new chat session when clearing
        chat = client.chats.create(model=selected_model)
        return selected_model, chat

    if question.lower() == "model":
        new_model = select_model()
        if new_model != selected_model:
            chat = client.chats.create(model=new_model)
        return new_model, chat

    try:
        if stream:
            # Use Rich's status for the spinner - it will appear inline with text
            status = Status("Waiting for response...")
            status.start()
            
            try:
                # Start the API request
                response = chat.send_message_stream(question)
                
                # For properly displaying streaming content
                full_response = ""
                first_chunk = None
                
                # Get first chunk before stopping spinner
                for chunk in response:
                    first_chunk = chunk
                    status.stop()
                    break
                
                # Process first chunk if we got one
                if first_chunk:
                    chunk_text = first_chunk.text or ""
                    full_response = chunk_text
                    
                    # Start streaming with the first chunk
                    with Live(Markdown(full_response), refresh_per_second=10) as live:
                        # Continue with remaining chunks
                        for chunk in response:
                            chunk_text = chunk.text or ""
                            full_response += chunk_text
                            live.update(Markdown(full_response))
                else:
                    # No chunks received
                    status.stop()
                    console.print("[yellow]Received empty response[/yellow]")
            
            except Exception as e:
                status.stop()
                raise e
                
        else:
            # Non-streaming mode with Rich status
            with Status("Waiting for response...") as status:
                response = chat.send_message(question)
                markdown_content = response.text
            
            # Print the complete response
            console.print(Markdown(markdown_content))

    except Exception as e:
        console.print(f"[bold red]An error occurred: {e}[/bold red]")
        return selected_model, chat

    # After response is complete, print a newline for separation
    console.print()
    return selected_model, chat

# Main loop to keep asking questions
def main():
    # Parse command-line arguments
    parser = argparse.ArgumentParser(description="Run nollama with Google Gemini API.")
    parser.add_argument("--stream", action="store_true", help="Enable live streaming of the output.", default=True)
    args = parser.parse_args()

    # Initialize client
    client = initialize_client()

    # Have user select model at startup
    console.print("[bold blue]Welcome to nollama - Gemini API Terminal Interface[/bold blue]")
    console.print("[yellow]Please select a model to get started:[/yellow]")
    selected_model = select_model()
    chat = client.chats.create(model=selected_model)
    
    console.clear()
    display_title_and_model(selected_model)

    try:
        while True:
            selected_model, chat = ask_question(client, chat, selected_model, stream=args.stream)
    except KeyboardInterrupt:
        console.print("\n[bold red]Exiting the prompt...[/bold red]")
        sys.exit()
    except EOFError:
        # Additional handler for Ctrl+D
        console.print("\n[bold red]Exiting the prompt...[/bold red]")
        sys.exit()

if __name__ == "__main__":
    main()
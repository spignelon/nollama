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
from litellm import completion, acompletion, get_valid_models
import litellm
from dotenv import load_dotenv
import json
from prompt_toolkit import prompt
from prompt_toolkit.completion import WordCompleter
from prompt_toolkit.key_binding import KeyBindings
from prompt_toolkit.keys import Keys

# Suppress LiteLLM's verbose debug output
litellm.suppress_debug_info = True
litellm.set_verbose = False

# Initialize the rich console
console = Console()

# Provider configurations (models are fetched dynamically)
PROVIDERS = {
    'Google Gemini': {
        'prefix': 'gemini/',
        'env_key': 'GEMINI_API_KEY',
        'litellm_provider': 'gemini',
    },
    'Vertex AI': {
        'prefix': 'vertex_ai/',
        'env_key': 'VERTEX_PROJECT',
        'litellm_provider': 'vertex_ai',
    },
    'Groq': {
        'prefix': 'groq/',
        'env_key': 'GROQ_API_KEY',
        'litellm_provider': 'groq',
    },
    'Ollama': {
        'prefix': 'ollama_chat/',
        'env_key': 'OLLAMA_API_BASE',
        'litellm_provider': 'ollama',
    },
    'Anthropic': {
        'prefix': 'anthropic/',
        'env_key': 'ANTHROPIC_API_KEY',
        'litellm_provider': 'anthropic',
    },
    'DeepSeek': {
        'prefix': 'deepseek/',
        'env_key': 'DEEPSEEK_API_KEY',
        'litellm_provider': 'deepseek',
    },
    'OpenAI': {
        'prefix': 'openai/',
        'env_key': 'OPENAI_API_KEY',
        'litellm_provider': 'openai',
    },
    'OpenRouter': {
        'prefix': 'openrouter/',
        'env_key': 'OPENROUTER_API_KEY',
        'litellm_provider': 'openrouter',
    },
}

# Function to load environment variables from .env or ~/.nollama
def load_config():
    # First try to load from .env in the current directory or project root
    env_path = Path.cwd() / ".env"
    if not env_path.exists():
        # Try project root (where nollama is installed)
        env_path = Path(__file__).parent.parent / ".env"
    
    if env_path.exists():
        load_dotenv(env_path)
        return True
    
    # Fall back to ~/.nollama for backward compatibility
    nollama_file = Path.home() / ".nollama"
    if nollama_file.exists():
        with open(nollama_file, "r") as f:
            for line in f:
                line = line.strip()
                if line and not line.startswith("#") and "=" in line:
                    key, value = line.split("=", 1)
                    os.environ[key] = value
        return True
    
    return False

# Fetch available models for a provider dynamically
def fetch_models_for_provider(provider_name):
    """Fetch available models from the provider using LiteLLM's get_valid_models()."""
    provider = PROVIDERS[provider_name]
    litellm_provider = provider.get('litellm_provider')
    
    with Status(f"Fetching available models from {provider_name}...") as status:
        try:
            # Use get_valid_models with provider-specific endpoint checking
            models = get_valid_models(
                check_provider_endpoint=True,
                custom_llm_provider=litellm_provider
            )
            
            if not models:
                console.print(f"[yellow]Warning: No models returned from {provider_name}. Using fallback.[/yellow]")
                return None
            
            # Filter models to only those for this provider (remove prefix if present)
            provider_prefix = provider['prefix']
            filtered_models = []
            for model in models:
                # Remove provider prefix if it exists
                if model.startswith(provider_prefix):
                    model_id = model[len(provider_prefix):]
                else:
                    model_id = model
                filtered_models.append(model_id)
            
            return filtered_models if filtered_models else models
            
        except Exception as e:
            console.print(f"[yellow]Warning: Could not fetch models from {provider_name}: {e}[/yellow]")
            console.print(f"[yellow]You may need to configure your API credentials properly.[/yellow]")
            return None

# Validate that required API keys are set for the selected provider
def validate_provider_config(provider_name):
    provider = PROVIDERS[provider_name]
    env_key = provider['env_key']
    
    if not os.environ.get(env_key):
        console.print(f"[bold red]Error: {env_key} not found in environment.[/bold red]")
        console.print(f"[yellow]Please set {env_key} in .env or ~/.nollama file[/yellow]")
        
        if provider_name == 'Ollama':
            console.print(f"[yellow]For Ollama, set: {env_key}=http://localhost:11434[/yellow]")
        else:
            console.print(f"[yellow]Example: {env_key}=your_api_key_here[/yellow]")
        
        sys.exit(1)

# Function to display the title, provider, and model
def display_title_and_info(provider_name, model_name):
    title = Text("nollama", style="bold red underline")
    provider_text = Text(f"Provider: {provider_name}", style="bold cyan")
    model_text = Text(f"Model: {model_name}", style="bold yellow")
    console.print(title, justify="center")
    console.print(provider_text, justify="right")
    console.print(model_text, justify="right")

# Function to select a provider
def select_provider():
    questions = [
        inquirer.List('provider',
                      message="Select a provider",
                      choices=list(PROVIDERS.keys()))
    ]
    answer = inquirer.prompt(questions)
    return answer['provider']

# Function to select a model with vim-style search interface
def select_model_with_search(provider_name, models):
    """Present models in a searchable list with vim-style search using '/'."""
    if not models:
        console.print("[bold red]No models available for selection.[/bold red]")
        return None
    
    console.print(f"\n[yellow]Available models from {provider_name} ({len(models)} total):[/yellow]")
    console.print("[dim]Type '/' to search, use arrow keys to navigate, press Enter to select[/dim]\n")
    
    # Display first 20 models as preview
    for i, model in enumerate(models[:20]):
        console.print(f"  {i+1}. {model}")
    
    if len(models) > 20:
        console.print(f"\n[dim]... and {len(models) - 20} more models[/dim]")
    
    # Create a completer with all model names for searchable dropdown
    completer = WordCompleter(models, ignore_case=True, sentence=True)
    
    console.print("\n[cyan]>>> Search/select model (type '/' + search term, or full model name):[/cyan]")
    
    try:
        selected = prompt(
            "> ",
            completer=completer,
            complete_while_typing=True,
        ).strip()
        
        # Handle vim-style search (if starts with /)
        if selected.startswith('/'):
            selected = selected[1:].strip()
        
        # Find matching model
        if selected in models:
            return selected
        
        # Try case-insensitive match
        for model in models:
            if model.lower() == selected.lower():
                return model
        
        # Try partial match
        matches = [m for m in models if selected.lower() in m.lower()]
        if len(matches) == 1:
            console.print(f"[green]Selected: {matches[0]}[/green]")
            return matches[0]
        elif len(matches) > 1:
            console.print(f"[yellow]Multiple matches found ({len(matches)}). Please be more specific:[/yellow]")
            for i, match in enumerate(matches[:10]):
                console.print(f"  {i+1}. {match}")
            # Recursively call for refinement
            return select_model_with_search(provider_name, matches)
        else:
            console.print(f"[red]No model found matching '{selected}'. Please try again.[/red]")
            return select_model_with_search(provider_name, models)
            
    except (KeyboardInterrupt, EOFError):
        console.print("\n[yellow]Selection cancelled.[/yellow]")
        return None

# Function to select a model for the chosen provider
def select_model(provider_name):
    provider = PROVIDERS[provider_name]
    
    # Fetch models dynamically from provider
    models = fetch_models_for_provider(provider_name)
    
    if not models:
        console.print(f"[bold red]Could not fetch models from {provider_name}.[/bold red]")
        sys.exit(1)
    
    # Sort models for better UX
    models = sorted(models)
    
    # Use searchable selection
    model_id = select_model_with_search(provider_name, models)
    
    if not model_id:
        console.print("[bold red]No model selected. Exiting.[/bold red]")
        sys.exit(1)
    
    # Construct full model name with provider prefix
    full_model_name = f"{provider['prefix']}{model_id}"
    
    # Use model_id as display name (can be enhanced later)
    model_display_name = model_id
    
    return model_display_name, full_model_name

# Function to handle asking a question
def ask_question(provider_name, model_display_name, full_model_name, messages, stream):
    # Prompt the user for input
    try:
        question = input(">>> ").strip()
    except EOFError:
        # Handle Ctrl+D
        console.print("\n[bold red]Exiting the prompt...[/bold red]")
        sys.exit()

    if not question:
        console.print("[bold red]Error: Input is empty. Please type something.[/bold red]")
        return provider_name, model_display_name, full_model_name, messages

    if question.lower() in ["quit", "exit", "q"]:
        console.print("[bold red]Exiting the prompt...[/bold red]")
        sys.exit()
    
    if question.lower() == "clear":
        console.clear()
        display_title_and_info(provider_name, model_display_name)
        # Display available commands after clearing
        console.print("[dim]Commands: 'model' to change model | 'provider' to change provider | 'clear' to clear history | 'quit/exit/q' to exit[/dim]")
        console.print()
        # Create a new message history when clearing
        messages = []
        return provider_name, model_display_name, full_model_name, messages

    if question.lower() == "model":
        new_model_display_name, new_full_model_name = select_model(provider_name)
        console.clear()
        display_title_and_info(provider_name, new_model_display_name)
        return provider_name, new_model_display_name, new_full_model_name, messages
    
    if question.lower() == "provider":
        new_provider_name = select_provider()
        validate_provider_config(new_provider_name)
        new_model_display_name, new_full_model_name = select_model(new_provider_name)
        console.clear()
        display_title_and_info(new_provider_name, new_model_display_name)
        # Clear message history when switching providers
        messages = []
        return new_provider_name, new_model_display_name, new_full_model_name, messages

    # Add user message to history
    messages.append({"role": "user", "content": question})

    try:
        if stream:
            # Use Rich's status for the spinner
            status = Status("Waiting for response...")
            status.start()
            
            try:
                # Start the API request with streaming
                response = completion(
                    model=full_model_name,
                    messages=messages,
                    stream=True
                )
                
                full_response = ""
                first_chunk_received = False
                
                # Collect and stream chunks as plain text for real-time feedback
                for chunk in response:
                    if hasattr(chunk.choices[0].delta, 'content') and chunk.choices[0].delta.content:
                        chunk_text = chunk.choices[0].delta.content
                        full_response += chunk_text
                        
                        # Stop spinner on first chunk
                        if not first_chunk_received:
                            status.stop()
                            first_chunk_received = True
                        
                        # Stream text in real-time
                        print(chunk_text, end='', flush=True)
                
                # Print newline after streaming
                print()
                
                # Stop spinner if still running
                if not first_chunk_received and status._live.is_started:
                    status.stop()
                
                if not full_response:
                    console.print("[yellow]Received empty response[/yellow]")
                else:
                    # Now render the complete response as markdown
                    console.print("\n[dim]Rendering markdown...[/dim]")
                    # Move cursor up and clear the line
                    print("\033[F\033[K", end='')
                    # Clear the plain text output (move up by number of lines)
                    lines_to_clear = full_response.count('\n') + 1
                    for _ in range(lines_to_clear):
                        print("\033[F\033[K", end='')
                    # Now render the beautiful markdown
                    console.print(Markdown(full_response))
                
                # Add assistant response to message history
                if full_response:
                    messages.append({"role": "assistant", "content": full_response})
            
            except Exception as e:
                if status._live.is_started:
                    status.stop()
                raise e
                
        else:
            # Non-streaming mode with Rich status
            with Status("Waiting for response...") as status:
                response = completion(
                    model=full_model_name,
                    messages=messages
                )
                markdown_content = response.choices[0].message.content
            
            # Print the complete response
            console.print(Markdown(markdown_content))
            
            # Add assistant response to message history
            messages.append({"role": "assistant", "content": markdown_content})

    except Exception as e:
        console.print(f"[bold red]An error occurred: {e}[/bold red]")
        # Remove the failed user message from history
        if messages and messages[-1]["role"] == "user":
            messages.pop()
        return provider_name, model_display_name, full_model_name, messages

    # After response is complete, print a newline for separation
    console.print()
    return provider_name, model_display_name, full_model_name, messages

# Main loop to keep asking questions
def main():
    # Parse command-line arguments
    parser = argparse.ArgumentParser(description="Run nollama with multiple LLM providers via LiteLLM.")
    parser.add_argument("--stream", action="store_true", help="Enable live streaming of the output.", default=True)
    parser.add_argument("--no-stream", action="store_false", dest="stream", help="Disable streaming.")
    args = parser.parse_args()

    # Load configuration from .env or ~/.nollama
    load_config()

    # Display welcome message
    console.print("[bold blue]Welcome to nollama - Multi-Provider LLM Terminal Interface[/bold blue]")
    console.print("[yellow]Powered by LiteLLM - Supporting 100+ LLM providers[/yellow]")
    console.print()
    
    # Select provider
    console.print("[yellow]Please select a provider:[/yellow]")
    provider_name = select_provider()
    
    # Validate provider configuration
    validate_provider_config(provider_name)
    
    # Select model
    console.print(f"[yellow]Please select a model from {provider_name}:[/yellow]")
    model_display_name, full_model_name = select_model(provider_name)
    
    # Initialize message history for conversation context
    messages = []
    
    console.clear()
    display_title_and_info(provider_name, model_display_name)
    
    # Display available commands
    console.print("[dim]Commands: 'model' to change model | 'provider' to change provider | 'clear' to clear history | 'quit/exit/q' to exit[/dim]")
    console.print()

    try:
        while True:
            provider_name, model_display_name, full_model_name, messages = ask_question(
                provider_name, model_display_name, full_model_name, messages, stream=args.stream
            )
    except KeyboardInterrupt:
        console.print("\n[bold red]Exiting the prompt...[/bold red]")
        sys.exit()
    except EOFError:
        # Additional handler for Ctrl+D
        console.print("\n[bold red]Exiting the prompt...[/bold red]")
        sys.exit()

if __name__ == "__main__":
    main()
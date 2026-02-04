# NoLlama

NoLlama is a powerful terminal-based interface for interacting with **multiple LLM providers** directly from your terminal. Powered by [LiteLLM](https://litellm.ai/), NoLlama provides a unified interface for chatting with models from **8 major providers**: Google Gemini, Vertex AI, Anthropic Claude, OpenAI, Groq, DeepSeek, OpenRouter, and Ollama.

Inspired by [Ollama](https://ollama.com/), NoLlama offers a neat terminal interface for powerful language models with features like **dynamic model discovery**, **vim-style searchable model selection**, colorful markdown rendering, multi-turn conversations, and efficient memory usage.

![NoLlama](https://i.imgur.com/0ZOaXwv.png)

## Features

- **🌐 8 Major LLM Providers:** Access models from Google Gemini, Vertex AI, Anthropic Claude, OpenAI, Groq, DeepSeek, OpenRouter, and Ollama via LiteLLM
- **🔍 Dynamic Model Discovery:** Automatically fetches latest available models from each provider - no hardcoded lists!
- **⚡ Smart Model Search:** Type to search with auto-completion, or use vim-style `/search` - navigate hundreds of models with ease
- **💬 Multi-turn Conversations:** Maintain context between prompts for coherent conversations
- **🎨 Neat Terminal UI:** Clean and intuitive interface with colorful markdown rendering
- **⚡ Live Streaming Responses:** Watch responses appear in real-time as they're generated
- **🎯 Easy Provider/Model Switching:** Type `provider` or `model` to switch anytime during chat
- **🧹 Clear Chat History:** Type `clear` to reset conversation while keeping the interface
- **💾 Low Memory Usage:** Efficient memory management compared to browser-based interfaces
- **🔧 Flexible Configuration:** Use `.env` file or `~/.nollama` for API key management
- **🚪 Exit Commands:** Type `q`, `quit`, or `exit` to leave, or use Ctrl+C / Ctrl+D

## Installation

### Install from PyPI (Recommended)

```bash
pip install nollama
```

### Or Install from Source

```bash
git clone https://github.com/spignelon/nollama.git
cd nollama
pip install -e .
```

## Configuration

NoLlama supports two configuration methods:

### Option 1: `.env` File (For Development/Git Clone)

If you're developing or cloned the repository, create a `.env` file in your **project directory**:

**Linux/macOS:**
```bash
# Create .env in your working directory
touch .env
nano .env  # or use your preferred editor
```

**Windows (PowerShell):**
```powershell
# Create .env in your working directory
New-Item .env -ItemType File
notepad .env
```

**Windows (Command Prompt):**
```cmd
echo. > .env
notepad .env
```

### Option 2: `~/.nollama` File (For Pip Install)

If you installed via `pip install nollama`, create a `.nollama` file in your **home directory**:

**Linux/macOS:**
```bash
touch ~/.nollama
nano ~/.nollama
```

**Windows (PowerShell):**
```powershell
New-Item $env:USERPROFILE\.nollama -ItemType File
notepad $env:USERPROFILE\.nollama
```

### Configuration Template

Copy and paste this complete configuration template into your `.env` or `~/.nollama` file:

```bash
## ============================================================================
## NOLLAMA CONFIGURATION
## ============================================================================
## This file contains all configuration options for nollama.
## Uncomment and fill in the API keys for providers you want to use.
## ============================================================================

## ----------------------------------------------------------------------------
## API KEYS - Google Gemini (Google AI Studio)
## ----------------------------------------------------------------------------
## Get your key from: https://makersuite.google.com/app/apikey
GEMINI_API_KEY=your_gemini_api_key_here

## ----------------------------------------------------------------------------
## API KEYS - Google Vertex AI
## ----------------------------------------------------------------------------
## For Vertex AI, you need to set up Google Cloud authentication
# VERTEX_PROJECT=your_gcp_project_id
# VERTEX_LOCATION=us-central1
# GOOGLE_APPLICATION_CREDENTIALS=/path/to/service-account-key.json

## ----------------------------------------------------------------------------
## API KEYS - Groq
## ----------------------------------------------------------------------------
## Get your key from: https://console.groq.com/keys
GROQ_API_KEY=your_groq_api_key_here

## ----------------------------------------------------------------------------
## API KEYS - Ollama
## ----------------------------------------------------------------------------
## Ollama runs locally, just specify the base URL
OLLAMA_API_BASE=http://localhost:11434

## ----------------------------------------------------------------------------
## API KEYS - Anthropic (Claude)
## ----------------------------------------------------------------------------
## Get your key from: https://console.anthropic.com/
# ANTHROPIC_API_KEY=your_anthropic_api_key_here

## ----------------------------------------------------------------------------
## API KEYS - DeepSeek
## ----------------------------------------------------------------------------
## Get your key from: https://platform.deepseek.com/
# DEEPSEEK_API_KEY=your_deepseek_api_key_here

## ----------------------------------------------------------------------------
## API KEYS - OpenAI
## ----------------------------------------------------------------------------
## Get your key from: https://platform.openai.com/api-keys
# OPENAI_API_KEY=your_openai_api_key_here

## ----------------------------------------------------------------------------
## API KEYS - OpenRouter
## ----------------------------------------------------------------------------
## Get your key from: https://openrouter.ai/keys
OPENROUTER_API_KEY=your_openrouter_api_key_here
OPENROUTER_API_BASE=https://openrouter.ai/api/v1
# OR_SITE_URL=https://yoursite.com  ## Optional: for OpenRouter rankings
# OR_APP_NAME=nollama  ## Optional: for OpenRouter rankings

## ----------------------------------------------------------------------------
## ADVANCED SETTINGS (Optional)
## ----------------------------------------------------------------------------
## Maximum conversation pairs to keep in multi-turn context
## One pair = user message + AI response
## Set to 0 or leave empty for unlimited context (default)
## Example: MAX_MULTITURN_PAIRS=5 keeps only the last 5 conversation pairs
# MAX_MULTITURN_PAIRS=5

## Maximum tokens for completion
# MAX_TOKENS=4096

## Temperature (0.0 to 2.0)
# TEMPERATURE=0.7

## Top-p sampling
# TOP_P=1.0
```

### Quick Start Examples

**For Google Gemini (Free tier available):**
```bash
GEMINI_API_KEY=your_api_key_from_makersuite
```

**For Groq (Free tier with fast inference):**
```bash
GROQ_API_KEY=your_groq_api_key
```

**For OpenRouter (Access to models from multiple providers):**
```bash
OPENROUTER_API_KEY=your_openrouter_api_key
```

## Run NoLlama

```bash
nollama
```

## Usage

### First Time Setup

1. **Select a Provider:** Choose from 8 available providers (Gemini, Groq, Anthropic, OpenAI, etc.)
2. **Select a Model:** Models are fetched dynamically from the provider
   - See a preview of available models
   - **Type to search** with auto-completion suggestions as you type
   - Or use **vim-style search**: type `/model-name` to filter
   - Navigate with arrow keys and press Enter to select
3. **Start Chatting:** Type your questions and enjoy rich markdown responses!

### Commands During Chat

- **`provider`** - Switch to a different provider (keeps conversation history)
- **`model`** - Switch to a different model within the same provider
- **`clear`** - Clear conversation history (keeps interface and help text)
- **`q`, `quit`, `exit`** - Exit the application
- **Ctrl+C or Ctrl+D** - Quick exit

### Model Selection Tips

With potentially hundreds of models available:

1. **Browse:** Scroll through the initial preview (first 20 models shown)
2. **Type to Search:** Start typing a model name and get auto-completion suggestions
3. **Vim-Style Search:** Type `/` followed by keywords (e.g., `/gpt-4`, `/claude`, `/llama`)
4. **Refine:** If multiple matches, you'll be prompted to narrow down
5. **Select:** Use arrow keys to navigate, Enter to confirm

### Example Workflow

```
# Start nollama
$ nollama

# Select provider: Groq
# Search for model: /llama-3.3
# Start chatting!
>>> What is the capital of France?

# Switch provider mid-conversation
>>> provider
# Select: OpenRouter
# Continue conversation with new provider
```

## Roadmap

- [x] Multi-provider support via LiteLLM
- [x] Dynamic model discovery from provider APIs
- [x] Smart searchable model selection with auto-completion
- [x] Context window (multi-turn conversations)
- [x] Configurable context window size
- [x] Support for Groq
- [x] Support for OpenRouter
- [x] Support for Ollama API
- [x] Support for Anthropic Claude
- [x] Support for OpenAI
- [x] Support for DeepSeek
- [x] Support for Vertex AI
- [ ] Web interface
- [ ] Custom API endpoints
- [ ] Conversation export/import
- [ ] System prompt customization
- [ ] Multi-modal support (images, etc.)

## Contribution

Contributions are welcome! If you have suggestions for new features or improvements, feel free to open an issue or submit a pull request.

## Disclaimer

NoLlama is not affiliated with Ollama. It is an independent project inspired by the concept of providing a neat terminal interface for interacting with language models.

## License

This project is licensed under the [GPL-3.0 License](LICENSE). <br>
[![GNU GPLv3 Image](https://www.gnu.org/graphics/gplv3-127x51.png)](https://www.gnu.org/licenses/gpl-3.0.en.html)

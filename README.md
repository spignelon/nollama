# NoLlama

NoLlama is a terminal-based interface for interacting with Google's Gemini API directly from your terminal. Inspired by [Ollama](https://ollama.com/), NoLlama provides a streamlined experience for chatting with Gemini models like Gemini 2.0 Flash, Gemini 2.5 Flash Preview, and Gemini 2.5 Pro Preview. **Groq and OpenRouter support will be added soon**.

NoLlama offers a neat terminal interface for powerful language models that aren't easily available for local execution, complete with colorful markdown rendering, multiple model choices, and efficient memory usage.

![NoLlama](https://i.imgur.com/0ZOaXwv.png)

## Features

- **Google Gemini Models:** Access to powerful models like Gemini 2.0 Flash, Gemini 2.5 Flash Preview, and Gemini 2.5 Pro Preview.
- **Multi-turn Conversations:** Maintain context between prompts for more coherent conversations.
- **Neat Terminal UI:** Enjoy a clean and intuitive interface for your interactions.
- **Live Streaming Responses:** Watch responses appear in real-time as they're generated.
- **Colorful Markdown Rendering:** Rich text formatting and syntax highlighting in your terminal.
- **Low Memory Usage:** Efficient memory management makes it lightweight compared to using a browser.
- **Easy Model Switching:** Simply type `model` in the chat to switch between models.
- **Clear Chat History:** Type `clear` to clear the chat history.
- **Exit Commands:** Type `q`, `quit`, or `exit` to leave the chat, or use Ctrl+C or Ctrl+D.

## Setup

1. **API Key Configuration:**

   Create a `.nollama` file in your home directory with your Gemini API key:

   ```bash
   echo "GEMINI=your_api_key_here" > ~/.nollama
   ```
   
   You can get a free API key from [Google AI Studio](https://aistudio.google.com/).

2. **Installation:**

   a. Install from PyPI (recommended):

   ```bash
   pip install nollama
   ```

   b. Or clone and install from source:

   ```bash
   git clone https://github.com/spignelon/nollama.git
   cd nollama
   pip install -e .
   ```

3. **Run NoLlama:**

   ```bash
   nollama
   ```

## Usage

- **Select a Model:** At startup, choose from available Gemini models.
- **Chat Normally:** Type your questions and see the responses with rich formatting.
- **Switch Models:** Type `model` in the chat to choose a different model.
- **Clear Chat:** Type `clear` to clear the chat history.
- **Exit:** Type `q`, `quit`, or `exit` to leave the chat, or press Ctrl+C or Ctrl+D.

# Todos
- [x] Add context window
- [ ] Web interface
- [ ] Add support for Groq
- [ ] Add support for OpenRouter
- [ ] Support for APIs

## Contribution

Contributions are welcome! If you have suggestions for new features or improvements, feel free to open an issue or submit a pull request.

## Disclaimer

NoLlama is not affiliated with Ollama. It is an independent project inspired by the concept of providing a neat terminal interface for interacting with language models.

## License

This project is licensed under the [GPL-3.0 License](LICENSE). <br>
[![GNU GPLv3 Image](https://www.gnu.org/graphics/gplv3-127x51.png)](https://www.gnu.org/licenses/gpl-3.0.en.html)

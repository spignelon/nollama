# NoLlama

NoLlama is a terminal-based interface for interacting with large language models (LLMs) that you can't run locally on your laptop. Inspired by [Ollama](https://ollama.com/), NoLlama provides a streamlined experience for chatting with models like GPT-4o, GPT-4o-mini, Claude 3 haiku, Mixtral, LLaMA 70B, and more, directly from your terminal.

While Ollama offers a neat interface for running local LLMs, their performance and capabilities often fall short of these massive models. NoLlama bridges this gap by allowing you to interact with these powerful models using a lightweight terminal UI, complete with colorful markdown rendering, multiple model choices, and efficient memory usage.

![NoLlama](https://i.imgur.com/Py1qESW.png)

## Features

- **Multiple Model Choices:** Switch between various LLMs like GPT-4o, GPT-4o-mini, Mixtral, LLaMA 70B, Claude 3 haiku and more.
- **Neat Terminal UI:** Enjoy a clean and intuitive interface for your interactions.
- **Colorful Markdown Rendering:** Unlike Ollama, NoLlama supports rich text formatting in markdown.
- **Low Memory Usage:** Efficient memory management makes it lightweight compared to using a browser for similar tasks.
- **Easy Model Switching:** Simply type `model` in the chat to switch between models.
- **Clear Chat History:** Type `clear` to clear the chat history.
- **Exit Prompt:** Type `q`, `quit`, or `exit` to leave the chat.
- **Default Mode:** NoLlama runs in standard mode by default—just type `nollama` in the terminal to start.
- **Experimental Feature:** Enable live streaming of output with the `--stream` flag (unstable).
- **Anonymous and Private Usage:** Use `torsocks` to route all traffic through the Tor network for privacy.

## Installation

1. **Download the Binary:**

    Download the latest binary from the [Releases](https://github.com/spignelon/nollama/releases) page.

2. **Move the Binary to `/usr/bin/`:**

    After downloading, move the binary to `/usr/bin/` for easy access from anywhere in your terminal:

    ```bash
    sudo mv nollama /usr/bin/
    ```

3. **Run NoLlama:**

    Start NoLlama from the terminal by simply typing:

    ```bash
    nollama
    ```

    This will start NoLlama in the default mode.

## Building from Source

If you'd like to build NoLlama from source, follow these steps:

1. **Clone the Repository:**

    ```bash
    git clone https://github.com/spignelon/nollama.git
    cd nollama
    ```

2. **Install Dependencies:**

    You can install the required dependencies using `pip`:
    Creating a python virtual environment:
    ```bash
    virtualenv .venv
    source .venv/bin/activate
    ```

    ```bash
    pip install -r requirements.txt
    ```

3. **Compile the Script (Optional):**

    If you want to compile the script into a standalone executable, you can use PyInstaller:

    First set `version_check: bool = False` in `.venv/lib/python3.12/site-packages/g4f/debug.py`

    Then:
    ```bash
    pyinstaller --onefile --name=nollama --collect-all readchar nollama.py
    ```

4. **Move the Executable to `/usr/bin/`:**

    After compilation, move the binary to `/usr/bin/`:

    ```bash
    sudo mv dist/nollama /usr/bin/nollama
    ```

5. **Run NoLlama:**

    Start NoLlama by typing:

    ```bash
    nollama
    ```

## Usage

- **Switch Models:** Type `model` in the chat to choose a different LLM.
- **Clear Chat:** Type `clear` to clear the chat history.
- **Exit:** Type `q`, `quit`, or `exit` to leave the chat.
- **Default Mode:** Run NoLlama without any flags for standard operation:

    ```bash
    nollama
    ```

## Anonymous and Private Usage

For enhanced privacy and anonymity, you can use `torsocks` to route NoLlama's traffic through the Tor network. This ensures that all requests are anonymized and cannot be traced back to you.

### Step 1: Install Tor

#### Debian/Ubuntu:

```bash
sudo apt update
sudo apt install tor
```

#### Arch Linux:

```bash
sudo pacman -S tor
```

#### Fedora:

```bash
sudo dnf install tor
```

### Step 2: Enable and Start Tor

After installation, you need to enable and start the Tor service:

```bash
sudo systemctl enable tor
sudo systemctl start tor
```

### Step 3: Run NoLlama with Tor

Once Tor is running, you can use `torsocks` to run NoLlama anonymously:

```bash
torsocks nollama
```

This will ensure that all your interactions with NoLlama are routed through the Tor network, providing a layer of privacy and anonymity.

## Experimental Feature

- **Streaming Mode:**

    NoLlama includes an experimental streaming mode that allows you to see responses as they are generated. This mode is currently unstable and may cause issues. To enable streaming, use the `--stream` flag:

    ```bash
    nollama --stream
    ```

## Contribution

Contributions are welcome! If you have suggestions for new features or improvements, feel free to open an issue or submit a pull request.

## Acknowledgments

- **[g4f](https://pypi.org/project/g4f/):** Used for connecting to various LLMs.
- **[Python Rich](https://pypi.org/project/rich/):** Used for colorful markdown rendering and improved terminal UI.

## Disclaimer

NoLlama is not affiliated with Ollama. It is an independent project inspired by the concept of providing a neat terminal interface for interacting with language models, particularly those that are too large to run locally on typical consumer hardware or not available for self hosting.

## License

This project is licensed under the [GPL-3.0 License](LICENSE). <br>
[![GNU GPLv3 Image](https://www.gnu.org/graphics/gplv3-127x51.png)](https://www.gnu.org/licenses/gpl-3.0.en.html)
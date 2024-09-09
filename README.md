# Flux Generator Bot

This project is a Telegram bot that generates images using a flux model based on user prompts. It integrates with a local ComfyUI server to process image generation requests.

## Prerequisites

- Python 3.7+
- ComfyUI server running locally
- Telegram Bot Token

## Installation

1. Clone the repository:
   ```bash
   git clone https://github.com/yourusername/flux-generator-bot.git
   cd flux-generator-bot
   ```

2. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

3. Set up environment variables:
   Create a `.env` file in the project root and add your Telegram Bot Token:
   ```bash
   TELEGRAM_BOT=your_telegram_bot_token_here
   ```

4. Ensure your ComfyUI server is running on `127.0.0.1:8188`.

## Configuration

1. Update the `AUTHORIZED_USERS` list in `flux_generator_bot.py` with the Telegram user IDs that are allowed to use the bot.

2. Ensure the workflow JSON files (`workflow_api_flux_dev.json`, `workflow_api_flux_dev_lora.json`, and `workflow_api_lora_Tami.json`) are present in the project directory.

## Running the Bot

To start the bot, run:

```
python Comffi\ files/scripts/flux_generator_bot.py
```

## Usage

1. Start a chat with your bot on Telegram.
2. Use the `/start` command to initiate the bot.
3. Use the `/steps` command followed by a number to set the number of steps for image generation (e.g., `/steps 20`).
4. Send any text message to generate an image based on that prompt.

## Features

- Image generation based on text prompts
- Adjustable steps for image generation
- Authorization check for bot usage
- Support for different workflows (default, 'Y' for lora, 'T' for Tami lora)

## Project Structure

- `flux_generator_bot.py`: Main bot script
- `websockets_api.py`: Handles communication with the ComfyUI server
- `requirements.txt`: List of Python dependencies
- Workflow JSON files: Define the image generation workflows

## Contributing

Please feel free to submit issues or pull requests if you have suggestions for improvements or find any bugs.

## License

[Specify your license here]

## Acknowledgements

This project uses the ComfyUI backend for image generation and the python-telegram-bot library for the Telegram bot functionality.

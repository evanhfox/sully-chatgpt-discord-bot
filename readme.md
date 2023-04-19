[![CodeQL Scanning](https://github.com/evanhfox/sully-chatgpt-discord/actions/workflows/github-code-scanning/codeql/badge.svg?branch=main)](https://github.com/evanhfox/sully-chatgpt-discord/actions/workflows/github-code-scanning/codeql)
[![Trivy Container Scanning](https://github.com/evanhfox/sully-chatgpt-discord/actions/workflows/trivy.yml/badge.svg)](https://github.com/evanhfox/sully-chatgpt-discord/actions/workflows/trivy.yml)
[![Build Status](https://github.com/evanhfox/sully-chatgpt-discord/actions/workflows/main.yml/badge.svg)](https://github.com/evanhfox/sully-chatgpt-discord/actions/workflows/main.yml)

# ChatGPT Discord Bot

This Discord bot enables users to interact with OpenAI's ChatGPT within a Discord server. The bot allows users to ask questions or provide prompts, and it responds with generated content from ChatGPT.

## Features

- Simple command to query ChatGPT: `!ask`
- Rate limiting to prevent spamming ChatGPT requests
- Maintains a basic understanding of conversations for more coherent responses.
- Basic error handling for OpenAI API and Discord API issues

## Installation

### Prerequisites

- Python 3.8 or higher
- Docker (optional, for containerized deployment)

### Setting Up the Project

1. Clone the repository:

`git clone https://github.com/evanhfox/sully-chatgpt-discord.git`

`cd sully-chatgpt-discord` 

2. Install the required Python packages:

`pip3 install -r requirements.txt`

3. Set up the required environment variables:
```
export DISCORD_BOT_TOKEN=your-discord-bot-token
export OPENAI_API_KEY=your-openai-api-key
```

Replace `your-discord-bot-token` and `your-openai-api-key` with your actual tokens.

### Running the Bot

#### Without Docker

Simply run the `chatgpt_discord_bot.py` script:

`python3 bot.py`

#### With Docker

Note: [A Docker image based on Apline is available for public use here.](https://github.com/evanhfox/sully-chatgpt-discord/pkgs/container/sully-chatgpt-discord/86517351?tag=latest) This docker image is updated with all new stable builds and is also re-built if any critical vulnerabilities are detected on a daily basis.

1. Build the Docker image:

`docker build -t chatgpt-discord-bot .`

2. Run the Docker container:

`docker run -e DISCORD_BOT_TOKEN=your-discord-bot-token -e OPENAI_API_KEY=your-openai-api-key --name chatgpt-discord-bot chatgpt-discord-bot`

Replace `your-discord-bot-token` and `your-openai-api-key` with your actual tokens.

## Adding the Bot to Your Discord Server

1. Go to the [Discord Developer Portal](https://discord.com/developers/applications) and sign in with your Discord account.

2. Click on the "New Application" button in the top right corner, and give your application a name.

3. Navigate to the "Bot" tab on the left side menu, and click "Add Bot" to create a new bot.

4. Under the "Token" section, click "Copy" to copy your bot's token. This is the `DISCORD_BOT_TOKEN` you'll use in the environment variable.

5. Go to the "OAuth2" tab on the left side menu, scroll down to the "Authorization Method" and select "In-App Authorization". From the now visible "Scopes" section select "bot" scope.

6. In the "Bot Permissions" section, select the following permissions: "Send Messages", "Manage Messages" and "Read Message Content".

7. After selecting the appropriate permissions, a URL will be generated in the "Scopes" section. Copy this URL and paste it into your browser.

8. Choose the server you want to add the bot to, and click "Authorize". You may be prompted to complete a CAPTCHA.

9. The bot should now be added to your server and is ready to use once you run it.

## Usage

To interact with the ChatGPT Discord bot, use the `!ask` command followed by your question or prompt:
Example:
!ask What is the capital of France?
<ChatGPT Response>
!ask Are you sure about that?
<Further ChatGPT Response>

To clear a current conversation, a discord user can yse the `!reset` command to clear the conversation history.

To cleanup the current discord channel a discord user with the role "Admin" can use the `!clear` command to clear all messages.

The bot will respond with the generated content from ChatGPT.

## Customization

You can customize the rate limiting, error handling, and other settings in the `bot.py` script according to your specific requirements.

## License

This project is licensed under the [MIT License](LICENSE).

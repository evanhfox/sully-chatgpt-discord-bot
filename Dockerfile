# Use the latest Alpine base image with Python
FROM python:3-alpine

# Set the working directory
WORKDIR /app

# Copy the requirements.txt file into the container
COPY requirements.txt .

# Install the required packages
RUN pip install --no-cache-dir -r requirements.txt

# Copy the chatgpt_discord_bot.py script into the container
COPY chatgpt_discord_bot.py .

# Run the chatgpt_discord_bot.py script when the container starts
CMD ["python", "chatgpt_discord_bot.py"]

# Note - this discord bot requires environment variables to be set. To do this securely,
# you need to pass the environment variables as the docker container is being ran instead of doing so 
# directly in this dockerfile. Other methods could exist depending on how you plan to run this continer 
# (K8S Secrets, etc)
#
# Environmental Variables Required
#
# Replace <your-discord-bot-token> and <your-openai-api-key> with your actual tokens.
# Example: docker run -e DISCORD_BOT_TOKEN=<your-discord-bot-token> -e OPENAI_API_KEY=<your-openai-api-key> --name chatgpt-discord-bot chatgpt-discord-bot
#
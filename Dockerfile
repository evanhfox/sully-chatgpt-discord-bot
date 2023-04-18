# Set the base image to the most recent Alpine Linux
FROM alpine:latest

# Install necessary packages
RUN apk update && \
    apk add --no-cache python3 py3-pip

# Set the working directory
WORKDIR /app

# Copy the requirements file and install dependencies
COPY requirements.txt /app/
RUN pip3 install -r requirements.txt

# Copy the rest of the code
COPY bot.py /app/

# Start the bot
CMD ["python3", "bot.py"]

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
import os
import time
import asyncio
import openai
import discord
from discord.ext import commands

# Set up your OpenAI API key
openai.api_key = os.environ["OPENAI_API_KEY"]

# Set up your Discord bot token
TOKEN = os.environ["DISCORD_BOT_TOKEN"]

# Define the required intents
intents = discord.Intents.default()
intents.message_content = True

# Set up your bot
bot = commands.Bot(command_prefix="!", intents=intents)

# Rate limiting variables
rate_limit_time = 10  # seconds
rate_limit_dict = {}

async def query_chatgpt(prompt):
    try:
        response = openai.Completion.create(
            engine="text-davinci-002",
            prompt=prompt,
            max_tokens=150,
            n=1,
            stop=None,
            temperature=0.8,
        )
    except openai.Error as e:
        print(f"OpenAI error: {e}")
        return "Error: Failed to query ChatGPT. Please try again later."

    return response.choices[0].text.strip()

async def check_rate_limit(user_id):
    try:
        if user_id in rate_limit_dict:
            time_remaining = rate_limit_time - (time.time() - rate_limit_dict[user_id])
            if time_remaining > 0:
                return time_remaining
        rate_limit_dict[user_id] = time.time()
        return 0
    except Exception as e:
        print(f"Rate limiting error: {e}")
        return -1

@bot.command(name="ask")
async def ask(ctx, *, question):
    try:
        time_remaining = await check_rate_limit(ctx.author.id)
        if time_remaining > 0:
            await ctx.send(f"Please wait {time_remaining:.1f} seconds before sending another request.")
            return
        elif time_remaining == -1:
            await ctx.send("Error: Rate limiting failed. Please try again later.")
            return

        prompt = f"{question}"
        response = await query_chatgpt(prompt)
        await ctx.send(response)
    except discord.errors.HTTPException as e:
        print(f"Discord API error: {e}")
        await ctx.send("Error: Failed to send message. Please try again later.")
    except Exception as e:
        print(f"Unknown error: {e}")
        await ctx.send("Error: An unknown error occurred. Please try again later.")

@bot.event
async def on_ready():
    print(f"{bot.user.name} has connected to Discord!")

bot.run(TOKEN)

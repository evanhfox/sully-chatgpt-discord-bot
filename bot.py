import os
import time
import openai
import discord
from discord.ext import commands

# Set up your OpenAI API key
try:
    openai.api_key = os.environ["OPENAI_API_KEY"]
    TOKEN = os.environ["DISCORD_BOT_TOKEN"]
except KeyError as e:
    raise ValueError("Missing environment variable: {}".format(str(e))) from None

# Define the required intents
intents = discord.Intents.default()
intents.message_content = True

# Set up your bot
bot = commands.Bot(command_prefix="!", intents=intents, case_insensitive=True)

# Rate limiting variables
rate_limit_time = 10  # seconds
rate_limit_dict = {}


async def query_chatgpt(prompt):
    try:
        completion = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",
            messages=[{"role": "user", "content": prompt}]
        )
    except openai.error.OpenAIError as e:
        raise ValueError("Error communicating with OpenAI API: {}".format(str(e))) from None
    return completion.choices[0].message.content


async def check_rate_limit(user_id):
    try:
        if user_id in rate_limit_dict:
            time_remaining = rate_limit_time - (time.time() - rate_limit_dict[user_id])
            if time_remaining > 0:
                return time_remaining
        rate_limit_dict[user_id] = time.time()
        return 0
    except Exception as e:
        raise ValueError("Error with rate limiting logic: {}".format(str(e))) from None


@bot.command(name="ask", help="Ask GPT-3.5 Turbo a question or send a message")
async def ask(ctx, *, question):
    try:
        time_remaining = await check_rate_limit(ctx.author.id)
        if time_remaining > 0:
            await ctx.send(f"{ctx.author.mention}, please wait {time_remaining:.1f} seconds before sending another request.")
            return
        elif time_remaining == -1:
            await ctx.send(f"{ctx.author.mention}, error: Rate limiting failed. Please try again later.")
            return

        prompt = f"{question.lower()}"
        response = await query_chatgpt(prompt)
        await ctx.send(f"{ctx.author.mention}, {response}")
    except discord.errors.HTTPException as e:
        raise ValueError("Error sending message to Discord: {}".format(str(e))) from None
    except Exception as e:
        raise ValueError("Unknown error: {}".format(str(e))) from None


@bot.event
async def on_ready():
    print(f"{bot.user.name} has connected to Discord!")

bot.run(TOKEN)

import os
import time
import openai
import discord
from discord.ext import commands

try:
    openai.api_key = os.environ["OPENAI_API_KEY"]
    TOKEN = os.environ["DISCORD_BOT_TOKEN"]
except KeyError as e:
    raise ValueError("Missing environment variable: {}".format(str(e))) from None

intents = discord.Intents.default()
intents.message_content = True

bot = commands.Bot(command_prefix="!", intents=intents, case_insensitive=True)

rate_limit_time = 5  # seconds
rate_limit_dict = {}
conversation_history = {}


async def query_chatgpt(messages):
    try:
        completion = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",
            messages=messages
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


@bot.command(name="ask", help="Ask GPT-3.5 Turbo a question or send a message. To do this, use the !ask followed by your question or prompt.")
async def ask(ctx, *, question):
    try:
        user_id = ctx.author.id
        time_remaining = await check_rate_limit(user_id)
        if time_remaining > 0:
            await ctx.send(f"{ctx.author.mention}, please wait {time_remaining:.1f} seconds before sending another request.")
            return
        elif time_remaining == -1:
            await ctx.send(f"{ctx.author.mention}, error: Rate limiting failed. Please try again later.")
            return

        if user_id not in conversation_history:
            conversation_history[user_id] = []

        conversation_history[user_id].append({"role": "user", "content": question})
        response = await query_chatgpt(conversation_history[user_id])
        conversation_history[user_id].append({"role": "assistant", "content": response})

        # Trim conversation history if it becomes too long
        if len(conversation_history[user_id]) > 10:
            conversation_history[user_id] = conversation_history[user_id][-10:]

        await ctx.send(f"{ctx.author.mention}, {response}")
    except discord.errors.HTTPException as e:
        raise ValueError("Error sending message to Discord: {}".format(str(e))) from None
    except Exception as e:
        raise ValueError("Unknown error: {}".format(str(e))) from None


@bot.event
async def on_ready():
    print(f"{bot.user.name} has connected to Discord!")

bot.run(TOKEN)
import os
import time
import openai
import discord
from discord.ext import commands
import datetime

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
            model="gpt-4",
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


@bot.command(name="reset", help="Reset your conversation history with GPT-3.5 Turbo. To do this, use the !reset command.")
async def reset(ctx):
    user_id = ctx.author.id
    if user_id in conversation_history:
        del conversation_history[user_id]
        await ctx.send(f"{ctx.author.mention}, your conversation history has been reset.")
    else:
        await ctx.send(f"{ctx.author.mention}, there is no conversation history to reset.")


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
        if len(conversation_history[user_id]) > 25:
            conversation_history[user_id] = conversation_history[user_id][-25:]

        await ctx.send(f"{ctx.author.mention}, {response}")
    except discord.errors.HTTPException as e:
        raise ValueError("Error sending message to Discord: {}".format(str(e))) from None
    except Exception as e:
        raise ValueError("Unknown error: {}".format(str(e))) from None

@bot.command(name="clear", help="Delete all messages in the current channel. Only usable by members with the 'Admin' role.")
@commands.has_role("Admin")
async def clear(ctx):
    try:
        # Code to set only deletion after 14 days
        # def is_old_message(message):
        #     # Get the current time in UTC with timezone information
        #     now = datetime.datetime.now(datetime.timezone.utc)

        #     # Convert the message creation time to a naive datetime object
        #     created_at_naive = message.created_at.astimezone(None)

        #     # Returns True if the message is older than 14 days
        #     return (now - created_at_naive) > datetime.timedelta(days=14)

        def is_old_message(message):
            # Always return True to delete all messages
            return True

        # Use the bulk_delete method to delete all messages in the channel
        deleted_messages = await ctx.channel.purge(limit=None, check=is_old_message)

        # Send a confirmation message to the user who executed the command
        await ctx.send(f"{ctx.author.mention}, {len(deleted_messages)} messages in this channel have been deleted.")
    except discord.errors.HTTPException as e:
        raise ValueError("Error deleting messages: {}".format(str(e))) from None
    except Exception as e:
        raise ValueError("Unknown error: {}".format(str(e))) from None


@bot.event
async def on_ready():
    print(f"{bot.user.name} has connected to Discord!")

bot.run(TOKEN)

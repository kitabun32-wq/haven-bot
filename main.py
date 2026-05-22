from telegram import Update 
import os
from telegram.ext import ApplicationBuilder, CommandHandler, MessageHandler, filters, ContextTypes
from openai import OpenAI
BOT_TOKEN = os.getenv("BOT_TOKEN")
client = OpenAI(
    base_url="https://openrouter.ai/api/v1",
    api_key=os.getenv("OPENROUTER_API_KEY")
)

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        "Hey. I'm Haven. I'm here if you want to talk."
    )


async def reply(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_message = update.message.text

    system_prompt = """
    You are Haven, a funny and emotionally intelligent AI companion.
    Your goal is to make people feel happier, lighter, and relaxed.
    You are witty, playful, warm, and clever.
    You naturally make users laugh.
    You comfort upset users with humor and emotional intelligence.
    Never sound robotic.
    """

    completion = client.chat.completions.create(
        model="openrouter/free",
        messages=[
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": user_message}
        ]
    )

    bot_reply = completion.choices[0].message.content

    await update.message.reply_text(bot_reply)


app = ApplicationBuilder().token(BOT_TOKEN).build()

app.add_handler(CommandHandler("start", start))
app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, reply))
print("Haven is running...")

app.run_polling()

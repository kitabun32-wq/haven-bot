from telegram import Update 
import os
from telegram.ext import ApplicationBuilder, CommandHandler, MessageHandler, filters, ContextTypes
from openai import OpenAI
BOT_TOKEN = "8904215890:AAG7-PbRJJKVNQ3wayS52nm-J8O8WUIEe4w"
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

    completion = client.chat.completions.create(
        model="openrouter/free",
        messages=[
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

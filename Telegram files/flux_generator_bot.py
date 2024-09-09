import os
from telegram import Update, InputFile, BotCommand
from telegram.ext import ApplicationBuilder, CommandHandler, MessageHandler, filters, ContextTypes
from PIL import Image
import websockets_api as flux_model
import io

TOKEN = "6722764728:AAFmjdSDjun1izL1-1X_7Go4Ljrr8M7vV9w"
AUTHORIZED_USERS = [357036102]  # List of authorized user IDs

def is_authorized(user_id: int) -> bool:
    return user_id in AUTHORIZED_USERS

async def check_authorization(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if not is_authorized(update.effective_user.id):
        await update.message.reply_text("You are not authorized to use this bot.")
        return False
    return True

steps_value = 20
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    if not await check_authorization(update, context):
        return
    await update.message.reply_text('Hello! Send any message, and I will echo it back with a greeting and an image.')

async def steps(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    if not await check_authorization(update, context):
        return
    try:
        # Get the number of steps from the user's command
        steps_value = int(context.args[0])
        context.user_data['steps'] = steps_value
        await update.message.reply_text(f"Steps set to {steps_value}.")
    except (IndexError, ValueError):
        await update.message.reply_text("Please provide a valid number of steps. Usage: /steps <number>")


async def echo(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    if not await check_authorization(update, context):
        return
    # Get the user's message
    user_message = update.message.text
    steps = context.user_data.get('steps', 10)
    images = flux_model.load_prompt(user_message[1:], steps, user_message[0])  # Replace with your actual image loading function
    for node_id in images:
        for image_byte_array in images[node_id]:
            # Send image to user with a caption
            await update.message.reply_photo(photo=image_byte_array, caption=f"{user_message}\n Steps = {steps}")

    
    
    # Send the response message
    #await update.message.reply_text(user_message)
async def setup_commands(application):
    commands = [
        BotCommand("start", "Start the bot"),
        BotCommand("steps", "Show steps"),
    ]
    await application.bot.set_my_commands(commands)

def main() -> None:
    # Create the Application
    application = ApplicationBuilder().token(TOKEN).build()

    # Register the /start command handler
    application.add_handler(CommandHandler("start", start))

    # Register the /steps command handler
    application.add_handler(CommandHandler("steps", steps))

    # Register a handler for all text messages
    application.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, echo))

    # Start the bot
    application.run_polling()

    # Set up commands
    application.job_queue.run_once(setup_commands, 0)

if __name__ == '__main__':
    main()
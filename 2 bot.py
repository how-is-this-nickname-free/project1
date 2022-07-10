import logging
from random import choice, sample

from telegram.ext import ApplicationBuilder, ContextTypes, CommandHandler, \
    MessageHandler, filters, InlineQueryHandler
from telegram import Update, InlineQueryResultArticle, InputTextMessageContent

import emoji.unicode_codes.data_dict as codes


TOKEN = '5559983919:AAFVdGEtjta79Dw1ouGkcPLr1sFYTpaEHa8'
RESPONSES = [
    "As I see it, yes.", "Ask again later.", "Better not tell you now.",
    "Cannot predict now.", "Concentrate and ask again.",
    "Don’t count on it.", "It is certain.", "It is decidedly so.",
    "Most likely.", "My reply is no.", "My sources say no.",
    "Outlook not so good.", "Outlook good.", "Reply hazy, try again.",
    "Signs point to yes.", "Very doubtful.", "Without a doubt.", "Yes.",
    "Yes – definitely.", "You may rely on it."
]
EMOJIS = list(codes.EMOJI_DATA.keys())

logging.basicConfig(
    filename='2bot_logs.log',
    format='%(asctime)s--%(name)s--%(levelname)s--%(message)s',
    level=logging.INFO
)


async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    first_name = update.message.from_user.first_name
    await context.bot.send_message(
        chat_id=update.effective_chat.id,
        text=f'Hello {first_name}!'
    )


async def eight_ball(update: Update, context: ContextTypes.DEFAULT_TYPE):
    question = ' '.join(context.args)
    if question == '':
        await context.bot.send_message(
            chat_id=update.effective_chat.id,
            text='...'
        )
    else:
        response = choice(RESPONSES)
        await context.bot.send_message(
            chat_id=update.effective_chat.id,
            text=response
        )


async def random_emoji(update: Update, context: ContextTypes.DEFAULT_TYPE):
    emoji = choice(EMOJIS)
    print(emoji)
    await context.bot.send_message(
        chat_id=update.effective_chat.id,
        text=emoji
    )


async def say(update: Update, context: ContextTypes.DEFAULT_TYPE):
    text = update.message.text
    await context.bot.send_message(
        chat_id=update.effective_chat.id,
        text=text
    )
    await context.bot.send_message(
        chat_id=update.effective_chat.id,
        text='I`m your echo',
        reply_to_message_id=update.message.id
    )


async def unknown_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await context.bot.send_message(
        chat_id=update.effective_chat.id,
        text='Sorry, this command is unsupported'
    )


async def inline_emoji(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.inline_query.query
    emoji1, emoji2, emoji3 = sample(EMOJIS, k=3)
    results = [InlineQueryResultArticle(
        id=emoji1,
        title=emoji1,
        input_message_content=InputTextMessageContent(emoji1)
    ), InlineQueryResultArticle(
        id=emoji2,
        title=emoji2,
        input_message_content=InputTextMessageContent(emoji2)
    ), InlineQueryResultArticle(
        id=emoji3,
        title=emoji3,
        input_message_content=InputTextMessageContent(emoji3)
    )]
    await context.bot.answer_inline_query(update.inline_query.id, results)


if __name__ == '__main__':
    application = ApplicationBuilder().token(TOKEN).build()

    start_handler = CommandHandler('start', start)
    application.add_handler(start_handler)

    eight_ball_handler = CommandHandler('ask', eight_ball)
    application.add_handler(eight_ball_handler)

    rnd_emoji = CommandHandler('emoji', random_emoji)
    application.add_handler(rnd_emoji)

    inline_emoji_handler = InlineQueryHandler(inline_emoji)
    application.add_handler(inline_emoji_handler)

    echo_handler = MessageHandler(filters.TEXT & (~filters.COMMAND), say)
    application.add_handler(echo_handler)

    unknown_handler = MessageHandler(filters.COMMAND, unknown_command)
    application.add_handler(unknown_handler)

    application.run_polling()

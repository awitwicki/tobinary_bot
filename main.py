import os

import requests
from telegram import ParseMode
from telegram import InlineQueryResultArticle, ParseMode, InputTextMessageContent, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import Updater, InlineQueryHandler, CommandHandler
from telegram.utils.helpers import escape_markdown
# from logs import logger
from uuid import *

# t.me/tobinary_bot
bot_token = os.getenv('TOBINARYBOT_TELEGRAM_TOKEN')
influx_query_url = os.getenv('TOBINARYBOT_INFLUX_QUERY')

def influx_query(query_str: str):
    if influx_query:
        try:
            url = influx_query_url
            headers = {'Content-Type': 'application/Text'}

            x = requests.post(url, data=query_str.encode('utf-8'), headers=headers)
        except Exception as e:
            print(e)


def start(update, context):
    influx_query('bots,botname=tobinarybot,actiontype=message action=true')

    keyboard = [
        [InlineKeyboardButton("Начать работу здесь", switch_inline_query_current_chat='')],
        [InlineKeyboardButton("Выслать в чат", switch_inline_query='')]
        ]
    reply_markup = InlineKeyboardMarkup(keyboard)

    start_msg = 'Привет, меня зовут @tobinary\\_bot, я помогу '\
        'тебе закодировать текст в бинарный код, '\
        'упомяни мой ник в чате через @ и впиши свой текст'

    update.message.reply_text(start_msg, parse_mode=ParseMode.MARKDOWN, reply_markup=reply_markup)


def inlinequery(update, context):
    """Handle the inline query."""
    influx_query('bots,botname=tobinarybot,actiontype=inline action=true')

    query = update.inline_query.query
    if not query:
        query = "@tobinary_bot - впиши текст или число"
        results = [
        InlineQueryResultArticle(
            id=uuid4(),
            title=query,
            input_message_content=InputTextMessageContent(query))
        ]
    else:

        binary_text = query + " = " + ' '.join(format(ord(x), 'b') for x in query)

        results = [
            InlineQueryResultArticle(
                id=uuid4(),
                title="To binary string: " + binary_text[:15] + '...',
                input_message_content=InputTextMessageContent(binary_text)),
            ]

        #int to bin or hex
        try:
            number = int(query)

            int_to_binary = query + " = " + bin(number)
            int_to_hex = query + " = " + hex(number)

            results.append(
                InlineQueryResultArticle(
                    id=uuid4(),
                    title="Int To Binary: " + int_to_binary,
                    input_message_content=InputTextMessageContent(int_to_binary)))

            results.append(
                InlineQueryResultArticle(
                    id=uuid4(),
                    title="Int To Hex: " + int_to_hex,
                    input_message_content=InputTextMessageContent(int_to_hex)))
        except:
            pass

        #bin int
        try:
            number_bin = f'{query} = {int(query,2)}'

            results.append(
                InlineQueryResultArticle(
                    id=uuid4(),
                    title="Binary to Int: " + number_bin,
                    input_message_content=InputTextMessageContent(str(number_bin))))
        except:
            pass

        #hex int
        try:
            number_hex = f'{query} = {int(query,16)}'

            results.append(
                InlineQueryResultArticle(
                    id=uuid4(),
                    title="Hex to Int: " + number_hex,
                    input_message_content=InputTextMessageContent(str(number_hex))))
        except:
            pass

    update.inline_query.answer(results, cache_time=0)


def error(update, context):
    """Log Errors caused by Updates."""
    influx_query('bots,botname=tobinarybot,actiontype=errors error=true')

    # logger.warning('Update "%s" caused error "%s"', update, context.error)


def main():
    # logger.info(f"Application started")

    #setup telegram bot
    updater = Updater(bot_token, use_context=True)

    # Get the dispatcher to register handlers
    dp = updater.dispatcher

    # message handlers
    dp.add_handler(CommandHandler("start", start))
    dp.add_handler(InlineQueryHandler(inlinequery))

    # log all errors
    dp.add_error_handler(error)

    # logger.info(f"Starting bot")

    # Start the Bot
    updater.start_polling()

    # Run the bot until you press Ctrl-C or the process receives SIGINT,
    # SIGTERM or SIGABRT. This should be used most of the time, since
    # start_polling() is non-blocking and will stop the bot gracefully.
    updater.idle()

if __name__ == '__main__':
    main()

from pyrogram.types import InlineKeyboardButton
from pyrogram.types import InlineQueryResultArticle
from pyrogram.types import InputTextMessageContent

from pykeyboard import InlineKeyboard

from nana import app


async def inline_search(string, answers):
    query = string.split(None, 1)[1]
    async for message in app.search_global(query, limit=50):
        chat = message.chat
        keyboard = InlineKeyboard(row_width=2)
        keyboard.add(
            InlineKeyboardButton(
                'Link',
                url=message.link,
            ),
        )
        try:
            text = message.text[:99] + '...'
        except TypeError:
            text = message.caption[:99] + '...'
        answers.append(
            InlineQueryResultArticle(
                title=f'From: {chat.title} | {chat.id}',
                description=text,
                input_message_content=InputTextMessageContent(
                    f'**Chat:** `{chat.id}`\n\n' + text,
                    parse_mode='markdown',
                ),
                reply_markup=keyboard,
            ),
        )

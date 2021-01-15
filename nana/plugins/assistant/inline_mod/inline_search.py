from pyrogram.types import InlineKeyboardButton
from pyrogram.types import InlineQueryResultArticle
from pyrogram.types import InputTextMessageContent

from pykeyboard import InlineKeyboard

from nana import app


async def inline_search(string, answers):
    query = string.split(None, 1)[1]
    async for message in app.search_global(query, limit=50):
        user = message.from_user
        keyboard = InlineKeyboard(row_width=2)
        keyboard.add(
            InlineKeyboardButton(
                'Link',
                url=message.link,
            ),
            InlineKeyboardButton(
                'User',
                url=f'tg://user?id={user.id}',
            ),
        )
        thumbnail = f'https://t.me/{user.username}' if user.username else None
        try:
            text = message.text[:45] + '...'
        except TypeError:
            text = message.caption[:45] + '...'
        chat = message.chat.id
        answers.append(
            InlineQueryResultArticle(
                title=f'From: {user.first_name} | {user.id}',
                description=text,
                input_message_content=InputTextMessageContent(
                    f'**From:** `{user.id}`\n**Chat: **`{chat}`\n\n' + text,
                    parse_mode='markdown',
                ),
                reply_markup=keyboard,
                thumb_url=thumbnail,
            ),
        )

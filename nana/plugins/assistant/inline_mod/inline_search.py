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
        answers.append(
            InlineQueryResultArticle(
                title=f'From: {user.first_name} | {user.id}',
                description=message.text,
                input_message_content=InputTextMessageContent(
                    message.text[:60] + '...',
                    parse_mode='markdown',
                ),
                thumb_url=user.photo.small_file_id or None,
            ),
        )

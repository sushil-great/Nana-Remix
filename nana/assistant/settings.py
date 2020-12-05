from platform import python_version

import heroku3
from pyrogram import filters, errors
from pyrogram.types import InlineKeyboardButton, InlineKeyboardMarkup
from nana import (
    AdminSettings,
    setbot,
    app,
    USERBOT_VERSION,
    ASSISTANT_VERSION,
    DB_AVAILABLE,
    HEROKU_API,
    NANA_IMG,
)
from nana.__main__ import reload_userbot, restart_all
from nana.assistant.__main__ import dynamic_data_filter
from nana.tr_engine.strings import tld


async def is_userbot_run():
    try:
        return await app.get_me()
    except ConnectionError:
        return None


async def get_text_settings():
    me = await is_userbot_run()
    if not me:
        text = tld("settings_userbot_stop").format(USERBOT_VERSION)
    else:
        text = tld("settings_userbot_running").format(USERBOT_VERSION)
    text += tld("settings_assistant_running").format(ASSISTANT_VERSION)
    text += tld("settings_database").format(DB_AVAILABLE)
    text += tld("settings_python").format(python_version())
    return text


async def get_button_settings():
    me = await is_userbot_run()
    toggle = (
        tld("settings_userbot_stopbutton")
        if me
        else tld("settings_userbot_startbutton")
    )
    list_button = [
        [
            InlineKeyboardButton(toggle, callback_data="toggle_startbot"),
            InlineKeyboardButton(
                tld("settings_userbot_restartbutton"), callback_data="restart_bot"
            ),
        ],
        [
            InlineKeyboardButton(
                tld("settings_setstickerbutton"), callback_data="setsticker"
            )
        ],
    ]
    if HEROKU_API:
        list_button.append(
            [
                InlineKeyboardButton(
                    tld("settings_herokubutton"), callback_data="heroku_vars"
                )
            ]
        )
        list_button.append(
            [
                InlineKeyboardButton(
                    tld("settings_heroku_restartbutton"), callback_data="restart_heroku"
                )
            ]
        )
        list_button.append(
            [
                InlineKeyboardButton(
                    tld("settings_change_repo_button"), callback_data="change_repo"
                )
            ]
        )
    return InlineKeyboardMarkup(list_button)


@setbot.on_message(
    filters.user(AdminSettings) & filters.command(["settings"]) & filters.private
)
async def settings(_, message):
    text = await get_text_settings()
    button = await get_button_settings()
    await setbot.send_photo(
        message.chat.id, NANA_IMG, caption=text, reply_markup=button
    )


@setbot.on_callback_query(dynamic_data_filter("toggle_startbot"))
async def start_stop_bot(client, query):
    try:
        await app.stop()
    except ConnectionError:
        await reload_userbot()
        text = await get_text_settings()
        button = await get_button_settings()
        text += tld("settings_stats_botstart")
        try:
            await query.message.edit_text(text, reply_markup=button)
        except errors.exceptions.bad_request_400.MessageNotModified:
            pass
        await client.answer_callback_query(query.id, tld("settings_stats_botstart"))
        return
    text = await get_text_settings()
    button = await get_button_settings()
    text += tld("settings_stats_botstop")
    try:
        await query.message.edit_text(text, reply_markup=button)
    except errors.exceptions.bad_request_400.MessageNotModified:
        pass
    await client.answer_callback_query(query.id, tld("settings_stats_botstop"))


@setbot.on_callback_query(dynamic_data_filter("restart_bot"))
async def reboot_bot(client, query):
    try:
        await restart_all()
    except ConnectionError:
        await client.answer_callback_query(
            query.id, tld("settings_bot_stoprestart_err")
        )
        return
    text = await get_text_settings()
    text += tld("settings_stats_botrestart")
    button = await get_button_settings()
    try:
        await query.message.edit_text(text, reply_markup=button)
    except errors.exceptions.bad_request_400.MessageNotModified:
        pass
    await client.answer_callback_query(query.id, tld("settings_bot_restarting"))


@setbot.on_callback_query(dynamic_data_filter("restart_heroku"))
async def reboot_heroku(client, query):
    text = await get_text_settings()
    button = await get_button_settings()
    if HEROKU_API is not None:
        text += "\nPlease wait..."
        try:
            await query.message.edit_text(text, reply_markup=button)
        except errors.exceptions.bad_request_400.MessageNotModified:
            pass
        await client.answer_callback_query(
            query.id, tld("settings_bot_restarting_heroku")
        )
        heroku = heroku3.from_key(HEROKU_API)
        heroku_applications = heroku.apps()
        if len(heroku_applications) >= 1:
            heroku_app = heroku_applications[0]
            heroku_app.restart()
        else:
            text += tld("settings_no_heroku_app")
    try:
        await query.message.edit_text(text, reply_markup=button)
    except errors.exceptions.bad_request_400.MessageNotModified:
        pass
    await client.answer_callback_query(query.id, tld("settings_no_heroku_app"))


@setbot.on_callback_query(dynamic_data_filter("heroku_vars"))
async def vars_heroku(_, query):
    text = tld("settings_heroku_config")
    list_button = [
        [
            InlineKeyboardButton("⬅ back️", callback_data="back"),
            InlineKeyboardButton("➕  add️", callback_data="add_vars"),
        ]
    ]
    if HEROKU_API:
        heroku = heroku3.from_key(HEROKU_API)
        heroku_applications = heroku.apps()
        if len(heroku_applications) >= 1:
            app = heroku_applications[0]
            config = app.config()
            # if config["api_id"]:
            #     list_button.insert(0, [InlineKeyboardButton("api_id✅", callback_data="api_id")])
            # else:
            #     list_button.insert(0, [InlineKeyboardButton("api_id🚫", callback_data="api_id")])
            configdict = config.to_dict()
            for x, _ in configdict.items():
                list_button.insert(
                    0, [InlineKeyboardButton("{}✅".format(x), callback_data="tes")]
                )
    button = InlineKeyboardMarkup(list_button)
    await query.message.edit_text(text, reply_markup=button)


# Back button


@setbot.on_callback_query(dynamic_data_filter("back"))
async def back(_, message):
    text = await get_text_settings()
    button = await get_button_settings()
    await setbot.send_photo(
        message.chat.id, NANA_IMG, caption=text, reply_markup=button
    )

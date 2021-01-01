import html
import re


MAX_MESSAGE_LENGTH = 2048


def split_limits(text):
    if len(text) < MAX_MESSAGE_LENGTH:
        return [text]

    lines = text.splitlines(True)
    small_msg = ""
    result = []
    for line in lines:
        if len(small_msg) + len(line) < MAX_MESSAGE_LENGTH:
            small_msg += line
        else:
            result.append(small_msg)
            small_msg = line
    else:
        result.append(small_msg)

    return result


def cleanhtml(raw_html):
    cleanr = re.compile("<.*?>")
    return re.sub(cleanr, "", raw_html)


def escape_markdown(text):
    """Helper function to escape telegram markup symbols."""
    escape_chars = r"\*_`\["
    return re.sub(r"([%s])" % escape_chars, r"\\\1", text)


def mention_html(user_id, name):
    return u'<a href="tg://user?id={}">{}</a>'.format(
        user_id,
        html.escape(name)
    )


def mention_markdown(user_id, name):
    return u"[{}](tg://user?id={})".format(escape_markdown(name), user_id)

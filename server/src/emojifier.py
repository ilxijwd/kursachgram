def emojifier(message):
    emoticons_to_emoji = {
        ':)': '😊',
        ':D': '😃',
        ':(': '☹️',
        ':\'(': '😢',
        ':\')': '😂',
        ':O': '😮',
        ':*': '😗',
        ';)': '😉',
        ':P': '😛',
        ':/': '🤔',
        ':|': '😐'
    }

    for emoticon, emoji in emoticons_to_emoji.items():
        message = message.replace(emoticon, emoji)

    return message

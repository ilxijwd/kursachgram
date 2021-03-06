def emojifier(message):
    emoticons_to_emoji = {
        ':)': 'đ',
        ':D': 'đ',
        ':(': 'âšī¸',
        ':\'(': 'đĸ',
        ':\')': 'đ',
        ':O': 'đŽ',
        ':*': 'đ',
        ';)': 'đ',
        ':P': 'đ',
        ':/': 'đ¤',
        ':|': 'đ'
    }

    for emoticon, emoji in emoticons_to_emoji.items():
        message = message.replace(emoticon, emoji)

    return message

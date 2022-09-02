import unicodedata


def remove_accents(text):
    text = unicodedata.normalize('NFKD', text)

    return "".join([char for char in text if not unicodedata.combining(char)])

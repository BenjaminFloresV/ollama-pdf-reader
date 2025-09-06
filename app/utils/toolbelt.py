


import unicodedata


def normalize_text(text: str, lowercase: bool = True, replace_spaces: bool = True) -> str:
    """
     This function normalizes the text by removing accents and replacing spaces with underscores.
    """
    # 1. Normalize the text to NFD to separate accents
    text_nfd = unicodedata.normalize('NFD', text)
    # 2. Filter only the characters that are not accent marks (Mn)
    text_without_accents = ''.join(
        char for char in text_nfd
        if unicodedata.category(char) != 'Mn'
    )

    if replace_spaces:
        normalized_text = text_without_accents.replace(' ', '_')
    else:
        normalized_text = text_without_accents
        
    if lowercase:
        normalized_text = normalized_text.lower()
    normalized_text = normalized_text.replace('/', '_')
    return normalized_text
import difflib

KNOWN_WORDS = [
    "youtube",
    "google",
    "spotify",
    "github",
    "gmail"
]

def suggest_correction(word, threshold=0.7):
    """
    Returns the closest matching known word
    if similarity is above threshold.
    """
    matches = difflib.get_close_matches(
        word,
        KNOWN_WORDS,
        n=1,
        cutoff=threshold
    )

    if matches:
        return matches[0]

    return None



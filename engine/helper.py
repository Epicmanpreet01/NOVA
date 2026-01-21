import re
import pygetwindow as gw

def yt_term_extraction(term):
    pattern = r'play\s+(.*?)\s+on\s+youtube'
    match = re.search(pattern,term, re.IGNORECASE)
    return match.group(1) if match else None

def removeWords(input_string: str,wordsToRemove):
    words = input_string.split()
    filtered_words = [word for word in words if word.lower() not in wordsToRemove]
    result_string = ' '.join(filtered_words)
    return result_string

def is_window_open(window_name):
    windows = gw.getWindowsWithTitle(window_name)
    return len(windows) > 0
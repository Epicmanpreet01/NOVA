import re
import win32gui
#helper functions that can be used in any file

#youtube link extraction
def yt_term_extraction(term):
    pattern = r'play\s+(.*?)\s+on\s+youtube'
    match = re.search(pattern,term, re.IGNORECASE)
    return match.group(1) if match else None

#removing unnecessary words from command
def removeWords(input_string: str,wordsToRemove):
    words = input_string.split()
    filtered_words = [word for word in words if word.lower() not in wordsToRemove]
    result_string = ' '.join(filtered_words)
    return result_string

def is_window_open(window_name):
    hwnd = win32gui.FindWindow(None, window_name) 

    return hwnd is not None
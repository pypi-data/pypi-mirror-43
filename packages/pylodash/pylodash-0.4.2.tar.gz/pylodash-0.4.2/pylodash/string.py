import re 
import pylodash.arrays as _

def camelCase(string=''):
    items = replace_special_characters(string)

    # format first letter for word
    result = [item.lower() if index == 0 else item[0].upper() + item[1:].lower() for index, item in enumerate(items)]

    return ''.join(result)

def replace_special_characters(string=''):
    # remove all special characters base on pattern
    items = re.split('[-_*)( %^$#@!]', string)

    # remove all elements is empty, None, False
    return _.compact(items)

def capitalize(string=''):
    return string[0].upper() + string[1:].lower()

def endsWith(string='', target=None, position=None):
    if position is None:
        position = len(string)

    return string[position-1] == target

def string_replace(string, old_character, new_character):
    if old_character in string:
        string = string.replace(old_character, new_character)
    return string

def escape(string=''):
    characters = {
        '&': '&amp;',
        '>': '&gt;',
        '"': '&quot;',
        '\'': '&apos;',
        '<': '&lt;'
    }

    for key, value in characters.items():
        string = string_replace(string, key, value)

    return string

def lowerCase(string=''):
    items = replace_special_characters(string)
    result = [i.lower() for i in items]

    return ' '.join(result)

def lowerFirst(string=''):
    return string[0].lower() + string[1:]

def pad_characters(chars, position):
    return (chars*position)[0:position]

def pad(string='', length=0, chars=' '):
    left = length % len(string)
    right = length - len(string) - left
    return pad_characters(chars, left) + string + pad_characters(chars, right)

def padEnd(string='', length=0, chars=' '):
    right = length - len(string)
    return string + pad_characters(chars, right)

def padStart(string='', length=0, chars=' '):
    left = length - len(string)
    return pad_characters(chars, left) + string

def repeat(string='', n=1):
    return string*n

def replace(string, pattern, replacement):
    return string.replace(pattern, replacement)

def startsWith(string, target, position=0):
    return string[position] == target
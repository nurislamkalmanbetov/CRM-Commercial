import unicodedata as ud
from django.utils.safestring import mark_safe

latin_letters = {}


def is_latin(uchr):
    try:
        return latin_letters[uchr]
    except KeyError:
        return latin_letters.setdefault(uchr, 'LATIN' in ud.name(uchr))


def only_roman_chars(unistr):
    return all(is_latin(uchr)
           for uchr in unistr
           if uchr.isalpha())


def user_directory_path(instance, filename):
    return 'documents/profile_{0}/{1}'.format(instance.id, filename)


def get_mark_safe(filename_id):
    filename = ''
    if filename_id == 0:
        filename = 'non_flag'
    elif filename_id == 1:
        filename = 'single_flag'
    elif filename_id == 2:
        filename = 'double_flag'
    else:
        filename = 'question_flag'
    return mark_safe(f'<img src="/static/images/icons/{filename}.svg" width="18" height="18" />')

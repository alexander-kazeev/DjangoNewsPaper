from django import template
import re

register = template.Library()

@register.filter(name='addswearwords')
def addswearwords(value):
    if isinstance(value, str):
        return str(value) + f' охуительно пиздец заебал'
    else:
        raise ValueError(f'Нельзя добавить бранные слова (текст) в тип {type(value)}')


# Добавляю только три шаблона матерных слов. Расширять можно до бесконечности.
SWEARWORDS = [
        r'\w*ху[йяие]\w*',
        r'\w*ебал\w*',
        r'\w*пизд\w*',
]

@register.filter(name='censor')
def censor(value):
    if isinstance(value, str):
        censored_text = ''
        for one_word in value.split():
            for swearword in SWEARWORDS:
                if re.search(swearword, one_word.strip('.,;:?!-').lower()):
                    censored_text += '!censored! '
                    break
            else:
                censored_text += one_word + ' '
        return str(censored_text)
    else:
        raise ValueError('Цензор умеет работать только со строками.')

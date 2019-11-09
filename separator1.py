# -*- coding: utf-8 -*-


from sys import argv
script, filename = argv

# Sentences can end with:
# 1. period .
# 2. question mark ?
# exclaimation mark !
# quotation mark plus period '.'

# first replace 'U.S.' with 'US'
with open(filename, 'r+', encoding='utf-8') as f:
    content = f.read()
    if content.find('U.S.'):
        state_clear = content.replace('U.S.', 'US')
        En_question_clear = state_clear.replace('? ', '?\n')
        Ch_question_clear = En_question_clear.replace('？','？\n')
        En_exclaimation_clear = Ch_question_clear.replace('! ', '!\n')
        Ch_exclaimation_clear = En_exclaimation_clear.replace('！', '\n')
        Ch_period_clear = Ch_exclaimation_clear.replace('。', '\n')
        Ch_comma_clear = Ch_period_clear.replace('，', ' ')
        Rquotation_clear = Ch_comma_clear.replace('”', '')
        Lquotation_clear = Rquotation_clear.replace('：“', ' ')
        draft = Lquotation_clear.replace('. ', '.\n')
        new_content = draft.replace('US', 'U.S.')
    else:
        En_question_clear = content.replace('? ', '?\n')
        Ch_question_clear = En_question_clear.replace('？','？\n')
        En_exclaimation_clear = Ch_question_clear.replace('! ', '!\n')
        Ch_exclaimation_clear = En_exclaimation_clear.replace('！', '\n')
        Ch_period_clear = Ch_exclaimation_clear.replace('。', '\n')
        Ch_comma_clear = Ch_period_clear.replace('，', ' ')
        Rquotation_clear = Ch_comma_clear.replace('”', '')
        Lquotation_clear = Rquotation_clear.replace('：“', ' ')
        new_content = Lquotation_clear.replace('. ', '.\n')

#with open(filename, 'w') as new_f:
    #new_f.write(new_content)

    f.write(new_content)

# next, may need delete empty lines

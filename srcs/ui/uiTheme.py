'''

[ui] uiTheme.py

Author: seith <seith.corp@gmail.com>

Created: 10/03/2021 18:00:54 by seith
Updated: 10/03/2021 18:00:54 by seith

Synezia Corp. (c) 2021 - MIT

'''

from PyInquirer import style_from_dict, Token

uiDefaultTheme = style_from_dict({
    Token.Separator: '#cc5454',
    Token.QuestionMark: '#673ab7',
    Token.Selected: '#5d5bc5',  # default
    Token.Pointer: '#673ab7 bold',
    Token.Instruction: '#f44336', # default
    Token.Answer: '#f44336 bold',
    Token.Question: '',
})
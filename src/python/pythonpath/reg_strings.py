# (string to be replaced, new string)
CLEAN_REPLACING_STR = [
    # ('(\d{2}),\d{2}\]', "$1]"),  # remove milliseconds

    # Replace . or blank char with ':' Ex: [01 : 22 : 38.39] -> [01:22:39.59]
    ("(\d{1,2})\s?[:|.]\s?(\d{2})\s?[:|.]\s?(\d{2})(\.\d{2})?", "$1:$2:$3$4"),

    # Be sure hours is made of 2 chars
    ("\[(\d{1}):", '[0$1:'),

    # if milliseconds, use . as decimal
    ("(\d{2}),(\d+\])", '$1.$2'),

    # Remove double open bracket (ie. [INAUDIBLE [33:29:11])
    ('(\[[^\]]+)\[', '$1'),

    # Double space to simple
    ('^\s+', ('')),
    ('\s{2,}', (' ')),
    ('[ ]+', (' ')),

]

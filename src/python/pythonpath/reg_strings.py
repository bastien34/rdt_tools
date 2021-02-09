# (string to be replaced, new string)
CLEAN_REPLACING_STR = [
    ('(\d{2}),\d{2}\]', "$1]"),  # remove milliseconds

    # Replace . or blank char with ':'
    ('[\(|\[]?(\d{1,2})\s?[:|.]\s?(\d{2})\s?[:|.]\s?(\d{2})[\)|\]]?', '[$1:$2:$3]'),

    # Be sure hours is made of 2 chars
    ('\[(\d{1}):', '[0$1:'),

    ('^\s?(\[\d{2}:\d{2}:\d{2}\])\s?$', '$1'),

    # Remove double open bracket (ie. [INAUDIBLE [33:29:11])
    ('(\[[^\]]+)\[', '$1'),

    ('^\s+', ('')),
    ('\s{2,}', (' ')),
    ('[ ]+', (' ')),

]

import re

var_regex = re.compile(r"""
        \{              # The exact character "{"
        (\w+)           # The variable name (restricted to 0-9, a-z, _)
        (?::([^}]+))?   # The optional ::regex part
        \}              # The exact character "}"
        """, re.VERBOSE)

def template_to_regex(template):
    regex = ''
    last_pos = 0
    for match in var_regex.finditer(template):
        regex += re.escape(template[last_pos:match.start()])
        var_name = match.group(1)
        pattern = match.group(2) or '[^/]+'
        regex += '(?P<%s>%s)' % (var_name, pattern)
        last_pos = match.end()
    regex += re.escape(template[last_pos:])
    regex = '^%s$' % regex
    return regex

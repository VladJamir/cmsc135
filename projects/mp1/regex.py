import re
strings = ['[VladJamir] /join test channel',
            '[VladJamir] /list',
            '[VladJamir] /asdkasjdasidsadosai'
]
regex = '\[(.+)\]\s(.+)*\s?(.*)'
pattern = re.compile(regex)
for string in strings:
    m = pattern.match(string)
    print m.group(1)
    print m.group(2)
    print m.group(3)
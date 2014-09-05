#!/usr/bin/env python3

import sys


if sys.version_info < (3,):
    sys.stderr.write('This script requires Python 3 or higher version.\n')
    sys.exit(1)


wholereplacetable = (
    ('bo', 'buo'), ('po', 'puo'), ('mo', 'muo'), ('fo', 'fuo'), ('zhi', 'zh'),
    ('chi', 'ch'), ('shi', 'sh'), ('ri', 'r'), ('zi', 'z'), ('ci', 'c'),
    ('si', 's')
)
localreplacetable = (
    ('yu', 'v'), ('yi', 'i'), ('wu', 'u'), ('ju', 'jv'), ('qu', 'qv'),
    ('xu', 'xv'), ('y', 'i'), ('w', 'u'), ('\u00fc', 'v')
)
initialtable = (
    ('b', 'p'), ('p', 'p_h'), ('m', 'm'), ('f', 'f'), ('d', 't'), ('t', 't_h'),
    ('ng', 'N'), ('n', 'n'), ('l', 'l'), ('g', 'k'), ('k', 'k_h'), ('h', 'x'),
    ('j', 'ts\\'), ('q', 'ts\\_h'), ('x', 's\\'), ('zh', 'ts`'),
    ('ch', 'ts`_h'), ('sh', 's`'), ('r', 'z`'), ('z', 'ts'), ('c', 'ts_h'),
    ('s', 's')
)
finaltable = (
    ('\u00ea', 'E'), ('ai', 'aI'), ('ei', 'eI'), ('ao', 'AU'), ('ou', '@U'),
    ('ang', 'A N'), ('eng', '7 N'), ('an', 'a n'), ('ong', 'o N'),
    ('en', '@ n'), ('ie', 'iE'), ('iu', 'i@U'), ('ian', 'iE n'),
    ('ing', 'iM N'), ('ui', 'ueI'), ('uo', 'uO'), ('un', 'u@ n'), ('ve', 'yE'),
    ('vn', 'yi n'), ('ng', 'N'), ('n', 'n'), ('m', 'm'), ('a', 'a'),
    ('o', 'o'), ('e', 'MV'), ('i', 'i'), ('u', 'u'), ('v', 'y')
)


def main():
    while True:
        try:
            line = input()
        except EOFError:
            break
        line = line.replace("'", ' ')
        words = line.split()
        pho = []
        for word in words:
            if word == 'er':
                pho.append('a r\\')
                break
            if word.endswith('r'):
                word = word[:-1]
                endwithr = 'r\\'
            else:
                endwithr = ''
            for i in wholereplacetable:
                if word == i[0]:
                    word = i[1]
                    break
            for i in localreplacetable:
                wordn = word.replace(i[0], i[1])
                if wordn != word:
                    word = wordn
                    break
            initial = ''
            for i in initialtable:
                if word.startswith(i[0]):
                    initial = i[1]
                    word = word[len(i[0]):]
                    break
            final = ''
            while True:
                foundfinal = False
                for i in finaltable:
                    if word.startswith(i[0]):
                        final += i[1]
                        word = word[len(i[0]):]
                        foundfinal = True
                if not foundfinal:
                    break
            if not final:
                if initial in ('ts`', 'ts`_h', 's`', 'z`'):
                    final = 'M'
                elif initial in ('ts', 'ts_h', 's'):
                    final = '1'
            pho.append(' '.join((initial, final, endwithr)).strip())
        print(' '.join(('[' + i + ']' for i in pho)).strip())

if __name__ == '__main__':
    main()

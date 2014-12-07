#!/usr/bin/env python3

import sys


if sys.version_info < (3,):
    sys.stderr.write('This script requires Python 3 or higher version.\n')
    sys.exit(1)


wholereplacetable = (
    ('bo', 'buo'), ('po', 'puo'), ('mo', 'muo'), ('fo', 'fuo'),
    ('zhi', 'zhirh'), ('chi', 'chirh'), ('shi', 'shirh'), ('ri', 'rirh'),
    ('zi', 'zih'), ('ci', 'cih'), ('si', 'sih')
)
localreplacetable = (
    ('yi', 'i'), ('wu', 'u'), ('yu', 'v'), ('ju', 'jv'), ('qu', 'qv'),
    ('xu', 'xv'), ('y', 'i'), ('w', 'u'), ('\u00ea', 'eh'), ('\u00fc', 'v'),
    ('iu', 'iou'), ('ui', 'uei'), ('un', 'uen'), ('um', 'uem')
)
initialtable = (
    ('b', 'p'), ('p', 'p_h'), ('m', 'm'), ('f', 'f'), ('d', 't'), ('t', 't_h'),
    ('ng', 'N'), ('n', 'n'), ('l', 'l'), ('g', 'k'), ('k', 'k_h'), ('h', 'x'),
    ('j', 'ts\\'), ('q', 'ts\\_h'), ('x', 's\\'), ('zh', 'ts`'),
    ('ch', 'ts`_h'), ('sh', 's`'), ('r', 'z`'), ('z', 'ts'), ('c', 'ts_h'),
    ('s', 's')
)
finaltable = (
    ('iamg', 'iA m'), ('iang', 'iA N'), ('iomg', 'io m'), ('iong', 'io N'),
    ('uamg', 'uA m'), ('uang', 'uA N'), ('uemg', 'u7 m'), ('ueng', 'u7 N'),
    ('amg', 'A m'), ('ang', 'A N'), ('emg', '7 m'), ('eng', '7 N'),
    ('iam', 'iE m'), ('ian', 'iE n'), ('iao', 'iaU'), ('img', 'i m'),
    ('ing', 'iM N'), ('iou', 'i7U'), ('ong', 'o N'), ('uai', 'uaI'),
    ('uam', 'ua m'), ('uan', 'ua n'), ('uei', 'ueI'), ('uem', 'u@ m'),
    ('uen', 'u@ n'), ('van', 'ya n'), ('ai', 'aI'), ('am', 'a m'),
    ('an', 'a n'), ('ao', 'AU'), ('ei', 'eI'), ('em', '@ m'), ('en', '@ n'),
    ('ia', 'ia'), ('ie', 'iE'), ('im', 'i m'), ('in', 'i n'), ('io', 'io'),
    ('ou', '7U'), ('ua', 'ua'), ('uo', 'uO'), ('ve', 'yE'), ('vm', 'yi m'),
    ('vn', 'yi n'), ('m', 'm'), ('ng', 'N'), ('n', 'n'), ('a', 'a'),
    ('o', 'o'), ('eh', 'E'), ('e', 'MV'), ('ih', 'M'), ('irh', '1'),
    ('i', 'i'), ('u', 'u'), ('v', 'y')
)


def main():
    while True:
        try:
            line = input('> ') if sys.stdin.isatty() else input()
        except EOFError:
            break
        line = line.replace("'", ' ')
        words = line.split()
        pho = []
        for word in words:
            if word == 'er':
                pho.append('A r\\')
                continue
            if word[1:].endswith('r'):
                word = word[:-1]
                endswithr = True
            else:
                endswithr = False
            for i in wholereplacetable:
                if word == i[0]:
                    word = i[1]
                    break
            while True:
                for i in localreplacetable:
                    wordnew = word.replace(i[0], i[1])
                    if wordnew != word:
                        word = wordnew
                        break
                else:
                    break
            phonetics = []
            for i in initialtable:
                if word.startswith(i[0]):
                    phonetics.append(i[1])
                    word = word[len(i[0]):]
                    break
            while True:
                for i in finaltable:
                    if word.startswith(i[0]):
                        phonetics.append(i[1])
                        word = word[len(i[0]):]
                        break
                else:
                    break
            if word:
                pho.append('ERROR')
                continue
            if endswithr:
                phonetics.append('r\\')
            pho.append(' '.join(phonetics))
        print(' '.join(('[' + i + ']' for i in pho)).strip())

if __name__ == '__main__':
    main()

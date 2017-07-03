#!/usr/bin/env python3

# Copyright (C) 2014  StarBrilliant <m13253@hotmail.com>
#
# This program is free software; you can redistribute it and/or
# modify it under the terms of the GNU Lesser General Public
# License as published by the Free Software Foundation; either
# version 3.0 of the License, or (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the GNU
# Lesser General Public License for more details.
#
# You should have received a copy of the GNU Lesser General Public
# License along with this program.  If not,
# see <http://www.gnu.org/licenses/>.

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
    ('iamg', 'iAm'), ('iang', 'iAN'), ('iomg', 'iUm'), ('iong', 'iUN'),
    ('uamg', 'uAm'), ('uang', 'uAN'), ('uemg', 'u7m'), ('ueng', 'u7N'),
    ('amg', 'Am'), ('ang', 'AN'), ('emg', '7m'), ('eng', '7N'), ('iam', 'iEm'),
    ('ian', 'iE_n'), ('iao', 'iaU'), ('img', 'im'), ('ing', 'iMN'),
    ('iou', 'i7U'), ('ong', 'UN'), ('uai', 'uaI'), ('uam', 'uam'),
    ('uan', 'ua_n'), ('uei', 'ueI'), ('uem', 'u@m'), ('uen', 'u@_n'),
    ('vam', 'yEm'), ('van', 'yE_n'), ('ai', 'aI'), ('am', 'am'), ('an', 'a_n'),
    ('ao', 'AU'), ('ei', 'eI'), ('em', '@m'), ('en', '@_n'), ('ia', 'ia'),
    ('ie', 'iE'), ('im', 'im'), ('in', 'i_n'), ('io', 'io'), ('ou', '7U'),
    ('ua', 'ua'), ('uo', 'uO'), ('ve', 'yE'), ('vm', 'yim'), ('vn', 'yi_n'),
    ('m', 'm'), ('ng', 'N'), ('n', 'n'), ('a', 'a'), ('o', 'o'), ('eh', 'E'),
    ('e', 'MV'), ('ih', 'M'), ('irh', '1'), ('i', 'i'), ('u', 'u'), ('v', 'y')
)


def pinyin2xsampa(word):
    if word == 'er':
        return 'A r\\'
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
        return 'ERROR'
    phonetics = ' '.join(phonetics)
    if endswithr:
        if phonetics.endswith(' n') or phonetics.endswith(' N'):
            phonetics = phonetics[:-2] + '~ r\\'
        else:
            phonetics += ' r\\'
    return phonetics


def main():
    retval = 0
    while True:
        try:
            line = input('> ') if sys.stdin.isatty() else input()
        except EOFError:
            break
        line = line.replace("'", ' ')
        words = line.split()
        output_line = []
        for word in words:
            phonetics = pinyin2xsampa(word)
            output_line.append('[' + phonetics + ']')
        print(' '.join(output_line))
    return retval

if __name__ == '__main__':
    sys.exit(main())

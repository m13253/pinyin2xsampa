Pinyin to X-SAMPA
=================

This Python script converts Pinyin to X-SAMPA phonetic symbols.

Released under LGPL 3.0 and above version.


Usage
-----

Input with Pinyin separated with a space between each words.

Feel free to submit bug reports.


Notice
------

`'` is equivalent of `_j` suffix, and `~` is equivalent of `_n` suffix.

Maybe you expect the latter form. Please do simple `grep` in your own.


Nasals
------

Why you get me a `a~` instead of `an`?

Although [Wikipedia](http://en.wikipedia.org/wiki/Pinyin#Pronunciation_of_finals) suggests use of `an`, I think Mandarin Chinese speakers are acturally prouncing `a~`. In addition, `a~` is better for TTS processing.


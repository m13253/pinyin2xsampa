/*
  Copyright (C) 2014  StarBrilliant <m13253@hotmail.com>

  This program is free software; you can redistribute it and/or
  modify it under the terms of the GNU Lesser General Public
  License as published by the Free Software Foundation; either
  version 3.0 of the License, or (at your option) any later version.

  This program is distributed in the hope that it will be useful,
  but WITHOUT ANY WARRANTY; without even the implied warranty of
  MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the GNU
  Lesser General Public License for more details.

  You should have received a copy of the GNU Lesser General Public
  License along with this program.  If not,
  see <http://www.gnu.org/licenses/>.
*/

#if __cplusplus <= 199711L
#error This program requires a compiler supporting at least C++ 11
#endif

#include <cstddef>
#include <cstdio>
#include <iostream>
#include <sstream>
#include <string>
#include <unistd.h>
#include <utility>
#include <vector>

typedef const std::pair<std::string, std::string> pinyin2xsampa_replacetable[];

static pinyin2xsampa_replacetable wholereplacetable = {
    {"bo", "buo"}, {"po", "puo"}, {"mo", "muo"}, {"fo", "fuo"},
    {"zhi", "zhirh"}, {"chi", "chirh"}, {"shi", "shirh"}, {"ri", "rirh"},
    {"zi", "zih"}, {"ci", "cih"}, {"si", "sih"}
};
static pinyin2xsampa_replacetable localreplacetable = {
    {"yi", "i"}, {"wu", "u"}, {"yu", "v"}, {"ju", "jv"}, {"qu", "qv"},
    {"xu", "xv"}, {"y", "i"}, {"w", "u"}, {u8"\u00ea", "eh"},
    {u8"\u00fc", "v"}, {"iu", "iou"}, {"ui", "uei"}, {"un", "uen"},
    {"um", "uem"}
};
static pinyin2xsampa_replacetable initialtable = {
    {"b", "p"}, {"p", "p_h"}, {"m", "m"}, {"f", "f"}, {"d", "t"}, {"t", "t_h"},
    {"ng", "N"}, {"n", "n"}, {"l", "l"}, {"g", "k"}, {"k", "k_h"}, {"h", "x"},
    {"j", "ts\\"}, {"q", "ts\\_h"}, {"x", "s\\"}, {"zh", "ts`"},
    {"ch", "ts`_h"}, {"sh", "s`"}, {"r", "z`"}, {"z", "ts"}, {"c", "ts_h"},
    {"s", "s"}
};
static pinyin2xsampa_replacetable finaltable = {
    {"iamg", "iA m"}, {"iang", "iA N"}, {"iomg", "iU m"}, {"iong", "iU N"},
    {"uamg", "uA m"}, {"uang", "uA N"}, {"uemg", "u7 m"}, {"ueng", "u7 N"},
    {"amg", "A m"}, {"ang", "A N"}, {"emg", "7 m"}, {"eng", "7 N"},
    {"iam", "iE m"}, {"ian", "iE n"}, {"iao", "iaU"}, {"img", "i m"},
    {"ing", "iM N"}, {"iou", "i7U"}, {"ong", "o N"}, {"uai", "uaI"},
    {"uam", "ua m"}, {"uan", "ua n"}, {"uei", "ueI"}, {"uem", "u@ m"},
    {"uen", "u@ n"}, {"vam" , "yE m"}, {"van", "yE n"}, {"ai", "aI"},
    {"am", "a m"}, {"an", "a n"}, {"ao", "AU"}, {"ei", "eI"}, {"em", "@ m"},
    {"en", "@ n"}, {"ia", "ia"}, {"ie", "iE"}, {"im", "i m"}, {"in", "i n"},
    {"io", "io"}, {"ou", "7U"}, {"ua", "ua"}, {"uo", "uO"}, {"ve", "yE"},
    {"vm", "yi m"}, {"vn", "yi n"}, {"m", "m"}, {"ng", "N"}, {"n", "n"},
    {"a", "a"}, {"o", "o"}, {"eh", "E"}, {"e", "MV"}, {"ih", "M"},
    {"irh", "1"}, {"i", "i"}, {"u", "u"}, {"v", "y"}
};

static inline bool string_is_startswith(const std::string &str, const std::string &substr) {
    if(str.length() < substr.length())
        return false;
    else
        return str.compare(0, substr.length(), substr) == 0;
}

static inline bool string_is_endwith(const std::string &str, const std::string &substr) {
    if(str.length() < substr.length())
        return false;
    else
        return str.compare(str.length()-substr.length(), std::string::npos, substr) == 0;
}

static inline bool string_replace_all(std::string &result, const std::string &str, const std::string &from, const std::string &to) {
    result.reserve(str.length());
    size_t pos = 0;
    bool replaced = false;
    for(;;) {
        size_t found = str.find(from, pos);
        if(found != std::string::npos) {
            replaced = true;
            result.append(str, pos, found-pos);
            result.append(to);
            pos = found+from.length();
        } else {
            result.append(str, pos, std::string::npos);
            result.shrink_to_fit();
            return replaced;
        }
    }
}

std::string pinyin2xsampa(std::string word) {
    if(word == std::string("er"))
        return "A r\\";
    bool endswithr = false;
    if(word.length() > 1 && string_is_endwith(word, "r")) {
        endswithr = true;
        word = word.substr(0, word.length()-1);
    }
    for(const auto &i : wholereplacetable)
        if(word == i.first) {
            word = i.second;
            break;
        }
    for(;;) {
        bool flag = false;
        for(const auto &i : localreplacetable) {
            std::string wordnew;
            if(string_replace_all(wordnew, word, i.first, i.second)) {
                word = std::move(wordnew);
                flag = true;
                break;
            }
        }
        if(!flag)
            break;
    }
    std::string phonetics;
    for(const auto &i : initialtable)
        if(string_is_startswith(word, i.first)) {
            phonetics = i.second;
            word = word.substr(i.first.length(), std::string::npos);
            break;
        }
    for(;;) {
        bool flag = false;
        for(const auto &i : finaltable)
            if(string_is_startswith(word, i.first)) {
                if(!phonetics.empty())
                    phonetics += ' ';
                phonetics += i.second;
                word = word.substr(i.first.length(), std::string::npos);
                flag = true;
                break;
            }
        if(!flag)
            break;
    }
    if(!word.empty())
        return "ERROR";
    if(endswithr)
        phonetics += std::string(" r\\");
    return phonetics;
}

int main() {
    int retval = 0;
    while(std::cin) {
        if(isatty(fileno(stdin)))
            std::cerr << "> " << std::flush;
        std::string line;
        if(std::getline(std::cin, line)) {
            std::string linerep;
            string_replace_all(linerep, line, "'", " ");
            std::stringstream linebuf(std::move(linerep));
            bool not_first_word = false;
            std::string word;
            while(linebuf >> word) {
                if(not_first_word)
                    std::cout << ' ';
                else
                    not_first_word = true;
                std::string phonetics = pinyin2xsampa(word);
                std::cout << '[' << phonetics << ']';
                if(phonetics == std::string("ERROR"))
                    retval = 1;
            }
            std::cout << std::endl;
        }
    }
    return retval;
}

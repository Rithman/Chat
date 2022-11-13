import subprocess
import locale
import os
from chardet.universaldetector import UniversalDetector
import chardet

# 1
words = ["разработка", "сокет", "декоратор"]

print(*(f"{word}: {type(word)}\n" for word in words))

words_unicode = [
    "\u0440\u0430\u0437\u0440\u0430\u0431\u043E\u0442\u043A\u0430",
    "\u0441\u043E\u043A\u0435\u0442",
    "\u0434\u0435\u043A\u043E\u0440\u0430\u0442\u043E\u0440"
]

print(*(f"{word}: {type(word)}\n" for word in words_unicode))

# 2
words = [b'class', b'function', b'method']
print(*(f"{word}: {type(word)}" for word in words))

# 3
# "класс" и "функция" невозможно записать в байтовом типе, т.к. они содержат символы, не входящие в ASCII
words_3 = ["attribute", "класс", "функция", "type"]
for word in words_3:
    try:
        print(bytes(word, encoding="ASCII"))
    except:
        print(
            f"Can't encode word {word}. Only ASCII characters are allowed in bytes")

# 4
words2 = ["разработка", "администрирование", "protocol", "standart"]
words2_bytes = [word.encode(encoding='utf-8') for word in words2]
print(words2_bytes)

words2_str = [word.decode(encoding='utf-8') for word in words2_bytes]
print(words2_str)

# 5
args = ['ping', 'yandex.ru', 'youtube.com']
ping1 = subprocess.Popen(args[:2], stdout=subprocess.PIPE)
for line in ping1.stdout:
    result = chardet.detect(line)
    print(line.decode(result['encoding']).encode('utf-8').decode('utf-8'))

ping2 = subprocess.Popen((args[0], args[2]), stdout=subprocess.PIPE)
for line in ping2.stdout:
    result = chardet.detect(line)
    print(line.decode(result['encoding']).encode('utf-8').decode('utf-8'))


# 6
coding = locale.getpreferredencoding()
print(coding)

# не хочет просто так открывать файл в том же каталоге
detector = UniversalDetector()
with open(os.getcwd()+'\\chat\\test_file.txt', 'rb') as f:
    for line in f:
        detector.feed(line)
        if detector.done:
            break
    detector.close()
print(detector.result)

with open(os.getcwd()+'\\chat\\test_file.txt', 'r', encoding=detector.result['encoding']) as f:
    for el in f:
        print(el, end="")
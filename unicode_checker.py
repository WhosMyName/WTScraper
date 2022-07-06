# curtessy to https://www.utf8-chartable.de

import re

filename = "Object_685.html"
pattern = re.compile(r"[^\u0020-\u007d\s→°·]") # re search to find all non ASCII Unicode chars, excluding the arrows, degrees and llist dots
outfile = "regex.chk"
newline = "\n"
utf_8_encoding = "utf-8"

with open(file=outfile, mode="a", encoding=utf_8_encoding) as outf:
    with open(file=filename, mode="r", encoding=utf_8_encoding) as fifo:
        results = re.findall(pattern=pattern, string=fifo.read())
        if len(results) > 2:
            outf.write(f"{filename}: {newline}{newline.join(f'{x} -->  {bytes(x, encoding=utf_8_encoding)}'  for x in results[:-1])}{newline}{'*' * 75}{newline}")
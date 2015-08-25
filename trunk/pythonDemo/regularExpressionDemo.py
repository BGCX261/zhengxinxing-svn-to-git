import re

# 查看某个字符串是否存指定的子串
s = 'asdf1'
pattern = '[1-9]'
re.search(pattern, s)
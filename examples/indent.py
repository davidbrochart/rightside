import sys
sys.path.append('../rightside')

import rightside

text = '''\
This is just to show what you can do with rightside.

You can filter lines,
remove unwanted ones, *if* a == 3
and keep only the ones that you want. *elif* a + 1 == 3

You can word1 word2. *for* word1, word2 in [('replace', 'things'), ('repeat', 'them')]

*for* _ in range(3):
You can repeat/replace conditionally (_). *if* _ == 1
*endfor*
'''

print(rightside.indent(text))

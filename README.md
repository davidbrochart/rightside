A tiny template engine that doesn't invite itself inside your code, but discreetly shows on the right side.

```python
import rightside

text = '''\
This is just to show what you can do with rightside.

You can filter lines,
remove unwanted ones,                                   *if* a == 3
and keep only the ones that you want.                   *elif* a + 1 == 3

You can word1 word2.                                    *for* word1, word2 in [('replace', 'things'), ('repeat', 'them')]
                                                        *for* _ in range(3):
You can repeat/replace conditionally (_).                   *if* _ == 1
                                                        *endfor*
'''

rightside.a = 2
print(rightside.process(text))
```

```
This is just to show what you can do with rightside.

You can filter lines,
and keep only the ones that you want.

You can replace things.
You can repeat them.



You can repeat/replace conditionally (1).




```

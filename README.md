A tiny template engine that doesn't invite itself inside your code, but discretely shows on the right side.

```python
import rightside

text = '''\
This is a simple test.
It's just to show what you can do with rightside.
You can repeat things.                                  *for* _ in range(3)
You can word1 word2.                                    *for* word1, word2 in [('replace', 'things')]
You can filter lines conditionally,
remove unwanted ones,                                   *if* a == 3
and keep only the ones that you want.                   *else*
Multi-line constructs are supported,                    *for* colon in ['":"']:
through the use of colon.
Any kind of nested processing is word3.                     *for* word3 in ['allowed']
Python-like identation can be used inside a block.          *if* True
This helps debugging.                                   *endfor*
'''

rightside.a = 2
print(rightside.process(text))
```

```
This is a simple test.
It's just to show what you can do with rightside.
You can repeat things.
You can repeat things.
You can repeat things.
You can replace things.
You can filter lines conditionally,
and keep only the ones that you want.
Multi-line constructs are supported,
through the use of ":".
Any kind of nested processing is allowed.
Python-like identation can be used inside a block.
This helps debugging.
```

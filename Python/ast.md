### String to Dict (ast)
```
* 파이썬 2.6 이상에서는 ast모듈에 ast.literal_eval(node_or_string)이 추가되었습니다.
  * ast.literal_eval(node_or_string)은 eval()보다 안전한 방법으로 node 또는 string을 인자로 받아 적절한 strings, bytes, numbers, tuples, lists, dicts, sets, booleans, None값을 return 해 줍니다.

사용 예:
import ast
ast.literal_eval("{'muffin' : 'lolz', 'foo' : 'kitty'}") # = {'muffin': 'lolz', 'foo': 'kitty'}
```

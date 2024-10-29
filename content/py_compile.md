title: CPython compile code chạy "Hello world"
date: 2024-10-28
tags: ast, Python, compile, C, readcode
category: news
slug: compile
authors: Pymier0
description: Python compile, rồi interpret

### CPython có compile không?
Có.

Bước compile code của CPython được thực hiện trước khi chạy code, mặc dù người dùng **thường** không nhìn thấy, nhưng nó có xảy ra, đôi khi nó còn tạo ra các file có đuôi `.pyc`.
Tài liệu <https://docs.python.org/3.12/glossary.html#term-bytecode> viết:

> Python source code is compiled into bytecode, the internal representation of a Python program in the CPython interpreter. The bytecode is also cached in .pyc files so that executing the same file is faster the second time (recompilation from source to bytecode can be avoided). This “intermediate language” is said to run on a virtual machine that executes the machine code corresponding to each bytecode. Do note that bytecodes are not expected to work between different Python virtual machines, nor to be stable between Python releases.

- Python source code được compile thành **bytecode**
- bytecode có thể được ghi vào file `.pyc`
- máy ảo Python Virtual Machine (VM) chạy machine code (mã máy) tương đương với bytecode.

### Các bước biến đổi để chạy code "hello world"

Document mới [3.14](https://github.com/python/cpython/blob/v3.14.0a1/InternalDocs/compiler.md) viết:

```
In CPython, the compilation from source code to bytecode involves several steps:

    Tokenize the source code Parser/lexer/ and Parser/tokenizer/.
    Parse the stream of tokens into an Abstract Syntax Tree Parser/parser.c.
    Transform AST into an instruction sequence Python/compile.c.
    Construct a Control Flow Graph and apply optimizations to it Python/flowgraph.c.
    Emit bytecode based on the Control Flow Graph Python/assemble.c.
```

Quá trình compile từ source code thành bytecode bao gồm các bước:

- tokenize: biến source code thành các "token" - thành phần nhỏ nhất. `Parser/lexer/` `Parser/tokenizer`
- biến chuỗi token thành Abstract Syntax Tree (AST) `Parser/parser.c`
- biến đổi AST thành các câu lệnh `Python/compile.c`
- tạo Control Flow graph qua `Python/flowgraph.c`
- sinh ra bytecode từ Control Flow Graph `Python/assemble.c`

### Xem hello world trải qua các bước

Tạo file hello.py với nội dung `print("Hello" + " Pymier 2024")`

[Build Python từ source]({filename}/slice_reverse.md) rồi chạy [lldb](https://familug.github.io/doc-code-bash-xem-vi-sao-echo-khong-hien-ten-file-an.html), đặt breakpoint tại function `pyrun_file` :

```c
$ lldb ./python
(lldb) target create "./python"
Current executable set to '/home/foss/python3120/python' (x86_64).
(lldb) b pyrun_file
Breakpoint 1: 5 locations.
(lldb) process launch -- hello.py
Process 4000 launched: '/home/foss/python3120/python' (x86_64)
Process 4000 stopped
* thread #1, name = 'python', stop reason = breakpoint 1.4
    frame #0: 0x00005555558415a0 python`_PyRun_SimpleFileObject at pythonrun.c:1599:22
   1596	pyrun_file(FILE *fp, PyObject *filename, int start, PyObject *globals,
   1597	           PyObject *locals, int closeit, PyCompilerFlags *flags)
   1598	{
-> 1599	    PyArena *arena = _PyArena_New();
   1600	    if (arena == NULL) {
   1601	        return NULL;
   1602	    }
(lldb) bt
* thread #1, name = 'python', stop reason = breakpoint 1.4
  * frame #0: 0x00005555558415a0 python`_PyRun_SimpleFileObject at pythonrun.c:1599:22
    frame #1: 0x00005555558415a0 python`_PyRun_SimpleFileObject(fp=0x0000555555c2d740, filename=0x00007ffff7109840, closeit=1, flags=0x00007fffffffe318) at pythonrun.c:433:13
    frame #2: 0x0000555555841b7f python`_PyRun_AnyFileObject(fp=0x0000555555c2d740, filename=0x00007ffff7109840, closeit=1, flags=0x00007fffffffe318) at pythonrun.c:78:15
    frame #3: 0x00005555558696a8 python`pymain_run_python at main.c:360:15
    frame #4: 0x0000555555869612 python`pymain_run_python at main.c:379:15
    frame #5: 0x00005555558695c0 python`pymain_run_python(exitcode=0x00007fffffffe460) at main.c:610:21
    frame #6: 0x0000555555869e00 python`Py_BytesMain at main.c:689:5
    frame #7: 0x0000555555869dee python`Py_BytesMain at main.c:719:12
    frame #8: 0x0000555555869dcf python`Py_BytesMain(argc=<unavailable>, argv=<unavailable>) at main.c:743:12
    frame #9: 0x00007ffff7c29d90 libc.so.6`__libc_start_call_main(main=(python`main at python.c:14:1), argc=2, argv=0x00007fffffffe5a8) at libc_start_call_main.h:58:16
    frame #10: 0x00007ffff7c29e40 libc.so.6`__libc_start_main_impl(main=(python`main at python.c:14:1), argc=2, argv=0x00007fffffffe5a8, init=0x00007ffff7ffd040, fini=<unavailable>, rtld_fini=<unavailable>, stack_end=0x00007fffffffe598) at libc-start.c:392:3
    frame #11: 0x0000555555660c85 python`_start + 37
```


[Function `pyrun_file` trong pythonrun.c](https://github.com/python/cpython/blob/3.12/Python/pythonrun.c#L1624-L1651)

```c
static PyObject *
pyrun_file(FILE *fp, PyObject *filename, int start, PyObject *globals,
           PyObject *locals, int closeit, PyCompilerFlags *flags)
{
    PyArena *arena = _PyArena_New();
    if (arena == NULL) {
        return NULL;
    }

    mod_ty mod;
    mod = _PyParser_ASTFromFile(fp, filename, NULL, start, NULL, NULL,
                                flags, NULL, arena);

    if (closeit) {
        fclose(fp);
    }

    PyObject *ret;
    if (mod != NULL) {
        ret = run_mod(mod, filename, globals, locals, flags, arena, NULL, 0);
    }
    else {
        ret = NULL;
    }
    _PyArena_Free(arena);

    return ret;
}
```

- `_PyParser_ASTFromFile` đọc file vào và biến thành AST, trả về kiểu `mod_ty`. Tìm trong tài liệu [Python viết](https://docs.python.org/3.12/whatsnew/changelog.html#id280) : AST object (`mod_ty` type). `_PyParser_ASTFromFile` gọi tới [`_PyPegen_run_parser_from_file_pointer` trong pegen.c](https://github.com/python/cpython/blob/3.12/Parser/pegen.c#L969) tại đây gọi `_PyTokenizer_FromFile` để biến source code thành các token rồi gọi [`_PyPegen_parse trong parser.c`](https://github.com/python/cpython/blob/3.12/Parser/parser.c#L41910) để parse token stream thành AST.
- [`run_mod`](https://github.com/python/cpython/blob/3.12/Python/pythonrun.c#L1729-L1746) sau đó gọi [`_PyAST_Compile` trong compile.c](https://github.com/python/cpython/blob/3.12/Python/compile.c#L577) để compile code từ AST `mod_py`, trả về object kiểu `PyCodeObject`, sau đó chạy code này bằng [`run_eval_code_obj` trong ceval.c](https://github.com/python/cpython/blob/main/Python/ceval.c#L636).

```c
static PyObject *
run_mod(mod_ty mod, PyObject *filename, PyObject *globals, PyObject *locals,
            PyCompilerFlags *flags, PyArena *arena)
{
    PyThreadState *tstate = _PyThreadState_GET();
    PyCodeObject *co = _PyAST_Compile(mod, filename, flags, -1, arena);
    if (co == NULL)
        return NULL;

    if (_PySys_Audit(tstate, "exec", "O", co) < 0) {
        Py_DECREF(co);
        return NULL;
    }

    PyObject *v = run_eval_code_obj(tstate, co, globals, locals);
    Py_DECREF(co);
    return v;
}
```

### Kết luận
CPython có compile code.

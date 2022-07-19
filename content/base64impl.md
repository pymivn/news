title: Thư viện base64 trong Python được viết thế nào
date: 2022-02-16
modified: 2022-02-16
tags: Base64, encoding, stdlib, crypto
category: news
slug: base64impl
authors: Pymier0
description: liệu có phải viết bằng Python?

![img](https://images.unsplash.com/photo-1507499739999-097706ad8914?crop=entropy&cs=tinysrgb&fit=max&fm=jpg&ixid=MnwyMzI1MzN8MHwxfHJhbmRvbXx8fHx8fHx8fDE2NDQ5Nzk4Njk&ixlib=rb-1.2.1&q=80&w=600)

[Bài trước]({filename}/base64.md) đã tự viết code Python để encoding từ bytes sang base64, code đơn giản, mang tính chất minh họa. Vậy stdlib base64 Python viết thế nào?

[https://github.com/python/cpython/blob/3.10/Lib/base64.py#L51-L62](https://github.com/python/cpython/blob/3.10/Lib/base64.py#L51-L62)

```py
# Base64 encoding/decoding uses binascii

def b64encode(s, altchars=None):
    """Encode the bytes-like object s using Base64 and return a bytes object.
    Optional altchars should be a byte string of length 2 which specifies an
    alternative alphabet for the '+' and '/' characters.  This allows an
    application to e.g. generate url or filesystem safe Base64 strings.
    """
    encoded = binascii.b2a_base64(s, newline=False)
    if altchars is not None:
        assert len(altchars) == 2, repr(altchars)
        return encoded.translate(bytes.maketrans(b'+/', altchars))
    return encoded
```

hóa ra base64 lại gọi 1 thư viện khác `binascii` để thực hiện việc encoding.

> The binascii module contains a number of methods to convert between binary and various ASCII-encoded binary representations. Normally, you will not use these functions directly but use wrapper modules like uu, base64, or binhex instead. 

**The binascii module contains low-level functions written in C for greater speed that are used by the higher-level modules.**

[https://docs.python.org/3/library/binascii.html](https://docs.python.org/3/library/binascii.html)

Chú ý function `b64encode(s, altchars=None)` nhận 1 đầu vào optional altchars, là 2 ký tự thay thế `+/` (thường là `-_` để encode URL).

vậy [binascii là thư viện viết bằng C](https://github.com/python/cpython/blob/3.8/Modules/binascii.c#L570), để có được tốc độ nhanh hơn. 

Tò mò xem PyPy - Python viết bằng Python thì sao:

```py
table_b2a_base64 = (
    "ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789+/")

@unwrap_spec(bin='bufferstr', newline=bool)
def b2a_base64(space, bin, __kwonly__, newline=True):
    "Base64-code line of data."

    newlength = (len(bin) + 2) // 3
    try:
        newlength = ovfcheck(newlength * 4)
    except OverflowError:
        raise OperationError(space.w_MemoryError, space.w_None)
    newlength += 1
    res = StringBuilder(newlength)

    leftchar = 0
    leftbits = 0
    for c in bin:
        # Shift into our buffer, and output any 6bits ready
        leftchar = (leftchar << 8) | ord(c)
        leftbits += 8
        res.append(table_b2a_base64[(leftchar >> (leftbits-6)) & 0x3f])
        leftbits -= 6
        if leftbits >= 6:
            res.append(table_b2a_base64[(leftchar >> (leftbits-6)) & 0x3f])
            leftbits -= 6
    #
    if leftbits == 2:
        res.append(table_b2a_base64[(leftchar & 3) << 4])
        res.append(PAD)
        res.append(PAD)
    elif leftbits == 4:
        res.append(table_b2a_base64[(leftchar & 0xf) << 2])
        res.append(PAD)
    if newline:
        res.append('\n')
    return space.newbytes(res.build())
```

[https://foss.heptapod.net/pypy/pypy/-/blob/branch/py3.8/pypy/module/binascii/interp_base64.py#L92-124](https://foss.heptapod.net/pypy/pypy/-/blob/branch/py3.8/pypy/module/binascii/interp_base64.py#L92-124)

Đăng ký ngay tại [PyMI.vn](https://pymi.vn) để học Python tại Hà Nội TP HCM (Sài Gòn),
trở thành lập trình viên #python chuyên nghiệp ngay sau khóa học.
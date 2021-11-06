title: Compound Interest
date: 2021-10-30
modified: 2021-10-30
tags: calculus, finance, math
category: news
slug: compound
authors: Pymier0
description: 1% lãi mỗi năm, thì bao giờ tiền gửi sẽ gấp đôi?

> 1% lãi mỗi năm, thì bao giờ tiền gửi sẽ gấp đôi?

Câu trả lời sai dễ dàng là 100 năm, vì mỗi năm là 1%, 100 * 1 == 100.

![img](https://images.unsplash.com/photo-1579621970795-87facc2f976d?ixid=MnwxMjA3fDB8MHxwaG90by1wYWdlfHx8fGVufDB8fHx8&ixlib=rb-1.2.1&auto=format&fit=crop&w=600&q=80)

Điều kỳ diệu ở đây là phần lãi 1% này được gộp vào để tính lãi sau năm đầu tiên.
Năm thứ 2 lãi là 1% * (100+1), con số rất nhỏ này tăng lên rất nhanh theo thời gian.

Khái niệm này phổ biến với tên "compound interest" (lãi kép/ lãi gộp)
trong tài chính, khiến
người giàu càng giàu hơn, người nợ ngân hàng thì ngày càng nợ nhiều hơn (hello thẻ tín dụng).

Một vòng for đơn giản đủ để thấy sự kỳ diệu này, trước hết là vài con số:

- tiền gửi sẽ gấp đôi sau 70 năm
- sau 100 năm, tiền gửi đã là 270%, tức gấp 2.7 lần.

```py
>>> m = 100
>>> for i in range(1, 101):
...     m = m * 1/100 + m
...     print(i, m)
...
1 101.0
2 102.01
3 103.0301
4 104.060401
5 105.10100501
6 106.1520150601
7 107.213535210701
8 108.28567056280801
9 109.36852726843608
10 110.46221254112044
11 111.56683466653165
12 112.68250301319696
13 113.80932804332893
14 114.94742132376223
15 116.09689553699985
16 117.25786449236985
17 118.43044313729355
18 119.61474756866649
19 120.81089504435315
20 122.01900399479668
21 123.23919403474464
22 124.47158597509208
23 125.71630183484301
24 126.97346485319144
25 128.24319950172335
26 129.52563149674057
27 130.820887811708
28 132.12909668982508
29 133.45038765672334
30 134.78489153329056
31 136.13274044862348
32 137.49406785310973
33 138.86900853164082
34 140.2576986169572
35 141.6602756031268
36 143.07687835915806
37 144.50764714274965
38 145.95272361417713
39 147.4122508503189
40 148.8863733588221
41 150.37523709241034
42 151.87898946333445
43 153.3977793579678
44 154.9317571515475
45 156.48107472306296
46 158.0458854702936
47 159.62634432499652
48 161.2226077682465
49 162.83483384592896
50 164.46318218438824
51 166.10781400623213
52 167.76889214629446
53 169.4465810677574
54 171.14104687843496
55 172.8524573472193
56 174.5809819206915
57 176.32679173989843
58 178.09005965729742
59 179.87096025387038
60 181.6696698564091
61 183.4863665549732
62 185.32123022052292
63 187.17444252272816
64 189.04618694795545
65 190.936648817435
66 192.84601530560937
67 194.77447545866548
68 196.72222021325214
69 198.68944241538466
70 200.67633683953852
71 202.6831002079339
72 204.70993121001325
73 206.75703052211338
74 208.8246008273345
75 210.91284683560787
76 213.02197530396396
77 215.15219505700358
78 217.30371700757362
79 219.47675417764935
80 221.67152171942584
81 223.8882369366201
82 226.1271193059863
83 228.38839049904615
84 230.6722744040366
85 232.97899714807699
86 235.30878711955776
87 237.66187499075335
88 240.03849374066087
89 242.43887867806748
90 244.86326746484815
91 247.31190013949663
92 249.7850191408916
93 252.28286933230052
94 254.8056980256235
95 257.35375500587975
96 259.92729255593855
97 262.5265654814979
98 265.1518311363129
99 267.80334944767606
100 270.48138294215283
```

Hết.

Đăng ký ngay tại [PyMI.vn](https://pymi.vn) để học Python tại Hà Nội TP HCM (Sài Gòn),
trở thành lập trình viên #python chuyên nghiệp ngay sau khóa học.
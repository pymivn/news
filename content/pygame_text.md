title: pygame - đồng hồ và hiện bàn phím bấm gì
date: 2024-10-27
tags: python, pygame, draw, text, clock
category: news
slug: pygame-text
authors: Pymier0
description: hiển thị text trên pygame

Bài trước đã giới thiệu các khái niệm cơ bản trong Pygame và [vẽ logo Windows trên Pygame]({filename}/pygame_draw.md), bài này sẽ hiển thị thời gian hiện tại và ký tự bàn phím người chơi bấm.

### Pygame Font
> The font module allows for rendering TrueType fonts into Surface objects.

```py
font = pygame.font.SysFont("FreeMono", bold=True, size=30)
```
Tạo font object từ system font, nếu không có, pygame sẽ dùng font mặc định đi kèm pygame.

```py
# render(text, antialias, color, background=None) -> Surface
quit_surface = font.render("type q to quit", True, (255, 255, 255))
```
render trả về 1 Surface sau khi đã viết chữ lên, ở đây dùng màu trắng (255,255,255).

### Keyboard event
> Pygame handles all its event messaging through an event queue
Khi di chuột, bấm chuột, bấm phím, đề sinh ra event. Duyệt qua các event với

```py
for event in pygame.event.get():
```

lấy event.key tương ứng với ký tự bàn phím ở dạng int, đổi sang str với `chr` rồi hiển thị ra giữa cửa sổ:


```py
    current_char = chr(event.key)
    text_surface = font.render(current_char, False, (255, 255, 255))
    screen.blit(text_surface, (WIDTH // 2, HEIGHT // 2))
```

### Kết quả

![pygame_text]({static}/images/pygame_text.png)

### Code

```py
import datetime
import sys

import pygame

pygame.init()

WIDTH, HEIGHT = 600, 800

screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Keyboard Echo")

clock = pygame.time.Clock()
pygame.font.init()
font = pygame.font.SysFont("FreeMono", bold=True, size=30)
BACKGROUND = (149, 225, 211)
screen.fill(BACKGROUND)
quit_surface = font.render("type q to quit", True, (255, 255, 255))
current_char = ""

while True:
    screen.fill(BACKGROUND)
    clock_surface = font.render(
        str(datetime.datetime.now()), True, (255, 255, 255)
    )
    screen.blit(quit_surface, (20, 20))
    screen.blit(clock_surface, (20, 60))
    for event in pygame.event.get():
        print(event.type)
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()

        if event.type == pygame.KEYDOWN and event.key < 256:
            if event.key == ord("q"):
                pygame.quit()
                sys.exit()
            print("you hit", chr(event.key), event.key)
            current_char = chr(event.key)

    text_surface = font.render(current_char, False, (255, 255, 255))
    screen.blit(text_surface, (WIDTH // 2, HEIGHT // 2))

    pygame.display.update()
    clock.tick(60)
```

### Kết luận
Pygame giúp hiển thị text dễ dàng.

Hết.

Đăng ký ngay tại [PyMI.vn](https://pymi.vn) để học Python tại Hà Nội TP HCM (Sài Gòn),
trở thành lập trình viên #python chuyên nghiệp ngay sau khóa học.

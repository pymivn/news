import time
import pygame

pygame.init()


def find_queens():
    from z3 import Int, And, Distinct, Solver, sat, Or

    queens = [Int(f"Q{i+1}") for i in range(8)]
    columns = [And(1 <= q, q <= 8) for q in queens]
    distinct = [Distinct(queens)]
    diags = [
        And(queens[i] - queens[j] != i - j, queens[i] - queens[j] != j - i)
        for i in range(8)
        for j in range(i)
    ]

    solver = Solver()
    solver.add(columns + distinct + diags)
    while solver.check() == sat:
        m = solver.model()
        yield m

        block = []
        for var in m:
            v = var()
            block.append(v != m[v])

        solver.add(Or(block))


display = pygame.display.set_mode((800, 800))
pygame.display.set_caption("Z3 8 queens - hit SPACE to next - pymi.vn")

white = (0xFF, 0xFF, 0xFF)
black = (0x00, 0x00, 0x00)

cell_size = 100


it = find_queens()
m = next(it)
d = {i.name(): m[i].as_long() for i in m}
image = pygame.image.load("beerqueen.png")


board = pygame.Surface((cell_size * 8, cell_size * 8))


def draw_board(board):
    board.fill(white)

    cntr = 0
    for x in range(8):
        for y in range(8):
            if cntr % 2 == 0:
                pygame.draw.rect(
                    board,
                    black,
                    (x * cell_size, y * cell_size, cell_size, cell_size),
                )
            cntr += 1
        cntr += 1


running = True
draw_board(board)
counter = 1

myfont = pygame.font.SysFont("monospace", 80)
while running:
    time.sleep(0.2)
    display.blit(board, board.get_rect())

    for row in range(8):
        for col in range(8):
            if row + 1 == d[f"Q{col+1}"]:
                board.blit(image, (row * cell_size, col * cell_size))

    scoretext = myfont.render("#{0}".format(counter), 10, (0xFF, 0, 0))
    display.blit(scoretext, (5, 10))

    pygame.display.flip()

    for e in pygame.event.get():
        if e.type == pygame.KEYDOWN:
            if e.key == pygame.K_SPACE:
                draw_board(board)
                try:
                    m = next(it)
                    counter += 1
                except Exception:
                    draw_board(board)
                    board.fill(black)
                    scoretext = myfont.render("GAME OVER", 10, (0xFF, 0, 0))
                    display.blit(scoretext, (200, 200))
                    pygame.display.flip()
                    time.sleep(3)
                    pygame.quit()
                    exit()

                d = {i.name(): m[i].as_long() for i in m}

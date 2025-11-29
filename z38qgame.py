import time
import pygame

pygame.init()


def find_queens():
    from z3 import Int, And, Distinct, Solver

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
    solver.check()
    m = solver.model()
    return m


display = pygame.display.set_mode((800, 800))
pygame.display.set_caption("Z3 8 queens - pymi.vn")

white = (0xFF, 0xFF, 0xFF)
black = (0x00, 0x00, 0x00)

cell_size = 100
board = pygame.Surface((cell_size * 8, cell_size * 8))
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


m = find_queens()
d = {i.name(): m[i].as_long() for i in m}
image = pygame.image.load("beerqueen.png")

running = True
while running:
    display.blit(board, board.get_rect())

    for row in range(8):
        for col in range(8):
            if row + 1 == d[f"Q{col+1}"]:
                board.blit(image, (row * cell_size, col * cell_size))

    pygame.display.flip()
    time.sleep(1)

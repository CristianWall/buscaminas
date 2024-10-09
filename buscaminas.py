import pygame
import random
import time 

pygame.init()

WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
GRAY = (192, 192, 192)
RED = (255, 0, 0)
GREEN = (0, 255, 0)

CELL_SIZE = 40
GRID_WIDTH = 8
GRID_HEIGHT = 8
MINES_COUNT = 10

RIGHT_MARGIN = 150  

CELL_BACKGROUND = pygame.image.load('cuadrado.png')
CELL_BACKGROUND = pygame.transform.scale(CELL_BACKGROUND, (CELL_SIZE, CELL_SIZE))  

pygame.mixer.music.load('musica.mp3')
pygame.mixer.music.play(-1)  

screen = pygame.display.set_mode((GRID_WIDTH * CELL_SIZE + RIGHT_MARGIN, GRID_HEIGHT * CELL_SIZE))
pygame.display.set_caption('Buscaminas con IA')

class Cell:
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.is_mine = False
        self.is_revealed = False
        self.is_flagged = False
        self.adjacent_mines = 0

    def draw(self):
        rect = pygame.Rect(self.x * CELL_SIZE, self.y * CELL_SIZE, CELL_SIZE, CELL_SIZE)

        screen.blit(CELL_BACKGROUND, rect.topleft)

        pygame.draw.rect(screen, BLACK, rect, 1)

        if self.is_revealed:
            if self.is_mine:
                pygame.draw.circle(screen, RED, rect.center, CELL_SIZE // 4)
            elif self.adjacent_mines > 0:
                font = pygame.font.Font(None, 36)
                text = font.render(str(self.adjacent_mines), True, BLACK)
                screen.blit(text, rect.move(12, 6).topleft)

class Minesweeper:
    def __init__(self):
        self.grid = [[Cell(x, y) for y in range(GRID_HEIGHT)] for x in range(GRID_WIDTH)]
        self.place_mines()

    def place_mines(self):
        mines_placed = 0
        while mines_placed < MINES_COUNT:
            x, y = random.randint(0, GRID_WIDTH - 1), random.randint(0, GRID_HEIGHT - 1)
            if not self.grid[x][y].is_mine:
                self.grid[x][y].is_mine = True
                mines_placed += 1
        self.calculate_adjacent_mines()

    def calculate_adjacent_mines(self):
        for x in range(GRID_WIDTH):
            for y in range(GRID_HEIGHT):
                if not self.grid[x][y].is_mine:
                    self.grid[x][y].adjacent_mines = sum(
                        1 for i, j in self.get_neighbors(x, y) if self.grid[i][j].is_mine
                    )

    def get_neighbors(self, x, y):
        neighbors = []
        for i in range(max(0, x - 1), min(GRID_WIDTH, x + 2)):
            for j in range(max(0, y - 1), min(GRID_HEIGHT, y + 2)):
                if i != x or j != y:
                    neighbors.append((i, j))
        return neighbors

    def reveal_cell(self, x, y):
        if not self.grid[x][y].is_revealed:
            self.grid[x][y].is_revealed = True
            if self.grid[x][y].adjacent_mines == 0:
                for i, j in self.get_neighbors(x, y):
                    self.reveal_cell(i, j)

    def draw(self):
        for row in self.grid:
            for cell in row:
                cell.draw()

    def ai_solve(self):
        for x in range(GRID_WIDTH):
            for y in range(GRID_HEIGHT):
                if not self.grid[x][y].is_revealed:
                    self.reveal_cell(x, y)
                    self.update_screen()
                    time.sleep(1)  

    def update_screen(self):
        screen.fill(WHITE)
        self.draw()
        draw_buttons()
        pygame.display.flip()

def draw_buttons():
    font = pygame.font.Font(None, 36)
    
    pygame.draw.rect(screen, GREEN, (GRID_WIDTH * CELL_SIZE + 20, 100, 120, 40))
    text = font.render("IA Resolver", True, WHITE)
    screen.blit(text, (GRID_WIDTH * CELL_SIZE + 30, 110))

    pygame.draw.rect(screen, RED, (GRID_WIDTH * CELL_SIZE + 20, 160, 120, 40))
    text = font.render("Salir", True, WHITE)
    screen.blit(text, (GRID_WIDTH * CELL_SIZE + 50, 170))

def check_button_click(x, y):
    if GRID_WIDTH * CELL_SIZE + 20 <= x <= GRID_WIDTH * CELL_SIZE + 140 and 100 <= y <= 140:
        return "IA"
    elif GRID_WIDTH * CELL_SIZE + 20 <= x <= GRID_WIDTH * CELL_SIZE + 140 and 160 <= y <= 200:
        return "Salir"
    return None

game = Minesweeper()

running = True
auto_solve = False
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.MOUSEBUTTONDOWN:
            x, y = pygame.mouse.get_pos()
            button_clicked = check_button_click(x, y)
            if button_clicked == "IA":
                auto_solve = True
            elif button_clicked == "Salir":
                running = False
            else:
                cell_x, cell_y = x // CELL_SIZE, y // CELL_SIZE
                if cell_x < GRID_WIDTH and not game.grid[cell_x][cell_y].is_flagged:
                    game.reveal_cell(cell_x, cell_y)

    if auto_solve:
        game.ai_solve()
        auto_solve = False  

    screen.fill(WHITE)
    game.draw()
    draw_buttons()
    pygame.display.flip()

pygame.quit()

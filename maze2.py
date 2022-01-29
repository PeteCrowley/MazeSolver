import random
import pygame

pygame.init()
SCREEN_SIZE = WIDTH, HEIGHT, = 600, 600
SCREEN = pygame.display.set_mode(SCREEN_SIZE)
pygame.display.set_caption("Maze")
pygame.event.set_allowed([pygame.QUIT, pygame.KEYDOWN])

CLOCK = pygame.time.Clock()
FPS = 5

BLACK = (0, 0, 0)
BLUE = (0, 100, 204)
RED = (220, 20, 60)
LIME = (50, 205, 50)
DARK_BLUE = (0, 0, 139)


class Maze:
    def __init__(self, size=20):
        self.size = size
        self.maze = [[0] * size for _ in range(size)]
        self.rectsize = WIDTH * 9 // 10 // size
        self.start = (1, 1)
        self.end = (size - 2, size - 2)
        self.player_x, self.player_y = self.start
        self.visited = {(1, 1): 1}
        self.last = (1, 1)
        self.gen_random_maze()

    def gen_random_maze(self):
        for c in range(self.size):
            for r in range(self.size):
                if r == 0 or c == 0 or r == self.size - 1 or c == self.size - 1:
                    self.maze[r][c] = 1
                elif r == 1 and c == 1 or r == self.size - 2 or c == self.size - 2:
                    pass
                elif r < 4 and c < 4 or r > self.size - 5 or c > self.size - 5:
                    if random.random() > 0.9:
                        self.maze[r][c] = 1
                elif random.random() > 0.7:
                    self.maze[r][c] = 1

    def update_maze(self):
        for column in range(len(self.maze)):
            for row in range(len(self.maze)):
                if self.maze[column][row] == 1:
                    continue
                elif (row, column) == (self.player_x, self.player_y):
                    self.maze[column][row] = 2
                elif (row, column) == self.start:
                    self.maze[column][row] = 3
                elif (row, column) == self.end:
                    self.maze[column][row] = 4
                elif (row, column) in self.visited:
                    self.maze[column][row] = 5
                else:
                    self.maze[column][row] = 0

    def show_maze(self):
        for row in self.maze:
            print(row)
        print('\n')

    def pygame_maze(self, screen):
        x = 50
        y = 50
        for column in range(len(self.maze)):
            for row in range(len(self.maze)):
                square = pygame.Rect((x, y), (self.rectsize, self.rectsize))
                if self.maze[column][row] == 1:
                    screen.fill(BLACK, square)
                elif self.maze[column][row] == 2:
                    screen.fill(RED, square)
                elif self.maze[column][row] == 3:
                    screen.fill(DARK_BLUE, square)
                elif self.maze[column][row] == 4:
                    screen.fill(LIME, square)
                x += self.rectsize
            x = 50
            y += self.rectsize

    def reset(self):
        self.maze = [[0] * self.size for _ in range(self.size)]
        self.gen_random_maze()
        self.player_x, self.player_y = self.start
        self.visited = {(1, 1): 1}

    def move_down(self):
        if self.maze[self.player_y + 1][self.player_x] != 1:
            self.last = (self.player_x, self.player_y)
            self.player_y += 1
            self.add_to_set((self.player_x, self.player_y))

    def move_up(self):
        if self.maze[self.player_y - 1][self.player_x] != 1:
            self.last = (self.player_x, self.player_y)
            self.player_y -= 1
            self.add_to_set((self.player_x, self.player_y))

    def move_right(self):
        if self.maze[self.player_y][self.player_x + 1] != 1:
            self.last = (self.player_x, self.player_y)
            self.player_x += 1
            self.add_to_set((self.player_x, self.player_y))

    def move_left(self):
        if self.maze[self.player_y][self.player_x - 1] != 1:
            self.last = (self.player_x, self.player_y)
            self.player_x -= 1
            self.add_to_set((self.player_x, self.player_y))

    def ai_move(self):
        right = (self.player_x + 1, self.player_y)
        down = (self.player_x, self.player_y + 1)
        left = (self.player_x - 1, self.player_y)
        up = (self.player_x, self.player_y - 1)
        first = []
        second = []
        third = []
        back = None
        for square in [up, down, left, right]:
            if self.is_wall(square):
                continue
            elif square not in self.visited and (square == right or square == down):
                first.append(square)
            elif square not in self.visited:
                second.append(square)
            elif square != self.last:
                third.append((self.visited[square], square))
            else:
                back = square
        if first:
            choice = random.choice(first)
        elif second:
            choice = random.choice(second)
        elif third:
            random.shuffle(third)
            third.sort()
            choice = third[0][1]
        else:
            choice = back
        if choice == up:
            self.move_up()
        elif choice == down:
            self.move_down()
        elif choice == right:
            self.move_right()
        elif choice == left:
            self.move_left()

    def is_wall(self, square):
        return self.maze[square[1]][square[0]] == 1

    def add_to_set(self, square):
        if square in self.visited:
            self.visited[square] += 1
        else:
            self.visited[square] = 1


def start(maze):
    running = True
    while running:
        CLOCK.tick(FPS)
        maze.ai_move()
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_DOWN:
                    maze.move_down()
                elif event.key == pygame.K_UP:
                    maze.move_up()
                elif event.key == pygame.K_LEFT:
                    maze.move_left()
                elif event.key == pygame.K_RIGHT:
                    maze.move_right()
                elif event.key == pygame.K_s:
                    maze.show_maze()
                elif event.key == pygame.K_r:
                    maze.reset()

        if (maze.player_x, maze.player_y) == maze.end:
            # maze.reset()
            return
        SCREEN.fill(BLUE)
        maze.update_maze()
        maze.pygame_maze(SCREEN)
        pygame.display.flip()


if __name__ == "__main__":
    maze1 = Maze(size=20)
    start(maze1)
    FPS = 20
    maze2 = Maze(size=50)
    start(maze2)
    FPS = 50
    maze3 = Maze(size=100)
    start(maze3)

# self.maze = [[1, 1, 1, 1, 1, 1, 1, 1, 1],
#              [1, 0, 1, 0, 0, 0, 0, 0, 1],
#              [1, 0, 1, 0, 1, 0, 1, 0, 1],
#              [1, 0, 1, 0, 1, 0, 1, 0, 1],
#              [1, 0, 1, 0, 1, 0, 1, 0, 1],
#              [1, 0, 1, 0, 1, 0, 1, 0, 1],
#              [1, 0, 1, 1, 1, 0, 1, 0, 1],
#              [1, 0, 0, 0, 0, 0, 1, 0, 1],
#              [1, 1, 1, 1, 1, 1, 1, 1, 1]]
# self.maze = [[1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1],
#              [1, 0, 1, 0, 0, 1, 1, 1, 1, 0, 0, 1, 1, 0, 0, 0, 0, 0, 0, 1],
#              [1, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1],
#              [1, 0, 1, 0, 0, 1, 1, 1, 1, 1, 0, 1, 1, 1, 1, 0, 1, 0, 1, 1],
#              [1, 0, 1, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1],
#              [1, 0, 1, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1],
#              [1, 0, 1, 1, 1, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1],
#              [1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1],
#              [1, 0, 0, 1, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1],
#              [1, 0, 1, 0, 0, 0, 0, 0, 0, 0, 1, 1, 1, 1, 1, 1, 1, 1, 0, 1],
#              [1, 0, 0, 1, 1, 1, 1, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 1],
#              [1, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 1],
#              [1, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1],
#              [1, 1, 1, 1, 1, 1, 0, 0, 0, 0, 0, 0, 0, 1, 1, 1, 1, 1, 0, 1],
#              [1, 0, 0, 0, 0, 1, 0, 0, 1, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 1],
#              [1, 0, 0, 0, 0, 1, 0, 0, 1, 1, 1, 0, 0, 1, 1, 1, 1, 1, 0, 1],
#              [1, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 1, 0, 1],
#              [1, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 1, 0, 1],
#              [1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 1, 0, 1],
#              [1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1]]

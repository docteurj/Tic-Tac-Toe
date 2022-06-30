import pygame as pg
import sys
from random import randint
#window and cell size
size_window = 600
size_cell = size_window // 3
INF = float('inf')
v2 = pg.math.Vector2
center_cell = v2(size_cell / 2)

class Game:
    def __init__(self):
        pg.init()
        self.screen = pg.display.set_mode([size_window] * 2)
        self.clock = pg.time.Clock()
        self.tic_tac_toe = TicTacToe(self)

    def new_game(self):
        self.tic_tac_toe = TicTacToe(self)

    def check_events(self):
        for event in pg.event.get():
            if event.type == pg.QUIT:
                pg.quit()
                sys.exit()
            if event.type == pg.KEYDOWN:
                if event.key == pg.K_SPACE:
                    self.new_game()

    def run(self):
        while True:
            self.tic_tac_toe.run()
            self.check_events()
            pg.display.update()
            self.clock.tick(60)

class TicTacToe:
    def __init__(self, game):
        self.game = game
#images for x and o
        self.field_image = self.get_scaled_image(path='resources/grid.png', res=[size_window] * 2)
        self.O_image = self.get_scaled_image(path='resources/o.png', res=[size_cell] * 2)
        self.X_image = self.get_scaled_image(path='resources/x2.png', res=[size_cell] * 2)
#array for tic tac toe
        self.game_array = [[INF, INF, INF],
                           [INF, INF, INF],
                           [INF, INF, INF]]
        self.player = randint(0, 1)

        self.line_indices_array = [[(0, 0), (0, 1), (0, 2)],
                                   [(1, 0), (1, 1), (1, 2)],
                                   [(2, 0), (2, 1), (2, 2)],
                                   [(0, 0), (1, 0), (2, 0)],
                                   [(0, 1), (1, 1), (2, 1)],
                                   [(0, 2), (1, 2), (2, 2)],
                                   [(0, 0), (1, 1), (2, 2)],
                                   [(0, 2), (1, 1), (2, 0)]]
        self.winner = None
        self.game_steps = 0
        self.font = pg.font.SysFont('Verdana', size_cell // 4, True)
#check win condtions
    def check_winner(self):
        for line_indices in self.line_indices_array:
            sum_line = sum([self.game_array[i][j] for i, j in line_indices])
            if sum_line in {0, 3}:
                self.winner = 'XO'[sum_line == 0]
                self.winner_line = [v2(line_indices[0][::-1]) * size_cell + center_cell,
                                    v2(line_indices[2][::-1]) * size_cell + center_cell]

    def run_game_process(self):
        current_cell = v2(pg.mouse.get_pos()) // size_cell
        col, row = map(int, current_cell)
        left_click = pg.mouse.get_pressed()[0]

        if left_click and self.game_array[row][col] == INF and not self.winner:
            self.game_array[row][col] = self.player
            self.player = not self.player
            self.game_steps += 1
            self.check_winner()

    def draw_objects(self):
        for y, row in enumerate(self.game_array):
            for x, obj in enumerate(row):
                if obj != INF:
                    self.game.screen.blit(self.X_image if obj else self.O_image, v2(x, y) * size_cell)
#win line and winner announcement
    def draw_winner(self):
        if self.winner:
            pg.draw.line(self.game.screen, 'red', *self.winner_line, size_cell // 8)
            label = self.font.render(f'Player "{self.winner}" wins!', True, 'red', 'black')
            self.game.screen.blit(label, (size_window // 2 - label.get_width() // 2, size_window // 4))

    def draw(self):
        self.game.screen.blit(self.field_image, (0, 0))
        self.draw_objects()
        self.draw_winner()

    @staticmethod
    def get_scaled_image(path, res):
        img = pg.image.load(path)
        return pg.transform.smoothscale(img, res)
    
    def print_caption(self):
        pg.display.set_caption(f'Player "{"OX"[self.player]}" turn!')
        if self.winner:
            pg.display.set_caption(f'Player "{self.winner}" wins!')
        elif self.game_steps == 9:
            pg.display.set_caption(f'Game Over! Press Space to Restart')
    

    def run(self):
        self.print_caption()
        self.draw()
        self.run_game_process()

#run game
if __name__ == '__main__':
    game = Game()
    game.run()

#possible future improvements:
#add a score counter
#possible bots: easy, hard
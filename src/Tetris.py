import pygame
import random
import copy
import numpy as np
from copy import deepcopy
from collections import Counter
from Agent import Agent
# Cài đặt màn hình
SCREEN_WIDTH = 1000  # Tăng chiều rộng để chứa bảng điểm
SCREEN_HEIGHT = 600
GRID_WIDTH = 10
GRID_HEIGHT = 20
BLOCK_SIZE = 30

# Kích thước và vị trí bảng chơi
GAME_AREA_WIDTH = GRID_WIDTH * BLOCK_SIZE
GAME_AREA_HEIGHT = GRID_HEIGHT * BLOCK_SIZE
GAME_AREA_X = (SCREEN_WIDTH - GAME_AREA_WIDTH - 300) // 2  # Dịch sang trái để chừa chỗ cho bảng điểm
GAME_AREA_Y = (SCREEN_HEIGHT - GAME_AREA_HEIGHT) // 2

# Vị trí bảng điểm
SCORE_BOARD_X = GAME_AREA_X + GAME_AREA_WIDTH + 50
SCORE_BOARD_Y = GAME_AREA_Y
SCORE_BOARD_WIDTH = 250
SCORE_BOARD_HEIGHT = GAME_AREA_HEIGHT

# Giữ nguyên các định nghĩa về BLOCK_WIDTH, BLOCK_LENGTH, COLORS, PIECES_DICT và POSSIBLE_KEYS như cũ
# Cài đặt Tetromino
BLOCK_WIDTH = 4
BLOCK_LENGTH = 4

# Màu sắc
COLORS = [
    (0, 0, 0),        # Đen (nền)
    (0, 255, 255),    # Xanh lam (I)
    (255, 255, 0),    # Vàng (O)
    (0, 0, 255),      # Xanh dương (J)
    (255, 165, 0),    # Cam (L)
    (255, 0, 0),      # Đỏ (Z)
    (0, 255, 0),      # Xanh lá (S)
    (128, 0, 128)     # Tím (T)
]

# Các hình dạng Tetromino
ipieces = [[[0, 0, 1, 0], 
            [0, 0, 1, 0], 
            [0, 0, 1, 0], 
            [0, 0, 1, 0]],
                          [[0, 0, 0, 0], 
                           [0, 0, 0, 0], 
                           [1, 1, 1, 1], 
                           [0, 0, 0, 0]],
                                         [[0, 1, 0, 0], 
                                          [0, 1, 0, 0], 
                                          [0, 1, 0, 0], 
                                          [0, 1, 0, 0]],
                                                        [[0, 0, 0, 0], 
                                                         [1, 1, 1, 1], 
                                                         [0, 0, 0, 0], 
                                                         [0, 0, 0, 0]]]
opieces = [[[0, 0, 0, 0], 
            [0, 2, 2, 0], 
            [0, 2, 2, 0], 
            [0, 0, 0, 0]],
                          [[0, 0, 0, 0], 
                           [0, 2, 2, 0], 
                           [0, 2, 2, 0], 
                           [0, 0, 0, 0]],
                                         [[0, 0, 0, 0], 
                                          [0, 2, 2, 0], 
                                          [0, 2, 2, 0], 
                                          [0, 0, 0, 0]],
                                                        [[0, 0, 0, 0], 
                                                         [0, 2, 2, 0], 
                                                         [0, 2, 2, 0], 
                                                         [0, 0, 0, 0]]]

jpieces = [[[0, 3, 3, 0], 
            [0, 0, 3, 0], 
            [0, 0, 3, 0], 
            [0, 0, 0, 0]],
                          [[0, 0, 0, 0], 
                           [0, 3, 3, 3], 
                           [0, 3, 0, 0], 
                           [0, 0, 0, 0]],
                                         [[0, 0, 3, 0], 
                                          [0, 0, 3, 0], 
                                          [0, 0, 3, 3], 
                                          [0, 0, 0, 0]],
                                                        [[0, 0, 0, 3], 
                                                         [0, 3, 3, 3], 
                                                         [0, 0, 0, 0], 
                                                         [0, 0, 0, 0]]]

lpieces = [[[0, 0, 4, 0], 
            [0, 0, 4, 0], 
            [0, 4, 4, 0], 
            [0, 0, 0, 0]],
                          [[0, 0, 0, 0], 
                           [0, 4, 4, 4], 
                           [0, 0, 0, 4], 
                           [0, 0, 0, 0]],
                                         [[0, 0, 4, 4], 
                                          [0, 0, 4, 0], 
                                          [0, 0, 4, 0], 
                                          [0, 0, 0, 0]],
                                                        [[0, 4, 0, 0], 
                                                         [0, 4, 4, 4], 
                                                         [0, 0, 0, 0], 
                                                         [0, 0, 0, 0]]]
zpieces = [[[0, 5, 0, 0], 
            [0, 5, 5, 0], 
            [0, 0, 5, 0], 
            [0, 0, 0, 0]],
                          [[0, 0, 0, 0], 
                           [0, 5, 5, 0], 
                           [5, 5, 0, 0], 
                           [0, 0, 0, 0]],
                                         [[0, 5, 0, 0], 
                                          [0, 5, 5, 0], 
                                          [0, 0, 5, 0], 
                                          [0, 0, 0, 0]],
                                                        [[0, 0, 5, 5], 
                                                         [0, 5, 5, 0], 
                                                         [0, 0, 0, 0], 
                                                         [0, 0, 0, 0]]]
spieces = [[[0, 0, 6, 0], 
            [0, 6, 6, 0], 
            [0, 6, 0, 0], 
            [0, 0, 0, 0]],
                          [[0, 0, 0, 0], 
                           [0, 6, 6, 0], 
                           [0, 0, 6, 6], 
                           [0, 0, 0, 0]],
                                         [[0, 0, 6, 0], 
                                          [0, 6, 6, 0], 
                                          [0, 6, 0, 0], 
                                          [0, 0, 0, 0]],
                                                        [[6, 6, 0, 0], 
                                                         [0, 6, 6, 0], 
                                                         [0, 0, 0, 0], 
                                                         [0, 0, 0, 0]]]


tpieces = [[[0, 0, 7, 0], 
            [0, 7, 7, 0], 
            [0, 0, 7, 0], 
            [0, 0, 0, 0]],
                          [[0, 0, 0, 0], 
                           [0, 7, 7, 7], 
                           [0, 0, 7, 0], 
                           [0, 0, 0, 0]],
                                         [[0, 0, 7, 0], 
                                          [0, 0, 7, 7], 
                                          [0, 0, 7, 0], 
                                          [0, 0, 0, 0]],
                                                        [[0, 0, 7, 0], 
                                                         [0, 7, 7, 7], 
                                                         [0, 0, 0, 0], 
                                                         [0, 0, 0, 0]]]


PIECES_DICT = {
    'I': ipieces,
    'O': opieces,
    'J': jpieces,
    'L': lpieces,
    'Z': zpieces,
    'S': spieces,
    'T': tpieces
}

POSSIBLE_KEYS = ['I', 'O', 'J', 'L', 'Z', 'S', 'T']

class Piece:
    def __init__(self, _type, possible_shapes):
        self._type = _type
        self.possible_shapes = possible_shapes
        self.current_shape_id = 0 

    def block_type(self):
        return self._type

    def reset(self):
        self.current_shape_id = 0

    def return_pos_color(self, px, py):
        feasibles = []
        block = self.now_block()

        for x in range(BLOCK_WIDTH):
            for y in range(BLOCK_LENGTH):
                if block[x][y] > 0:
                    feasibles.append([px + x, py + y, block[x][y]])
        return feasibles

    def return_pos(self, px, py):
        feasibles = []
        block = self.now_block()

        for x in range(BLOCK_WIDTH):
            for y in range(BLOCK_LENGTH):
                if block[x][y] > 0:
                    feasibles.append([px + x, py + y])
        return feasibles

    def get_feasible(self):
        feasibles = []
        b = self.now_block()

        for x in range(BLOCK_WIDTH):
            for y in range(BLOCK_LENGTH):
                if b[x][y] > 0:
                    feasibles.append([x, y])
        return feasibles

    def now_block(self):
        return self.possible_shapes[self.current_shape_id]

    def rotate(self, _dir=1):
        self.current_shape_id += _dir
        self.current_shape_id %= len(self.possible_shapes)

class Buffer:
    def __init__(self):
        self.now_list = []
        self.next_list = []

        self.fill(self.now_list)
        self.fill(self.next_list)

    def new_block(self):
        out = self.now_list.pop(0)
        self.now_list.append(self.next_list.pop(0))

        if len(self.next_list) == 0:
            self.fill(self.next_list)

        return out

    def fill(self, _list):
        pieces_keys = copy.deepcopy(POSSIBLE_KEYS)
        random.shuffle(pieces_keys)

        for key in pieces_keys:
            _list.append(Piece(key, PIECES_DICT[key]))
class Tetris:
    def __init__(self):
        pygame.init()
        self.screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
        pygame.display.set_caption('DAI CHÌM 2K4')
        self.clock = pygame.time.Clock()
        self.font = pygame.font.Font(None, 36)
        
        # Khởi tạo trạng thái game
        self.grid = [[0 for _ in range(GRID_WIDTH)] for _ in range(GRID_HEIGHT)]
        self.score = 0
        self.lines = 0
        self.level = 1
        self.game_over = False
        
        # Khởi tạo Buffer và Piece
        self.piece_buffer = Buffer()
        self.current_piece = self.piece_buffer.new_block()
        self.next_piece = self.piece_buffer.now_list[0]
        
        # Vị trí hiện tại của Tetromino
        self.current_x = GRID_WIDTH // 2 - BLOCK_WIDTH // 2
        self.current_y = -2
        
        # Tốc độ rơi
        self.drop_speed = 0.5 
        self.drop_time = 0 
        # Các action có thể dùng 
        """
            action_meaning = {
                0: "drop",
                1: "rotate_right",
                2: "right",
                3: "left", 
            }
        """
        self.mode = "player"  # Chế độ mặc định là người chơi
        self.mode_switch_time = 0  # Thời gian chuyển đổi chế độ
        self.mode_switch_delay = 2000  # 2 giây (2000 ms)
        
        # Kích thước và vị trí các nút chuyển đổi chế độ
        self.player_mode_button_rect = pygame.Rect(
            SCORE_BOARD_X + 20, SCORE_BOARD_Y + 300, 100, 40
        )
        self.ai_mode_button_rect = pygame.Rect(
            SCORE_BOARD_X + 130, SCORE_BOARD_Y + 300, 100, 40
        )

    def draw_mode_buttons(self):
        # Vẽ nút "Player Mode"
        pygame.draw.rect(self.screen, (0, 255, 0), self.player_mode_button_rect)
        player_text = self.font.render("Player", True, (0, 0, 0))
        self.screen.blit(player_text, (self.player_mode_button_rect.x + 10, self.player_mode_button_rect.y + 10))
        
        # Vẽ nút "AI Mode"
        pygame.draw.rect(self.screen, (255, 0, 0), self.ai_mode_button_rect)
        ai_text = self.font.render("AI", True, (0, 0, 0))
        self.screen.blit(ai_text, (self.ai_mode_button_rect.x + 30, self.ai_mode_button_rect.y + 10))
    def handle_events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return False
            if event.type == pygame.MOUSEBUTTONDOWN:
                if self.player_mode_button_rect.collidepoint(event.pos):
                    self.mode = "player"
                    self.mode_switch_time = pygame.time.get_ticks()  # Lưu thời gian chuyển đổi
                elif self.ai_mode_button_rect.collidepoint(event.pos):
                    self.mode = "ai"
                    self.mode_switch_time = pygame.time.get_ticks()  # Lưu thời gian chuyển đổi
        return True

    def check_mode_switch_timeout(self):
        # Kiểm tra xem đã đủ thời gian để quay về chế độ mặc định chưa
        current_time = pygame.time.get_ticks()
        if current_time - self.mode_switch_time > self.mode_switch_delay and self.game_over:
            self.mode = "ai"  # Quay về chế độ mặc định
    def draw_game_area(self):
        # Vẽ khung bảng chơi
        pygame.draw.rect(self.screen, (50, 50, 50), 
                        (GAME_AREA_X - 2, GAME_AREA_Y - 2, 
                         GAME_AREA_WIDTH + 4, GAME_AREA_HEIGHT + 4), 2)
        
        # Vẽ lưới
        for y in range(GRID_HEIGHT):
            for x in range(GRID_WIDTH):
                rect = pygame.Rect(
                    GAME_AREA_X + x * BLOCK_SIZE,
                    GAME_AREA_Y + y * BLOCK_SIZE,
                    BLOCK_SIZE, BLOCK_SIZE
                )
                if self.grid[y][x] != 0:
                    pygame.draw.rect(self.screen, COLORS[self.grid[y][x]], rect)
                pygame.draw.rect(self.screen, (30, 30, 30), rect, 1)

    def draw_score_board(self):
        # Vẽ khung bảng điểm
        pygame.draw.rect(self.screen, (50, 50, 50),
                        (SCORE_BOARD_X, SCORE_BOARD_Y,
                         SCORE_BOARD_WIDTH, SCORE_BOARD_HEIGHT), 2)
        
        # Hiển thị thông tin
        texts = [
            f"Score: {self.score}",
            f"Lines: {self.lines}",
            f"Level: {self.level}",
            "Next Piece:",
        ]
        
        for i, text in enumerate(texts):
            text_surface = self.font.render(text, True, (255, 255, 255))
            self.screen.blit(text_surface, 
                           (SCORE_BOARD_X + 20, 
                            SCORE_BOARD_Y + 30 + i * 40))

        # Vẽ next piece
        self.draw_next_piece()

    def draw_next_piece(self):
        next_block = self.next_piece.now_block()
        next_piece_x = SCORE_BOARD_X + 70
        next_piece_y = SCORE_BOARD_Y + 180
        
        for x in range(BLOCK_WIDTH):
            for y in range(BLOCK_LENGTH):
                if next_block[x][y] > 0:
                    rect = pygame.Rect(
                        next_piece_x + x * (BLOCK_SIZE - 5),
                        next_piece_y + y * (BLOCK_SIZE - 5),
                        BLOCK_SIZE - 5, BLOCK_SIZE - 5
                    )
                    pygame.draw.rect(self.screen, COLORS[next_block[x][y]], rect)
                    pygame.draw.rect(self.screen, (0, 0, 0), rect, 1)

    def draw_piece(self):
        current_block = self.current_piece.now_block()
        for x in range(BLOCK_WIDTH):
            for y in range(BLOCK_LENGTH):
                if current_block[x][y] > 0:
                    rect = pygame.Rect(
                        GAME_AREA_X + (self.current_x + x) * BLOCK_SIZE,
                        GAME_AREA_Y + (self.current_y + y) * BLOCK_SIZE,
                        BLOCK_SIZE, BLOCK_SIZE
                    )
                    pygame.draw.rect(self.screen, COLORS[current_block[x][y]], rect)
                    pygame.draw.rect(self.screen, (0, 0, 0), rect, 1)
    def is_valid_move(self, piece, offset_x, offset_y):
        current_block = piece.now_block()
        for x in range(BLOCK_WIDTH):
            for y in range(BLOCK_LENGTH):
                if current_block[x][y] > 0:
                    new_x = self.current_x + x + offset_x
                    new_y = self.current_y + y + offset_y
                    
                    if (new_x < 0 or new_x >= GRID_WIDTH or 
                        new_y >= GRID_HEIGHT or 
                        (new_y >= 0 and self.grid[new_y][new_x] != 0)):
                        return False
        return True

    def lock_piece(self):
        current_block = self.current_piece.now_block()
        for x in range(BLOCK_WIDTH):
            for y in range(BLOCK_LENGTH):
                if current_block[x][y] > 0:
                    self.grid[self.current_y + y][self.current_x + x] = current_block[x][y]
        
        # Kiểm tra và xóa các hàng đầy
        lines_cleared = 0
        y = GRID_HEIGHT - 1
        while y >= 0:
            if all(self.grid[y]):
                del self.grid[y]
                self.grid.insert(0, [0 for _ in range(GRID_WIDTH)])
                lines_cleared += 1
            else:
                y -= 1
        
        # Cập nhật điểm và level
        if lines_cleared > 0:
            self.lines += lines_cleared
            self.score += lines_cleared * 100 * self.level
            self.level = self.lines // 10 + 1
            self.drop_speed = max(0.1, 0.5 - (self.level - 1) * 0.05)
        
        # Sinh Tetromino mới
        self.current_piece = self.next_piece
        self.next_piece = self.piece_buffer.new_block()
        self.current_x = GRID_WIDTH // 2 - BLOCK_WIDTH // 2
        self.current_y = -2
        
        if not self.is_valid_move(self.current_piece, 0, 0):
            self.game_over = True

    def draw_game_over(self):
        # Tạo một lớp phủ mờ
        overlay = pygame.Surface((SCREEN_WIDTH, SCREEN_HEIGHT))
        overlay.fill((0, 0, 0))
        overlay.set_alpha(128)
        self.screen.blit(overlay, (0, 0))

        # Vẽ thông báo game over
        game_over_text = self.font.render('GAME OVER', True, (255, 0, 0))
        final_score_text = self.font.render(f'Final Score: {self.score}', True, (255, 255, 255))
        press_key_text = self.font.render('Press any key to exit', True, (255, 255, 255))

        self.screen.blit(game_over_text, 
                        (SCREEN_WIDTH // 2 - game_over_text.get_width() // 2, 
                         SCREEN_HEIGHT // 2 - 50))
        self.screen.blit(final_score_text, 
                        (SCREEN_WIDTH // 2 - final_score_text.get_width() // 2, 
                         SCREEN_HEIGHT // 2))
        self.screen.blit(press_key_text, 
                        (SCREEN_WIDTH // 2 - press_key_text.get_width() // 2, 
                         SCREEN_HEIGHT // 2 + 50))
    def rotate_piece(self):
        # Xoay Tetromino
        test_piece = copy.deepcopy(self.current_piece)
        test_piece.rotate()
        
        if self.is_valid_move(test_piece, 0, 0):
            self.current_piece = test_piece
    def preprocess_input(self):
        # padding left 5 unit and padding right 5 unit
        binary_matrix = np.array(self.grid) 
        for i in range(len(binary_matrix)):
            for j in range(len(binary_matrix[0])):
                binary_matrix[i][j] = 1 if binary_matrix[i][j] > 0 else 0
        padding = 5
        new_binary_matrix = np.zeros((20, 20), dtype=np.int32)
        for i in range(len(binary_matrix)):
            for j in range(len(binary_matrix[0])):
                new_binary_matrix[i][padding + j] = binary_matrix[i][j]
        # add block in new binary matrix
        feasibles = []
        block_start = deepcopy(self.current_piece)
        block_start.current_shape_id = 0
        b = block_start.now_block()
        b = np.array(b).T
        for x in range(BLOCK_WIDTH):
            for y in range(BLOCK_LENGTH):
                if b[x][y] > 0:
                    feasibles.append([x, y])
        if block_start.block_type() == 'I': # piece I
            for i in range(len(feasibles)):
                new_binary_matrix[-2 + feasibles[i][0]][feasibles[i][1]] = 1
        elif block_start.block_type() == 'O': # piece O
            for i in range(len(feasibles)):
                new_binary_matrix[14 + feasibles[i][0]][feasibles[i][1]] = 1
        elif block_start.block_type() == 'J': # piece J
            for i in range(len(feasibles)):
                new_binary_matrix[4 + feasibles[i][0]][feasibles[i][1]] = 1
        elif block_start.block_type() == 'L': # piece L
            for i in range(len(feasibles)):
                new_binary_matrix[9 + feasibles[i][0]][feasibles[i][1]] = 1
        elif block_start.block_type() == 'Z': # piece Z
            for i in range(len(feasibles)):
                new_binary_matrix[9 + feasibles[i][0]][17 + feasibles[i][1]] = 1
        elif block_start.block_type() == 'S': # piece S
            for i in range(len(feasibles)):
                new_binary_matrix[-1 + feasibles[i][0]][17 + feasibles[i][1]] = 1
        elif block_start.block_type() == 'T': # piece T
            for i in range(len(feasibles)):
                new_binary_matrix[4 + feasibles[i][0]][17 + feasibles[i][1]] = 1
        # fill holes 
        new_binary_matrix = np.copy(self.fill_holes(new_binary_matrix))
        return new_binary_matrix
    def fill_holes(self, binary_matrix):
        binary_matrix = binary_matrix.T
        new_binary_matrix = np.copy(binary_matrix)
        for i in range(5, len(binary_matrix) - 5):
            occupied = 0  # Set the 'Occupied' flag to 0 for each new column
            for j in range(0, len(binary_matrix[0])):  # Scan from top to bottom
                if int(binary_matrix[i][j]) > 0:
                    occupied = 1  # If a block is found, set the 'Occupied' flag to 1
                if int(binary_matrix[i][j]) == 0 and occupied == 1: 
                    new_binary_matrix[i][j] = 1
        return new_binary_matrix.T 
    # def run_auto(self): # Cho AI chơi
    #     agent = Agent()
    #     while not self.game_over:
    #         state = self.preprocess_input()
    #         action = agent.choose_action(state)
    #         # action = agent.choose_action_data(self)
    #         """
    #             action_meaning = {
    #                 0: "drop",
    #                 1: "rotate_right",
    #                 2: "right",
    #                 3: "left", 
    #             }
    #         """
    #         if action == 0: # Drop khối 
    #             # Hard drop
    #             while self.is_valid_move(self.current_piece, 0, 1):
    #                 self.current_y += 1
    #                 self.score += 2
    #             self.lock_piece()
    #         elif action == 1: # Xoay phải 
    #             self.rotate_piece()
    #         elif action == 2: # Dịch phải 
    #             if self.is_valid_move(self.current_piece, 1, 0):
    #                 self.current_x += 1
    #         elif action == 3: # Dịch trái
    #             if self.is_valid_move(self.current_piece, -1, 0):
    #                 self.current_x -= 1
    #         # # Xử lý sự kiện
    #         # for event in pygame.event.get():
    #         #     if event.type == pygame.QUIT:
    #         #         return
    #         #     if event.type == pygame.KEYDOWN:
    #         #         if event.key == pygame.K_LEFT:
    #         #             if self.is_valid_move(self.current_piece, -1, 0):
    #         #                 self.current_x -= 1
    #         #         elif event.key == pygame.K_RIGHT:
    #         #             if self.is_valid_move(self.current_piece, 1, 0):
    #         #                 self.current_x += 1
    #         #         elif event.key == pygame.K_DOWN:
    #         #             if self.is_valid_move(self.current_piece, 0, 1):
    #         #                 self.current_y += 1
    #         #                 self.score += 1
    #         #         elif event.key == pygame.K_UP:
    #         #             self.rotate_piece()
    #         #         elif event.key == pygame.K_SPACE:
    #         #             # Hard drop
    #         #             while self.is_valid_move(self.current_piece, 0, 1):
    #         #                 self.current_y += 1
    #         #                 self.score += 2
    #         #             self.lock_piece()
            
    #         # Tự động rơi
    #         current_time = pygame.time.get_ticks() / 1000
    #         if current_time - self.drop_time > self.drop_speed:
    #             self.drop_time = current_time
    #             if self.is_valid_move(self.current_piece, 0, 1):
    #                 self.current_y += 1
    #             else:
    #                 self.lock_piece()
            
    #         # Vẽ màn hình
    #         self.screen.fill((0, 0, 0))
    #         self.draw_game_area()
    #         self.draw_score_board()
    #         self.draw_piece()
    #         pygame.display.update()
    #         self.clock.tick(60)

    #     # Game Over
    #     # while True:
    #     #     for event in pygame.event.get():
    #     #         if event.type == pygame.QUIT or event.type == pygame.KEYDOWN:
    #     #             pygame.quit()
    #     #             return
            
    #     #     self.draw_game_over()
    #     #     pygame.display.update()
    # def run(self): # Cho người chơi 
    #     while not self.game_over:
    #         # Xử lý sự kiện

    #         for event in pygame.event.get():
    #             if event.type == pygame.QUIT:
    #                 return
                
    #             if event.type == pygame.KEYDOWN:
    #                 if event.key == pygame.K_LEFT:
    #                     if self.is_valid_move(self.current_piece, -1, 0):
    #                         self.current_x -= 1
    #                 elif event.key == pygame.K_RIGHT:
    #                     if self.is_valid_move(self.current_piece, 1, 0):
    #                         self.current_x += 1
    #                 elif event.key == pygame.K_DOWN:
    #                     if self.is_valid_move(self.current_piece, 0, 1):
    #                         self.current_y += 1
    #                         self.score += 1
    #                 elif event.key == pygame.K_UP:
    #                     self.rotate_piece()
    #                 elif event.key == pygame.K_SPACE:
    #                     # Hard drop
    #                     while self.is_valid_move(self.current_piece, 0, 1):
    #                         self.current_y += 1
    #                         self.score += 2
    #                     self.lock_piece()
            
    #         # Tự động rơi
    #         current_time = pygame.time.get_ticks() / 1000
    #         if current_time - self.drop_time > self.drop_speed:
    #             self.drop_time = current_time
    #             if self.is_valid_move(self.current_piece, 0, 1):
    #                 self.current_y += 1
    #             else:
    #                 self.lock_piece()
            
    #         # Vẽ màn hình
    #         self.screen.fill((0, 0, 0))
    #         self.draw_game_area()
    #         self.draw_score_board()
    #         self.draw_piece()
    #         pygame.display.update()
    #         self.clock.tick(60)

    #     # Game Over
    #     while True:
    #         for event in pygame.event.get():
    #             if event.type == pygame.QUIT or event.type == pygame.KEYDOWN:
    #                 pygame.quit()
    #                 return
            
    #         self.draw_game_over()
    #         pygame.display.update()
    def run_player_mode(self):
        # Logic dành cho chế độ người chơi
        current_time = pygame.time.get_ticks() / 1000
        if current_time - self.drop_time > self.drop_speed:
            self.drop_time = current_time
            if self.is_valid_move(self.current_piece, 0, 1):
                self.current_y += 1
            else:
                self.lock_piece()
        
        # Xử lý sự kiện bàn phím
        keys = pygame.key.get_pressed()
        if keys[pygame.K_LEFT]:
            if self.is_valid_move(self.current_piece, -1, 0):
                self.current_x -= 1
        if keys[pygame.K_RIGHT]:
            if self.is_valid_move(self.current_piece, 1, 0):
                self.current_x += 1
        if keys[pygame.K_DOWN]:
            if self.is_valid_move(self.current_piece, 0, 1):
                self.current_y += 1
                self.score += 1
        if keys[pygame.K_UP]:
            self.rotate_piece()
        if keys[pygame.K_SPACE]:
            # Hard drop
            while self.is_valid_move(self.current_piece, 0, 1):
                self.current_y += 1
                self.score += 2
            self.lock_piece()

    def run_ai_mode(self, agent):
        # Logic dành cho chế độ AI
        state = self.preprocess_input()
        action = agent.choose_action(state)
        
        if action == 0:  # Drop
            while self.is_valid_move(self.current_piece, 0, 1):
                self.current_y += 1
                self.score += 2
            self.lock_piece()
        elif action == 1:  # Xoay phải
            self.rotate_piece()
        elif action == 2:  # Dịch phải
            if self.is_valid_move(self.current_piece, 1, 0):
                self.current_x += 1
        elif action == 3:  # Dịch trái
            if self.is_valid_move(self.current_piece, -1, 0):
                self.current_x -= 1
    def main_loop(self):
        agent = Agent()
        while not self.game_over:
            if not self.handle_events():
                return
            
            # Kiểm tra thời gian chuyển đổi chế độ
            self.check_mode_switch_timeout()
            
            # Chạy chế độ tương ứng
            if self.mode == "player":
                self.run_player_mode()
            elif self.mode == "ai":
                self.run_ai_mode(agent)
            
            # Vẽ giao diện
            self.screen.fill((0, 0, 0))
            self.draw_game_area()
            self.draw_score_board()
            self.draw_piece()
            self.draw_mode_buttons()
            pygame.display.update()
            
            self.clock.tick(30)

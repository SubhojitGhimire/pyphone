import random
from PySide6.QtWidgets import QWidget
from PySide6.QtCore import Qt, QTimer, QPoint, QRect
from PySide6.QtGui import QPainter, QColor, QFont

class SnakeApp(QWidget):
    BOARD_WIDTH = 20
    BOARD_HEIGHT = 20
    DOT_SIZE = 15
    DIFFICULTIES = {"Easy": 150, "Medium": 100, "Hard": 60}

    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowTitle("Snake")
        self.setFixedSize(self.BOARD_WIDTH * self.DOT_SIZE, self.BOARD_HEIGHT * self.DOT_SIZE + 30)
        self.setFocusPolicy(Qt.FocusPolicy.StrongFocus)

        self.timer = QTimer(self)
        self.timer.timeout.connect(self.game_loop)
        
        self.game_state = "MENU"
        self.score = 0
        self.current_speed = 0

    def start_game(self, difficulty):
        self.game_state = "PLAYING"
        self.score = 0
        self.direction = "right"
        self.snake = [QPoint(5, 5), QPoint(4, 5), QPoint(3, 5)]
        self.locate_apple()
        
        self.current_speed = self.DIFFICULTIES[difficulty]
        self.timer.start(self.current_speed)
        self.update()

    def paintEvent(self, event):
        painter = QPainter(self)
        
        painter.fillRect(self.rect(), QColor("black"))
        
        if self.game_state == "PLAYING":
            self.draw_game_objects(painter)
        elif self.game_state == "GAME_OVER":
            self.draw_game_objects(painter)
            self.draw_game_over_screen(painter)
        elif self.game_state == "MENU":
            self.draw_menu_screen(painter)
            
    def draw_game_objects(self, painter):
        painter.setPen(QColor("white"))
        font = QFont('Arial', 10)
        painter.setFont(font)
        painter.drawText(10, 20, f"Score: {self.score}")

        painter.setBrush(QColor("red"))
        painter.drawRect(self.apple.x() * self.DOT_SIZE, self.apple.y() * self.DOT_SIZE + 30, self.DOT_SIZE, self.DOT_SIZE)

        painter.setBrush(QColor("green"))
        for dot in self.snake:
            painter.drawRect(dot.x() * self.DOT_SIZE, dot.y() * self.DOT_SIZE + 30, self.DOT_SIZE, self.DOT_SIZE)

    def draw_menu_screen(self, painter):
        painter.setPen(QColor("white"))
        font = QFont('Arial', 20, QFont.Weight.Bold)
        painter.setFont(font)
        painter.drawText(QRect(75, 100, 150, 40), Qt.AlignmentFlag.AlignCenter, "SNAKE")

        self.easy_button_rect = QRect(75, 175, 150, 40)
        self.medium_button_rect = QRect(75, 225, 150, 40)
        self.hard_button_rect = QRect(75, 275, 150, 40)
        
        font.setPointSize(14)
        painter.setFont(font)
        painter.drawRect(self.easy_button_rect)
        painter.drawText(self.easy_button_rect, Qt.AlignmentFlag.AlignCenter, "Easy")
        painter.drawRect(self.medium_button_rect)
        painter.drawText(self.medium_button_rect, Qt.AlignmentFlag.AlignCenter, "Medium")
        painter.drawRect(self.hard_button_rect)
        painter.drawText(self.hard_button_rect, Qt.AlignmentFlag.AlignCenter, "Hard")

    def draw_game_over_screen(self, painter):
        painter.setPen(QColor("white"))
        font = QFont('Arial', 20, QFont.Weight.Bold)
        painter.setFont(font)
        painter.drawText(self.rect(), Qt.AlignmentFlag.AlignCenter, f"Game Over\nFinal Score: {self.score}\n\nPlay Again?")

        self.easy_button_rect = QRect(75, 250, 150, 40)
        font.setPointSize(14)
        painter.setFont(font)
        painter.drawRect(self.easy_button_rect)
        painter.drawText(self.easy_button_rect, Qt.AlignmentFlag.AlignCenter, "Restart")
        
    def game_loop(self):
        if self.game_state == "PLAYING":
            self.check_apple()
            self.move_snake()
            self.check_collision()
        self.update()

    def move_snake(self):
        for i in range(len(self.snake) - 1, 0, -1):
            self.snake[i] = QPoint(self.snake[i-1].x(), self.snake[i-1].y())
        head = self.snake[0]
        if self.direction == "left": self.snake[0] = QPoint(head.x() - 1, head.y())
        elif self.direction == "right": self.snake[0] = QPoint(head.x() + 1, head.y())
        elif self.direction == "up": self.snake[0] = QPoint(head.x(), head.y() - 1)
        elif self.direction == "down": self.snake[0] = QPoint(head.x(), head.y() + 1)
            
    def check_apple(self):
        if self.snake[0] == self.apple:
            self.score += 1
            self.snake.append(QPoint(-1, -1))
            self.locate_apple()
            
    def check_collision(self):
        head = self.snake[0]
        if head in self.snake[1:] or not (0 <= head.x() < self.BOARD_WIDTH and 0 <= head.y() < self.BOARD_HEIGHT):
            self.game_state = "GAME_OVER"
            self.timer.stop()

    def locate_apple(self):
        self.apple = QPoint(random.randint(0, self.BOARD_WIDTH - 1), random.randint(0, self.BOARD_HEIGHT - 1))
        while self.apple in self.snake:
            self.apple = QPoint(random.randint(0, self.BOARD_WIDTH - 1), random.randint(0, self.BOARD_HEIGHT - 1))
            
    def keyPressEvent(self, event):
        if self.game_state != "PLAYING": return
        key = event.key()
        if key == Qt.Key.Key_Left and self.direction != "right": self.direction = "left"
        elif key == Qt.Key.Key_Right and self.direction != "left": self.direction = "right"
        elif key == Qt.Key.Key_Up and self.direction != "down": self.direction = "up"
        elif key == Qt.Key.Key_Down and self.direction != "up": self.direction = "down"
        else: super().keyPressEvent(event)

    def mousePressEvent(self, event):
        click_pos = event.pos()
        if self.game_state == "MENU":
            if self.easy_button_rect.contains(click_pos): self.start_game("Easy")
            elif self.medium_button_rect.contains(click_pos): self.start_game("Medium")
            elif self.hard_button_rect.contains(click_pos): self.start_game("Hard")
        elif self.game_state == "GAME_OVER":
             if self.easy_button_rect.contains(click_pos): self.game_state = "MENU"; self.update()
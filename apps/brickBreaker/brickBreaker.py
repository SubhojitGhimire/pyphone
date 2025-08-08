from PySide6.QtWidgets import QWidget
from PySide6.QtCore import Qt, QTimer, QRect, QPoint
from PySide6.QtGui import QPainter, QColor, QBrush, QFont

class BrickBreakerApp(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowTitle("Brick Breaker")
        
        self.setFixedSize(360, 480)
        self.setMouseTracking(True)

        self.timer = QTimer(self)
        self.timer.timeout.connect(self.game_loop)
        
        self.init_game()

    def init_game(self):
        self.game_state = "READY"
        self.score = 0

        self.paddle = QRect(150, 440, 80, 10)
        
        self.ball = QRect(0, 0, 10, 10)
        self.reset_ball()
        
        self.bricks = []
        for y in range(5):
            for x in range(6):
                self.bricks.append(QRect(x * 60 + 5, y * 20 + 50, 50, 10))

        self.timer.start(10)

    def reset_ball(self):
        self.ball_on_paddle = True
        self.ball_x_vel = 0
        self.ball_y_vel = 0
        self.ball.moveCenter(QPoint(self.paddle.center().x(), self.paddle.top() - self.ball.height()/2))

    def paintEvent(self, event):
        with QPainter(self) as painter:
            painter.setRenderHint(QPainter.RenderHint.Antialiasing)
            painter.fillRect(self.rect(), QColor("#1c1c1c"))

            font = QFont("Roboto", 12, QFont.Weight.Bold)
            painter.setFont(font)
            painter.setPen(QColor("white"))
            painter.drawText(10, 20, f"Score: {self.score}")

            painter.setBrush(QColor("lightblue"))
            painter.drawRect(self.paddle)

            painter.setBrush(QColor("white"))
            painter.drawEllipse(self.ball)

            painter.setBrush(QColor("teal"))
            for brick in self.bricks:
                painter.drawRect(brick)

            if self.game_state in ["GAME_OVER", "YOU_WIN"]:
                font.setPointSize(24)
                painter.setFont(font)
                text = "Game Over" if self.game_state == "GAME_OVER" else "You Win!"
                painter.drawText(self.rect(), Qt.AlignmentFlag.AlignCenter, f"{text}\nClick to Restart")

    def game_loop(self):
        if self.game_state == "PLAYING":
            self.move_ball()
        self.update()

    def move_ball(self):
        self.ball.translate(self.ball_x_vel, self.ball_y_vel)
        self.check_collisions()

    def check_collisions(self):
        if self.ball.left() <= 0 or self.ball.right() >= self.width():
            self.ball_x_vel = -self.ball_x_vel
        if self.ball.top() <= 0:
            self.ball_y_vel = -self.ball_y_vel
        if self.ball.top() >= self.height():
            self.game_state = "GAME_OVER"

        if self.ball.intersects(self.paddle):
            offset = self.paddle.center().x() - self.ball.center().x()
            self.ball_x_vel = -int(offset / (self.paddle.width() / 16))
            self.ball_y_vel = -abs(self.ball_y_vel)

        for brick in self.bricks[:]:
            if self.ball.intersects(brick):
                self.bricks.remove(brick)
                self.score += 10
                self.ball_y_vel = -self.ball_y_vel
                break

        if not self.bricks:
            self.game_state = "YOU_WIN"

    def mouseMoveEvent(self, event):
        new_x = event.position().x()
        half_paddle = self.paddle.width() / 2
        
        if new_x < half_paddle: new_x = half_paddle
        if new_x > self.width() - half_paddle: new_x = self.width() - half_paddle
        
        self.paddle.moveCenter(QPoint(int(new_x), self.paddle.center().y()))
        
        if self.ball_on_paddle:
            self.ball.moveCenter(QPoint(self.paddle.center().x(), self.ball.center().y()))

    def mousePressEvent(self, event):
        if self.game_state in ["GAME_OVER", "YOU_WIN"]:
            self.init_game()
        elif self.game_state == "READY":
            self.game_state = "PLAYING"
            self.ball_on_paddle = False
            self.ball_x_vel = 2 
            self.ball_y_vel = -4
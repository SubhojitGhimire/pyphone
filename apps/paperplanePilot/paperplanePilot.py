import random
from PySide6.QtWidgets import QWidget
from PySide6.QtCore import Qt, QTimer, QRect
from PySide6.QtGui import QPainter, QPixmap, QFont, QColor

class PaperPlanePilotApp(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowTitle("Paper Plane Pilot")
        self.setFixedSize(360, 640)

        self.background = QPixmap("assets/paperplanePilot/background.png")
        self.airplane_pixmap = QPixmap("assets/paperplanePilot/airplane.png").scaled(60, 40, Qt.AspectRatioMode.KeepAspectRatio, Qt.TransformationMode.SmoothTransformation)
        self.obstacle_top_pixmap = QPixmap("assets/paperplanePilot/obstacle_top.png")
        self.obstacle_bottom_pixmap = QPixmap("assets/paperplanePilot/obstacle_bottom.png")

        self.timer = QTimer(self)
        self.timer.timeout.connect(self.game_loop)
        
        self.init_game()

    def init_game(self):
        self.game_state = "READY"
        
        self.airplane_y = self.height() // 2 - self.airplane_pixmap.height() // 2
        self.airplane_velocity = 0
        self.gravity = 0.5
        self.flap_strength = -9
        
        self.obstacles = []
        self.obstacle_gap = 200
        self.obstacle_width = self.obstacle_top_pixmap.width()
        self.obstacle_speed = 3
        
        self.score = 0
        self.background_scroll_x = 0
        
        self.add_new_obstacle(self.width() + 50)
        self.add_new_obstacle(self.width() + 50 + (self.width() // 2))
        
        self.timer.start(16) # ~60 FPS

    def paintEvent(self, event):
        with QPainter(self) as painter:
            painter.setRenderHint(QPainter.RenderHint.Antialiasing)

            if not self.background.isNull():
                # self.background_scroll_x = (self.background_scroll_x - 1) % self.background.width()
                painter.drawPixmap(self.background_scroll_x, 0, self.background)
                # painter.drawPixmap(self.background_scroll_x + self.background.width(), 0, self.background)
            else:
                painter.fillRect(self.rect(), QColor("black"))
            
            for obstacle in self.obstacles:
                painter.drawPixmap(obstacle['rect_top'], self.obstacle_top_pixmap)
                painter.drawPixmap(obstacle['rect_bottom'], self.obstacle_bottom_pixmap)
            
            painter.drawPixmap(50, int(self.airplane_y), self.airplane_pixmap)

            painter.setPen(QColor("white"))
            font = QFont("Roboto", 24, QFont.Weight.Bold)
            painter.setFont(font)

            if self.game_state == "PLAYING":
                painter.drawText(self.rect(), Qt.AlignmentFlag.AlignHCenter | Qt.AlignmentFlag.AlignTop, str(self.score))
            elif self.game_state == "READY":
                painter.drawText(self.rect(), Qt.AlignmentFlag.AlignCenter, "Tap to Start")
            elif self.game_state == "GAME_OVER":
                painter.drawText(self.rect(), Qt.AlignmentFlag.AlignCenter, f"Game Over\nScore: {self.score}\nTap to Restart")

    def game_loop(self):
        if self.game_state == "PLAYING":
            self.airplane_velocity += self.gravity
            self.airplane_y += self.airplane_velocity

            for obstacle in self.obstacles:
                obstacle['rect_top'].translate(-self.obstacle_speed, 0)
                obstacle['rect_bottom'].translate(-self.obstacle_speed, 0)
                if not obstacle.get('passed') and obstacle['rect_top'].right() < 50:
                    self.score += 1
                    obstacle['passed'] = True

            if self.obstacles and self.obstacles[0]['rect_top'].right() < 0:
                self.obstacles.pop(0)
                self.add_new_obstacle(self.width())
            
            self.check_collisions()
        
        self.update()
    def mousePressEvent(self, event):
        if self.game_state == "PLAYING":
            self.airplane_velocity = self.flap_strength
        elif self.game_state == "READY":
            self.game_state = "PLAYING"
            self.airplane_velocity = self.flap_strength
        elif self.game_state == "GAME_OVER":
            self.init_game()

    def add_new_obstacle(self, x_pos):
        top_height = random.randint(100, self.height() - self.obstacle_gap - 100)
        rect_top = QRect(x_pos, 0, self.obstacle_width, top_height)
        
        bottom_y = top_height + self.obstacle_gap
        bottom_height = self.height() - bottom_y
        rect_bottom = QRect(x_pos, bottom_y, self.obstacle_width, bottom_height)
        
        self.obstacles.append({'rect_top': rect_top, 'rect_bottom': rect_bottom, 'passed': False})

    def check_collisions(self):
        airplane_rect = QRect(50, int(self.airplane_y), self.airplane_pixmap.width(), self.airplane_pixmap.height())

        if airplane_rect.bottom() > self.height() or airplane_rect.top() < 0:
            self.game_state = "GAME_OVER"
            return

        for obstacle in self.obstacles:
            print(obstacle)
            if airplane_rect.intersects(obstacle['rect_top']) or airplane_rect.intersects(obstacle['rect_bottom']):
                self.game_state = "GAME_OVER"
                return
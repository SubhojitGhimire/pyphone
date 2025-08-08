import os
import chess
import chess.pgn
import chess.engine
from PySide6.QtCore import Qt, QPointF
from PySide6.QtGui import QPixmap, QColor, QBrush, QFont
from PySide6.QtWidgets import QWidget, QHBoxLayout, QVBoxLayout, QGraphicsView, QGraphicsScene, QGraphicsRectItem, QGraphicsPixmapItem, QListWidget, QComboBox, QLabel, QPushButton, QSlider, QMessageBox, QFileDialog, QGridLayout, QFrame

THEMES = {
    "Brown": {"light": QColor("#F0D9B5"), "dark": QColor("#B58863"), "highlight": QColor(255, 255, 0, 100), "pieces": ":/assets/chess/theme_1/"},
    "Green": {"light": QColor("#EAD7B9"), "dark": QColor("#769656"), "highlight": QColor(255, 255, 0, 100), "pieces": ":/assets/chess/theme_2/"},
    "Blue": {"light": QColor("#DEE3E6"), "dark": QColor("#8CA2AD"), "highlight": QColor(255, 255, 0, 100), "pieces": ":/assets/chess/theme_3/"}
}

class ChessPieceItem(QGraphicsPixmapItem):
    def __init__(self, piece, size):
        super().__init__()
        self.piece = piece; self.size = size
        self.set_pixmap(THEMES["Brown"]["pieces"])
        self.setFlag(QGraphicsPixmapItem.GraphicsItemFlag.ItemIsMovable)
    
    def set_pixmap(self, piece_path):
        piece_char = self.piece.symbol()
        color = "white" if self.piece.color == chess.WHITE else "black"
        piece_map = {'P':'Pawn','R':'Rook','N':'Knight','B':'Bishop','Q':'Queen','K':'King'}
        filename = f"{color}{piece_map[piece_char.upper()]}.png"
        pixmap = QPixmap(os.path.join(piece_path, filename))
        self.setPixmap(pixmap.scaled(self.size, self.size, Qt.AspectRatioMode.KeepAspectRatio, Qt.TransformationMode.SmoothTransformation))

    def mouseReleaseEvent(self, event):
        super().mouseReleaseEvent(event)
        self.scene().handle_piece_drop(self, self.pos())

class ChessApp(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.board = chess.Board()
        self.SQUARE_SIZE = 35
        self.engine = None
        self.current_theme = "Brown"
        self.last_move = None
        self.board_is_flipped = False
        
        self.game_state = "READY"

        main_layout = QVBoxLayout(self)
        main_layout.setContentsMargins(5, 5, 5, 5)
        main_layout.setSpacing(10)
        
        self.scene = QGraphicsScene()
        self.scene.handle_piece_drop = self.handle_piece_drop
        self.view = QGraphicsView(self.scene)
        self.view.setFixedSize(9* self.SQUARE_SIZE + 2, 9 * self.SQUARE_SIZE + 2)
        main_layout.addWidget(self.view, 0, Qt.AlignmentFlag.AlignCenter)

        options_panel = self.create_options_panel()
        main_layout.addWidget(options_panel)

        main_layout.addWidget(QLabel("Moves:"))
        self.move_list = QListWidget()
        main_layout.addWidget(self.move_list)

        self.new_game()
        self.init_engine()

    def create_options_panel(self):
        panel = QFrame()
        panel.setFrameShape(QFrame.Shape.StyledPanel)
        layout = QGridLayout(panel)

        self.mode_combo = QComboBox(); self.mode_combo.addItems(["Player vs. AI", "Player vs. Player"])
        self.theme_combo = QComboBox(); self.theme_combo.addItems(THEMES.keys())
        self.theme_combo.currentTextChanged.connect(self.change_theme)
        layout.addWidget(QLabel("Mode:"), 0, 0); layout.addWidget(self.mode_combo, 0, 1)
        layout.addWidget(QLabel("Theme:"), 0, 2); layout.addWidget(self.theme_combo, 0, 3)

        self.ai_level_label = QLabel("AI Level: 1")
        self.ai_level_slider = QSlider(Qt.Orientation.Horizontal); self.ai_level_slider.setRange(1, 20)
        self.ai_level_slider.valueChanged.connect(self.set_ai_difficulty)
        layout.addWidget(self.ai_level_label, 1, 0, 1, 2)
        layout.addWidget(self.ai_level_slider, 1, 2, 1, 2)
        
        start_btn = QPushButton("Start Game"); start_btn.clicked.connect(self.start_game)
        reset_btn = QPushButton("Reset Board"); reset_btn.clicked.connect(self.new_game)
        flip_btn = QPushButton("Flip Board"); flip_btn.clicked.connect(self.flip_board)
        layout.addWidget(start_btn, 2, 0, 1, 2)
        layout.addWidget(reset_btn, 2, 2, 1, 2)
        layout.addWidget(flip_btn, 3, 0, 1, 4)

        import_btn = QPushButton("Import PGN"); import_btn.clicked.connect(self.import_pgn)
        export_btn = QPushButton("Export PGN"); export_btn.clicked.connect(self.export_pgn)
        layout.addWidget(import_btn, 4, 0, 1, 2)
        layout.addWidget(export_btn, 4, 2, 1, 2)

        return panel

    def new_game(self):
        self.game_state = "READY"
        self.board.reset()
        self.last_move = None
        self.move_list.clear()
        if self.engine: self.engine.quit(); self.init_engine()
        self.draw_board_and_pieces()

    def start_game(self):
        self.game_state = "PLAYING"
        if self.mode_combo.currentText() == "Player vs. AI" and self.board.turn == chess.BLACK:
            self.ai_move()

    def handle_piece_drop(self, piece_item, pos):
        if self.game_state != "PLAYING":
            QMessageBox.information(self, "Game Not Started", "Press Start Button after selecting game modes")
            self.draw_board_and_pieces()
            return
        
        file = int(pos.x() / self.SQUARE_SIZE)
        rank = int(pos.y() / self.SQUARE_SIZE)
        rank = 7 - rank if not self.board_is_flipped else rank
        file = file if not self.board_is_flipped else 7 - file
        
        to_square = chess.square(file, rank)
        from_square = piece_item.from_square
        
        move = chess.Move(from_square, to_square)
        if self.board.piece_type_at(from_square) == chess.PAWN and rank in [0, 7]:
            move.promotion = chess.QUEEN

        if move in self.board.legal_moves:
            self.make_move(move)
            if self.mode_combo.currentText() == "Player vs. AI":
                self.ai_move()
        
        self.draw_board_and_pieces()
    
    def make_move(self, move):
        self.last_move = move
        self.move_list.addItem(self.board.san(move))
        self.board.push(move)
        self.check_game_over()
        
    def ai_move(self):
        if self.engine and self.game_state == "PLAYING" and not self.board.is_game_over():
            result = self.engine.play(self.board, chess.engine.Limit(time=0.5))
            self.make_move(result.move)
        else:
            QMessageBox.information(self, "Game Engine Not Found", "stockfish.exe not found. To play against AI, please follow instructions on README.md on how to initiate free stockfish engine.\n\nYou can only play PVP mode for now.")

    def check_game_over(self):
        if self.board.is_game_over():
            self.game_state = "GAME_OVER"
            outcome = self.board.outcome()
            if outcome.winner is True: msg = "Checkmate! White wins."
            elif outcome.winner is False: msg = "Checkmate! Black wins."
            else: msg = f"{outcome.termination.name.title()}! It's a draw."
            QMessageBox.information(self, "Game Over", msg)
    
    def init_engine(self):
        stockfish_path = "stockfish.exe" if os.name == 'nt' else "stockfish"
        if os.path.exists(stockfish_path):
            try:
                self.engine = chess.engine.SimpleEngine.popen_uci(stockfish_path)
                self.set_ai_difficulty(self.ai_level_slider.value())
            except Exception as e: self.engine = None
        else: self.engine = None

    def set_ai_difficulty(self, value):
        self.ai_level_label.setText(f"AI Level: {value}")
        if self.engine: self.engine.configure({"Skill Level": value})

    def draw_board_and_pieces(self):
        self.scene.clear()
        theme = THEMES[self.current_theme]
        for i in range(64):
            rank, file = divmod(i, 8)
            color = theme['light'] if (rank + file) % 2 == 0 else theme['dark']
            rect_item = QGraphicsRectItem(file * self.SQUARE_SIZE, rank * self.SQUARE_SIZE, self.SQUARE_SIZE, self.SQUARE_SIZE)
            rect_item.setBrush(QBrush(color)); self.scene.addItem(rect_item)
        if self.last_move:
            for square in [self.last_move.from_square, self.last_move.to_square]:
                r = 7 - chess.square_rank(square) if not self.board_is_flipped else chess.square_rank(square)
                f = chess.square_file(square) if not self.board_is_flipped else 7 - chess.square_file(square)
                highlight_item = QGraphicsRectItem(f * self.SQUARE_SIZE, r * self.SQUARE_SIZE, self.SQUARE_SIZE, self.SQUARE_SIZE)
                highlight_item.setBrush(QBrush(theme['highlight'])); self.scene.addItem(highlight_item)
        for square in chess.SQUARES:
            piece = self.board.piece_at(square)
            if piece:
                rank = 7 - chess.square_rank(square) if not self.board_is_flipped else chess.square_rank(square)
                file = chess.square_file(square) if not self.board_is_flipped else 7 - chess.square_file(square)
                piece_item = ChessPieceItem(piece, self.SQUARE_SIZE)
                piece_item.set_pixmap(theme["pieces"]); piece_item.setPos(file * self.SQUARE_SIZE, rank * self.SQUARE_SIZE)
                piece_item.from_square = square; self.scene.addItem(piece_item)

    def change_theme(self, theme_name):
        self.current_theme = theme_name; self.draw_board_and_pieces()

    def flip_board(self):
        self.board_is_flipped = not self.board_is_flipped; self.draw_board_and_pieces()

    def import_pgn(self):
        path, _ = QFileDialog.getOpenFileName(self, "Import PGN", "", "PGN Files (*.pgn)")
        if path:
            with open(path) as f:
                game = chess.pgn.read_game(f)
                if game:
                    self.new_game()
                    self.board = game.board()
                    for move in game.mainline_moves(): self.make_move(move)
                    self.draw_board_and_pieces()

    def export_pgn(self):
        path, _ = QFileDialog.getSaveFileName(self, "Export PGN", "", "PGN Files (*.pgn)")
        if path:
            game = chess.pgn.Game.from_board(self.board)
            with open(path, "w") as f: f.write(str(game))

    def closeEvent(self, event):
        if self.engine: self.engine.quit()
        super().closeEvent(event)
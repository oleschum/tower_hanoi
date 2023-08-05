import sys
from PySide6.QtWidgets import QApplication, QWidget, QPushButton, QLabel, QSpinBox, QHBoxLayout, QVBoxLayout
from PySide6.QtCore import QTimer
from matplotlib.figure import Figure
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas


class HanoiGame:
    def __init__(self, num_disk):
        self.num_disk = num_disk
        self.rods = [[i for i in range(num_disk, 0, -1)], [], []]
        self.current_move = 0
        self.n_moves = 0
        self.moves = []
        self.solve()

    def solve(self):
        self.solve_hanoi(self.num_disk, 0, 2, 1)

    def solve_hanoi(self, n, source, target, auxiliary):
        if n > 0:
            self.solve_hanoi(n - 1, source, auxiliary, target)
            self.moves.append((source, target))
            self.n_moves += 1
            self.solve_hanoi(n - 1, auxiliary, target, source)

    def next_move(self):
        if self.current_move < self.n_moves:
            source, target = self.moves[self.current_move]
            # print("next move: put top element from {} to {}".format(source, target))
            if self.rods[source]:
                self.rods[target].insert(0, self.rods[source].pop(0))
                self.current_move += 1
        else:
            print("Done")

    def prev_move(self):
        if self.current_move > 0:
            self.current_move -= 1
            target, source = self.moves[self.current_move]
            # print("prev move: put top element from {} to {}".format(source, target))
            self.rods[target].insert(0, self.rods[source].pop(0))
        else:
            print("At start")

    def reset(self, clear_moves=False):
        self.rods = [[i for i in range(self.num_disk, 0, -1)], [], []]
        self.current_move = 0

        if clear_moves:
            self.moves = []


class TowerOfHanoi(QWidget):
    def __init__(self):
        super().__init__()
        self.num_disk = 3
        self.hanoi_game = HanoiGame(self.num_disk)
        self.playing = False
        self.play_timer = None
        self.play_timeout_ms = 300

        self.init_ui()

    def init_ui(self):
        self.fig = Figure()
        self.canvas = FigureCanvas(self.fig)
        self.ax = self.fig.add_subplot(111)

        self.setup_axis()
        self.create_disk()

        self.play_button = QPushButton('Play', self)
        self.play_button.clicked.connect(self.play)

        self.next_button = QPushButton('Next', self)
        self.next_button.clicked.connect(self.next_move)

        self.prev_button = QPushButton('Previous', self)
        self.prev_button.clicked.connect(self.prev_move)

        self.reset_button = QPushButton('Reset', self)
        self.reset_button.clicked.connect(self.reset)

        self.disk_label = QLabel('Number of disk:', self)
        self.disk_spinbox = QSpinBox(self)
        self.disk_spinbox.setMinimum(1)
        self.disk_spinbox.setMaximum(10)
        self.disk_spinbox.setValue(self.num_disk)
        self.disk_spinbox.valueChanged.connect(self.change_num_disk)

        hbox = QHBoxLayout()
        hbox.addWidget(self.play_button)
        hbox.addWidget(self.next_button)
        hbox.addWidget(self.prev_button)
        hbox.addWidget(self.reset_button)
        hbox.addStretch(1)
        hbox.addWidget(self.disk_label)
        hbox.addWidget(self.disk_spinbox)

        vbox = QVBoxLayout()
        vbox.addWidget(self.canvas)
        vbox.addLayout(hbox)

        self.setLayout(vbox)

        self.setGeometry(300, 300, 400, 300)
        self.setWindowTitle('Towers of Hanoi')
        self.show()

    def setup_axis(self):
        self.ax.set_xlim(-1, 3)
        self.ax.set_ylim(0, self.num_disk + 2)
        self.ax.set_xticks([0, 1, 2])
        self.ax.set_xticklabels(['A', 'B', 'C'])
        self.ax.set_yticks([])
        self.ax.grid(True)

    def create_disk(self):
        self.disk = []
        colors = ['#FF355E', '#FF6037', '#FF9966', '#FFD700', '#EAEA77', '#A4C639', '#77DD77', '#50BFE6', '#FF6EFF',
                  '#C88141']
        for i in range(self.num_disk):
            height = 1
            width = 0.9 / self.num_disk * (self.num_disk - i)
            x = 0  # -width / 2 #+ i * 2 * self.num_disk
            rect = self.ax.bar(x, height, bottom=i, width=width, color=colors[i])
            self.disk.append(rect)

    def update_disk(self):
        for i, rod in enumerate(self.hanoi_game.rods):
            for j, disk in enumerate(rod):
                bar_container = self.disk[disk - 1]
                rect = bar_container[0]
                rect.set_x(i - rect.get_width() / 2)
                rect.set_y(len(rod) - j - 1)
        self.ax.set_title("Move {} of {}".format(self.hanoi_game.current_move, self.hanoi_game.n_moves))
        self.canvas.draw()

    def _pause(self):
        self.playing = False
        self.play_button.setText("Play")
        if self.play_timer is not None:
            self.play_timer.stop()
        self.play_timer = None

    def _play(self):
        self.play_button.setText("Pause")
        self.play_timer = QTimer()
        self.play_timer.setSingleShot(True)
        self.play_timer.timeout.connect(self.next_move)

        self.play_timer.start(self.play_timeout_ms)  # Call next_move() every timeout_ms milliseconds

    def play(self):
        if not self.playing and self.hanoi_game.n_moves == self.hanoi_game.current_move:
            self.reset()
        self.playing = not self.playing
        if self.playing:
            self._play()
        else:
            self._pause()

    def next_move(self):
        self.hanoi_game.next_move()
        self.update_disk()
        if self.playing and self.play_timer is not None:
            if self.hanoi_game.n_moves > self.hanoi_game.current_move:
                self.play_timer.start(self.play_timeout_ms)
            else:
                self._pause()

    def prev_move(self):
        self.hanoi_game.prev_move()
        self.update_disk()

    def clear_board(self):
        self.ax.cla()
        self.setup_axis()
        self.create_disk()

    def change_num_disk(self, value):
        self.num_disk = value
        self.hanoi_game = HanoiGame(self.num_disk)
        self.ax.set_ylim(0, self.num_disk + 1)
        self.clear_board()
        self.update_disk()
        self.canvas.draw()

    def reset(self):
        self.ax.set_ylim(0, self.num_disk + 1)
        self.hanoi_game.reset()
        self.clear_board()
        self.update_disk()
        self.canvas.draw()


if __name__ == '__main__':
    app = QApplication(sys.argv)
    tower_of_hanoi = TowerOfHanoi()
    sys.exit(app.exec())

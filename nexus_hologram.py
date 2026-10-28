
import sys
import math
import webbrowser

from PySide6.QtCore import Qt, QTimer
from PySide6.QtGui import (
    QColor, QPainter, QRadialGradient, QPen, QAction, QCursor
)
from PySide6.QtWidgets import (
    QApplication, QWidget, QMenu, QSystemTrayIcon
)


CHAT_URL = "http://127.0.0.1:5000"


class NexusHologram(QWidget):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("NEXUS Hologram")
        self.setFixedSize(240, 240)

        self.setWindowFlags(
            Qt.WindowType.FramelessWindowHint
            | Qt.WindowType.WindowStaysOnTopHint
            | Qt.WindowType.Tool
        )
        self.setAttribute(
            Qt.WidgetAttribute.WA_TranslucentBackground
        )

        self.phase = 0
        self.drag_position = None
        self.press_position = None
        self.dragged = False

        screen = QApplication.primaryScreen().availableGeometry()
        self.move(
            screen.x() + screen.width() - self.width() - 35,
            screen.y() + screen.height() - self.height() - 70
        )

        # Menu acessível pelo ícone na bandeja do Windows
        self.tray = QSystemTrayIcon(self)
        self.tray.setIcon(
            QApplication.style().standardIcon(
                QApplication.style().StandardPixmap.SP_ComputerIcon
            )
        )
        self.tray.setToolTip("NEXUS AI")

        menu = QMenu()

        show_action = QAction("Mostrar holograma", self)
        show_action.triggered.connect(self.show_hologram)
        menu.addAction(show_action)

        hide_action = QAction("Ocultar holograma", self)
        hide_action.triggered.connect(self.hide)
        menu.addAction(hide_action)

        menu.addSeparator()

        exit_action = QAction("Encerrar holograma", self)
        exit_action.triggered.connect(QApplication.quit)
        menu.addAction(exit_action)

        self.tray.setContextMenu(menu)
        self.tray.show()

        self.timer = QTimer(self)
        self.timer.timeout.connect(self.animate)
        self.timer.start(30)

    def show_hologram(self):
        self.show()
        self.raise_()

    def animate(self):
        self.phase += 1
        self.update()

    def paintEvent(self, event):
        painter = QPainter(self)
        painter.setRenderHint(QPainter.RenderHint.Antialiasing)

        cx = self.width() / 2
        cy = self.height() / 2

        pulse = math.sin(self.phase * 0.045) * 5
        radius = 48 + pulse

        glow = QRadialGradient(cx, cy, 100)
        glow.setColorAt(0.0, QColor(0, 190, 255, 90))
        glow.setColorAt(0.45, QColor(0, 100, 255, 35))
        glow.setColorAt(1.0, QColor(0, 40, 150, 0))

        painter.setPen(Qt.PenStyle.NoPen)
        painter.setBrush(glow)
        painter.drawEllipse(
            int(cx - 100), int(cy - 100), 200, 200
        )

        orb = QRadialGradient(
            cx - radius * 0.3,
            cy - radius * 0.35,
            radius * 1.7
        )
        orb.setColorAt(0.0, QColor(180, 250, 255, 255))
        orb.setColorAt(0.25, QColor(35, 190, 255, 240))
        orb.setColorAt(0.65, QColor(0, 85, 230, 225))
        orb.setColorAt(1.0, QColor(0, 20, 100, 210))

        painter.setBrush(orb)
        painter.setPen(QPen(QColor(100, 235, 255, 230), 2))
        painter.drawEllipse(
            int(cx - radius), int(cy - radius),
            int(radius * 2), int(radius * 2)
        )

        painter.setBrush(Qt.BrushStyle.NoBrush)
        painter.save()
        painter.translate(cx, cy)
        painter.rotate(self.phase * 1.2)

        painter.setPen(QPen(QColor(90, 230, 255, 190), 2))
        painter.drawEllipse(-67, -24, 134, 48)

        painter.rotate(65)
        painter.setPen(QPen(QColor(50, 160, 255, 150), 2))
        painter.drawEllipse(-64, -20, 128, 40)

        painter.restore()
        painter.end()

    def mousePressEvent(self, event):
        if event.button() == Qt.MouseButton.LeftButton:
            self.drag_position = (
                event.globalPosition().toPoint() - self.frameGeometry().topLeft()
            )
            self.press_position = event.globalPosition().toPoint()
            self.dragged = False

        elif event.button() == Qt.MouseButton.RightButton:
            menu = QMenu(self)
            menu.addAction(
                "Abrir chat",
                lambda: webbrowser.open(CHAT_URL)
            )
            menu.addAction("Ocultar holograma", self.hide)
            menu.exec(QCursor.pos())

    def mouseMoveEvent(self, event):
        if (
            self.drag_position is not None
            and event.buttons() & Qt.MouseButton.LeftButton
        ):
            current = event.globalPosition().toPoint()

            if (current - self.press_position).manhattanLength() > 5:
                self.dragged = True

            if self.dragged:
                self.move(current - self.drag_position)

    def mouseReleaseEvent(self, event):
        if event.button() == Qt.MouseButton.LeftButton:
            if not self.dragged:
                webbrowser.open(CHAT_URL)

            self.drag_position = None
            self.press_position = None
            self.dragged = False


if __name__ == "__main__":
    app = QApplication(sys.argv)
    app.setQuitOnLastWindowClosed(False)

    hologram = NexusHologram()
    hologram.show()

    sys.exit(app.exec())

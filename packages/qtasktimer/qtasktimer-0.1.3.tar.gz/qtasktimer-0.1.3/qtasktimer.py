"""Simple timer for Pomodoro technique, etc."""

import sys

from PyQt5 import Qt, QtCore, QtGui, QtWidgets


def time_to_text(t):
    """Convert time to text."""
    if t <= 0:
        return '--:--'
    elif t < 3600:
        minutes = t // 60
        seconds = t % 60
        return '{:02d}:{:02d}'.format(minutes, seconds)
    else:
        hours = t // 3600
        minutes = t % 3600 // 60
        seconds = t % 60
        return '{:d}:{:02d}:{:02d}'.format(hours, minutes, seconds)


class Timer(QtCore.QTimer):
    """Keep track of time and call handlers."""

    def __init__(self, on_update, on_end):
        super().__init__()
        self.on_update = on_update
        self.on_end = on_end
        self.timeout.connect(self.tick)
        self.time_total = None
        self.time_remaining = None

    def _check_and_show_remaining(self):
        """Check if the timer has expired and show remaining time."""
        if self.time_left is None:
            self.on_update(0, 0)
        elif self.time_left <= 0:
            self.on_end(self.time_total)
            self.stop_timer()
        else:
            self.on_update(self.time_total, self.time_left)

    def is_active(self):
        """Return True if timer is active."""
        return self.time_total is not None

    def set_timer(self, seconds):
        """Set timer for specified number of seconds."""
        self.time_total = seconds
        self.time_left = seconds
        self.start(1000)
        self._check_and_show_remaining()

    def stop_timer(self):
        """Stop the timer."""
        self.time_total = None
        self.time_left = None
        self.stop()
        self._check_and_show_remaining()

    def tick(self):
        """One more second passed."""
        self.time_left -= 1
        self._check_and_show_remaining()

    def add_time(self, seconds):
        """Add more time (`seconds` can be negative to subtract)."""
        if self.time_total is None:
            if seconds > 0:
                self.set_timer(seconds)
        else:
            self.time_left = max(0, self.time_left + seconds)
            self.time_total = max(0, self.time_total + seconds)
            self._check_and_show_remaining()


class TimerTrayIcon(QtWidgets.QSystemTrayIcon):
    """Autoupdating timer tray icon."""

    icon_size = 44
    radius = 16
    small_radius = 5

    def __init__(self):
        super().__init__()
        self.pixmap = QtGui.QPixmap(self.icon_size, self.icon_size)
        self.update_time_display(0, 0)

    def update_time_display(self, total, left):
        """Display time on the icon and in the tooltip."""
        self.setToolTip(time_to_text(left))
        self.repaint_icon(total, left)

    def repaint_icon(self, total, left):
        """Draw the timer icon based on total and remaining time."""
        background = Qt.QColor(220, 220, 220, 255)
        black = Qt.QColor(40, 40, 40, 255)
        white = Qt.QColor(255, 255, 255, 255)

        painter = QtGui.QPainter(self.pixmap)
        painter.setRenderHint(painter.Antialiasing)
        painter.setBackground(background)
        painter.eraseRect(0, 0, self.icon_size, self.icon_size)
        painter.translate(self.icon_size / 2, self.icon_size / 2)
        painter.setBrush(white)
        painter.setPen(black)
        r = self.radius
        painter.drawEllipse(-r, -r, r * 2, r * 2)
        painter.setBrush(black)
        if total != 0:
            fc = 5760  # Full clircle.
            start = fc / 4  # 12 o'clock.
            span = fc * left / total
            painter.drawPie(-r, -r, r * 2, r * 2, start, span)
            painter.setBrush(white)
            painter.setPen(white)
        sr = self.small_radius
        painter.drawEllipse(-sr, -sr, sr * 2, sr * 2)
        self.icon = QtGui.QIcon(self.pixmap)
        self.setIcon(self.icon)


class MenuButton(QtWidgets.QPushButton):
    """Narrow button for inserting into the popup menu."""

    def __init__(self, title, target):
        super().__init__(title)
        self.setStyleSheet('padding: 3px');
        self.clicked.connect(target)


class TimerApplication(QtWidgets.QApplication):
    """Timer that sits in system dock."""

    def __init__(self, argv):
        super().__init__(argv)
        self.timer = Timer(self.time_tick, self.time_out)
        self._make_tray_icon()

    def _make_tray_icon(self):
        """Create tray icon and add menu to it."""
        self.tray_icon = TimerTrayIcon()
        self.tray_icon.activated.connect(self.icon_activated)
        self._make_menu()
        self.tray_icon.show()

    def _make_menu(self):
        """Create popup menu for the tray icon."""
        menu = self.menu = QtWidgets.QMenu()
        self.tray_icon.setContextMenu(self.menu)
        time_action = QtWidgets.QWidgetAction(menu)
        self.time_label = QtWidgets.QLabel('--:--')
        self.time_label.setStyleSheet('padding: 7px;')
        time_action.setDefaultWidget(self.time_label)
        menu.addAction(time_action)
        menu.addSeparator()  # --------------------------------------
        button_action = QtWidgets.QWidgetAction(menu)
        button_box = QtWidgets.QWidget()
        button_layout = QtWidgets.QHBoxLayout()
        button_layout.addWidget(MenuButton('-5', self.minus5))
        button_layout.addWidget(MenuButton('-1', self.minus1))
        button_layout.addWidget(MenuButton('+1', self.plus1))
        button_layout.addWidget(MenuButton('+5', self.plus5))
        button_box.setLayout(button_layout)
        button_action.setDefaultWidget(button_box)
        menu.addAction(button_action)
        menu.addSeparator()  # --------------------------------------
        menu.addAction('5 minutes', self.start5)
        menu.addAction('10 minutes', self.start10)
        menu.addAction('25 minutes', self.start25)
        menu.addAction('45 minutes', self.start45)
        menu.addAction('cancel timer', self.timer.stop_timer)
        menu.addSeparator()  # --------------------------------------
        menu.addAction('exit', self.exit)

    def time_tick(self, total, left):
        """One second passed."""
        self.update_time_display(total, left)

    def update_time_display(self, total, left):
        """Update time display."""        
        self.time_label.setText(time_to_text(left))
        self.tray_icon.update_time_display(total, left)

    def time_out(self, total):
        """Time is up."""
        self.update_time_display(total, 0)
        minutes = total // 60
        if minutes == 1:
            message = 'One minute is over'
        else:
            message = '{} minutes are over'.format(minutes)
        self.tray_icon.showMessage('Time is up', message, 0)

    def icon_activated(self, reason):
        """Handle clicks on the icon."""
        if reason == QtWidgets.QSystemTrayIcon.Trigger:
            if not self.timer.is_active():
                self.start25()

    def start5(self):
        """Set timer for 5 minutes."""
        self.timer.set_timer(300)

    def start10(self):
        """Set timer for 10 minutes."""
        self.timer.set_timer(600)

    def start25(self):
        """Set timer for 25 minutes."""
        self.timer.set_timer(1500)

    def start45(self):
        """Set timer for 45 minutes."""
        self.timer.set_timer(2700)

    def plus1(self):
        """Add one minute to the timer."""
        self.timer.add_time(60)

    def plus5(self):
        self.timer.add_time(300)

    def minus1(self):
        self.timer.add_time(-60)

    def minus5(self):
        self.timer.add_time(-300)


def main():
    app = TimerApplication(sys.argv)
    sys.exit(app.exec_())


if __name__ == '__main__':
    main()

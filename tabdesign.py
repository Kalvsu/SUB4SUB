
import os
from PyQt5.QtCore import Qt, QSize
from PyQt5.QtGui import QColor, QPainter, QPen, QLinearGradient, QMouseEvent
from PyQt5.QtWidgets import QTabWidget, QWidget, QVBoxLayout, QLabel, \
    QPushButton, QHBoxLayout, QTableWidget, QTableWidgetItem, QHeaderView, QDialog, \
    QLineEdit, QStyleOptionTab, QFileDialog


class TitleBar(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.parent = parent  # Reference to the parent window

        self.layout = QHBoxLayout()
        self.layout.setContentsMargins(0, 0, 0, 0)
        self.setLayout(self.layout)

        self.title_label = QLabel("Comment List", self)
        self.title_label.setStyleSheet("color: white; font-size: 18px; font-weight: bold;")

        self.close_button = QPushButton("X", self)
        self.close_button.setStyleSheet("color: white; background-color: transparent; font-size: 18px;")
        self.close_button.setFixedSize(20, 20)
        self.close_button.clicked.connect(self.parent.close)  # Close the parent window

        self.layout.addWidget(self.title_label)
        self.layout.addStretch()
        self.layout.addWidget(self.close_button)

    def paintEvent(self, event):
        painter = QPainter(self)
        gradient = QLinearGradient(0, 0, self.width(), self.height())
        gradient.setColorAt(0, QColor("#1E90FF"))  # Gradient start color
        gradient.setColorAt(1, QColor("#0073CF"))  # Gradient end color
        painter.fillRect(self.rect(), gradient)

    def mousePressEvent(self, event: QMouseEvent):
        if event.button() == Qt.LeftButton:
            self.parent.drag_start_position = event.globalPos() - self.parent.frameGeometry().topLeft()
            event.accept()

    def mouseMoveEvent(self, event: QMouseEvent):
        if event.buttons() == Qt.LeftButton:
            if hasattr(self.parent, "drag_start_position"):
                self.parent.move(event.globalPos() - self.parent.drag_start_position)
                event.accept()
class CommentListWindow(QDialog):
    def __init__(self):
        super().__init__()

        self.setWindowTitle('Comment List')
        self.setWindowFlags(Qt.FramelessWindowHint)

        self.layout = QVBoxLayout()

        # Custom title bar
        title_bar = TitleBar(self)
        title_bar.setFixedHeight(40)
        self.layout.addWidget(title_bar)

        self.table_widget = QTableWidget()
        self.table_widget.setColumnCount(1)
        self.table_widget.setHorizontalHeaderLabels(['Comment'])

        # Set the stretch factor of the column to 1
        self.table_widget.horizontalHeader().setSectionResizeMode(0, QHeaderView.Stretch)

        self.layout.addWidget(self.table_widget)

        # Comment input
        self.comment_input = QLineEdit()
        self.comment_input.setPlaceholderText("Enter your comment")
        self.layout.addWidget(self.comment_input)

        button_layout = QHBoxLayout()

        # Set styles for the buttons
        button_style = """
                            QPushButton {
                                background-color: %s;
                                color: #ffffff;
                                border: none;
                                border-radius: 3px;
                                padding: 6px 12px;
                                font-weight: bold;
                            }
                            QPushButton:hover {
                                background-color: %s;
                            }
                        """

        add_comment_button = QPushButton('Add Comment')
        delete_comment_button = QPushButton('Delete Comment')
        import_comment_button = QPushButton('Import Comment')

        add_comment_button.setStyleSheet(button_style % ("#ef1010", "#ff2f2f"))
        delete_comment_button.setStyleSheet(button_style % ("#ef1010", "#ff2f2f"))
        import_comment_button.setStyleSheet(button_style % ("#1033ef", "#2958ff"))


        button_layout.addWidget(add_comment_button)
        button_layout.addWidget(delete_comment_button)
        button_layout.addWidget(import_comment_button)


        self.layout.addLayout(button_layout)
        self.setLayout(self.layout)

        add_comment_button.clicked.connect(self.add_comment)
        delete_comment_button.clicked.connect(self.delete_comment)
        import_comment_button.clicked.connect(self.import_comments)


        # Check if "comments.txt" file exists and import its content
        if os.path.isfile("data\\comments.txt"):
            self.import_comments("data\\comments.txt")

    def add_comment(self):
        comment = self.comment_input.text()
        if comment:
            row_count = self.table_widget.rowCount()
            self.table_widget.insertRow(row_count)
            item = QTableWidgetItem(comment)
            self.table_widget.setItem(row_count, 0, item)
            self.comment_input.clear()

            # Write comments to "comments.txt"
            comments = []
            for row in range(self.table_widget.rowCount()):
                comment_item = self.table_widget.item(row, 0)
                if comment_item:
                    comment = comment_item.text()
                    comments.append(comment)

            with open("data\\comments.txt", "w") as file:
                file.write('\n'.join(comments))

    def delete_comment(self):
        selected_row = self.table_widget.currentRow()
        if selected_row >= 0:
            self.table_widget.removeRow(selected_row)

            # Update comments in "comments.txt"
            comments = []
            for row in range(self.table_widget.rowCount()):
                comment_item = self.table_widget.item(row, 0)
                if comment_item:
                    comment = comment_item.text()
                    comments.append(comment)

            with open("data\\comments.txt", "w") as file:
                file.write('\n'.join(comments))


    def import_comments(self, filename=None):
        if not filename:
            filename, _ = QFileDialog.getOpenFileName(self, "Import Comment", "", "Text Files (*.txt)")

        if filename:
            with open(filename, 'r') as file:
                comments = file.read().splitlines()

            for comment in comments:
                row_count = self.table_widget.rowCount()
                self.table_widget.insertRow(row_count)
                item = QTableWidgetItem(comment)
                self.table_widget.setItem(row_count, 0, item)

class CoolTabWidget(QTabWidget):
    def __init__(self):
        super().__init__()

        # Set the application style
        self.setStyleSheet(
            """
            CoolTabWidget {
                background-color: #f2f2f2;
            }

            QTabWidget::pane {
                border: none;
                background-color: #f2f2f2;
            }

            QTabBar::tab {
                background-color: #2196f3;  /* Cool blue color */
                color: #ffffff;  /* White text color */
                padding: 12px;
                font-family: "Arial";
                font-size: 14px;
            }

            QTabBar::tab:selected {
                background-color: #1e88e5;  /* Darker shade of blue for selected tab */
            }

            QTabBar::tab:hover {
                background-color: #1e88e5;  /* Darker shade of blue on hover */
            }
            """
        )

    def paintEvent(self, event):
        super().paintEvent(event)

        # Draw a border around the tab widget
        painter = QPainter(self)
        painter.setPen(QPen(Qt.black, 2, Qt.SolidLine))
        painter.drawRect(self.rect())

    def tabLayoutChange(self):
        # Stretch tabs to the right
        for index in range(self.count()):
            tab_rect = self.tabRect(index)
            tab_rect.moveLeft(self.width() - tab_rect.width() - self.style().pixelMetric(QStyleOptionTab.Margin))
            self.setTabRect(index, tab_rect)

class ResizableCorner(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.parent = parent
        self.setFixedSize(20, 20)
        self.setCursor(Qt.SizeFDiagCursor)
        self.mouse_pressed = False
        self.resize_origin = None

    def mousePressEvent(self, event):
        if event.button() == Qt.LeftButton:
            self.mouse_pressed = True
            self.resize_origin = event.globalPos()

    def mouseMoveEvent(self, event):
        if self.mouse_pressed:
            diff = event.globalPos() - self.resize_origin
            new_size = self.parent.size() + QSize(diff.x(), diff.y())

            # Set minimum and maximum sizes for the main window
            minimum_size = self.parent.minimumSize()
            maximum_size = self.parent.maximumSize()

            new_size = new_size.boundedTo(maximum_size).expandedTo(minimum_size)
            self.parent.resize(new_size)

            self.resize_origin = event.globalPos()  # Update the resize origin

    def mouseReleaseEvent(self, event):
        if event.button() == Qt.LeftButton:
            self.mouse_pressed = False
            self.resize_origin = None

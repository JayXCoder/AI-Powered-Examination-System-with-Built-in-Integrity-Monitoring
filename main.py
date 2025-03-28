from PyQt5.QtWidgets import (
    QApplication, QWidget, QPushButton, QLabel, QVBoxLayout, 
    QStackedWidget, QLineEdit, QComboBox, QTextEdit
)
from PyQt5.QtCore import Qt
import sys

class ExamSystemGUI(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Examination System with Integrity Monitoring")
        self.setGeometry(100, 100, 800, 500)
        
        # Main Layout
        self.layout = QVBoxLayout()
        
        # Stack to switch between screens
        self.stack = QStackedWidget(self)
        
        # Screens
        self.login_screen = self.create_login_screen()
        self.dashboard_screen = self.create_dashboard()
        self.exam_screen = self.create_exam_interface()
        self.admin_screen = self.create_admin_panel()
        
        # Add Screens to Stack
        self.stack.addWidget(self.login_screen)
        self.stack.addWidget(self.dashboard_screen)
        self.stack.addWidget(self.exam_screen)
        self.stack.addWidget(self.admin_screen)

        self.layout.addWidget(self.stack)
        self.setLayout(self.layout)

        # Show login first
        self.stack.setCurrentWidget(self.login_screen)

        # Background Colour
        self.setStyleSheet("background-image: url('assets/background.jpg'); background-position: center; background-repeat: no-repeat;")

    # 1️⃣ Login Screen
    def create_login_screen(self):
        widget = QWidget()
        layout = QVBoxLayout()
        
        title = QLabel("Login")
        title.setStyleSheet("font-size: 20px; font-weight: bold;")
        title.setAlignment(Qt.AlignCenter)

        self.user_role = QComboBox()
        self.user_role.addItems(["Student", "Admin"])

        self.username = QLineEdit()
        self.username.setPlaceholderText("Enter username")

        self.password = QLineEdit()
        self.password.setPlaceholderText("Enter password")
        self.password.setEchoMode(QLineEdit.Password)

        login_btn = QPushButton("Login")
        login_btn.clicked.connect(self.go_to_dashboard)

        layout.addWidget(title)
        layout.addWidget(self.user_role)
        layout.addWidget(self.username)
        layout.addWidget(self.password)
        layout.addWidget(login_btn)
        widget.setLayout(layout)
        return widget

    # 2️⃣ Dashboard Screen
    def create_dashboard(self):
        widget = QWidget()
        layout = QVBoxLayout()

        title = QLabel("Dashboard")
        title.setStyleSheet("font-size: 20px; font-weight: bold;")
        title.setAlignment(Qt.AlignCenter)

        start_exam_btn = QPushButton("Start Exam")
        start_exam_btn.clicked.connect(self.go_to_exam)

        view_results_btn = QPushButton("View Results")

        admin_panel_btn = QPushButton("Admin Panel")
        admin_panel_btn.clicked.connect(self.go_to_admin_panel)

        layout.addWidget(title)
        layout.addWidget(start_exam_btn)
        layout.addWidget(view_results_btn)
        layout.addWidget(admin_panel_btn)
        widget.setLayout(layout)
        return widget

    # 3️⃣ Exam Interface
    def create_exam_interface(self):
        widget = QWidget()
        layout = QVBoxLayout()

        title = QLabel("Exam in Progress")
        title.setStyleSheet("font-size: 20px; font-weight: bold;")
        title.setAlignment(Qt.AlignCenter)

        question_label = QLabel("Question: What is 2 + 2?")
        answer_box = QTextEdit()

        submit_btn = QPushButton("Submit Exam")
        submit_btn.clicked.connect(self.go_to_dashboard)

        layout.addWidget(title)
        layout.addWidget(question_label)
        layout.addWidget(answer_box)
        layout.addWidget(submit_btn)
        widget.setLayout(layout)
        return widget

    # 4️⃣ Admin Panel
    def create_admin_panel(self):
        widget = QWidget()
        layout = QVBoxLayout()

        title = QLabel("Admin Panel")
        title.setStyleSheet("font-size: 20px; font-weight: bold;")
        title.setAlignment(Qt.AlignCenter)

        manage_questions_btn = QPushButton("Manage Questions")
        monitor_exam_btn = QPushButton("Monitor Exams")

        back_btn = QPushButton("Back to Dashboard")
        back_btn.clicked.connect(self.go_to_dashboard)

        layout.addWidget(title)
        layout.addWidget(manage_questions_btn)
        layout.addWidget(monitor_exam_btn)
        layout.addWidget(back_btn)
        widget.setLayout(layout)
        return widget

    # Navigation Functions
    def go_to_dashboard(self):
        self.stack.setCurrentWidget(self.dashboard_screen)

    def go_to_exam(self):
        self.stack.setCurrentWidget(self.exam_screen)

    def go_to_admin_panel(self):
        self.stack.setCurrentWidget(self.admin_screen)

# Run Application
if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = ExamSystemGUI()
    window.show()
    sys.exit(app.exec_())

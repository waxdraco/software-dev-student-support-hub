import sys
import json
import os
from PyQt6.QtWidgets import (
    QApplication, QMainWindow, QWidget, QLabel, QPushButton, 
    QVBoxLayout, QHBoxLayout, QLineEdit, QTextEdit, QComboBox, 
    QStackedWidget, QMessageBox, QListWidget
)

DATA_FILE = "data.json"

# Data Handler & Logic 
def load_data():
    if not os.path.exists(DATA_FILE):
        default_data = {
            "topics": [
                {"category": "Academic Skills", "description": "Help with assignments, referencing, and study plans."},
                {"category": "IT Help", "description": "Campus Wi-Fi, password resets, and software access."},
                {"category": "Careers", "description": "Resume reviews, interview prep, and internships."},
                {"category": "Accessibility", "description": "Support plans and assistive technology."},
                {"category": "Wellbeing", "description": "Counseling and mental health services."}
            ],
            "announcements": [
                "Library research workshop",
                "Campus Wi-Fi maintenance",
                "Careers resume session"
            ],
            "requests": []
        }
        save_data(default_data)
        return default_data
    with open(DATA_FILE, 'r', encoding='utf-8') as file:
        return json.load(file)

def save_data(data):
    with open(DATA_FILE, 'w', encoding='utf-8') as file:
        json.dump(data, file, indent=4)

def get_all_topics():
    return load_data().get("topics", [])

def get_all_announcements():
    return load_data().get("announcements", [])

def search_support(keyword):
    data = load_data()
    keyword = keyword.lower()
    return [
        t for t in data.get("topics", [])
        if keyword in t["category"].lower() or keyword in t["description"].lower()
    ]

def create_support_request(category, description):
    if not category.strip() or not description.strip():
        return False, "Category and description cannot be empty."
    data = load_data()
    requests = data.get("requests", [])
    new_id = len(requests) + 1
    new_request = {
        "RequestID": new_id,
        "Category": category,
        "Description": description,
        "Status": "Submitted"
    }
    requests.append(new_request)
    data["requests"] = requests
    save_data(data)
    return True, f"Request {new_id} was created successfully."

def get_user_requests():
    return load_data().get("requests", [])

#  Graphical User Interface
class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Student Support Hub")
        self.resize(800, 600)
        
        main_widget = QWidget()
        self.setCentralWidget(main_widget)
        layout = QHBoxLayout(main_widget)
        
        # Left Navigation Menu
        nav_layout = QVBoxLayout()
        nav_layout.addWidget(QLabel("<b>NAVIGATION</b>"))
        
        self.btn_home = QPushButton("Home")
        self.btn_support = QPushButton("Support Services")
        self.btn_new_request = QPushButton("New Request")
        self.btn_my_requests = QPushButton("My Requests")
        
        nav_layout.addWidget(self.btn_home)
        nav_layout.addWidget(self.btn_support)
        nav_layout.addWidget(self.btn_new_request)
        nav_layout.addWidget(self.btn_my_requests)
        nav_layout.addStretch()
        
        layout.addLayout(nav_layout, 1)
        
        # Stacked Widget for Screens
        self.stack = QStackedWidget()
        layout.addWidget(self.stack, 3)
        
        self.init_home_screen()
        self.init_support_screen()
        self.init_request_screen()
        self.init_view_requests_screen()
        
        self.btn_home.clicked.connect(lambda: self.stack.setCurrentIndex(0))
        self.btn_support.clicked.connect(lambda: self.stack.setCurrentIndex(1))
        self.btn_new_request.clicked.connect(lambda: self.stack.setCurrentIndex(2))
        self.btn_my_requests.clicked.connect(lambda: (self.load_requests_list(), self.stack.setCurrentIndex(3)))

    def init_home_screen(self):
        screen = QWidget()
        v = QVBoxLayout(screen)
        v.addWidget(QLabel("<h2>Welcome to Student Support Hub</h2>"))
        
        search_row = QHBoxLayout()
        self.search_input = QLineEdit()
        self.search_input.setPlaceholderText("Search services by keyword...")
        btn_search = QPushButton("Search")
        btn_search.clicked.connect(self.perform_search)
        search_row.addWidget(QLabel("Search Services:"))
        search_row.addWidget(self.search_input)
        search_row.addWidget(btn_search)
        v.addLayout(search_row)
        
        btn_row = QHBoxLayout()
        b_browse = QPushButton("Browse Support")
        b_browse.clicked.connect(lambda: self.stack.setCurrentIndex(1))
        b_req = QPushButton("New Request")
        b_req.clicked.connect(lambda: self.stack.setCurrentIndex(2))
        btn_row.addWidget(b_browse)
        btn_row.addWidget(b_req)
        v.addLayout(btn_row)
        
        v.addWidget(QLabel("<b>Recent Announcements:</b>"))
        self.announcement_list = QListWidget()
        for ann in get_all_announcements():
            self.announcement_list.addItem(ann)
        v.addWidget(self.announcement_list)
        
        self.stack.addWidget(screen)

    def init_support_screen(self):
        screen = QWidget()
        v = QVBoxLayout(screen)
        v.addWidget(QLabel("<h2>Support Services Categories</h2>"))
        self.topic_list = QListWidget()
        for topic in get_all_topics():
            self.topic_list.addItem(f"{topic['category']}: {topic['description']}")
        v.addWidget(self.topic_list)
        
        btn_home = QPushButton("Home")
        btn_home.clicked.connect(lambda: self.stack.setCurrentIndex(0))
        v.addWidget(btn_home)
        self.stack.addWidget(screen)

    def init_request_screen(self):
        screen = QWidget()
        v = QVBoxLayout(screen)
        v.addWidget(QLabel("<h2>Create Support Request</h2>"))
        
        v.addWidget(QLabel("Category:"))
        self.cat_combo = QComboBox()
        for topic in get_all_topics():
            self.cat_combo.addItem(topic['category'])
        v.addWidget(self.cat_combo)
        
        v.addWidget(QLabel("Description:"))
        self.desc_input = QTextEdit()
        v.addWidget(self.desc_input)
        
        btn_submit = QPushButton("Submit Request")
        btn_submit.clicked.connect(self.submit_request_action)
        v.addWidget(btn_submit)
        
        btn_home = QPushButton("Home")
        btn_home.clicked.connect(lambda: self.stack.setCurrentIndex(0))
        v.addWidget(btn_home)
        self.stack.addWidget(screen)

    def init_view_requests_screen(self):
        screen = QWidget()
        v = QVBoxLayout(screen)
        v.addWidget(QLabel("<h2>My Support Requests</h2>"))
        self.requests_list_widget = QListWidget()
        v.addWidget(self.requests_list_widget)
        
        btn_home = QPushButton("Home")
        btn_home.clicked.connect(lambda: self.stack.setCurrentIndex(0))
        v.addWidget(btn_home)
        self.stack.addWidget(screen)

    def perform_search(self):
        keyword = self.search_input.text()
        results = search_support(keyword)
        msg = "\n".join([f"- {r['category']}: {r['description']}" for r in results]) if results else "No matching topics found."
        QMessageBox.information(self, "Search Results", msg)

    def submit_request_action(self):
        cat = self.cat_combo.currentText()
        desc = self.desc_input.toPlainText()
        success, message = create_support_request(cat, desc)
        QMessageBox.information(self, "Result", message)
        if success:
            self.desc_input.clear()
            self.stack.setCurrentIndex(0)

    def load_requests_list(self):
        self.requests_list_widget.clear()
        reqs = get_user_requests()
        for r in reqs:
            item_text = f"ID: {r['RequestID']} | Category: {r['Category']} | Status: {r['Status']}\nDetails: {r['Description']}"
            self.requests_list_widget.addItem(item_text)

def main():
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec())

if __name__ == "__main__":
    main()
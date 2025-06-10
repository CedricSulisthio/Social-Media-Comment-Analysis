from PyQt5.QtWidgets import QApplication, QMainWindow, QVBoxLayout, QLabel, QPushButton, QLineEdit, QWidget, QMessageBox, QInputDialog, QComboBox
import networkx as nx
import matplotlib
matplotlib.use('Qt5Agg')
import matplotlib.pyplot as plt

class SocialMediaAnalysisApp(QMainWindow):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("Social Media Analysis")
        self.setGeometry(100, 100, 800, 600)

        self.central_widget = QWidget(self)
        self.setCentralWidget(self.central_widget)

        self.layout = QVBoxLayout()
        self.central_widget.setLayout(self.layout)

        self.commenter_input = QLineEdit(self)
        self.layout.addWidget(QLabel("Enter your username (commenters):"))
        self.layout.addWidget(self.commenter_input)

        self.receiver_input = QLineEdit(self)
        self.layout.addWidget(QLabel("Enter recipient's username:"))
        self.layout.addWidget(self.receiver_input)

        self.comment_input = QLineEdit(self)
        self.layout.addWidget(QLabel("Enter a comment:"))
        self.layout.addWidget(self.comment_input)

        self.sentiment_combo = QComboBox()
        self.sentiment_combo.addItems(["Appraisal", "Critic"])
        self.layout.addWidget(QLabel("Select comment type:"))
        self.layout.addWidget(self.sentiment_combo)

        self.add_comment_button = QPushButton("Add Comment", self)
        self.add_comment_button.clicked.connect(self.add_comment)
        self.layout.addWidget(self.add_comment_button)

        self.add_password_button = QPushButton("Add Password (Recipients Only)", self)
        self.add_password_button.clicked.connect(self.add_password)
        self.layout.addWidget(self.add_password_button)

        self.view_comments_button = QPushButton("View Comments", self)
        self.view_comments_button.clicked.connect(self.view_comments)
        self.layout.addWidget(self.view_comments_button)

        self.view_graph_button = QPushButton("View Graph", self)
        self.view_graph_button.clicked.connect(self.view_graph)
        self.layout.addWidget(self.view_graph_button)

        self.quit_button = QPushButton("Quit", self)
        self.quit_button.clicked.connect(self.close)
        self.layout.addWidget(self.quit_button)

        self.social_graph = nx.MultiDiGraph()
        self.comments = {}
        self.password = None

    def add_comment(self):
        commenter = self.commenter_input.text()
        receiver = self.receiver_input.text()
        comment = self.comment_input.text()
        sentiment = self.sentiment_combo.currentText()

        if commenter and receiver and comment:
            if receiver in self.comments:
                self.comments[receiver].append((commenter, sentiment, comment))
            else:
                self.comments[receiver] = [(commenter, sentiment, comment)]

            self.show_notification(f"Comment added by {commenter}")

            self.comment_input.clear()

    def view_comments(self):
        password, ok = QInputDialog.getText(self, "Password", "Enter password:")
        if ok and password == self.password:
            receiver = self.receiver_input.text()
            if receiver in self.comments:
                comments = "\n".join([f"{comment[0]}: {comment[2]} ({comment[1]})" for comment in self.comments[receiver]])
                self.show_notification(f"Comments for {receiver}:\n{comments}")
            else:
                self.show_notification(f"No comments found for {receiver}")
        else:
            self.show_notification("Incorrect password")

    def add_password(self):
        password, ok = QInputDialog.getText(self, "Add Password", "Enter password:")
        if ok:
            self.password = password
            self.show_notification("Password set")

    def view_graph(self):
        password, ok = QInputDialog.getText(self, "Password", "Enter password:")
        if ok and password == self.password:
            fig, ax = plt.subplots(figsize=(8, 6))

            for receiver, comments_list in self.comments.items():
                for commenter, sentiment, comment in comments_list:
                    self.social_graph.add_node(comment)
                    self.social_graph.add_edge(sentiment, comment)

            pos = nx.spring_layout(self.social_graph)
            nx.draw(self.social_graph, pos, ax=ax, with_labels=True, node_color='skyblue', node_size=800)

            ax.set_title('Comment Graph')
            plt.show()
        else:
            self.show_notification("Incorrect password")

    def show_notification(self, message):
        msg_box = QMessageBox()
        msg_box.setWindowTitle("Notification")
        msg_box.setText(message)
        msg_box.exec_()

app = QApplication([])
window = SocialMediaAnalysisApp()
window.show()
app.exec_()
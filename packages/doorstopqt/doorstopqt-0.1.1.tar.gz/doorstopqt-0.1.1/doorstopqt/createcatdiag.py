from PyQt5.QtWidgets import *
from .categoryselector import CategorySelector


class CreateCategoryDialog(QDialog):
    def __init__(self, parent=None):
        super(CreateCategoryDialog, self).__init__(parent)

        self.setWindowTitle('Create new document type')
        self.vbox = QVBoxLayout()
        grid = QGridLayout()
        self.prefix = QLineEdit()
        self.catsel = CategorySelector()
        self.path = QLineEdit('./reqs/')
        self.create = QPushButton('Create')
        grid.addWidget(QLabel('Prefix:'), 0, 0)
        grid.addWidget(self.prefix, 0, 1)
        grid.addWidget(QLabel('Parent:'), 1, 0)
        grid.addWidget(self.catsel, 1, 1)
        grid.addWidget(QLabel('Path:'), 2, 0)
        grid.addWidget(self.path, 2, 1)
        self.db = None

        def updatepath(s):
            path = self.path.text()
            lastslash = path.rfind('/')
            if lastslash == -1:
                path = './reqs/' + s.lower()
            else:
                path = path[:lastslash + 1] + s.lower()
            self.path.setText(path)
        self.prefix.textChanged.connect(updatepath)

        def create(b):
            self.hide()
            prefix = self.prefix.text()
            path = self.path.text()
            parent = self.catsel.text()
            print('{} {} {}'.format(prefix, parent, path))
            self.prefix.setText('')
            self.db.root.create_document(path, prefix, parent=parent)
            self.db.reload()
        self.create.clicked.connect(create)

        g = QWidget()
        g.setLayout(grid)
        self.vbox.addWidget(g)
        self.vbox.addWidget(self.create)
        self.setLayout(self.vbox)

    def show(self):
        super(CreateCategoryDialog, self).show()
        self.prefix.setFocus()

    def connectdb(self, db):
        self.db = db
        self.catsel.connectdb(db)

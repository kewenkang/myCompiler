from PyQt4 import QtGui,QtCore
import sys
from lexer.Lexer import Lexer


class MyTable(QtGui.QTableWidget):
    def __init__(self, title):
        super(MyTable, self).__init__()
        self.setWindowTitle(title)
        self.resize(700, 600)


    def table(self, row, column, content):
        # 设置表格行列数
        self.setColumnCount(len(row))
        self.setRowCount(len(column))

        # 设置表头
        self.setHorizontalHeaderLabels(row)
        self.setVerticalHeaderLabels(column)

        # 添加内容
        for x in range(len(content)):
            for y in range(len(content[x])):
                self.setItem(x, y, QtGui.QTableWidgetItem(content[x][y]))

class MyWidget(QtGui.QWidget):
    def __init__(self, parent=None):
        super(MyWidget, self).__init__(parent)

        # set window's location and size
        self.setWindowTitle("tokens")
        self.resize(600, 700)
        self.center()
        self.setWindowIcon(QtGui.QIcon("image/icon.jpg"))

        self.textEdit = QtGui.QTextEdit(self)
        self.textEdit.setGeometry(10,10,580, 680)

    # 窗口居中
    def center(self):
        screen = QtGui.QDesktopWidget().screenGeometry()
        size = self.geometry()
        self.move((screen.width()-size.width())/2, (screen.height()-size.height())/2)


class MainWindow(QtGui.QMainWindow):
    def __init__(self):
        super(MainWindow, self).__init__()
        self.tokens_widget = MyWidget()
        self.dfa_table_widget = MyTable("DFA转换表")
        self.l = Lexer()
        self.initUI()

    def initUI(self):
        self.resize(750, 800)
        self.setWindowTitle("myCompiler")
        self.setWindowIcon(QtGui.QIcon("image/icon.jpg"))

        # exit toolbar
        self.exit = QtGui.QAction('Exit', self)
        self.exit.setShortcut('Ctrl+Q')
        self.exit.setStatusTip("Exit application")
        self.connect(self.exit, QtCore.SIGNAL('triggered()'), QtCore.SLOT("close()"))

        # open file toolbar
        self.openfile = QtGui.QAction('打开文件', self)
        self.openfile.setShortcut('Ctrl+O')
        self.openfile.setStatusTip("Open file")
        self.connect(self.openfile, QtCore.SIGNAL('triggered()'), self.open_file)

        # lexer toolbar
        self.lexer = QtGui.QAction('词法分析', self)
        self.lexer.setShortcut('Ctrl+L')
        self.lexer.setStatusTip("lexer")
        self.connect(self.lexer, QtCore.SIGNAL('triggered()'), self.lexer_ana)

        # lexer toolbar
        self.dfa_table = QtGui.QAction('词法规则', self)
        self.dfa_table.setShortcut('Ctrl+D')
        self.connect(self.dfa_table, QtCore.SIGNAL('triggered()'), self.show_dfa_table)

        # paser toolbar
        self.paser = QtGui.QAction('语法分析', self)
        self.paser.setShortcut('Ctrl+P')
        self.paser.setStatusTip("paser")
        self.connect(self.paser, QtCore.SIGNAL('triggered()'), self.paser_ana)

        # add toolbar
        self.toolbar1 = self.addToolBar("打开文件")
        self.toolbar2 = self.addToolBar("词法分析")
        self.toolbar3 = self.addToolBar("词法规则")
        self.toolbar4 = self.addToolBar("语法分析")
        self.toolbar1.addAction(self.openfile)
        self.toolbar2.addAction(self.lexer)
        self.toolbar3.addAction(self.dfa_table)
        self.toolbar4.addAction(self.paser)

        # add status bar
        self.statusBar().showMessage('Ready')

        # add menubar
        menubar = self.menuBar()
        file = menubar.addMenu("&File")
        file.addAction(self.exit)

        # 中央文本框
        self.textEdit = QtGui.QTextEdit()
        self.setCentralWidget(self.textEdit)
        self.setFocus()


    def open_file(self):
        # 文件选择器
        filename = QtGui.QFileDialog.getOpenFileName(self, "Open file", '.')
        print("open"+filename)
        fname = open(filename, 'r')
        data = fname.read()
        self.textEdit.setText(data)

    def lexer_ana(self):
        # 获取文本框内容
        data = self.textEdit.toPlainText()

        tokens = self.l.lex(data)
        tokens_str = '行数\ttoken\n'
        for t in tokens:
            tokens_str += t + "\n"
        self.tokens_widget.textEdit.setText(tokens_str)
        self.tokens_widget.show()

    def show_dfa_table(self):
        states, chars, t_content = self.l.dfa.get_table()
        # states = ['1', '2']
        # chars = ['a', 'b', 'c']
        # t_content = [['2', '2', '2'], ['1', '1', '1']]
        self.dfa_table_widget.table(chars, states, t_content)
        self.dfa_table_widget.show()

    def paser_ana(self):
        print("paser")
        pass

if __name__ == "__main__":
    app = QtGui.QApplication(sys.argv)

    window = MainWindow()
    window.show()

    sys.exit(app.exec_())
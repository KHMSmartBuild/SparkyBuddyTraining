from PyQt5.QtWidgets import QApplication, QWidget
import sys

app = QApplication(sys.argv)

window = QWidget()
window.setWindowTitle('PyQt5 Test')
window.show()

sys.exit(app.exec_())

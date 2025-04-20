import sys
from PyQt5.QtWidgets import QApplication
from .ui.widget import VoronoiWidget

def main():
    app = QApplication(sys.argv)
    w = VoronoiWidget(n_initial=50, tile_size=400)
    w.show()
    sys.exit(app.exec_())

if __name__ == "__main__":
    main() 
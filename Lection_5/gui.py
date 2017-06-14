import sys
import re
import time
from controller import ParticleController, ParticlePlot

from PyQt5.QtCore import Qt, QTimer
from PyQt5.QtGui import QIcon, QFont, QColor
from PyQt5.QtWidgets import (
    QApplication, QTextEdit, QLabel, QPushButton, QMessageBox, QDesktopWidget,
    QMainWindow, QSlider, QSizePolicy, QComboBox
)

class ParticleGUI(QMainWindow, ParticleController):

    def __init__(self):
        super().__init__(),
        self.lblw = 20
        self.lblh = 24
        self.tbtw = 55
        self.tbth = 25
        self.main_window()
        self.labels(left = 40, top = 40)
        self.textboxes(left = 60, top = 64)
        self.slider_particle_mass()
        self.combobox_verlet()
        self.button_add_particle()
        self.statistics()
        self.plot()
        self.show()

    def main_window(self):
        """ Init function for application's main window """
        self.resize(700, 400)
        self.setWindowTitle('Particles')
        frame = self.frameGeometry()
        frame.moveCenter(QDesktopWidget().availableGeometry().center())
        self.move(frame.topLeft())

    def labels(self, left, top):
        s_lbl = QLabel("Speed", self)
        s_lbl.setGeometry(left + self.lblw, top, self.tbtw,
            self.lblh)
        u_lbl = QLabel(" u: ", self)
        u_lbl.setGeometry(left, top + self.lblh,
            self.lblw, self.lblh)
        v_lbl = QLabel(" v: ", self)
        v_lbl.setGeometry(left + self.lblw + self.tbtw,
            top + self.lblh, self.lblw, self.lblh)
        p_lbl = QLabel("Coords", self)
        p_lbl.setGeometry(left + self.lblw,
            top + 2 * self.lblh, self.tbtw, self.lblh)
        x_lbl = QLabel(" x: ", self)
        x_lbl.setGeometry(left, top + 3 * self.lblh, self.lblw,
            self.lblh)
        y_lbl = QLabel(" y: ", self)
        y_lbl.setGeometry(left + self.lblw + self.tbtw,
            top + 3 * self.lblh, self.lblw, self.lblh)
        l_lbl = QLabel(" lifetime: ", self)
        l_lbl.setGeometry(left, top + 4.5 * self.lblh,
            self.tbtw, self.lblh)
        m_lbl = QLabel(" mass: ", self)
        m_lbl.setGeometry(left, top + 5.5 * self.lblh,
            self.tbtw, self.lblh)
        o_lbl = QLabel(" Methods: ", self)
        o_lbl.setGeometry(left, top + 10 * self.lblh,
            4 * self.lblw, self.lblh)

    def textboxes(self, left, top):
        self.u_tbx = QTextEdit(str(self.speed["u_x"]), self)
        self.u_tbx.setGeometry(left, top, self.tbtw, self.tbth)
        self.u_tbx.setTabChangesFocus(True)
        self.u_tbx.textChanged.connect(self.__u_tbx_changed)
        self.v_tbx = QTextEdit(str(self.speed["v_y"]), self)
        self.v_tbx.setGeometry(left + self.lblw + self.tbtw,
            top, self.tbtw, self.tbth)
        self.v_tbx.setTabChangesFocus(True)
        self.v_tbx.textChanged.connect(self.__v_tbx_changed)
        self.x_tbx = QTextEdit(str(self.coords["x"]), self)
        self.x_tbx.setGeometry(left, top + 2 * self.tbth,
            self.tbtw, self.tbth)
        self.x_tbx.setTabChangesFocus(True)
        self.x_tbx.textChanged.connect(self.__x_tbx_changed)
        self.y_tbx = QTextEdit(str(self.coords["y"]), self)
        self.y_tbx.setGeometry(left + self.lblw + self.tbtw,
            top + 2 * self.tbth, self.tbtw,
            self.tbth)
        self.y_tbx.setTabChangesFocus(True)
        self.y_tbx.textChanged.connect(self.__y_tbx_changed)
        self.l_tbx = QTextEdit(str(self.lifetime), self)
        self.l_tbx.setGeometry(left + 2 * self.lblw,
            top + 3.5 * self.tbth, self.tbtw,
            self.tbth)
        self.l_tbx.setTabChangesFocus(True)
        self.l_tbx.textChanged.connect(self.__l_tbx_changed)

    def slider_particle_mass(self):
        """Init function for slider that changes mass of the particle that will
        be created next"""
        sld = QSlider(Qt.Horizontal, self)
        sld.setFocusPolicy(Qt.NoFocus)
        sld.setGeometry(85, 180, 100, 30)
        sld.setMinimum(1)
        sld.setMaximum(1000)
        sld.setValue(self.mass / 5000)
        sld.valueChanged[int].connect(self.__sld_changed)

    def combobox_verlet(self):
        """ Init combobox for selecting different Verlet implementation """
        self.cmb = QComboBox(self);
        self.cmb.setObjectName("cmb")
        self.cmb.setGeometry(40, 320, 150, 30)
        self.cmb.addItems(self.methods)
        self.cmb.currentIndexChanged.connect(self.__cmb_changed)

    def button_add_particle(self):
        """ Init function for button that adds one particle to the plot """
        self.btn = QPushButton('Add particle', self)
        self.btn.setGeometry(40, 210, 150, 30)
        self.btn.clicked.connect(self._ParticleController__add_particle)
        self.btn.setDisabled(False)

    def plot(self):
        self.plot = ParticlePlot(self, 10, 8, 50, QSizePolicy.Fixed)
        self.plot.move(210, 0)
        self.timer = QTimer(self)
        self.timer.timeout.connect(self.__draw_plot)
        self.timer.start(42)

    def __draw_plot(self):
        self.plot.update_plot(self.particles, self.updaters[self.method])
        self.particles = list(filter(lambda p: p.lifetime > 0, self.particles))

    @staticmethod
    def __validate(textedit, pattern):
        if re.match(pattern, textedit.toPlainText()):
            textedit.setStyleSheet("QTextEdit {color: black}")
            return True
        else:
            textedit.setStyleSheet("QTextEdit {color: red}")
            return False

    def __u_tbx_changed(self):
        if __class__.__validate(self.u_tbx, r"^-?\d+(?:\.\d+)?$"):
            self.speed["u_x"] = float(self.u_tbx.toPlainText())

    def __v_tbx_changed(self):
        if __class__.__validate(self.v_tbx, r"^-?\d+(?:\.\d+)?$"):
            self.speed["v_y"] = float(self.v_tbx.toPlainText())

    def __x_tbx_changed(self):
        if __class__.__validate(self.x_tbx, r"^-?\d+(?:\.\d+)?$"):
            self.coords["x"] = float(self.x_tbx.toPlainText())

    def __y_tbx_changed(self):
        if __class__.__validate(self.y_tbx, r"^-?\d+(?:\.\d+)?$"):
            self.coords["y"] = float(self.y_tbx.toPlainText())

    def __l_tbx_changed(self):
        if __class__.__validate(self.l_tbx, r"^\d+?$"):
            self.lifetime = float(self.l_tbx.toPlainText())

    def __sld_changed(self, value):
        self.mass = value * 50000

    def statistics(self):
        self.sbtn = QPushButton('Statictics', self)
        self.sbtn.setGeometry(0, 0, 75, 30)
        self.sbtn.clicked.connect(self.__statistics)

    def __statistics(self):
        print("Particles: {}".format(len(self.particles)))
        for i in range(3):
            b = time.time()
            self.updaters[i](self.particles)
            e = time.time()
            print("{}: Time = {}".format(self.updaters[i].__name__, e - b))
        b = time.time()
        self.result = self._ParticleController__odeint_wrapper()
        e = time.time()
        print("Odeint: Time = {}".format(e - b))


    def __cmb_changed(self, value):
        self.method = value
        print("Current method: ", self.cmb.currentText())

    def closeEvent(self, event):
        reply = QMessageBox.question(self, 'Message', "Are you sure to quit?",
            QMessageBox.Yes | QMessageBox.No, QMessageBox.No)
        event.accept() if reply == QMessageBox.Yes else event.ignore()

if __name__ == '__main__':
    app = QApplication(sys.argv)
    gui = ParticleGUI()
    sys.exit(app.exec())

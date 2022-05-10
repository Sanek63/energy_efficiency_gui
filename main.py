import utils
import images
import about

from PyQt5.QtCore import QObject, pyqtSignal, QEvent
from PyQt5 import uic
from PyQt5.QtWidgets import QWidget, QApplication, QMainWindow, QDialog


W = ...


def clickable(widget):
    class Filter(QObject):
        clicked = pyqtSignal()

        def eventFilter(self, obj, event):
            if obj == widget:
                if event.type() == QEvent.MouseButtonRelease:
                    if obj.rect().contains(event.pos()):
                        self.clicked.emit()
                        return True
            return False

    filter = Filter(widget)
    widget.installEventFilter(filter)
    return filter.clicked


class PracticeWidget(QWidget):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        uic.loadUi('./ui/practice.ui', self)

        self.calculate_btn.clicked.connect(self.calculate)

    def calculate(self):
        t_v = float(self.estimated_indoor_air_temp_input.toPlainText())
        t_ot = float(self.avg_temp_out_air_input.toPlainText())
        z_ot = float(self.duration_of_the_heating_period_input.toPlainText())

        gsop = utils.calc_gsop(t_v=t_v, t_ot=t_ot, z_ot=z_ot)
        # r_s = utils.calc_r_s(a=..., b=..., d_d=gsop)

        a_ok = float(self.total_area_external_enclosing_window_and_balcone_doors_input.toPlainText())
        a_fas = float(self.total_area_external_enclosing_facade_input.toPlainText())
        f = utils.calc_f(a_fas=a_fas, a_ok=a_ok)

        a_n_sum = float(self.total_area_external_enclosing_input.toPlainText())
        v_ot = float(self.heated_volume_input.toPlainText())
        k_komp = utils.calc_comp(a_n_sum=a_n_sum, v_ot=v_ot)

        a_pokr = float(self.total_area_external_enclosing_coatings_input.toPlainText())
        a_cherd = float(self.total_area_external_enclosing_attics_input.toPlainText())
        r_pr_st = float(self.hear_transfer_resistance_walls_input.toPlainText())
        r_pr_ok = float(self.hear_transfer_resistance_window_input.toPlainText())
        r_pr_per = float(self.hear_transfer_resistance_overlaps_input.toPlainText())
        r_pr_cherd = float(self.hear_transfer_resistance_attics_input.toPlainText())
        k_obsh = utils.calc_k_obsh(a_n_sum=a_n_sum, a_fas=a_fas,
                                   a_ok=a_ok, a_pokr=a_pokr,
                                   a_cherd=a_cherd, r_pr_st=r_pr_st,
                                   r_pr_ok=r_pr_ok, r_pr_per=r_pr_per,
                                   r_pr_cherd=r_pr_cherd)

        a_sh = float(self.residentia_premises_input.toPlainText())
        cnt_floors = float(self.floor_input.toPlainText())
        n_v = utils.calc_n_v(a_sh=a_sh, cnt_floors=cnt_floors, t_ot=t_ot)

        k_ob = utils.calc_k_ob(k_obsh=k_obsh, k_komp=k_komp)
        k_vent = utils.calc_k_vent()
        k_bit = utils.calc_k_bit(a_sh=a_sh, v_ot=v_ot, t_v=t_v, t_ot=t_ot)
        k_rad = utils.calc_k_rad(gsop=gsop, v_ot=v_ot)

        u = utils.calc_u(gsop=gsop)

        q_ot_p = utils.calc_q_ot_p(k_ob=k_ob, k_vent=k_vent, k_bit=k_bit, k_rad=k_rad, u=u)

        q = utils.calc_q(gsop=gsop, q_ot_p=q_ot_p)
        q_god_ot = utils.calc_q_god_ot(gsop=gsop, q_ot_p=q_ot_p, v_ot=v_ot)

        q_tr_ot = utils.calc_q_tr_ot(cnt_floors=cnt_floors)
        energo_effencity = utils.calc_energo_effencity(q_p_ot=q_ot_p, q_tr_ot=q_tr_ot)

        class_name, class_naimenovation, recomendation = utils.get_result(energo_effencity)

        result_text = f"Класс - {class_name}\n" \
                      f"Наименование класса - {class_naimenovation}\n" \
                      f"Рекомендации - {recomendation}"

        self.result_text.setText(result_text)

        global W
        W = ResultDialog(
            gsop=gsop,
            f=f,
            k_komp=k_komp,
            k_obsh=k_obsh,
            n_v=n_v,
            k_ob=k_ob,
            k_vent=k_vent,
            k_bit=k_bit,
            k_rad=k_rad,
            u=u,
            q=q,
            q_ot_p=q_ot_p,
            q_god_ot=q_god_ot
        )
        W.show()


class TheoryWidget(QWidget):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        uic.loadUi('ui/theory.ui', self)

        clickable(self.label_1).connect(self.section_1)
        clickable(self.label_1_1).connect(self.section_1_1)
        clickable(self.label_1_2).connect(self.section_1_2)
        clickable(self.label_1_3).connect(self.section_1_3)
        clickable(self.label_1_4).connect(self.section_1_4)
        clickable(self.label_1_5).connect(self.section_1_5)
        clickable(self.label_1_6).connect(self.section_1_6)
        clickable(self.label_1_7).connect(self.section_1_7)
        clickable(self.label_1_8).connect(self.section_1_8)

        self.btn_1.clicked.connect(self.section_1)
        self.btn_1_1.clicked.connect(self.section_1_1)
        self.btn_1_2.clicked.connect(self.section_1_2)
        self.btn_1_3.clicked.connect(self.section_1_3)
        self.btn_1_4.clicked.connect(self.section_1_4)
        self.btn_1_5.clicked.connect(self.section_1_5)
        self.btn_1_6.clicked.connect(self.section_1_6)
        self.btn_1_7.clicked.connect(self.section_1_7)
        self.btn_1_8.clicked.connect(self.section_1_8)

    def section_1(self):
        self.scrollArea.verticalScrollBar().setValue(0)

    def section_1_1(self):
        self.scrollArea.verticalScrollBar().setValue(1080)

    def section_1_2(self):
        self.scrollArea.verticalScrollBar().setValue(3200)

    def section_1_3(self):
        self.scrollArea.verticalScrollBar().setValue(4340)

    def section_1_4(self):
        self.scrollArea.verticalScrollBar().setValue(5600)

    def section_1_5(self):
        self.scrollArea.verticalScrollBar().setValue(6900)

    def section_1_6(self):
        self.scrollArea.verticalScrollBar().setValue(8900)

    def section_1_7(self):
        self.scrollArea.verticalScrollBar().setValue(10900)

    def section_1_8(self):
        self.scrollArea.verticalScrollBar().setValue(14700)


class AboutWidget(QWidget):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        uic.loadUi('ui/about.ui', self)


class ResultDialog(QDialog):
    def __init__(self, *args, **kwargs):
        super().__init__()
        uic.loadUi('ui/result.ui', self)

        self.close_btn.clicked.connect(self.close)
        self.out(**kwargs)

    def out(self, **kwargs):
        self.gsop_out.setText(str(round(kwargs.get('gsop'), 4)))
        self.f_out.setText(str(round(kwargs.get('f'), 4)))
        self.k_komp_out.setText(str(round(kwargs.get('k_komp'), 4)))
        self.k_obsh_out.setText(str(round(kwargs.get('k_obsh'), 4)))
        self.nv_out.setText(str(round(kwargs.get('n_v'), 4)))
        self.k_ob_out.setText(str(round(kwargs.get('k_ob'), 4)))
        self.k_vent_out.setText(str(round(kwargs.get('k_vent'), 4)))
        self.k_bit_out.setText(str(round(kwargs.get('k_bit'), 4)))
        self.k_rad_out.setText(str(round(kwargs.get('k_rad'), 4)))
        self.u_out.setText(str(round(kwargs.get('u'), 4)))
        self.q_out.setText(str(round(kwargs.get('q'), 4)))
        self.q_p_ot_out.setText(str(round(kwargs.get('q_ot_p'), 4)))
        self.q_god_out.setText(str(round(kwargs.get('q_god_ot'), 4)))


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        uic.loadUi('ui/main.ui', self)
        self.about_widget = AboutWidget()
        self.stackedWidget.addWidget(self.about_widget)
        self.theory_widget = TheoryWidget()
        self.stackedWidget.addWidget(self.theory_widget)
        self.practice_widget = PracticeWidget()
        self.stackedWidget.addWidget(self.practice_widget)

        self.theory_change.clicked.connect(self.go_to_theory)
        self.practice_change.clicked.connect(self.go_to_practice)
        self.about_program_change.clicked.connect(self.go_to_about)

        self.setFixedSize(1350, 769)

    def go_to_theory(self):
        self.stackedWidget.setCurrentIndex(1)

    def go_to_practice(self):
        self.stackedWidget.setCurrentIndex(2)

    def go_to_about(self):
        self.stackedWidget.setCurrentIndex(0)


if __name__ == '__main__':
    app = QApplication([])
    window = MainWindow()
    window.show()
    app.exec_()

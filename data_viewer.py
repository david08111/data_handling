from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
from PyQt5.QtGui import QIcon, QPixmap, QKeyEvent
import threading
import shutil
import sys
import os
import pickle
import time
import math
# import keyboard



class BasicWindow(QWidget):
    def __init__(self):
        super().__init__()

        self.installEventFilter(self)

        self.box_ver_layout = QVBoxLayout()
        self.setLayout(self.box_ver_layout)

        self.prog_bar_label = QLabel("Data Progress:")
        self.box_ver_layout.addWidget(self.prog_bar_label)

        self.prog_bar = QProgressBar()
        # self.prog_bar.setRange(1, 200)
        # self.prog_bar.setValue(0)
        self.box_ver_layout.addWidget(self.prog_bar)

        self.box_hor_layout = QHBoxLayout()

        self.box_ver_layout.addLayout(self.box_hor_layout)

        self.box_ver_layout_buttons = QVBoxLayout()

        self.but_start = QPushButton("Start")
        self.box_ver_layout_buttons.addWidget(self.but_start)
        self.but_start.clicked.connect(self.but_start_clicked)

        self.but_export_data = QPushButton("Export Data")
        self.box_ver_layout_buttons.addWidget(self.but_export_data)
        self.but_export_data.clicked.connect(self.but_export_data_clicked)

        # self.label_input = QLabel("Input Path:")
        # box_ver_layout_buttons.addWidget(self.label_input)


        self.label_input_folder = QLabel("Input Folder:")
        self.box_ver_layout_buttons.addWidget(self.label_input_folder)

        self.but_input = QPushButton("Select Input Folder")
        self.box_ver_layout_buttons.addWidget(self.but_input)
        self.but_input.clicked.connect(self.get_input_file)


        self.label_output_folder = QLabel("Output Folder:")
        self.box_ver_layout_buttons.addWidget(self.label_output_folder)

        self.but_output = QPushButton("Select Output Folder")
        self.box_ver_layout_buttons.addWidget(self.but_output)
        self.but_output.clicked.connect(self.set_output_file)


        self.label_time = QLabel("Set Mode and Time:")
        self.box_ver_layout_buttons.addWidget(self.label_time)

        self.combobox_mode = QComboBox()
        self.combobox_mode.addItem("Manual")
        self.combobox_mode.addItem("Time")
        self.box_ver_layout_buttons.addWidget(self.combobox_mode)

        self.box_hor_layout_spinbox = QHBoxLayout()

        self.spinbox_time = QDoubleSpinBox()
        self.spinbox_time.setRange(0.1, 10)
        self.box_hor_layout_spinbox.addWidget(self.spinbox_time)
        self.spinbox_time.valueChanged.connect(self.time_value_change)

        self.label_time_estimate = QLabel("Estimated Time:")
        self.box_hor_layout_spinbox.addWidget(self.label_time_estimate)

        self.box_ver_layout_buttons.addLayout(self.box_hor_layout_spinbox)

        self.but_save_state = QPushButton("Save State")
        self.box_ver_layout_buttons.addWidget(self.but_save_state)
        self.but_save_state.clicked.connect(self.but_save_state_clicked)

        self.but_load_state = QPushButton("Load State")
        self.box_ver_layout_buttons.addWidget(self.but_load_state)
        self.but_load_state.clicked.connect(self.but_load_state_clicked)


        self.box_ver_layout_img = QVBoxLayout()

        self.img_name = QLabel("Img Name:")
        self.box_ver_layout_img.addWidget(self.img_name)

        self.img_disp = QLabel("Img:")
        pixmap = QPixmap("/home/david/dataset_ac/train_set_conv_256_test/dop10rgb_32_288_5626_1_nw_2019_0_22.png")
        pixmap = pixmap.scaled(350, 350, Qt.KeepAspectRatio)
        self.img_disp.setPixmap(pixmap)
        self.box_ver_layout_img.addWidget(self.img_disp)

        self.box_hor_layout.addLayout(self.box_ver_layout_img)

        self.box_hor_layout.addLayout(self.box_ver_layout_buttons)


        self.box_hor_select_but = QHBoxLayout()

        self.box_hor_select_but1 = QHBoxLayout()

        self.box_hor_select_but2 = QHBoxLayout()

        self.box_hor_select_but.addLayout(self.box_hor_select_but2)
        self.box_hor_select_but.addLayout(self.box_hor_select_but1)


        self.but_img_back = QPushButton("<-")
        self.box_hor_select_but1.addWidget(self.but_img_back)
        self.but_img_back.clicked.connect(self.but_img_back_clicked)

        self.but_img_del = QPushButton("X")
        self.box_hor_select_but1.addWidget(self.but_img_del)
        self.but_img_del.clicked.connect(self.but_img_del_clicked)

        self.but_img_next = QPushButton("->")
        self.box_hor_select_but1.addWidget(self.but_img_next)
        self.but_img_next.clicked.connect(self.but_img_next_clicked)

        self.but_img_play = QPushButton("Play")
        self.box_hor_select_but2.addWidget(self.but_img_play)
        self.but_img_play.clicked.connect(self.but_img_play_clicked)

        self.but_img_pause = QPushButton("Pause")
        self.box_hor_select_but2.addWidget(self.but_img_pause)
        self.but_img_pause.clicked.connect(self.but_img_pause_clicked)


        self.box_ver_layout_img.addLayout(self.box_hor_select_but)


        self.setWindowTitle("Data Viewer")
        # self.resize(800, 1000)

        self.state = Data_State(self)


    def but_start_clicked(self):
        self.state.start()

    def but_export_data_clicked(self):
        self.state.export_data()

    def but_save_state_clicked(self):
        self.state.save_state()

    def but_img_play_clicked(self):
        self.state.img_play()

    def but_img_pause_clicked(self):
        self.state.img_pause()

    def but_load_state_clicked(self):
        self.state.load_state()

    def but_img_back_clicked(self):
        self.state.load_prev_img()

    def but_img_next_clicked(self):
        self.state.load_next_img()

    def but_img_del_clicked(self):
        self.state.rem_curr_img()

    def time_value_change(self):
        self.state.set_time(self.spinbox_time.value())

    def get_input_file(self):
        # print("test")
        self.file_dialog = QFileDialog()
        self.file_dialog.setFileMode(QFileDialog.Directory)
        if self.file_dialog.exec_():
            input_path = self.file_dialog.selectedFiles()[0]
            self.state.set_input_file_names_from_path(input_path)
            self.label_input_folder.setText("Input Folder: " + input_path)
            # print(dir_name)

    def set_output_file(self):
        self.file_dialog = QFileDialog()
        self.file_dialog.setFileMode(QFileDialog.Directory)
        if self.file_dialog.exec_():
            output_path = self.file_dialog.selectedFiles()[0]
            self.state.set_output_path(output_path)
            self.label_output_folder.setText("Output Folder: " + output_path)

    def keyPressEvent(self, event: QKeyEvent) -> None:
        activate_again = False
        if event.key() == Qt.Key_A:
            self.state.load_prev_img()
        elif event.key() == Qt.Key_D:
            self.state.load_next_img()
        elif event.key() == Qt.Key_W:
            self.state.rem_curr_img()
        elif event.key() == Qt.Key_S:
            self.state.time_running = not self.state.time_running
        elif event.key() == Qt.Key_Q:
            if not self.state.time_rem_img:
                self.state.time_rem_img = True

    # def key_press(self, key):
    #     if key == "left":
    #         self.state.load_prev_img()
    #     elif key == "right":
    #         self.state.load_next_img()
    #     elif key == "up":
    #         self.state.rem_curr_img()
    #     elif key == "down":
    #         self.state.time_running = not self.state.time_running


# class KeyEventReceiver(QObject):
#     def __init__(self):
#         super().__init__()
#
#     def eventFilter(self, a0: 'QObject', event: 'QEvent') -> bool:
#         if (event.type() == QEvent.KeyPress):
#             if event.key() == Qt.Key_Left:
#                 self.state.load_prev_img()
#             elif event.key() == Qt.Key_Right:
#                 self.state.load_next_img()
#             elif event.key() == Qt.Key_Up:
#                 self.state.rem_curr_img()
#             elif event.key() == Qt.Key_Down:
#                 self.state.time_running = not self.state.time_running

class Data_State():
    def __init__(self, wind):
        self.window = wind
        self.img_out_list = []
        self.img_rem_list = []
        self.time_running = False
        self.time_rem_img = False
        self.estimated_time = 0
        self.img_size = 500
        self.auto_save_nr = 50

    def start(self):
        self.window.prog_bar.setRange(0, len(self.file_paths) - 1)
        self.img_counter = 0
        # self.window.prog_bar.setValue(self.img_counter)


        pixmap = QPixmap(self.file_paths[self.img_counter])
        pixmap = pixmap.scaled(self.img_size, self.img_size)
        self.window.img_disp.setPixmap(pixmap)
        self.window.img_name.setText("Img: " + os.path.basename(self.file_paths[self.img_counter]))

        self.update_prog_bar()
        if self.window.combobox_mode.currentText() == "Time" and not self.time_running ==True:
            self.update_estimated_time()
            thread_time = threading.Thread(target=self.time_loop, daemon=True)
            thread_time.start()
            self.time_running = True

    def set_time(self, wait_time):
        self.time = wait_time

    def load_next_img(self):
        if self.file_paths[self.img_counter] not in self.img_out_list:
            self.img_out_list.append(self.file_paths[self.img_counter])

        if self.img_counter + 1 < len(self.file_paths):
            self.img_counter += 1

        pixmap = QPixmap(self.file_paths[self.img_counter])
        # pixmap = pixmap.scaled(self.img_size, self.img_size, Qt.KeepAspectRatio)
        pixmap = pixmap.scaled(self.img_size, self.img_size)
        # pixmap = pixmap.scaledToHeight(self.img_size)
        self.window.img_disp.setPixmap(pixmap)
        self.window.img_name.setText("Img: " + os.path.basename(self.file_paths[self.img_counter]))

        self.update_prog_bar()

        if self.img_counter % self.auto_save_nr == 0:
            self.save_state()

    def load_prev_img(self):
        if self.file_paths[self.img_counter] not in self.img_out_list:
            self.img_out_list.append(self.file_paths[self.img_counter])

        if self.img_counter - 1 >= 0:
            self.img_counter -= 1

        pixmap = QPixmap(self.file_paths[self.img_counter])
        # pixmap = pixmap.scaled(self.img_size, self.img_size, Qt.KeepAspectRatio)
        pixmap = pixmap.scaled(self.img_size, self.img_size)
        # pixmap = pixmap.scaledToHeight(self.img_size)
        self.window.img_disp.setPixmap(pixmap)
        self.window.img_name.setText("Img: " + os.path.basename(self.file_paths[self.img_counter]))

        self.update_prog_bar()

    def rem_curr_img(self):
        if self.file_paths[self.img_counter] not in self.img_rem_list:
            self.img_rem_list.append(self.file_paths[self.img_counter])
        if self.file_paths[self.img_counter] in self.img_out_list:
            self.img_out_list.remove(self.file_paths[self.img_counter])

        if self.img_counter + 1 < len(self.file_paths):
            self.img_counter += 1

        pixmap = QPixmap(self.file_paths[self.img_counter])
        # pixmap = pixmap.scaled(self.img_size, self.img_size, Qt.KeepAspectRatio)
        pixmap = pixmap.scaled(self.img_size, self.img_size)
        # pixmap = pixmap.scaledToHeight(self.img_size)
        self.window.img_disp.setPixmap(pixmap)
        self.window.img_name.setText("Img: " + os.path.basename(self.file_paths[self.img_counter]))

        self.update_prog_bar()

    def update_prog_bar(self):
        self.window.prog_bar.setValue(self.img_counter)

    def set_input_file_names_from_path(self, in_path):
        self.file_paths = sorted([os.path.join(in_path, f) for f in os.listdir(in_path) if os.path.isfile(os.path.join(in_path, f))], key=str.lower)

    def set_output_path(self, out_path):
        self.output_path = out_path

    def export_data(self):
        self.img_out_list = list(set(self.img_out_list))

        self.img_rem_list = list(set(self.img_rem_list))

        for out_file in self.img_out_list:
            file_name = os.path.basename(out_file)
            shutil.copyfile(out_file, os.path.join(self.output_path, file_name))

        if not os.path.isdir(os.path.join(self.output_path, "removed_files")):
            os.makedirs(os.path.join(self.output_path, "removed_files"))

        for rem_file in self.img_rem_list:
            file_name = os.path.basename(rem_file)
            shutil.copyfile(rem_file, os.path.join(self.output_path, "removed_files", file_name))

    def save_state(self):
        save_state_dict = {"file_list": self.file_paths, "out_list": self.img_out_list, "rem_list": self.img_rem_list, "img_counter": self.img_counter}
        pickle.dump(save_state_dict, open("./data_save.p", "wb"))

    def load_state(self):
        load_state_dict = pickle.load(open("./data_save.p", "rb"))
        self.file_paths = load_state_dict["file_list"]
        self.img_out_list = load_state_dict["out_list"]
        self.img_rem_list = load_state_dict["rem_list"]
        self.img_counter = load_state_dict["img_counter"]
        self.window.prog_bar.setRange(0, len(self.file_paths) - 1)

        pixmap = QPixmap(self.file_paths[self.img_counter])
        pixmap = pixmap.scaled(self.img_size, self.img_size)
        self.window.img_disp.setPixmap(pixmap)
        self.window.img_name.setText("Img: " + os.path.basename(self.file_paths[self.img_counter]))

        if self.window.combobox_mode.currentText() == "Time" and not self.time_running ==True:
            self.update_estimated_time()
            thread_time = threading.Thread(target=self.time_loop, daemon=True)
            thread_time.start()
            self.time_running = True

    def img_pause(self):
        self.time_running = False

    def img_play(self):
        self.time_running = True

    def update_estimated_time(self):
        self.estimated_time = (len(self.file_paths) - self.img_counter + 1) * self.time
        hours = math.trunc(self.estimated_time / 3600)
        minutes = math.trunc((self.estimated_time % 3600) / 60)
        seconds = math.trunc((self.estimated_time % 3600) % 60)
        self.window.label_time_estimate.setText("Estimated Time: " + str(hours) + "hh " + str(minutes) + "mm " + str(seconds) + "ss" )

    def time_loop(self):
        while True:
            time.sleep(self.time)
            if self.time_running:
                # time.sleep(self.time)
                if not self.time_rem_img:
                    self.load_next_img()
                else:
                    self.rem_curr_img()
                    self.time_rem_img = False
                self.update_estimated_time()

if __name__ == '__main__':
    window_height = 650
    window_width = 1000
    app = QApplication(sys.argv)
    window = BasicWindow()

    # keyboard.on_press(window.key_press)

    window.setFixedSize(window_width, window_height)
    window.show()
    sys.exit(app.exec_())
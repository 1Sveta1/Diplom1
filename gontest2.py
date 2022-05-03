import sys
import pygame
import os
import random
from PyQt5 import QtGui
from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import (QApplication, QMainWindow, QPushButton,
                             QToolTip, QMessageBox, QLabel, QCheckBox, QLineEdit, QTextEdit)
import serial  # Serial imported for Serial communication
import time  # Required to use delay functions
import pyautogui
import ctypes
import keyboard
import pickle
import sqlite3
import numpy as np
from PyQt5.uic.properties import QtCore

global user_login
global user_password
global id_vers
global user_id
global func_1

db = sqlite3.connect('server1.db')
sql = db.cursor()

ArduinoSerial = serial.Serial('com4', 9600)  # Create Serial port object called arduinoSerialData
time.sleep(2)  # wait for 2 seconds for the communication to get established


# sql.execute(f"Update users SET id_version = '{id_vers}' WHERE login = '{user_login}'")
# sql.execute(f"INSERT INTO users(login, password) VALUES (?, ?)",(user_login, user_password))

def function(string):
    if 'down' == string:
        pyautogui.move(0, 20)

    if 'high' == string:
        # pyautogui.move(0, -20)
        pyautogui.typewrite(['space'], 0.2)

    if 'left' == string:
        pyautogui.move(-20, 0)

    if 'right' == string:
        pyautogui.move(20, 0)

    if 'click' == string:
        pyautogui.click()

    if 'center' == string:
        user32 = ctypes.windll.user32
        screensize = user32.GetSystemMetrics(0)
        screensize_1 = user32.GetSystemMetrics(1)
        center_x = screensize / 2
        center_y = screensize_1 / 2
        pyautogui.moveTo(center_x, center_y)

    # 2 датчик
    if 'Play/Pause' == string:
        pyautogui.typewrite(['space'], 0.2)

    if 'Vdown' == string:
        pyautogui.press('volumedown')

    if 'Vup' == string:
        pyautogui.press('volumeup')

    if 'language' == string:
        pyautogui.hotkey('shift', 'alt')

    if 'Rewind' == string:
        pyautogui.hotkey('left')

    if 'Forward' == string:
        pyautogui.hotkey('right')

    if 'Win+d' == string:
        pyautogui.hotkey('win', 'd')

    if 'ctrl+z' == string:
        pyautogui.hotkey('ctrl', 'z')

    if 'click_r' == string:
        pyautogui.rightClick()

    if 'Sdown' == string:
        pyautogui.scroll(-40)

    if 'Sup' == string:
        pyautogui.scroll(40)

    if 'ctrl+alt+delete' == string:
        pyautogui.hotkey('ctrl', 'shift', 'esc')


def game():
    pygame.init()

    SCREEN_HEIGHT = 600
    SCREEN_WIDTH = 1100
    SCREEN = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))

    RUNNING = [pygame.image.load("DinoRun1.png"),
               pygame.image.load("DinoRun2.png")]
    JUMPING = pygame.image.load("DinoJump.png")
    DUCKING = [pygame.image.load("DinoDuck1.png"),
               pygame.image.load("DinoDuck2.png")]

    SMALL_CACTUS = [pygame.image.load("SmallCactus1.png"),
                    pygame.image.load("SmallCactus2.png"),
                    pygame.image.load("SmallCactus3.png")]
    LARGE_CACTUS = [pygame.image.load("LargeCactus1.png"),
                    pygame.image.load("LargeCactus2.png"),
                    pygame.image.load("LargeCactus3.png")]

    BIRD = [pygame.image.load("Bird1.png"),
            pygame.image.load("Bird2.png")]

    CLOUD = pygame.image.load("Cloud.png")

    BG = pygame.image.load("Track.png")

    class Dinosaur:
        X_POS = 80
        Y_POS = 310
        Y_POS_DUCK = 340
        JUMP_VEL = 8.5

        def __init__(self):
            self.duck_img = DUCKING
            self.run_img = RUNNING
            self.jump_img = JUMPING

            self.dino_duck = False
            self.dino_run = True
            self.dino_jump = False

            self.step_index = 0
            self.jump_vel = self.JUMP_VEL
            self.image = self.run_img[0]
            self.dino_rect = self.image.get_rect()
            self.dino_rect.x = self.X_POS
            self.dino_rect.y = self.Y_POS

        def update(self, userInput):
            if self.dino_duck:
                self.duck()
            if self.dino_run:
                self.run()
            if self.dino_jump:
                self.jump()

            if self.step_index >= 10:
                self.step_index = 0

            if userInput[pygame.K_SPACE] and not self.dino_jump:
                self.dino_duck = False
                self.dino_run = False
                self.dino_jump = True
            elif userInput[pygame.K_DOWN] and not self.dino_jump:
                self.dino_duck = True
                self.dino_run = False
                self.dino_jump = False
            elif not (self.dino_jump or userInput[pygame.K_DOWN]):
                self.dino_duck = False
                self.dino_run = True
                self.dino_jump = False

        def duck(self):
            self.image = self.duck_img[self.step_index // 5]
            self.dino_rect = self.image.get_rect()
            self.dino_rect.x = self.X_POS
            self.dino_rect.y = self.Y_POS_DUCK
            self.step_index += 1

        def run(self):
            self.image = self.run_img[self.step_index // 5]
            self.dino_rect = self.image.get_rect()
            self.dino_rect.x = self.X_POS
            self.dino_rect.y = self.Y_POS
            self.step_index += 1

        def jump(self):
            self.image = self.jump_img
            if self.dino_jump:
                self.dino_rect.y -= self.jump_vel * 4
                self.jump_vel -= 0.8
            if self.jump_vel < - self.JUMP_VEL:
                self.dino_jump = False
                self.jump_vel = self.JUMP_VEL

        def draw(self, SCREEN):
            SCREEN.blit(self.image, (self.dino_rect.x, self.dino_rect.y))

    class Cloud:
        def __init__(self):
            self.x = SCREEN_WIDTH + random.randint(800, 1000)
            self.y = random.randint(50, 100)
            self.image = CLOUD
            self.width = self.image.get_width()

        def update(self):
            self.x -= game_speed
            if self.x < -self.width:
                self.x = SCREEN_WIDTH + random.randint(2500, 3000)
                self.y = random.randint(50, 100)

        def draw(self, SCREEN):
            SCREEN.blit(self.image, (self.x, self.y))

    class Obstacle:
        def __init__(self, image, type):
            self.image = image
            self.type = type
            self.rect = self.image[self.type].get_rect()
            self.rect.x = SCREEN_WIDTH

        def update(self):
            self.rect.x -= game_speed
            if self.rect.x < -self.rect.width:
                obstacles.pop()

        def draw(self, SCREEN):
            SCREEN.blit(self.image[self.type], self.rect)

    class SmallCactus(Obstacle):
        def __init__(self, image):
            self.type = random.randint(0, 2)
            super().__init__(image, self.type)
            self.rect.y = 325

    class LargeCactus(Obstacle):
        def __init__(self, image):
            self.type = random.randint(0, 2)
            super().__init__(image, self.type)
            self.rect.y = 300

    class Bird(Obstacle):
        def __init__(self, image):
            self.type = 0
            super().__init__(image, self.type)
            self.rect.y = 250
            self.index = 0

        def draw(self, SCREEN):
            if self.index >= 9:
                self.index = 0
            SCREEN.blit(self.image[self.index // 5], self.rect)
            self.index += 1

    def main():
        global game_speed, x_pos_bg, y_pos_bg, points, obstacles
        run = True
        clock = pygame.time.Clock()
        player = Dinosaur()
        cloud = Cloud()
        game_speed = 20
        x_pos_bg = 0
        y_pos_bg = 380
        points = 0
        font = pygame.font.Font('freesansbold.ttf', 20)
        obstacles = []
        death_count = 0

        def score():
            global points, game_speed
            points += 1
            if points % 100 == 0:
                game_speed += 1

            text = font.render("Points: " + str(points), True, (0, 0, 0))
            textRect = text.get_rect()
            textRect.center = (1000, 40)
            SCREEN.blit(text, textRect)

        def background():
            global x_pos_bg, y_pos_bg
            image_width = BG.get_width()
            SCREEN.blit(BG, (x_pos_bg, y_pos_bg))
            SCREEN.blit(BG, (image_width + x_pos_bg, y_pos_bg))
            if x_pos_bg <= -image_width:
                SCREEN.blit(BG, (image_width + x_pos_bg, y_pos_bg))
                x_pos_bg = 0
            x_pos_bg -= game_speed

        while run:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    run = False

            SCREEN.fill((255, 255, 255))
            userInput = pygame.key.get_pressed()

            player.draw(SCREEN)
            player.update(userInput)

            if len(obstacles) == 0:
                if random.randint(0, 2) == 0:
                    obstacles.append(SmallCactus(SMALL_CACTUS))
                elif random.randint(0, 2) == 1:
                    obstacles.append(LargeCactus(LARGE_CACTUS))
                elif random.randint(0, 2) == 2:
                    obstacles.append(Bird(BIRD))

            for obstacle in obstacles:
                obstacle.draw(SCREEN)
                obstacle.update()
                if player.dino_rect.colliderect(obstacle.rect):
                    pygame.time.delay(2000)
                    death_count += 1
                    menu(death_count)

            background()

            cloud.draw(SCREEN)
            cloud.update()

            score()

            clock.tick(30)
            pygame.display.update()

    def menu(death_count):
        global points
        run = True
        while run:
            SCREEN.fill((255, 255, 255))
            font = pygame.font.Font('freesansbold.ttf', 30)

            if death_count == 0:
                text = font.render("Press any Key to Start", True, (0, 0, 0))
            elif death_count > 0:
                text = font.render("Press any Key to Restart", True, (0, 0, 0))
                score = font.render("Your Score: " + str(points), True, (0, 0, 0))
                scoreRect = score.get_rect()
                scoreRect.center = (SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2 + 50)
                SCREEN.blit(score, scoreRect)
            textRect = text.get_rect()
            textRect.center = (SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2)
            SCREEN.blit(text, textRect)
            SCREEN.blit(RUNNING[0], (SCREEN_WIDTH // 2 - 20, SCREEN_HEIGHT // 2 - 140))
            pygame.display.update()
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    run = False
                if event.type == pygame.KEYDOWN:
                    main()

    menu(death_count=0)


class Settings(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Настройки")
        self.setStyleSheet("background-color: gray")
        self.resize(320, 280)
        self.setStyleSheet("QMainWindow { background-image: url(222.jpg); }")
        self.checkBox_13 = QCheckBox("Просунутий", self)
        self.checkBox_13.setGeometry(50, 152, 150, 20)
        self.checkBox_13.setObjectName("checkBox_13")
        self.checkBox_13.setStyleSheet("QCheckBox::indicator:pressed"
                                       "{"
                                       "background-color : lightgreen;"
                                       "}")
        self.label_2 = QLabel("Вибір версії", self)
        self.label_2.setGeometry(40, 20, 200, 30)
        self.label_2.setStyleSheet("color: rgb(255, 255, 255);""font: 75 italic 15pt \"Times New Roman\";")
        self.label_2.setObjectName("label_2")
        self.checkBox_11 = QCheckBox("Початкова", self)
        self.checkBox_11.setGeometry(50, 80, 130, 20)
        self.checkBox_11.setObjectName("checkBox_11")
        self.checkBox_12 = QCheckBox("Впевнене управління", self)
        self.checkBox_12.setGeometry(50, 116, 240, 20)
        self.checkBox_12.setObjectName("checkBox_12")
        self.checkBox_11.setStyleSheet("QCheckBox::indicator:pressed"
                                       "{"
                                       "background-color : lightgreen;"
                                       "}")
        self.checkBox_11.setStyleSheet("color: rgb(255, 255, 255);""font: 10pt \"Blackadder ITC\";\n""")
        self.checkBox_12.setStyleSheet("QCheckBox::indicator:pressed"
                                       "{"
                                       "background-color : lightgreen;"
                                       "}")
        self.checkBox_12.setStyleSheet("color: rgb(255, 255, 255);""font: 10pt \"Blackadder ITC\";\n""")
        self.checkBox_13.setStyleSheet("color: rgb(255, 255, 255);""font: 10pt \"Blackadder ITC\";\n""")
        self.Sohr = QPushButton("Зберегти", self)
        self.Sohr.setGeometry(30, 200, 120, 60)
        self.Sohr.setStyleSheet(" QPushButton {\n"
                                "     border: 2px solid #8f8f91;\n"

                                "     min-width: 80px;\n"
                                " }\n"
                                "\n"
                                " QPushButton:pressed {\n"
                                "     background-color: qlineargradient(x1: 0, y1: 0, x2: 0, y2: 1,\n"
                                "                                       stop: 0 #dadbde, stop: 1 #f6f7fa);\n"
                                " }\n"
                                "\n"
                                " QPushButton:flat {\n"
                                "     border: none; /* для плоской кнопки границы нет */\n"
                                " }\n"
                                "\n"
                                " QPushButton:default {\n"
                                "     border-color: navy; /* делаем кнопку по умолчанию выпуклой */\n"
                                " }")
        self.Sohr.setStyleSheet("""
                       QPushButton{
                           font-style: oblique;
                           font-weight: bold;
                           border: 2px solid #8f8f91;
                           border-radius: 10px;
                           color: #1DA1F2;
                           background-color: #fff;
                       }
                       """)
        self.Sohr.setObjectName("Sohr")
        self.back = QPushButton("Назад", self)
        self.back.setGeometry(160, 200, 120, 60)
        self.back.setStyleSheet(" QPushButton {\n"
                                "     border: 2px solid #8f8f91;\n"

                                "     min-width: 80px;\n"
                                " }\n"
                                "\n"
                                " QPushButton:pressed {\n"
                                "     background-color: qlineargradient(x1: 0, y1: 0, x2: 0, y2: 1,\n"
                                "                                       stop: 0 #dadbde, stop: 1 #f6f7fa);\n"
                                " }\n"
                                "\n"
                                " QPushButton:flat {\n"
                                "     border: none; /* для плоской кнопки границы нет */\n"
                                " }\n"
                                "\n"
                                " QPushButton:default {\n"
                                "     border-color: navy; /* делаем кнопку по умолчанию выпуклой */\n"
                                " }")
        self.back.setStyleSheet("""
                       QPushButton{
                           font-style: oblique;
                           font-weight: bold;
                           border: 2px solid #8f8f91;
                           border-radius: 10px;
                           color: #1DA1F2;
                           background-color: #fff;
                       }
                       """)
        self.back.setObjectName("back")
        self.back.clicked.connect(self.add)
        self.Sohr.clicked.connect(self.qwq)
        self.Sohr.clicked.connect(self.StateCheckBox)
        self.Sohr.clicked.connect(self.print_user_id)

    def print_user_id(self):
        global id_vers
        global user_id
        vers_start = sql.execute(f"Select id_version From users Where id = '{user_id}'")
        b = vers_start.fetchone()
        print(b[0])
        if b[0] == 1:
            window2.inform.setText("Обрано початкову версію")
            window2.inform.setStyleSheet("color: white;""font: 10pt \"Blackadder ITC\";\n""")
        if b[0] == 2:
            window2.inform.setText("Обрано версію: впевнен. упр.")
            window2.inform.setStyleSheet("color: white;""font: 10pt \"Blackadder ITC\";\n""")
        if b[0] == 3:
            window2.inform.setText("Обрано просунуту версію")
            window2.inform.setStyleSheet("color: white;""font: 10pt \"Blackadder ITC\";\n""")
        if b[0] is None:
            window2.inform.setText("Версія не обрана!!!")
            window2.inform.setStyleSheet("color: red;""font: 10pt \"Blackadder ITC\";\n""")

    def StateCheckBox(self):
        if self.checkBox_11.isChecked():
            self.checkBox_12.setDisabled(True)
            self.checkBox_13.setDisabled(True)
        if self.checkBox_12.isChecked():  # 2
            self.checkBox_11.setDisabled(True)
            self.checkBox_13.setDisabled(True)
        if self.checkBox_13.isChecked():  # 3
            self.checkBox_12.setDisabled(True)
            self.checkBox_11.setDisabled(True)

    def qwq(self):
        print(user_id)
        global id_vers
        if self.checkBox_11.isChecked():
            id_vers = 1
            sql.execute(f"Update users SET id_version = '{id_vers}' WHERE id = '{user_id}'")
            db.commit()
            for value in sql.execute("SELECT * FROM users"):
                print(value)
        if self.checkBox_12.isChecked():
            id_vers = 2
            sql.execute(f"Update users SET id_version = '{id_vers}' WHERE id = '{user_id}'")
            db.commit()
            for value in sql.execute("SELECT * FROM users"):
                print(value)
        if self.checkBox_13.isChecked():
            id_vers = 3
            sql.execute(f"Update users SET id_version = '{id_vers}' WHERE id = '{user_id}'")
            db.commit()
            for value in sql.execute("SELECT * FROM users"):
                print(value)

    def add(self):
        window2.show()
        self.hide()

    # def proverka(self):
    #     user_login = self.lineEdit.text()
    #     if id_vers == 1:
    #         sql.execute(f"INSERT INTO users(id_version) VALUES (?) WHERE login = '{user_login}'", (id_vers))
    #         db.commit()
    #         for value in sql.execute("SELECT * FROM users"):
    #              print(value)


class Avtoriz(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Вхід")
        self.setStyleSheet("background-color: gray")
        self.resize(350, 180)
        self.setStyleSheet("QMainWindow { background-image: url(222.jpg); }")
        self.vhod = QPushButton("Вход", self)
        self.vhod.setGeometry(180, 60, 150, 25)
        self.vhod.setStyleSheet(" QPushButton {\n"
                                "     border: 2px solid #8f8f91;\n"
                                "     border-radius: 6px;\n"
                                "     background-color: qlineargradient(x1: 0, y1: 0, x2: 0, y2: 1,\n"
                                "                                       stop: 0 #f6f7fa, stop: 1 #dadbde);\n"
                                "     min-width: 80px;\n"
                                " }\n"
                                "\n"
                                " QPushButton:pressed {\n"
                                "     background-color: qlineargradient(x1: 0, y1: 0, x2: 0, y2: 1,\n"
                                "                                       stop: 0 #dadbde, stop: 1 #f6f7fa);\n"
                                " }\n"
                                "\n"
                                " QPushButton:flat {\n"
                                "     border: none; /* для плоской кнопки границы нет */\n"
                                " }\n"
                                "\n"
                                " QPushButton:default {\n"
                                "     border-color: navy; /* делаем кнопку по умолчанию выпуклой */\n"
                                " }")
        self.vhod.setStyleSheet("""
               QPushButton{
                   font-style: oblique;
                   font-weight: bold;
                   border: 2px solid #8f8f91;
                   border-radius: 10px;
                   color: #1DA1F2;
                   background-color: #fff;
               }
               """)
        self.vhod.setObjectName("vhod")
        self.reg = QPushButton("Реєстрація", self)
        self.reg.setGeometry(180, 105, 150, 25)
        self.reg.setStyleSheet(" QPushButton {\n"
                               "     border: 2px solid #8f8f91;\n"

                               "     min-width: 80px;\n"
                               " }\n"
                               "\n"
                               " QPushButton:pressed {\n"
                               "     background-color: qlineargradient(x1: 0, y1: 0, x2: 0, y2: 1,\n"
                               "                                       stop: 0 #dadbde, stop: 1 #f6f7fa);\n"
                               " }\n"
                               "\n"
                               " QPushButton:flat {\n"
                               "     border: none; /* для плоской кнопки границы нет */\n"
                               " }\n"
                               "\n"
                               " QPushButton:default {\n"
                               "     border-color: navy; /* делаем кнопку по умолчанию выпуклой */\n"
                               " }")
        self.reg.setStyleSheet("""
        QPushButton{
            font-style: oblique;
            font-weight: bold;
            border: 2px solid #8f8f91;
            border-radius: 10px;
            color: #1DA1F2;
            background-color: #fff;
        }
        """)
        self.reg.setObjectName("reg")
        self.lineEdit = QLineEdit("Логін", self)
        self.lineEdit.setGeometry(10, 60, 150, 25)
        self.lineEdit.setStyleSheet("""
        QLineEdit{
            border: 1px solid #CCD6DD;
            border-radius: 10px;
        }
        """)
        self.lineEdit.setObjectName("lineEdit")
        self.lineEdit_2 = QLineEdit("Password", self)
        self.lineEdit_2.setGeometry(10, 105, 150, 25)
        self.lineEdit_2.setStyleSheet("""
        QLineEdit{
            border: 1px solid #CCD6DD;
            border-radius: 10px;
        }
        """)
        self.lineEdit_2.setEchoMode(self.lineEdit_2.Password)
        self.lineEdit_2.setObjectName("lineEdit_2")
        self.label = QLabel("Ласкаво просимо", self)
        # self.label.setStyleSheet("color: rgb(255, 255, 255);""font: 12pt \"Blackadder ITC\";\n""")
        self.label.setGeometry(70, 20, 250, 31)
        self.label.setAutoFillBackground(False)
        self.label.setStyleSheet("color: white;""font: 75 italic 12pt \"Times New Roman\";")
        self.label.setScaledContents(False)
        self.label.setWordWrap(False)
        self.label.setOpenExternalLinks(False)
        self.label.setObjectName("label")
        self.vhod.clicked.connect(self.click_vhod)
        self.reg.clicked.connect(self.reg_click)

    def add_23(self):
        self.hide()

    def reg_click(self):
        global user_id
        global user_login
        global id_vers
        global user_password
        user_login = self.lineEdit.text()
        user_password = self.lineEdit_2.text()
        sql.execute(f"SELECT login FROM users WHERE login = '{user_login}'  ")
        if sql.fetchone() is None:
            sql.execute(f"INSERT INTO users(login, password) VALUES (?, ?)", (user_login, user_password))
            db.commit()
            a = sql.execute(f"SELECT id FROM users WHERE login = '{user_login}' and password = '{user_password}' ")
            a = sql.fetchone()
            user_id = a[0]
            print(user_id)
            window2.show()
            self.hide()
            vers_start = sql.execute(f"Select id_version From users Where id = '{user_id}'")
            b = vers_start.fetchone()
            print(b[0])
            if b[0] == 1:
                window2.inform.setText("Обрано початкову версію")
                window2.inform.setStyleSheet("color: white;""font: 10pt \"Blackadder ITC\";\n""")
            if b[0] == 2:
                window2.inform.setText("Обрано версію: впевнен. упр.")
                window2.inform.setStyleSheet("color: white;""font: 10pt \"Blackadder ITC\";\n""")
            if b[0] == 3:
                window2.inform.setText("Обрано просунуту версію")
                window2.inform.setStyleSheet("color: white;""font: 10pt \"Blackadder ITC\";\n""")
            if b[0] is None:
                window2.inform.setText("Версія не обрана!!!")
                window2.inform.setStyleSheet("color: red;""font: 10pt \"Blackadder ITC\";\n""")

            for value in sql.execute("SELECT * FROM users"):
                print(value)
        else:
            msg = QMessageBox()
            msg.setIcon(QMessageBox.Critical)
            msg.setText("Error")
            msg.setInformativeText('More information')
            msg.setWindowTitle("Error")
            msg.exec_()

    def click_vhod(self):
        global user_id
        global user_login
        global id_vers
        global user_password
        user_login = self.lineEdit.text()
        user_password = self.lineEdit_2.text()
        a = sql.execute(f"SELECT id FROM users WHERE login = '{user_login}' and password = '{user_password}' ")
        a = sql.fetchone()
        if a is None:
            msg = QMessageBox()
            msg.setIcon(QMessageBox.Critical)
            msg.setText("Error")
            msg.setInformativeText('Такого логіну не існує')
            msg.setWindowTitle("Error")
            msg.exec_()
        else:
            user_id = a[0]
            print(user_id)
            window2.show()
            self.hide()
            vers_start = sql.execute(f"Select id_version From users Where id = '{user_id}'")
            b = vers_start.fetchone()
            print(b[0])
            if b[0] == 1:
                window2.inform.setText("Обрано початкову версію")
                window2.inform.setStyleSheet("color: white;""font: 10pt \"Blackadder ITC\";\n""")
            if b[0] == 2:
                window2.inform.setText("Обрано версію: впевнен. упр.")
                window2.inform.setStyleSheet("color: white;""font: 10pt \"Blackadder ITC\";\n""")
            if b[0] == 3:
                window2.inform.setText("Обрано просунуту версію")
                window2.inform.setStyleSheet("color: white;""font: 10pt \"Blackadder ITC\";\n""")
            if b[0] is None:
                window2.inform.setText("Версія не обрана!!!")
                window2.inform.setStyleSheet("color: red;""font: 10pt \"Blackadder ITC\";\n""")

            login_user = sql.execute(f"Select login From users Where id= '{user_id}'")
            c = login_user.fetchone()
            print(c[0])
            window2.login.setText("login: " + c[0])
            window2.login.setStyleSheet("color: white")


class Instruct(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Інструкція")
        self.setStyleSheet("background-color: gray")
        self.resize(750, 500)
        self.setStyleSheet("QMainWindow { background-image: url(instr.jpg); }")
        self.ph = QPushButton("Назад", self)
        self.ph.setGeometry(50, 300, 200, 40)
        self.ph.setStyleSheet(" QPushButton {\n"
                              "     border: 2px solid #8f8f91;\n"
                              "     border-radius: 6px;\n"
                              "     background-color: qlineargradient(x1: 0, y1: 0, x2: 0, y2: 1,\n"
                              "                                       stop: 0 #f6f7fa, stop: 1 #dadbde);\n"
                              "     min-width: 80px;\n"
                              " }\n"
                              "\n"
                              " QPushButton:pressed {\n"
                              "     background-color: qlineargradient(x1: 0, y1: 0, x2: 0, y2: 1,\n"
                              "                                       stop: 0 #dadbde, stop: 1 #6e7cff);\n"
                              " }\n"
                              "\n"
                              " QPushButton:flat {\n"
                              "     border: none; /* для плоской кнопки границы нет */\n"
                              " }\n"
                              "\n"
                              " QPushButton:default {\n"
                              "     border-color: navy; /* делаем кнопку по умолчанию выпуклой */\n"
                              " }")
        self.ph.setStyleSheet("""
                    QPushButton{
                        font-style: oblique;
                        font-weight: bold;
                        border: 2px solid #8f8f91;
                        border-radius: 10px;
                        color: #1DA1F2;
                        background-color: #fff;
                    }
                    """)
        self.textEdit = QTextEdit(self)
        self.textEdit.setGeometry(10, 20, 300, 250)
        self.textEdit.setObjectName("textEdit")
        self.textEdit.setText(
            "Ланцюжок-інструкція використання програми: Вхід-Налаштування-Вибір Версії-Клікніть на кнопку *Зберегти* - Повертаєтеся до головного вікна, натиснувши кнопку *Назад* - Для запуску натисніть кнопку *Запуск* - Залежно від вашої версії за допомогою жестів будуть виконуватися ті чи інші функції")
        self.textEdit.setDisabled(True)
        self.textEdit.setStyleSheet("""QTextEdit
        {
        font-style: oblique;
            font-weight: bold;
            border: 2px solid #8f8f91;
            border-radius: 10px;
            color: rgb(255, 255, 255);
            border-color: rgb(255, 255, 255);
            background-image: url(222.jpg) ;
        
        }""")
        self.textEdit2 = QTextEdit(self)
        self.textEdit2.setGeometry(400, 20, 300, 250)
        self.textEdit2.setObjectName("textEdit2")
        self.textEdit2.setStyleSheet("""QTextEdit
                {
                font-style: oblique;
                    font-weight: bold;
                    border: 2px solid #8f8f91;
                    border-radius: 10px;
                    color: rgb(255, 255, 255);
                    border-color: rgb(255, 255, 255);
                   background-image: url(222.jpg) ;
                }""")

        self.ph.clicked.connect(self.add_1)
        self.input_inform()

    def input_inform(self):
        global user_id
        vers_znach = sql.execute(f"Select id_version From users Where id = '{user_id}'")
        name = vers_znach.fetchone()
        if not name[0] is None:
            versionsFunc = sql.execute(
                f"Select name_func From versions_func Inner join  func ON versions_func.func_id = func.id Where version_id = '{name[0]}' Group By name_func  ")
            versionsFuncData = versionsFunc.fetchall()
            versionsFuncDataArray = np.array(versionsFuncData)
            self.textEdit2.setText(
                "Ваш id= " + str(user_id) + "\n Функції, які працюють при вибраній вами версії: " + str(
                    versionsFuncDataArray))

    def add_1(self):
        window2.show()
        self.hide()


class Main(QMainWindow):
    def __init__(self):
        super().__init__()
        global user_id
        self.resize(385, 380)
        self.setStyleSheet("background-color: gray;")
        self.title = "First Window"
        self.setStyleSheet("QMainWindow { background-image: url(one.jpg); }")
        self.pushButton = QPushButton(self)
        self.pushButton.setText("Запуск")

        self.pushButton.setGeometry(30, 100, 150, 60)
        self.pushButton.setStyleSheet(" QPushButton {\n"
                                      "     border: 2px solid #8f8f91;\n"
                                      "      border-color: rgb(255, 255, 255);\n"
                                      "     min-width: 80px;\n"
                                      "     color: white;\n"
                                      " }\n"
                                      "\n"
                                      " QPushButton:pressed {\n"
                                      "     background-color: gray\n"
                                      " }\n"
                                      "\n"
                                      " QPushButton:flat {\n"
                                      "     border: none; /* для плоской кнопки границы нет */\n"
                                      " }\n"
                                      "\n"
                                      " QPushButton:default {\n"
                                      "     border-color: navy; /* делаем кнопку по умолчанию выпуклой */\n"
                                      " }")

        self.pushButton.setObjectName("pushButton")
        self.pushButton_2 = QPushButton("Налаштування", self)
        self.pushButton_2.setStyleSheet(" QPushButton {\n"
                                        "     border: 2px solid #8f8f91;\n"
                                        "     border-color: rgb(255, 255, 255);\n"
                                        "     min-width: 80px;\n"
                                        "     color: white;\n"
                                        " }\n"
                                        "\n"
                                        " QPushButton:pressed {\n"
                                        "     background-color: gray\n"
                                        " }\n"
                                        "\n"
                                        " QPushButton:flat {\n"
                                        "     border: none; /* для плоской кнопки границы нет */\n"
                                        " }\n"
                                        "\n"
                                        " QPushButton:default {\n"
                                        "     border-color: navy; /* делаем кнопку по умолчанию выпуклой */\n"
                                        " }")

        self.pushButton_2.setGeometry(30, 270, 150, 60)
        # 190
        self.pushButton_2.setObjectName("pushButton_2")
        self.pushButton_3 = QPushButton("Інструкція", self)
        self.pushButton_3.setGeometry(200, 100, 150, 60)
        self.pushButton_3.setStyleSheet(" QPushButton {\n"
                                        "     border: 2px solid #8f8f91;\n"
                                        "     border-color: rgb(255, 255, 255);\n"
                                        "     min-width: 80px;\n"
                                        "     color: white;\n"
                                        " }\n"
                                        "\n"
                                        " QPushButton:pressed {\n"
                                        "     background-color: gray\n"
                                        " }\n"
                                        "\n"
                                        " QPushButton:flat {\n"
                                        "     border: none; /* для плоской кнопки границы нет */\n"
                                        " }\n"
                                        "\n"
                                        " QPushButton:default {\n"
                                        "     border-color: navy; /* делаем кнопку по умолчанию выпуклой */\n"
                                        " }")

        self.pushButton_3.setObjectName("pushButton_3")
        self.pushButton_4 = QPushButton("Вихід", self)
        self.pushButton_4.setGeometry(200, 270, 150, 60)
        self.pushButton_4.setStyleSheet(" QPushButton {\n"
                                        "     border: 2px solid #8f8f91;\n"
                                        "     border-color: rgb(255, 255, 255);\n"
                                        "     min-width: 80px;\n"
                                        "     color: white;\n"
                                        " }\n"
                                        "\n"
                                        " QPushButton:pressed {\n"
                                        "     background-color: gray\n"
                                        " }\n"
                                        "\n"
                                        " QPushButton:flat {\n"
                                        "     border: none; /* для плоской кнопки границы нет */\n"
                                        " }\n"
                                        "\n"
                                        " QPushButton:default {\n"
                                        "     border-color: navy; /* делаем кнопку по умолчанию выпуклой */\n"
                                        " }")

        self.pushButton_4.setObjectName("pushButton_4")
        self.pushButton_5 = QPushButton("Гра", self)
        self.pushButton_5.setGeometry(120, 190, 150, 60)
        self.pushButton_5.setStyleSheet(" QPushButton {\n"
                                        "     border: 2px solid #8f8f91;\n"
                                        "     border-color: rgb(255, 255, 255);\n"
                                        "     min-width: 80px;\n"
                                        "     color: white;\n"
                                        " }\n"
                                        "\n"
                                        " QPushButton:pressed {\n"
                                        "     background-color: gray\n"
                                        " }\n"
                                        "\n"
                                        " QPushButton:flat {\n"
                                        "     border: none; /* для плоской кнопки границы нет */\n"
                                        " }\n"
                                        "\n"
                                        " QPushButton:default {\n"
                                        "     border-color: navy; /* делаем кнопку по умолчанию выпуклой */\n"
                                        " }")

        self.pushButton_5.setObjectName("pushButton_5")

        self.label = QLabel("gesture control", self)
        self.label.setEnabled(True)
        self.label.setGeometry(45, 10, 400, 51)
        self.label.setAutoFillBackground(False)
        self.label.setStyleSheet("color: rgb(255, 255, 255);""font: 30pt \"Blackadder ITC\";\n""")
        self.label.setScaledContents(False)
        self.label.setWordWrap(False)
        self.label.setOpenExternalLinks(False)
        self.label.setObjectName("label")
        self.inform = QLabel(" ", self)
        self.inform.setEnabled(True)
        self.inform.setGeometry(60, 340, 300, 40)
        # self.inform.setGeometry(100, 50, 300, 40)
        self.inform.setAutoFillBackground(False)
        self.inform.setScaledContents(False)
        self.inform.setWordWrap(False)
        self.inform.setOpenExternalLinks(False)
        self.inform.setObjectName("label")
        self.login = QLabel(" ", self)
        self.login.setEnabled(True)
        self.login.setGeometry(140, 50, 300, 40)
        self.login.setAutoFillBackground(False)
        self.login.setScaledContents(False)
        self.login.setWordWrap(False)
        self.login.setOpenExternalLinks(False)
        self.login.setObjectName("login")
        # херня
        # Запуск
        self.pushButton.clicked.connect(self.arduino_start)
        self.pushButton_3.clicked.connect(self.window3)
        self.pushButton_2.clicked.connect(self.window2)
        self.pushButton_4.clicked.connect(self.exit)
        self.pushButton_5.clicked.connect(self.start_game)
        self.restart()

    def restart(self):
        if keyboard.is_pressed('A'):
            print("sfsf")

    def arduino_start(self):
        global id_vers
        global func_1
        global user_id
        self.hide()
        vers_znach = sql.execute(f"Select id_version From users Where id = '{user_id}'")
        name = vers_znach.fetchone()
        print(name[0])
        if not name[0] is None:
            versionsFunc = sql.execute(
                f"Select name_func From versions_func Inner join  func ON versions_func.func_id = func.id Where version_id = '{name[0]}' Group By name_func  ")
            versionsFuncData = versionsFunc.fetchall()
            versionsFuncDataArray = np.array(versionsFuncData)
            print(versionsFuncDataArray)
            while 1:
                incoming = str(ArduinoSerial.readline())  # read the serial data and print it as line
                print(incoming)
                for i in versionsFuncDataArray:
                    singleFuncName = i[0]
                    if singleFuncName in incoming:
                        function(singleFuncName)

        else:
            msg = QMessageBox()
            msg.setIcon(QMessageBox.Critical)
            msg.setText("Error")
            msg.setInformativeText('More information')
            msg.setWindowTitle("Error")
            msg.exec_()

    def start_game(self):
        game()

    def exit(self):
        window2.close()

    def main_window(self):
        self.label = QLabel("Manager", self)
        self.label.move(286, 175)
        self.setWindowTitle(self.title)
        self.resize(800, 600)
        self.show()

    def window2(self):  # <===
        self.w = Settings()
        self.w.show()
        self.hide()

    def window3(self):
        self.w = Instruct()
        self.w.show()
        self.hide()

    def avtoriz(self):
        self.w = Avtoriz()
        self.w.show()
        self.hide()


if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = Avtoriz()
    window2 = Main()
    window3 = Settings()
    window.show()
    sys.exit(app.exec())

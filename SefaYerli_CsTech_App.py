#############################
# Python Script Owner: Sefa Yerli
# Python Version: Python3.6
# Linux OS
# Libraries: random - tkinter
#############################

import random
from tkinter import *
from tkinter import ttk
from tkinter.ttk import Progressbar

pc_created_val = 0
user_created_val = 0

digit_number = 4  # Digit number of values according to request from pdf (Calibration value)
estimation = 0


class UserInterface(object):

    def get_user_value(self, user_text: str):
        """
        To create GUI to enter value from user.
        :return:
        """
        self.getvalue = 0
        self.window = Tk()
        self.window.title("User " + str(digit_number) + " Digit Number")
        lbl = Label(self.window, text=user_text)
        lbl.grid(column=0, row=0)
        self.txt = Entry(self.window, width=10)
        self.txt.grid(column=1, row=0)
        btn = Button(self.window, text="Enter", command=self.get_user_value_clicked).grid(column=2, row=0)
        self.window.mainloop()
        return self.getvalue

    def get_user_value_clicked(self):
        """
        To do action, when user clicked 'Enter' button.
        :return: Nothing
        """
        try:
            self.getvalue = int(self.txt.get())
            getvalue_list = NumberOperation.int_to_list_convert(self.getvalue)
            diff_digit_number = len(list(set(getvalue_list)))  # Remove dublicate member and find length
            if diff_digit_number == digit_number:
                self.window.destroy()
                self.message_popup("green", "It is successful")

            else:
                self.window.destroy()
                self.warning_popup()

            return int(self.getvalue)

        except ValueError:
            self.window.destroy()
            self.warning_popup()

    def message_popup(self, colour: str, mssg_txt: str):
        """
        To show popup for succeed message.
        :return:
        """
        self.message_window = Tk()
        self.message_window.title("CsTech")
        lbl = Label(self.message_window, bg=colour, text=mssg_txt)
        lbl.grid(column=0, row=0)
        btn = Button(self.message_window, text="OK", command=self.close_popup)
        btn.grid(column=0, row=1)
        self.message_window.mainloop()

    def close_popup(self):
        """
        To close , when user clicked 'OK' button.
        :return:
        """
        self.message_window.destroy()

    def warning_popup(self):
        """
        To show popup for warning message.
        :return:
        """
        self.warn_window = Tk()
        self.warn_window.title("WARNING")
        lbl = Label(self.warn_window, bg="red", text="You entered wrong value. Please enter a " + str(digit_number) +
                                                     "-digit number with different numbers!")
        lbl.grid(column=0, row=0)
        btn = Button(self.warn_window, text="OK", command=self.warning_popup_clicked)
        btn.grid(column=0, row=1)
        self.warn_window.mainloop()

    def warning_popup_clicked(self):
        """
        To get user value interface, when user clicked 'OK' button.
        :return:
        """
        self.warn_window.destroy()
        self.get_user_value(user_value_text)

    def progress_bar(self, progress_value: int, diff_digit_progress: int, mssg_txt, mssg_txt2):
        """
        To show same digits with progress window
        :param progress_value: Progress window percent
        :return:
        """

        def close_it():
            """
            To close progress bar
            :return:
            """
            progress_window.destroy()

        progress_window = Tk()

        progress_window.title("CsTech-App")
        lbl = Label(progress_window, text=mssg_txt + str(progress_value))
        lbl.grid(column=0, row=0)

        style = ttk.Style()
        style.theme_use('default')
        style.configure("black.Horizontal.TProgressbar", background='black')

        bar = Progressbar(progress_window, length=200, style='black.Horizontal.TProgressbar')
        bar['value'] = progress_value * 25
        bar.grid(column=0, row=1)

        lbl = Label(progress_window, text=str(diff_digit_progress) + mssg_txt2)
        lbl.grid(column=0, row=2)

        s = ttk.Style()
        s.theme_use('clam')
        s.configure("red.Horizontal.TProgressbar", foreground='red', background='red')

        bar2 = Progressbar(progress_window, length=200, style='red.Horizontal.TProgressbar')
        bar2['value'] = diff_digit_progress * 25
        bar2.grid(column=0, row=3)

        btn = Button(progress_window, text="OK", command=close_it)
        btn.grid(column=0, row=4)

        progress_window.mainloop()


class NumberOperation(object):

    def __init__(self):
        self.ran_array = [None] * digit_number
        self.ran_value_pc = 0

    def number_creator(self):
        """
        To create computer's random digit_number digit value.
        :return: Random digit_number digit value
        """
        self.ran_value_pc = 0
        for count in range(digit_number, 0, -1):
            ran_number = random.randint(0, 9)
            # print(ran_number, count)
            # TODO: Delete Print command

            while count == digit_number and ran_number == 0 or ran_number in self.ran_array:
                ran_number = random.randint(0, 9)
                # print(ran_number, count)
                # TODO: Delete Print command
            self.ran_array.append(ran_number)
            self.ran_value_pc = self.ran_value_pc + ran_number * 10 ** (count-1)

        print(self.ran_value_pc)
        # TODO: Delete Print command
        return self.ran_value_pc

    @staticmethod
    def int_to_list_convert(value: int):
        """
        To create list from value with digit sequence
        :param value: Integer value (int)
        :return: Converted list value digit by digit
        """
        ret_list = []
        for number in str(value):
            ret_list.append(number)
        return ret_list

    @staticmethod
    def similarity_check(est_val: int, real_val: int):
        """
        To compare estimation value with real value.
        :param est_val: Estimation value (int)
        :param real_val: Real value (int)
        :return: Number of same digits
        """
        same_value = 0
        estval_list = NumberOperation.int_to_list_convert(est_val)
        realval_list = NumberOperation.int_to_list_convert(real_val)
        lists_intersection = list(set(estval_list).intersection(realval_list))

        for count in range(0, digit_number):

            if estval_list.pop() == realval_list.pop():
                same_value = same_value + 1

        exist_val = len(lists_intersection) - same_value

        return same_value, exist_val


class CompAlgorithm(object):
    def __init__(self):
        self.guess_matrix = []
        self.rate_list = []
        self.banned_list = []
        self.best_estimation = [0, 0]
        self.number_rate = [[0, 0], [1, 0], [2, 0], [3, 0], [4, 0], [5, 0], [6, 0], [7, 0], [8, 0], [9, 0]]
        self.tree_count = 0
        self.tree_list = []
        self.pc_est_prev = 0
        self.same_digit_num_pc_prev = 0
        self.diff_digit_number_pc_prev = 0

    def elem_exist(self, search_list: list, elem):
        """
        To search sublist elements.
        :param search_list:
        :param elem:
        :return:
        """
        element_exist = 0
        for count in range(len(search_list)):
            if str(elem) == search_list[count][1] or elem == search_list[count][1]:
                element_exist = 1

        return element_exist

    def digit_exist(self, search_list: list, digit_number):
        """
        To search sublist elements.
        :param search_list:
        :param elem:
        :return:
        """
        digit_number_exist = 0
        for count in range(len(search_list)):
            if digit_number == search_list[count][0] or str(digit_number) == search_list[count][0]:
                digit_number_exist = 1

        return digit_number_exist

    def create_newguess(self, same_digit_num, diff_digit_num, guess_val):
        """
        To create new guess according to input and old guess
        :param same_digit_num: Count of exact digit guess
        :param diff_digit_num: Count of same number with wrong digit
        :param guess_val: Last guess
        :return: New guess
        """
        guess_list = NumberOperation.int_to_list_convert(guess_val)
        self.guess_matrix.append([guess_val, same_digit_num, diff_digit_num])
        digit_number_list = []  # Digit and number store for each []
        new_est_value = 0

        if self.best_estimation[0] < (same_digit_num * 1.2 + diff_digit_num):
            self.best_estimation = [(same_digit_num * 1.2 + diff_digit_num), guess_val]
            for count in range(0, digit_number):
                self.number_rate[int(guess_list[count])][0] += 100

        if same_digit_num == 0 and diff_digit_num == 0:
            for count in range(0, digit_number):
                self.banned_list.append(guess_list.pop())

        if (self.same_digit_num_pc_prev*1.2+self.diff_digit_number_pc_prev) > (same_digit_num*1.2+diff_digit_num) and not (same_digit_num == 0 and diff_digit_num == 0):
            guess_val = self.pc_est_prev
            same_digit_num = self.same_digit_num_pc_prev
            diff_digit_num = self.diff_digit_number_pc_prev
        guess_list = NumberOperation.int_to_list_convert(guess_val)

        for count in range(0, same_digit_num):
            random_digit = random.randint(0, digit_number - 1)
            while self.digit_exist(digit_number_list, random_digit) or (guess_list[random_digit] == 0 and random_digit == 0):
                random_digit = random.randint(0, digit_number - 1)
            digit_number_list.append([random_digit, guess_list[random_digit]])

        for count in range(0, diff_digit_num):
            random_digit = random.randint(0, digit_number - 1)
            while self.digit_exist(digit_number_list, random_digit):
                random_digit = random.randint(0, digit_number - 1)

            random_number_digit = random.randint(0, digit_number - 1)
            count = 0
            while (random_number_digit == random_digit or self.elem_exist(digit_number_list, guess_list[random_number_digit]) or (guess_list[random_number_digit] == 0 and random_digit == 0)) and count < 5 :
                random_number_digit = random.randint(0, digit_number - 1)
                count = count + 1
            digit_number_list.append([random_digit, guess_list[random_number_digit]])

        for count in range(0, digit_number - same_digit_num - diff_digit_num):
            random_number = random.randint(0, 9)
            while self.elem_exist(digit_number_list, random_number) or str(random_number) in self.banned_list:
                random_number = random.randint(0, 9)

            random_digit = random.randint(0, digit_number - 1)
            while self.digit_exist(digit_number_list, random_digit) or (random_number == 0 and random_digit == 0):
                random_digit = random.randint(0, digit_number - 1)
                if random_number == 0 and random_digit == 0:
                    random_number = random.randint(0, 9)
                    while self.elem_exist(digit_number_list, random_number) or str(random_number) in self.banned_list:
                        random_number = random.randint(0, 9)
            digit_number_list.append([random_digit, random_number])

        for count in range(0, digit_number):
            new_est_value = new_est_value + 10 ** (digit_number - 1 - int(digit_number_list[count][0])) * (int(digit_number_list[count][1]))

        if new_est_value == guess_val or self.digit_exist(self.guess_matrix, new_est_value) or new_est_value < 1000:
            new_est_value = self.create_newguess(same_digit_num, diff_digit_num, guess_val)
        print("Computer Estimation: " + str(new_est_value))

        self.pc_est_prev = guess_val
        self.same_digit_num_pc_prev = same_digit_num
        self.diff_digit_number_pc_prev = diff_digit_num
        return new_est_value


if __name__ == "__main__":
    user_value_text = "Please enter a " + str(digit_number) + "-digit number with different numbers ->"
    NumOp = NumberOperation()
    GUI = UserInterface()
    Pc_alg = CompAlgorithm()

    user_created_val = GUI.get_user_value(user_value_text)

    pc_created_val = NumOp.number_creator()

    same_digit_num_pc = 0
    same_digit_num_usr = 0
    pc_est_prev = 0
    same_digit_num_pc_prev = 0
    diff_digit_number_pc_prev = 0
    pc_est = NumOp.number_creator()
    while not (same_digit_num_usr == digit_number or same_digit_num_pc == digit_number):
        estimation = estimation + 1
        user_value_text = "Please enter estimation a " + str(digit_number) + "-digit number ->"
        user_est = GUI.get_user_value(user_value_text)

        if user_est == 0:
            GUI.message_popup("Red", "Program was canceled by user.")
            break

        same_digit_num_usr, diff_digit_number = NumOp.similarity_check(user_est, pc_created_val)
        GUI.progress_bar(same_digit_num_usr, diff_digit_number, "User's matching digits: ", " digit value exist with "
                                                                                            "different digit.")

        same_digit_num_pc, diff_digit_number_pc = NumOp.similarity_check(pc_est, user_created_val)
        GUI.progress_bar(same_digit_num_pc, diff_digit_number_pc, "PC's estimation: " + str(pc_est) +  "matching "
                                                                                                       "digits: ",
                         " digit value exist with different digit.")

        if same_digit_num_pc < digit_number:
            pc_est = Pc_alg.create_newguess(same_digit_num_pc, diff_digit_number_pc, pc_est)

    if same_digit_num_usr == digit_number or same_digit_num_pc == digit_number:
        GUI.message_popup("blue", "Scoreless")
    elif same_digit_num_usr == digit_number:
        GUI.message_popup("green", "Winner is user!")
    elif same_digit_num_pc == digit_number:
        GUI.message_popup("red", "Winner is PC.")


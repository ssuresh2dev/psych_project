import argparse
import atexit
import csv
import random
from tkinter import *
from PIL import Image, ImageTk
import matplotlib
matplotlib.use("TkAgg")
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg, NavigationToolbar2TkAgg
from matplotlib.figure import Figure
from threading import Timer,Thread,Event
from os import listdir

class Timer(Thread):

    def __init__(self, event, frequency, function):
        Thread.__init__(self)
        self.stopped = event
        self.frequency = frequency
        self.function = function

    def run(self):
        while not self.stopped.wait(self.frequency):
            self.function()

class Application(Frame):
    def __init__(self, master=None):
        Frame.__init__(self, master)

        row1 = Frame(master)
        self.im_freq_label = Label(row1, text="Image Replacement Frequency").pack(padx=10, pady=10, side=LEFT)
        self.im_freq_entry = Entry(row1)
        self.im_freq_entry.pack(side=RIGHT)

        row2 = Frame(master)
        self.s_freq_label = Label(row2, text="Mouse Sample Frequency").pack(padx=10, pady=10, side=LEFT)
        self.s_freq_entry = Entry(row2)
        self.s_freq_entry.pack(side=RIGHT)

        row3 = Frame(master)
        self.im_dir_label = Label(row3, text="Image Directory Path").pack(padx=10, pady=10, side=LEFT)
        self.im_dir_entry = Entry(row3)
        self.im_dir_entry.pack(side=RIGHT)

        row4 = Frame(master)
        self.startbtn = Button(row4, text="Start", command=self.start_sampling)
        self.startbtn.pack(padx=10, pady=10, side=LEFT)
        self.stopbtn = Button(row4, text="Stop", command=self.stop_sampling)
        self.stopbtn.pack(padx=10, pady=10, side=RIGHT)

        row5 = Frame(master)
        photo = ImageTk.PhotoImage(Image.open("white.jpg").resize((200, 200)))
        self.stimulus = Label(row5, image=photo)
        self.stimulus.image = photo
        self.stimulus.pack(padx=10, pady=10, side=LEFT)

        self.graph = Figure(figsize=(3,3), dpi=130)
        a = self.graph.add_subplot(111)
        self.canvas = FigureCanvasTkAgg(self.graph, row5)
        self.canvas.get_tk_widget().pack(side=RIGHT)
        self.canvas.mpl_connect('motion_notify_event', self.on_mouse_hover)

        row1.pack()
        row2.pack()
        row3.pack()
        row4.pack()
        row5.pack()

        self.last_x = None
        self.last_y = None

        with open('measurements.csv', 'w') as csvfile:
                w = csv.writer(csvfile, delimiter=' ',
                            quotechar='|', quoting=csv.QUOTE_MINIMAL)
                w.writerow(['X Position', 'Y Position'])

        self.stopFlag = Event()
        self.thread = None

        self.imageFlag = Event()
        self.imageThread = None

        self.current_image = None

    def start_sampling(self):
        self.thread = Timer(self.stopFlag, int(self.s_freq_entry.get()), self.sample_mouse_position)
        self.thread.start()
        self.imageThread = Timer(self.imageFlag, int(self.im_freq_entry.get()), self.update_image)
        self.imageThread.start()

    def stop_sampling(self):
        self.stopFlag.set()
        self.imageFlag.set()

    def on_mouse_hover(self, event):
        self.last_x = event.xdata
        self.last_y = event.ydata

    def update_image(self):
        images = listdir(self.im_dir_entry.get())
        ind = random.randint(0, len(images) - 1)
        photo = ImageTk.PhotoImage(Image.open(self.im_dir_entry.get() + "/" + images[ind]).resize((200, 200)))
        self.stimulus.configure(image=photo)
        self.stimulus.image = photo
        self.current_image = images[ind]
        self.update()

    def sample_mouse_position(self):
        x = self.last_x
        y = self.last_y
        if x is not None and y is not None:
            with open('measurements.csv', 'a') as csvfile:
                w = csv.writer(csvfile, delimiter=' ',
                            quotechar='|', quoting=csv.QUOTE_MINIMAL)
                w.writerow([self.current_image, x, y])


if __name__ == "__main__":
    root = Tk()
    app = Application(master=root)
    app.update()
    app.mainloop()
    try:
        root.destroy()
    except:
        pass
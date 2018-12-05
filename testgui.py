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
    def __init__(self, sample_freq, image_freq, image_directory, master=None):
        Frame.__init__(self, master)
        master.geometry("1000x500")

        self.sample_freq = sample_freq
        self.image_freq = image_freq
        self.image_directory = image_directory
        fm = Frame(master)

        # Set up UI elements
        self.startbtn = Button(fm, text="Start", command=self.start_sampling)
        self.startbtn.grid(row=0, column=0)
        self.stopbtn = Button(fm, text="Stop", command=self.stop_sampling)
        self.stopbtn.grid(row=0, column=1)

        image = Image.open("white.jpg")
        photo = ImageTk.PhotoImage(image)
        self.pic = Label(fm, image=photo)
        self.pic.image = photo
        self.pic.grid(row=1, column=0)

        self.f = Figure(figsize=(3,3), dpi=130)
        a = self.f.add_subplot(111)
        self.canvas = FigureCanvasTkAgg(self.f, fm)
        self.canvas.get_tk_widget().grid(row=1, column=1)
        self.canvas.mpl_connect('motion_notify_event', self.on_mouse_hover)
        fm.pack()

        self.last_x = None
        self.last_y = None

        with open('measurements.csv', 'w') as csvfile:
                w = csv.writer(csvfile, delimiter=' ',
                            quotechar='|', quoting=csv.QUOTE_MINIMAL)
                w.writerow(['X Position', 'Y Position'])

        self.stopFlag = Event()
        self.thread = Timer(self.stopFlag, sample_freq, self.sample_mouse_position)

        self.imageFlag = Event()
        self.imageThread = Timer(self.imageFlag, image_freq, self.update_image)

        self.current_image = None

    def start_sampling(self):
        self.thread.start()
        self.imageThread.start()

    def stop_sampling(self):
        self.stopFlag.set()
        self.imageFlag.set()

    def on_mouse_hover(self, event):
        self.last_x = event.xdata
        self.last_y = event.ydata

    def update_image(self):
        images = listdir(self.image_directory)
        ind = random.randint(0, len(images) - 1)
        image = Image.open(self.image_directory + "/" + images[ind])
        photo = ImageTk.PhotoImage(image)
        self.pic.configure(image=photo)
        self.pic.image = photo
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
    parser = argparse.ArgumentParser()
    parser.add_argument('-s', '--scale')
    parser.add_argument('-v', '--verbose')
    parser.add_argument('-sf', '--sample_freq', required=True)
    parser.add_argument('-if', '--image_freq', required=True)
    parser.add_argument('-d', '--image_directory', required=True)
    args = parser.parse_args()

    root = Tk()
    app = Application(float(args.sample_freq), float(args.image_freq), args.image_directory, master=root)
    app.update()
    app.mainloop()
    try:
        root.destroy()
    except:
        pass
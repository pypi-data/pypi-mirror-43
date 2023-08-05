from __future__ import print_function
try:
    # for Python2
    import Tkinter as tk
    import Tkinter as ttk
    # notice capitalized T in Tkinter
    import Queue as qu
except ImportError:
    # for Python3
    from tkinter import *
    import tkinter.ttk as ttk
    import queue as qu

import threading as th
import time as tim
from PIL import Image, ImageTk
import numpy as np
import requests
from io import BytesIO
import tensorflow as tf
from sox_chords.util import visualize
import sounddevice as sd
import soundfile as sf
import sys


class DataThread(th.Thread):
    def __init__(self, callback):
        th.Thread.__init__(self)

        self.callback = callback
        self.weights = "/home/baudcode/Code/DeepMusic/logs/model.h5"
        print("loading model")
        self.model = tf.keras.applications.DenseNet121(include_top=True, weights=self.weights, classes=7, input_shape=(128, 128, 3))

        print("model warmup")
        self.model.predict(np.expand_dims(np.random.sample((128, 128, 3)), axis=0))
        self.LABELS = [
            "C", "D", "E", "F", "G", "A", "B"
        ]
        self.go = True
        self.device = 0
        self.device_info = sd.query_devices(self.device, 'input')
        self.sampling_rate = int(self.device_info['default_samplerate'])
        self.queue = qu.Queue()

    def predict(self, data):
        data = np.squeeze(data, axis=-1)
        print("Data: ", data.shape)
        image = visualize.get_visual_data(data, size=(12.8, 12.8), sr=self.sampling_rate, v_func=visualize.power_spectrogram, bw=False)
        print("predicting with: ", image.shape)
        outputs = np.argmax(self.model.predict(np.expand_dims(image, axis=0))[0])
        print(outputs)
        return self.LABELS[outputs], image

    def run(self):

        def callback(indata, frames, time, status):
            if status:
                print(status, file=sys.stderr)
            self.queue.put(indata.copy())

        with sd.InputStream(samplerate=self.sampling_rate, device=self.device,
                            channels=1, callback=callback):
            print('#' * 80)
            print('press Ctrl+C to stop the recording')
            print('#' * 80)

            last_time = tim.time()
            while self.go:
                data = self.queue.get()
                if (tim.time() - last_time) > .5:
                    last_time = tim.time()
                    print("predicting...")
                    label, image = self.predict(data)
                    print("callback")
                    self.callback(label, image)
        print("DataThread abort")

    def stop_thread(self):
        self.go = False


def get_tk_image(image):
    image = Image.fromarray(image)
    photo = ImageTk.PhotoImage(image)
    return photo


class App(tk.Tk):
    def __init__(self):
        tk.Tk.__init__(self)
        self.geometry('512x512')
        # trap use hitting X button rather than Quit
        self.protocol('WM_DELETE_WINDOW', self.quit_app)

        # label will display the data
        self.image = ttk.Label(self)
        self.image.tmp = get_tk_image(np.zeros((256, 256, 3), dtype=np.uint8))
        self.image["image"] = self.image.tmp

        self.label = ttk.Label(self, text='Chord: ')
        self.label.pack()
        self.image.pack(side="top", expand=True, fill="both")

        # button to stop the app
        ttk.Button(self, text='Quit', command=self.quit_app).pack()

        # to keep things thread safe data is queued for display
        self.display_queue = qu.Queue()
        # check_queue is called periodically from the mainloop
        self.after(100, self.check_queue)

        # start the data generating thread
        self.data_thread = DataThread(self.callback)
        self.data_thread.start()
        self.withdraw()

    # put new data in the queue, called by data thread
    def callback(self, text, image):
        print("putting %s with image of shape %s" % (text, image.shape))
        self.display_queue.put((text, image))

    # called to close the app
    def quit_app(self):
        # stop the thread and wait for it to die
        self.data_thread.stop_thread()
        while(self.data_thread.is_alive()):
            tim.sleep(0.1)

        # now end the app
        self.destroy()

    #periodically check the queue - called in mainloop thread
    def check_queue(self):
        try:
            text, image = self.display_queue.get_nowait()
            print("text,image")
            self.label['text'] = "Chord: %s" % text
            self.image.tmp = get_tk_image(image)
            self.image["image"] = self.image.tmp
        except qu.Empty:
            pass
        # make another check in 100 msec time
        self.after_idle(self.check_queue)


try:
    App().mainloop()
except KeyboardInterrupt as e:
    exit(0)

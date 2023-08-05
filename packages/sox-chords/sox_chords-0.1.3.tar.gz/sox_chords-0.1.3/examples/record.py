#!/usr/bin/env python2.7
from __future__ import print_function
"""Create a recording with arbitrary duration.
PySoundFile (https://github.com/bastibe/PySoundFile/) has to be installed!
"""
import argparse
import tempfile
import Queue as queue
import sys
import time as time_lib
import tensorflow as tf
import numpy as np
from tensorflow.contrib.framework.python.ops import audio_ops
from sox_chords.util import visualize
import threading
import pickle

import imageio


def data2spectrogram(waveform, brightness=100, size=[128, 128], window_size=1024, stride=64):
    waveform = tf.convert_to_tensor(waveform)
    print("waveform: ", waveform.shape)

    # Compute the spectrogram
    spectrogram = audio_ops.audio_spectrogram(
        waveform,
        window_size=window_size,
        stride=stride)

    print("spectrogram: ", spectrogram.shape)
    # Custom brightness
    mul = tf.multiply(spectrogram, brightness)

    # Normalize pixels
    min_const = tf.constant(255.)
    minimum = tf.minimum(mul, min_const)

    # Expand dims so we get the proper shape
    expand_dims = tf.expand_dims(minimum, -1)

    # Resize the spectrogram to input size of the model
    resize = tf.image.resize_bilinear(expand_dims, size)

    # Remove the trailing dimension
    squeeze = tf.squeeze(resize, 0)

    # Tensorflow spectrogram has time along y axis and frequencies along x axis
    # so we fix that
    flip = tf.image.flip_left_right(squeeze)
    transpose = tf.image.transpose_image(flip)

    # Convert image to 3 channels, it's still a grayscale image however
    grayscale = tf.image.grayscale_to_rgb(transpose)

    # Cast to uint8 and encode as png
    cast = tf.cast(grayscale, tf.uint8)

    with tf.Session() as sess:
        # Run the computation graph and save the png encoded image to a file
        image = sess.run(cast)
    return image


def int_or_str(text):
    """Helper function for argument parsing."""
    try:
        return int(text)
    except ValueError:
        return text


parser = argparse.ArgumentParser(description=__doc__)
parser.add_argument(
    '-l', '--list-devices', action='store_true',
    help='show list of audio devices and exit')
parser.add_argument(
    '-d', '--device', type=int_or_str,
    help='input device (numeric ID or substring)')
parser.add_argument(
    '-r', '--samplerate', type=int, help='sampling rate')
parser.add_argument(
    '-c', '--channels', type=int, default=1, help='number of input channels')
parser.add_argument(
    'filename', nargs='?', metavar='FILENAME',
    help='audio file to store recording to')
parser.add_argument(
    '-t', '--subtype', type=str, help='sound file subtype (e.g. "PCM_24")')
args = parser.parse_args()

try:
    import sounddevice as sd
    import soundfile as sf
    import numpy  # Make sure NumPy is loaded before it is used in the callback
    assert numpy  # avoid "imported but unused" message (W0611)

    if args.list_devices:
        print(sd.query_devices())
        parser.exit(0)

    if args.samplerate is None:
        device_info = sd.query_devices(args.device, 'input')
        # soundfile expects an int, sounddevice provides a float:
        args.samplerate = int(device_info['default_samplerate'])
    if args.filename is None:
        args.filename = tempfile.mktemp(prefix='delme_rec_unlimited_',
                                        suffix='.wav', dir='')
    q = queue.Queue()
    last_time = time_lib.time()

    weights = "/home/baudcode/Code/DeepMusic/logs/model.h5"
    print("loading model")
    # model = tf.keras.applications.DenseNet121(include_top=True, weights=weights, classes=7, input_shape=(128, 128, 3))

    print("model warmup")
    # model.predict(np.expand_dims(np.random.sample((128, 128, 3)), axis=0))

    LABELS = [
        "C", "D", "E", "F", "G", "A", "B"
    ]

    def predict(data):
        data = np.squeeze(data, axis=-1)

        last_time = time_lib.time()
        data = visualize.get_visual_data(data, size=(12.8, 12.8), sr=args.samplerate, v_func=visualize.power_spectrogram, bw=False)
        outputs = np.argmax(model.predict(np.expand_dims(data, axis=0))[0])
        print("%s" % LABELS[outputs])

    def callback(indata, frames, time, status):
        global last_time
        """This is called (from a separate thread) for each audio block."""
        print(indata.shape)
        if status:
            print(status, file=sys.stderr)
        q.put(indata.copy())

    # Make sure the file is opened before recording anything:
    # with sf.SoundFile(args.filename, mode='x', samplerate=args.samplerate,
    #                  channels=args.channels, subtype=args.subtype) as file:
    with sd.InputStream(samplerate=args.samplerate, device=args.device, blocksize=2048,
                        channels=args.channels, callback=callback):
        print('#' * 80)
        print('press Ctrl+C to stop the recording')
        print('#' * 80)
        while True:
            data = q.get()
            pickle.dump(data, open("sample.data", "wb"))
            # file.write(data)
            time_elapsed = time_lib.time() - last_time

            if time_elapsed >= 0.5:
                print("predicting")
                image = data2spectrogram(data)
                print("saving", image.shape)
                imageio.imwrite("output.png", image)
                # threading.Thread(target=predict, args=(data, )).start()

except KeyboardInterrupt:
    print('\nRecording finished: ' + repr(args.filename))
    parser.exit(0)
except Exception as e:
    parser.exit(type(e).__name__ + ': ' + str(e))

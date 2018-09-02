import os
from datetime import datetime
import requests
from requests.exceptions import RequestException

import kivy

from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.popup import Popup
from kivy.logger import Logger

from plyer import camera

def name_imgs():
    prefix = 'IMG'
    name = datetime.now().strftime("%Y%m%d_%H%M%S")
    return "{}_{}".format(prefix, name)

class CameraClient(BoxLayout):
    def __init__(self, path):
        super(CameraClient, self).__init__()
        self.cwd = path
        self.ids.path_label.text = self.cwd
        self.img = 'image.jpg'

    def do_capture(self):
        name = name_imgs()
        ext = '.jpg'
        filename = "{}{}".format(name, ext)
        filepath = os.path.join(self.cwd, filename)

        try:
            camera.take_picture(filename=filepath,
                                on_complete=self.camera_callback)
        except NotImplementedError:
            popup = MsgPopup(
                "This feature has not yet been implemented for this platform.")
            popup.open()

    def camera_callback(self, filepath):
        self.ids.msg_label.text = filepath
        self.img = filepath

    def send_image(self):
        # if self.post_image(self.img) == 0:
        #     self.ids.results_label.text = 'Results from analysis'
        # elif self.post_image(self.img) == 1:
        #     self.ids.results_label.text = "Take a picture first"
        # else:
        #     self.ids.results_label.text = "Error to establish a connection"
        self.post_image(self.img)
        self.ids.results_label.text = self.img


    def post_image(self, img_file):
        # url for testing purposes
        url = "http://localhost:5000/upload"
        img = open(img_file, 'rb')
        img = {'image': img}
        try:
            response = requests.post(url, files=img) 
            print(response.text)
        except RequestException as e:
            print("Error to establish a connection")


class CameraClientApp(App):
    def __init__(self):
        super(CameraClientApp, self).__init__()
        self.demo = None

    def build(self):
        self.cwd = os.path.join(getattr(self, 'user_data_dir'), 'DCIM')
        self.demo = CameraClient(self.cwd)
        return self.demo

    def on_pause(self):
        return True

    def on_resume(self):
        pass


class MsgPopup(Popup):
    def __init__(self, msg):
        super(MsgPopup, self).__init__()
        self.ids.message_label.text = msg


if __name__ == '__main__':
    CameraClientApp().run()

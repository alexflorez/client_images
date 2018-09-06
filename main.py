import os
from datetime import datetime
import requests
from requests.exceptions import RequestException

import kivy

from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.image import Image
from kivy.uix.popup import Popup
from kivy.logger import Logger
from kivy.properties import StringProperty

from plyer import camera

def name_imgs():
    prefix = 'IMG'
    name = datetime.now().strftime("%Y%m%d_%H%M%S")
    return "{}_{}".format(prefix, name)

class CameraClient(BoxLayout):
    source = StringProperty(None)
    def __init__(self, path):
        super(CameraClient, self).__init__()
        self.cwd = path
        self.img = ''
        self.url = ''

    def clean(self):
        self.img = ''
        self.ids.results_label.text = ''

    def do_capture(self):
        self.clean()
        name = name_imgs()
        ext = '.jpg'
        filename = "{}{}".format(name, ext)
        filepath = os.path.join(self.cwd, filename)
        try:
            camera.take_picture(filename=filepath,
                                on_complete=self.camera_callback)
        except NotImplementedError:
            # self.camera_callback('image.jpg')
            popup = MsgPopup("This feature is not implemented for this platform.")
            popup.open()

    def camera_callback(self, filepath):
        # to show the captured image
        self.source = filepath
        self.ids.image.reload()
        print(self.source)
        self.img = filepath

    def set_server(self):
        self.url = self.ids.server_ip.text
        print(self.url)

    def send_image(self):
        # if self.post_image(self.img) == 0:
        #     self.ids.results_label.text = 'Results from analysis'
        # elif self.post_image(self.img) == 1:
        #     self.ids.results_label.text = "Take a picture first"
        # else:
        #     self.ids.results_label.text = "Error to establish a connection"
        result = self.post_image()
        if result:
            self.ids.results_label.text = result

    def post_image(self):
        if self.url == '':
            popup = MsgPopup("Set server IP first")
            popup.open()
            return
        # url for testing purposes 
        url = "http://{}:5000/upload".format(self.url)
        try:
            img = open(self.img, 'rb')
            img = {'image': img}
            response = requests.post(url, files=img) 
            return response.text
        except RequestException as e:
            print("Error to establish a connection")
        except IOError as e:
            print("Could not read file")    
        

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

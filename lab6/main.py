from kivy.app import App
from kivy.lang import Builder
from kivy.uix.boxlayout import BoxLayout
from kivy.properties import StringProperty
from kivy.uix.textinput import TextInput
import socket
import threading
from kivy.clock import mainthread
from database import check_db_data, input_db_data


KV = """
MyBL:
    orientation: "vertical"
    size_hint: (0.95, 0.95)
    pos_hint: {"center_x": 0.5, "center_y": 0.5}

    Label:
        font_size: "30sp"
        text: root.data_label

    TextInput:
        id: input
        multiline: False
        padding_y: (5,5)
        size_hint: (1, 0.5)
    Button:
        text: "Submit"
        bold: True
        background_color: '#00FFCE'
        size_hint: (1,0.5)
        on_press: root.callback(input.text)

"""

class MyBL(BoxLayout):
    data_label = StringProperty("Write number")

    def __init__(self, **kwargs):
        super().__init__(**kwargs)

    def on_text(self,instance,value):
        self.on_text.text = print(self.on_text)

    def btn_press(self, instance):
        print(self.text_input.text)
    
    def get_data(self, input):
        while App.get_running_app().running:
            output = check_db_data(int(input.text))
            self.set_data_label(output)


    @mainthread
    def set_data_label(self, data):
        self.data_label = "OUTPUT:" + str(data) + "\n"

    #function after press buton
    def callback(self, input):
        output = check_db_data(int(input))
        if output == None:
            output = input_db_data(int(input))
        self.set_data_label(output)
    

class MyApp(App):
    running = True

    def build(self):
        return Builder.load_string(KV)
    
    def on_stop(self):
        self.running = False

MyApp().run()
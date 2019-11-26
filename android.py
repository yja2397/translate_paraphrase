import os
os.environ['KIVY_GL_BACKEND'] = 'sdl2'

import kivy
kivy.require('1.11.1')

from kivy.app import App
from kivy.lang import Builder
from kivy.uix.button import Button
from kivy.uix.textinput import TextInput
from kivy.uix.anchorlayout import AnchorLayout
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.recycleboxlayout import RecycleBoxLayout
from kivy.uix.label import Label
from kivy.uix.widget import Widget
from kivy.config import Config

from module import db # db
from module import user
from module import paraphrase

class MyApp(App):

    def build(self):
        Config.set('graphics', 'width', '360')
        Config.set('graphics', 'height', '640')
        self.text = TextInput(multiline=False)
        self.text.bind(on_text_validate=self.on_enter)
        self.text.text_language = "kor"
        self.text.hint_text = "Input what you want to paraphrase."
        self.text.size_hint_y = None
        self.text.height = 40
        self.text.width = 120

        self.anchor1=AnchorLayout(anchor_x='center', anchor_y='top')
        self.anchor1.orientation = 'vertical'
        self.anchor1.add_widget(self.text)
        self.anchor1.spacing = 30
        
        self.boxLayout = BoxLayout()
        self.boxLayout.add_widget(self.anchor1)

        self.anchor2 = AnchorLayout()
        
        return self.boxLayout

    def on_enter(self, instance):
        print('User pressed enter in', self.text.text)

        self.boxLayout.remove_widget(self.anchor2)

        self.trans(self.text.text)


        return 


    def trans(self, message):
        tr = paraphrase.paraphrase()
        trans = tr.manyResult(message) # paraphrase

        if len(trans) > 18:
            transL = 18
        else:
            transL = len(trans)

        result = BoxLayout()
        result.orientation = 'vertical'
        result.height=400

        if transL > 10:
            transL = 10
        
        self.anchor1.remove_widget(self.text)
        self.text.text = ''
        result.add_widget(self.text)

        for i in range(0, transL):
            button = Button(text=trans[i])
            button.height=30
            result.add_widget(button)
        
        self.anchor2.anchor_x = 'left'
        self.anchor2.anchor_y = 'bottom'
        self.anchor2.add_widget(result)
        
        self.boxLayout.remove_widget(self.anchor1)
        self.boxLayout.add_widget(self.anchor2)

        return self.boxLayout
    

if __name__ == "__main__":
    MyApp().run()
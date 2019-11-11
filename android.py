import os
os.environ['KIVY_GL_BACKEND'] = 'sdl2'

import kivy
kivy.require('1.11.1')

from kivy.app import App
from kivy.uix.button import Button
from kivy.uix.textinput import TextInput
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.label import Label
from kivy.uix.widget import Widget

from module import db # db
from module import user
from module import paraphrase

# textinput = TextInput(text='Hello world', focus=True)



class MyApp(App):

    def build(self):
        self.text = TextInput(multiline=False)
        self.text.bind(on_text_validate=self.on_enter)
        self.text.text_language = "kor"

        layout=BoxLayout()
        layout.orientation = 'horizontal'
        layout.add_widget(self.text)

        return layout

    def on_enter(self, instance):
        print('User pressed enter in', self.text.text)

        return 



    # def on_focus(self, instance, value):
    #     if value:
    #         print('User focused', instance)
    #     else:
    #         print('User defocused', instance)

    # def build(self):        
    #     textinput = TextInput()
    #     textinput.bind(focus=self.on_focus)
    #     # text = TextInput(text='Hello world')
    #     # print(text)
    #     return 
    

if __name__ == "__main__":
    MyApp().run()
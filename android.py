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

class Layout(Widget):
    pass

class MyApp(App):

    def build(self):
        Config.set('graphics', 'width', '360')
        Config.set('graphics', 'height', '640')
        # self.text = TextInput(multiline=False)
        # self.text.bind(on_text_validate=self.on_enter)
        # self.text.text_language = "kor"
        # self.text.hint_text = "Input what you want to paraphrase."
        # self.text.size_hint_y = None
        # self.text.height = 50
        # self.text.width = 120

        # button = Button()

        # anchor1=AnchorLayout(anchor_x='center', anchor_y='top')
        # anchor1.orientation = 'vertical'
        # anchor1.add_widget(self.text)
        # anchor1.spacing = 30
        
        # # anchorLayout2    = AnchorLayout()
        # # anchorLayout2.anchor_x = 'right'
        # # anchorLayout2.anchor_y = 'top'

        
        # button2 = Button(text='Top-Right', size_hint = (0.3, 0.3))

        # # anchorLayout2.add_widget(button2)

        # self.boxLayout = BoxLayout()
        # self.boxLayout.add_widget(anchor1)
        # # boxLayout.add_widget(anchorLayout2)

        # self.anchor2 = AnchorLayout()
        
        return Layout() # self.boxLayout

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
        
        # response = ""

        print(trans)

        result = BoxLayout()
        result.orientation = 'vertical'
        result.height=400

        for i in range(0, transL):
            button = Button(text=trans[i])
            result.add_widget(button)
        
        self.anchor2.anchor_x = 'left'
        self.anchor2.anchor_y = 'bottom'
        self.anchor2.add_widget(result)
        
        self.boxLayout.add_widget(self.anchor2)

        # for i in range(0,transL):

        #     response += """
        #         <div class="chat-bubble result">
        #             <span class="chat-content order{1}" onclick='speakPara({1})' title="듣기">
        #                 {0}
        #             </span>
        #             <img class="insert" src="/static/insert.png" onclick='goPara({1})'/>
        #         </div>
        #     """.format(trans[i], i)

        # response_text = {"message":  message, "result": response}

        return self.boxLayout # jsonify(response_text)


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
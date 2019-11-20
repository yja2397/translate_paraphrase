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

        self.layout=BoxLayout()
        self.layout.orientation = 'horizontal'
        self.layout.add_widget(self.text)

        return self.layout

    def on_enter(self, instance):
        print('User pressed enter in', self.text.text)

        self.trans(self.text.text)

        return 


    def trans(self, message):
        tr = paraphrase.paraphrase()
        trans = tr.manyResult(message) # paraphrase

        if len(trans) > 20:
            transL = 20
        else:
            transL = len(trans)
        
        # response = ""

        print(trans)

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

        return # jsonify(response_text)


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
import requests, json
from kivy.app import App
from kivymd.textfields import MDTextField
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.floatlayout import FloatLayout
from kivymd.theming import ThemeManager
from kivymd.list import MDList
from kivymd.list import OneLineListItem
from kivymd.label import MDLabel
from kivy.uix.scrollview import ScrollView
from kivy.clock import Clock
from threading import Thread

class mainscreen(BoxLayout):
    def __init__(self,**kwargs):
        BoxLayout.__init__(self,**kwargs)
        self.orientation='vertical'
        self.add_widget(searchbar(pos_hint={'center_x':0.5,'center_y':0.5}))
        self.list=MDList()
        self.suggestions=[]
        self.scroll=ScrollView(do_scroll_x=False)
        self.scroll.add_widget(self.list)
        for x in range(10):
            self.suggestions.append(OneLineListItem())
        self.add_widget(self.scroll)
        self.add_widget(BoxLayout())
class searchbar(MDTextField):
    def __init__(self,**kwargs):
        MDTextField.__init__(self,**kwargs)
        self.previoustext=self.text
        Clock.schedule_interval(self.textcheck,0.5)
    def textcheck(self,dt):
        if self.text!=self.previoustext:
            print 'changed'
            vt=Thread(target=self.make_suggestionlist)
            vt.start()
    def make_suggestionlist(self):
        self.list=self.parent.list
        suggestions=searchsuggestions(self.text)
        suggestions=suggestions[1]
        if suggestions!=[]:
            for x in range(10):
                y=str(suggestions[x])
                self.parent.suggestions[x].text=y
            for x in self.parent.suggestions:
                if x.text!=[]:
                    if x.parent==None:
                        self.list.add_widget(x)
        if self.text=='':
            self.parent.list.clear_widgets()

def searchsuggestions(query):
    if query=='':
        return [[],[]]
    URL = "http://suggestqueries.google.com/complete/search?client=firefox&ds=yt&q="+query
    headers = {'User-agent': 'Mozilla/5.0'}
    response = requests.get(URL, headers=headers)
    result = json.loads(response.content.decode('utf-8'))
    return result
class testapp(App):
    theme_cls=ThemeManager()
    def build(self):
        return mainscreen()

if __name__=='__main__':
    testapp().run()
from __future__ import unicode_literals

from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.floatlayout import FloatLayout
from kivy.uix.scrollview import ScrollView
from kivy.uix.image import Image
from kivy.uix.image import AsyncImage
from kivy.core.window import Window
from kivymd.list import MDList
from kivy.uix.gridlayout import GridLayout
from kivymd.theming import ThemeManager
from kivymd.toolbar import Toolbar
from kivymd.navigationdrawer import NavigationLayout
from kivymd.navigationdrawer import MDNavigationDrawer
from kivymd.textfields import MDTextField
from kivymd.button import MDRaisedButton
from kivymd.button import MDFloatingActionButton
from kivymd.card import MDCard
from kivymd.label import MDLabel
from kivymd.button import MDFlatButton
from kivymd.progressbar import MDProgressBar
from kivymd.spinner import MDSpinner
from kivymd.menu import MDDropdownMenu
from kivymd.menu import MDMenuItem
from kivy.utils import platform
from kivy.uix.screenmanager import ScreenManager,Screen
from kivymd.tabs import MDBottomNavigation,MDBottomNavigationItem
import youtube_dl
import os
import shutil
from kivymd.card import MDSeparator
from kivy.lang import Builder
from threading import Thread
import seacher
if platform=='android':
    defaultlocation="/sdcard/Download/"
elif platform=='linux':
    defaultlocation=os.getenv("HOME")+'/kivdl/'

class searcherbox(seacher.mainscreen):
    pass
class ntoolbar(Toolbar):
    def __init__(self,**kwargs):
        Toolbar.__init__(self,**kwargs)
        self.md_bg_color=App.get_running_app().theme_cls.primary_color
        self.background_palette='Primary'
        self.background_hue='500'
class mainwid(NavigationLayout):
    def __init__(self,**kwargs):
        NavigationLayout.__init__(self,**kwargs)
        self.box=newwid()
        self.bottomnav = MDBottomNavigation(size_hint_y=0.1)
        self.bottomnavmainbutton = MDBottomNavigationItem(text="Home", icon='home')
        self.bottomnavbrowserbutton = MDBottomNavigationItem(text="Browser", icon='google-earth')
        self.scrrenmngr=ScreenManager(pos_hint={'center_x':0.5,'center_y':0.5})
        self.mainscreen=Screen(name="MainScreen")
        self.browserscreen=Screen(name="BrowserScreen")
        self.nd=MDNavigationDrawer()
        self.nd.add_widget(MDRaisedButton(text='sdsdsdsd',pos_hint={'center_x':0.5,'center_y':0.5}))
        self.mainui=BoxLayout(orientation='vertical')
        self.mainui.add_widget(self.scrrenmngr)
        self.add_widget(self.nd)
        kvv='''
        
Screen:
    name: 'bottom_navigation'
    MDBottomNavigation:
        id: bottom_navigation_demo
        MDBottomNavigationItem:
            name: 'home'
            text: "Home"
            icon: "home"
            BoxLayout:
                id: main
        MDBottomNavigationItem:
            name: 'Browser'
            text: "Browser"
            icon: 'google-earth'
            BoxLayout:
                id: browser
        '''
        self.nv=Builder.load_string(kvv)
        self.nv.ids.main.add_widget(self.box)
        self.add_widget(self.nv)
        self.nv.ids.browser.add_widget(self.browserscreen)
        self.browbox=BoxLayout(orientation='vertical')
        self.browbox.add_widget(ntoolbar(title='KivDL'))
        self.brow=searcherbox()
        self.browbox.add_widget(self.brow)

        self.browserscreen.add_widget(self.browbox)

class bottomwid(BoxLayout):
    def __init__(self,**kwargs):
        self.orientation='vertical'
        BoxLayout.__init__(self,**kwargs)
        self.mainwid=mainwid()
        self.add_widget(self.mainwid)
        self.bottomnav=MDBottomNavigation(size_hint_y=0.1)
        self.bottomnavmainbutton=MDBottomNavigationItem(text="Home",icon='home', on_press=self.change_screen)
        self.bottomnavbrowserbutton=MDBottomNavigationItem(text="Browser",icon='google-earth',on_press=self.change_screen)
        self.bottomnavbrowserbutton.bind(on_release=self.change_screen)
        self.bottomnav.add_widget(self.bottomnavmainbutton)
        self.bottomnav.add_widget(self.bottomnavbrowserbutton)
        self.add_widget(self.bottomnav)
    def change_screen(self,instance):

        if instance.text=="Home":
            self.mainwid.scrrenmngr.current="MainScreen"
        elif instance.text=="Browser":
            self.mainwid.scrrenmngr.current="BrowserScreen"
        print self.mainwid.scrrenmngr.current
class newwid(GridLayout,Thread):
    def __init__(self,**kwargs):

        GridLayout.__init__(self,**kwargs)
        Thread.__init__(self)

        self.cols=1
        self.tool=ntoolbar(title='KivDL')
        self.add_widget(self.tool)
        self.body=GridLayout(cols=1,padding=(0,20))
        self.add_widget(self.body)
        self.tex = MDTextField(pos_hint={'center_y':0.9},size_hint_x=0.8)
        self.tex.hint_text=" Enter URL to download"

        self.fetch_button=MDRaisedButton(text='Fetch',pos_hint={'center_y':0,'right':0.95},size_hint_x=0.1)
        self.fetch_button.bind(on_press=self.addcard)
        self.urlget=GridLayout(cols=2,size_hint_y=0.2)
        self.urlget.add_widget(self.tex)
        self.urlget.add_widget(self.fetch_button)
        self.body.add_widget(self.urlget)

        self.cardholder=ScrollView(do_scroll_x=False,size_hint_x=0.8)
        self.cardlist=MDList(padding=(10,20))
        self.cardlist.spacing=(10,20)
        self.cardholder.add_widget(self.cardlist)

        self.body.add_widget(self.cardholder)
        self.spacer=MDLabel(size_hint_y=0.2)
        self.cardlist.add_widget(self.spacer)
    def addcard(self,instance):
        if self.tex.text!='':
            self.cardlist.remove_widget(self.spacer)
            self.cardlist.add_widget(infocard(self.tex.text))
            self.cardlist.add_widget(self.spacer)
            self.tex.text=''
class infocard(MDCard,Thread):
    def __init__(self,url,**kwargs):
        self.url=url

        MDCard.__init__(self,**kwargs)
        Thread.__init__(self)
        self.size_hint_y=None
        self.size=(100,300)
        self.body=GridLayout(cols=1,padding=(2,5))
        self.desbody=GridLayout(cols=2,size_hint_y=0.5)
        self.downloadbody=GridLayout(cols=2,size_hint_y=0.1)
        self.titlebody=GridLayout(cols=2,size_hint_y=0.1)
        self.title=MDLabel(text='VIDEO TITLE',font_style='Body2',pos_hint={'center_x':0.51,'top':1.3})
        #self.title.bind(size=self.title.setter('text_size'))
        self.thumb=AsyncImage(source='load.jpg',pos_hint={'center_x':0},size_hint=(0.2,1))
        self.descriptionscroll=ScrollView()

        self.description=MDLabel(text='Descriptions',font_style='Caption',size_hint_y=None,pos_hint={'center_x':0.5,'top':1.15})
        self.description.bind(texture_size=self.description.setter('size'))
        self.descriptionscroll.add_widget(self.description)
        self.downloadbutton=MDFloatingActionButton(icon='download',pos_hint={'right':1},disabled=True)
        self.probar=MDProgressBar(max=100,pos_hint={'center_y':0,'center_x':0.4})
        self.titlebody.add_widget(self.thumb)
        self.titlebody.add_widget(self.title)
        self.desbody.add_widget(self.descriptionscroll)
        self.downloadbody.add_widget(self.probar)
        self.downloadbody.add_widget(self.downloadbutton)
        kvp = '''
#:import MDSpinner kivymd.spinner.MDSpinner
#:import MDCheckbox kivymd.selectioncontrols.MDCheckbox


Screen:

    MDSpinner:
        id: spinner
        size_hint: None, None
        size: dp(46), dp(46)
        pos_hint: {'center_x': 0.5, 'center_y': 0.5}
        active: True 
        '''
        self.sp = Builder.load_string(kvp)
        #self.spinner=MDSpinner()
        self.add_widget(self.sp)
        #self.add_widget(self.spinner)
        self.status='fetch'
        self.meta=[]
        self.start()

    def createbody(self):
        self.thumb.source=self.meta['id']+'.jpg'
        self.thumb.reload()
        self.body.add_widget(self.titlebody)
        self.body.add_widget(self.desbody)
        self.body.add_widget(self.downloadbody)
        self.add_widget(self.body)
    def run(self):

        try:
            with youtube_dl.YoutubeDL({}) as ydl:
                y = []
                y.append(self.url)
                self.meta=ydl.extract_info(self.url,download=False)
                print self.meta
                self.title.text=self.meta['title']
                try:
                    self.description.text=self.meta['description']
                except:
                    self.description.text="NO VIDEO DESCRIPTION FOUND"
                try:
                    import urllib
                    urllib.urlretrieve(self.meta['thumbnail'],self.meta['id']+'.jpg')
                except:
                    pass
                self.status='fetched'
                self.downloadbutton.disabled=False
                self.downloadbutton.bind(on_press=self.download)
                self.remove_widget(self.sp)
                self.createbody()
                self.createmenu()
                try:
                    for x in self.meta['requested_formats']:
                        print x['format']
                except:
                    for x in self.meta['formats']:
                        print x['format']

                return 0
        except Exception as e:
            print e.message
            self.description.text='Please check url and reenter'
            self.title.text='INVALID URL'
            self.status='error fetch'
            self.clear_widgets()
            self.errorlay=FloatLayout()
            self.dismiss=MDFloatingActionButton(icon='close-circle',pos_hint={'center_x':0.5,'center_y':0.5})
            self.errortitle=(MDLabel(align='center',font_style='Title',text='Failed to Fetch',pos_hint={'center_x':0.5,'center_y':0.2}))
            self.errorlay.add_widget(self.dismiss)
            self.errorlay.add_widget(self.errortitle)
            self.add_widget(self.errorlay)
            self.dismiss.bind(on_press=self.dell)
    def dell(self,instance):
        self.parent.remove_widget(self)
    def downloadthread(self):
        self.downloadbutton.disabled=True
        with youtube_dl.YoutubeDL({'progress_hooks': [self.progressbarupdate]}) as ydl:
            ydl.download([self.url])
            return 0
    def progressbarupdate(self,d):
        try:
            percentage=(float(d['downloaded_bytes'])/d['total_bytes'])*100
        except:
            for x in d:
                print x,d[x]
            percentage=(float(d['downloaded_bytes'])/d['total_bytes_estimate'])*100
        print('updating',percentage)
        self.probar.max=100
        self.probar.value=percentage
        if d['status']=='finished':
            import os
            import shutil
            self.status='completed'
            print os.listdir('./')
            x=os.listdir('./')
            for y in x:
                if y.find('.mp4')>=0:
                    print 'moving'
                    shutil.copy('./'+y,defaultlocation+y)
                    os.remove('./'+y)

    def download(self,instance):
        self.status='download'
        self.dt=Thread(target=self.downloadthread)
        self.dt.start()

    def createmenu(self):
        items=['3gp','mp4','webm','mkv']
        self.formatbuttons={}
        self.list=MDList()
        for x in items:
            self.formatbuttons[x]=MDFlatButton(text=x)
            self.list.add_widget(self.formatbuttons[x])
        self.formatbut=dropdownmb(text='mp4')
        self.formatbut.bind(on_press=self.show_list)
        self.formatbut.pos_hint={'center_x':0.5,'center_y':0.6}
        self.controllay=FloatLayout()
        self.controllay.add_widget(self.formatbut)
        #self.desbody.add_widget(self.controllay)
    def show_list(self,instance):
        instance.parent.add_widget(self.list)
        self.list.pos=instance.pos
class dropdownmb(MDFlatButton):
    def set_text(self):
        print self.text
class mainapp(App):
    theme_cls=ThemeManager()
    def build(self):
        return mainwid()
if __name__=='__main__':
    mainapp().run()

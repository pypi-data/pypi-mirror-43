import wx
import time

from wxasync import AsyncBind, WxAsyncApp, StartCoroutine
import asyncio
from asyncio.events import get_event_loop

class MainApp(WxAsyncApp):
# class MainApp(wx.App):
    def OnInit(self):
        self.frame = wx.Frame(None, -1, "test",)
        self.frame.CreateStatusBar()
        self.frame.Show(True)
        self.InitMenus()
        return True

    def InitMenus(self):
        menuBar = wx.MenuBar()
        menu1 = wx.Menu()
        id = wx.NewIdRef()
        item = menu1.Append(id, "test - async call\tCtrl-1")

        #self.Bind(wx.EVT_MENU, self.callback, id=id)
        AsyncBind(wx.EVT_MENU, self.async_callback, self.frame, id=id)

        menuBar.Append(menu1, "&Experiments")
        self.frame.SetMenuBar(menuBar)

    async def async_callback(self, event):
        f = wx.Frame(self.frame)
        f.Show()
        AsyncBind(wx.EVT_BUTTON, self.async_callback, f)
        
        self.frame.SetStatusText("Button clicked")
        await asyncio.sleep(1)
        self.frame.SetStatusText("Working")
        await asyncio.sleep(1)
        self.frame.SetStatusText("Completed")

def main():
    application = MainApp(0)
    application.MainLoop()

def main_async():
    # see https://github.com/sirk390/wxasync
    #print ("app")
    #app = WxAsyncApp()
    #print (app)
    #print (wx.App.Get())

    application = MainApp()
    loop = get_event_loop()
    loop.run_until_complete(application.MainLoop())

if __name__ == "__main__":
    main_async()
    # main_async()

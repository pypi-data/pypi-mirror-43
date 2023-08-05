import wx
from asyncio.events import get_event_loop
import time
from wx import UpdateUIEvent, IdleEvent, EVT_BUTTON
from wx.lib.newevent import NewEvent

TestEvent, EVT_TEST_EVENT = NewEvent()

class TestFrame(wx.Frame):
    def __init__(self, parent=None):
        super(TestFrame, self).__init__(parent)

        button1 =  wx.Button(self, label="AsyncBind (original wxasync example)")
        vbox = wx.BoxSizer(wx.VERTICAL)
        vbox.Add(button1, 2, wx.EXPAND|wx.ALL)
        self.SetSizer(vbox)
        self.Layout()

        self.Bind(EVT_BUTTON, self.on_button)

        self.Bind(EVT_TEST_EVENT, self.callback)

    def on_button(self, event):
        wx.PostEvent(self, TestEvent(t1=time.time()))
        
    def callback(self, event):
        print ("Event Received")


if __name__ == '__main__':
    app = wx.App()
    frame = TestFrame()
    frame.Show()
    app.SetTopWindow(frame)
    app.MainLoop()

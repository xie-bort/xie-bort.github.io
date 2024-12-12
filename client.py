#coding:utf-8
import wx
from socket import socket,AF_INET,SOCK_STREAM
import threading
from tkinter import *
import time
from tkinter import ttk

class xbrclient(wx.Frame):
    def __init__(self,client_name):
        #调用父类的初始化方法
        #NONe：没有父级窗口
        #id表示当前窗口的一个编号
        #pos表示窗口打开的位置

        wx.Frame.__init__(self, None, id=1001,title=client_name+'的客户端',pos=wx.DefaultPosition,size=(400,450))
        #创建面板对象
        pl=wx.Panel(self)
        #在面板中放上盒子
        box=wx.BoxSizer(wx.VERTICAL)
        #可伸缩的网格布局
        fgzl=wx.FlexGridSizer(wx.HSCROLL)

        #创建俩个按钮
        conn_btn=wx.Button(pl,size=(200,40),label='连接')
        dis_btn=wx.Button(pl,size=(200,40),label='断开')
        #添加到网格布局中
        fgzl.Add(conn_btn,1,wx.TOP|wx.LEFT)
        fgzl.Add(dis_btn,1,wx.TOP|wx.RIGHT)
        #可伸缩的网格布局添加到box中
        box.Add(fgzl,1,wx.ALIGN_CENTER)

        #只读文本框（用于显示聊天内容）
        self.show_text=wx.TextCtrl(pl,size=(400,210),style=wx.TE_MULTILINE|wx.TE_READONLY)
        box.Add(self.show_text,1,wx.ALIGN_CENTER)


        #创建聊天内容的文本框
        self.chat_text=wx.TextCtrl(pl,size=(400,120),style=wx.TE_MULTILINE)
        box.Add(self.chat_text,1,wx.ALIGN_CENTER)

        #创建可伸缩网格布局
        fgz=wx.FlexGridSizer(wx.HSCROLL)  #水平方向布局
        reset_btn=wx.Button(pl,size=(200,40),label='重置')
        send_btn=wx.Button(pl,size=(200,40),label='发送')
        fgz.Add(reset_btn,1,wx.TOP|wx.LEFT)
        fgz.Add(send_btn,1,wx.TOP|wx.RIGHT)

        #将可伸缩网格布局添加到box中
        box.Add(fgz,1,wx.ALIGN_CENTER)

       #将盒子放到面板中
        pl.SetSizer(box)




        self.Bind(wx.EVT_BUTTON,self.OnConn,conn_btn)
        #实例属性的设置
        self.client_name=client_name
        self.isconnect=False #默认值为FAlse
        self.client_socket=None  #设置客户端的socket对象为空
        #给发送按钮绑定一个事件
        self.Bind(wx.EVT_BUTTON,self.send_to_server,send_btn)
        #给断开按钮绑定一个事件
        self.Bind(wx.EVT_BUTTON,self.OnDis,dis_btn)
        #给重置按钮绑定一个事件
        self.Bind(wx.EVT_BUTTON,self.reset_text,reset_btn)
    def reset_text(self,event):
        self.show_text.Clear()#文本框中的内容就没有了



    def reset_text(self,event):
        self.chat_text.Clear()
    
    def OnDis(self,event):
        #发送断开的信息
        self.socket_client.send('Y-disconnect-sj'.encode('utf-8'))
        #改变连接状态
        self.isconnect=False




    def send_to_server(self,event):
        #判断连接状态
        if self.isconnect:
            #从可写文本框获取
            input_data=self.chat_text.GetValue()
            if input_data !='':
                #发送给服务器
                self.socket_client.send(input_data.encode('utf-8'))
                #发完数据后，清空文本框
                self.chat_text.Clear()






    def OnConn(self,event):
        #如果客户端没有连接服务器，则开始连接
        if not self.isconnect:#等价于self.isconnect==FAlse
            #TCP编程的步骤
            server_host=('127.0.0.1',8888)
            #创建socket对象
            self.socket_client=socket(AF_INET,SOCK_STREAM)
            #发送连接请求
            self.socket_client.connect(server_host)
            #只要连接成功，发送一条数据
            self.socket_client.send(self.client_name.encode('utf-8'))
            #启动一个线程，客户端要与服务器的会话线程进行会话
            client_thread=threading.Thread(target=self.recv_data)
            #设置成守护线程，窗体关闭，子进程也结束
            client_thread.daemon=True
            #修改一下连接状态
            self.isconnect=True
            #启动线程
            client_thread.start()





    def recv_data(self):
        #如果是连接状态，则开始接收数据
        while self.isconnect:
            #接收来自服务器的数据
            data=self.socket_client.recv(1024).decode('utf-8')
            #显示到只读文本框中
            self.show_text.AppendText('-'*40+'\n'+data+'\n')


























if __name__=="__main__":
    #初始化app
    app=wx.App()
    st='请输入你的名字'
    root=Tk()
    entry=Entry(root)
    entry.pack()
    entry.insert(0,st)
    def name1():
        global name
        name=entry.get()
        root.destroy()
    b=ttk.Button(root,text='确定',command=name1)
    b.pack()
    root.mainloop()
    #创建自己的客户端界面对象
    client=xbrclient(name)
    client.Show()
    #循环刷新显示
    app.MainLoop()
















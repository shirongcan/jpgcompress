from PIL import Image as Img

from tkinter.filedialog import *
from tkinter.messagebox import *
from tkinter import ttk
import os
import time
import threading
#保存用户选择的文件
info = {"path":[]}
outpath = "c:/Users/shibright/Desktop/temp/output/"
root = None
#用户界面
def make_app():
    app = Tk()
    frm1 = Frame(app, name="f1",bg="black")

    # 压缩比例，压缩质量
    c1 = StringVar(value=80)
    c2 = StringVar(value=60)
    Label(frm1,text="缩放比例（%）", bg='black',fg='white').pack(expand=YES,fill=X,side=LEFT)
    Entry(frm1,name="rate", width= 5, textvariable=c1).pack(side=LEFT)
    frm1.pack(side=TOP,fill=BOTH)

    frm2 = Frame(app,name= "f2")
    Label(frm2,text="质量百分比（%）").pack(side=LEFT,fill=X, expand=YES)
    Entry(frm2,name="quality",width=5, textvariable=c2).pack(side=LEFT)
    frm2.pack(side=TOP,fill=BOTH)
   # Label(text="简单文件压缩工具").pack()
    
    # listbox 的滚动条
     
    Listbox(app, name="lbox").pack(fill=BOTH, expand=True)

    frm3 = Frame(app, name='f3')
    Button(frm3,text=" 选择文件 ", command=ui_getdata).pack({"side":"left"})
    Button(frm3,text="选择文件夹", command=getdata_from_dir).pack(side=LEFT)

   # Button(frm3, text="测试进度条",command=test_progressbar).pack(side=LEFT)
    Button(frm3,text="  压缩  ", width=10, command=compress, bg="#b7b719", fg="white").pack({"side":"right"})

    frm3.pack(side=TOP,fill=BOTH)
   # app.geometry("400x500")
    
    # 加一个进度条 要使用线程，才能更新progressbar
    ttk.Progressbar(app, name='pbar', length=300, mode="determinate", orient=HORIZONTAL)
    return app


def test_progressbar():
    b1=app.children['pbar']
    b1.place(anchor=CENTER, x=200, y=260)
    
    b1['maximum']=100
    b1['value'] =0 
    for i in range(100):
        b1['value']=i+1
        app.update()
        time.sleep(0.1)  
    b1.place_forget()
    

def getdata_from_dir():
    f_dir = askdirectory()
    all_files=[]
    l1 = app.children['lbox']
    
    if f_dir:
        for f in os.listdir(f_dir):
            # 判断后缀是否为jpg
            f_ext = os.path.splitext(f)[-1]
            if (f_ext.upper() == ".JPG") :
                all_files.append(f_dir+"/"+f)
        
        info["path"]=all_files

        l1.delete(0,END)
        for f in all_files:
            l1.insert(END,f.split("/")[-1])


def ui_getdata():
    #选择JPEG文件
    f_names = askopenfilenames(filetypes=[('JPG 文件', "*.JPG")])
    info["path"] = f_names
    if info['path']:
        l1 = app.children['lbox']

        #清空列表里面的旧的文件名
        l1.delete(0,END)
        for f in f_names:
            l1.insert(END,f.split("/")[-1])

def compress():
    #用户选择输出目录
    p_name = askdirectory()
    # 压缩质量
    try:
        q1 = (app.children['f2']).children['quality']
        v1 = int(q1.get().strip())
        # 缩放比例
        r1 =int((app.children['f1']).children['rate'].get().strip()) / 100
    except:
        showinfo(message="压缩比例和缩放大小必须为数字！")
        return
    # 进度条
    mypbar = app.children['pbar']
    
    if p_name:
        mypbar.place(anchor=CENTER, x=200, y=260)
        mypbar['maximum'] = len(info['path'])
        mypbar['value'] = 0
        i = 0
        for f_path in info['path']:
                image = Img.open(f_path)
                #原始的exif 信息 二进制
                raw_exif = image.info['exif']
                #原图片的宽，高
                w = image.size[0]
                h = image.size[1]
                 
                image.thumbnail((w*r1,h*r1))
                
                image.save(os.path.join(p_name, "c_"+f_path.split("/")[-1]), quality=v1,exif=raw_exif)
                i = i + 1
                mypbar['value'] = i
                app.update()  #刷新界面显示
                #time.sleep(0.1)
                #考虑显示一下进度条。
        mypbar.place_forget()
        showinfo(message="图片全部压缩成功！")
    #完成后给个messagebox

if __name__ == '__main__':

    app = make_app()
    root = app
    xloc = (root.winfo_screenwidth()-400)/2
    yloc = (root.winfo_screenheight()-500)/2
    yloc = int(yloc)
    xloc=int(xloc)
    root.geometry("400x500-%s-%s" % (xloc,yloc))
    app.title("简单文件压缩工具")
    app.mainloop()
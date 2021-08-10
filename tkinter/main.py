import tkinter as tk
from tkinter.constants import ACTIVE, DISABLED, LEFT, NORMAL
import tkinter.font as tkFont
import requests
import bs4
import json
import demjson
import urllib
import os
import pathlib
import threading
from time import sleep


def isfloat(value):
  try:
    float(value)
    return True
  except ValueError:
    return False
try:
    path = str(pathlib.Path(__file__).resolve().parent)
except:
    import sys
    path = str(pathlib.Path(sys.argv[0]).resolve().parent)


bg_color = '#242526'
font_color = '#b0b0b0'
br_color = '#242424'



class App:
    def __init__(self, root):
        #setting title
        root.title("animefox.io downloader")
        #setting window size
        width=354
        height=533
        screenwidth = root.winfo_screenwidth()
        screenheight = root.winfo_screenheight()
        alignstr = '%dx%d+%d+%d' % (width, height, (screenwidth - width) / 2, (screenheight - height) / 2)
        root.geometry(alignstr)
        root.resizable(width=False, height=False)
        root.configure(bg=bg_color)
        self.title_label=tk.Label(root)
        ft = tkFont.Font(family='Times',size=15)
        self.title_label["font"] = ft
        self.title_label["fg"] = font_color
        self.title_label["bg"] = bg_color
        self.title_label["justify"] = "center"
        self.title_label["text"] = "animefox.io downloader"
        self.title_label.place(x=70,y=10,width=215,height=35)

        self.link_entry=tk.Entry(root)
        self.link_entry["borderwidth"] = "1px"
        ft = tkFont.Font(family='Times',size=10)
        self.link_entry["font"] = ft
        self.link_entry["fg"] = font_color
        self.link_entry["bg"] = bg_color
        self.link_entry["justify"] = "center"
        self.link_entry["text"] = ""
        self.link_entry.place(x=150,y=70,width=162,height=30)

        GLabel_279=tk.Label(root)
        ft = tkFont.Font(family='Times',size=10)
        GLabel_279["font"] = ft
        GLabel_279["fg"] = font_color
        GLabel_279["bg"] =  bg_color
        GLabel_279["justify"] = "center"
        GLabel_279["text"] = "Series link:"
        GLabel_279.place(x=60,y=70,width=70,height=25)

        GLabel_199=tk.Label(root)
        ft = tkFont.Font(family='Times',size=10)
        GLabel_199["font"] = ft
        GLabel_199["fg"] = font_color
        GLabel_199["bg"] = bg_color
        GLabel_199["justify"] = "center"
        GLabel_199["text"] = "Download epidodes:"
        GLabel_199.place(x=20,y=140,width=130,height=30)

        GLabel_335=tk.Label(root)
        ft = tkFont.Font(family='Times',size=10)
        GLabel_335["font"] = ft
        GLabel_335["fg"] = font_color
        GLabel_335["bg"] = bg_color
        GLabel_335["justify"] = "center"
        GLabel_335["text"] = "-"
        GLabel_335.place(x=200,y=140,width=70,height=25)

        self.from_entry=tk.Entry(root)
        self.from_entry["borderwidth"] = "1px"
        ft = tkFont.Font(family='Times',size=10)
        self.from_entry["font"] = ft
        self.from_entry["fg"] = font_color
        self.from_entry["bg"] = bg_color
        self.from_entry["justify"] = "center"
        self.from_entry["text"] = ""
        self.from_entry.place(x=150,y=140,width=70,height=25)

        self.to_entry=tk.Entry(root)
        self.to_entry["borderwidth"] = "1px"
        ft = tkFont.Font(family='Times',size=10)
        self.to_entry["font"] = ft
        self.to_entry["fg"] = font_color
        self.to_entry["bg"] = bg_color
        self.to_entry["justify"] = "center"
        self.to_entry["text"] = ""
        self.to_entry.place(x=250,y=140,width=70,height=25)

        self.start_button=tk.Button(root)
        self.start_button["bg"] = bg_color
        ft = tkFont.Font(family='Times',size=10)
        self.start_button["font"] = ft
        self.start_button["fg"] = font_color
        self.start_button["justify"] = "center"
        self.start_button["text"] = "Start Download"
        self.start_button["state"] = NORMAL
        self.start_button.place(x=70,y=190,width=216,height=47)
        

        self.output_box=tk.Label(root, anchor="nw", justify=LEFT)
        self.output_box["borderwidth"] = "1px"
        ft = tkFont.Font(family='Times',size=10)
        self.output_box["font"] = ft
        self.output_box["fg"] = font_color
        self.output_box["bg"] = bg_color
        self.output_box.config(highlightbackground=br_color)
        self.output_box.place(x=20,y=270,width=228,height=233)

        self.pause_button=tk.Button(root, highlightthickness=2)
        self.pause_button["fg"] = font_color
        self.pause_button["bg"] = bg_color
        ft = tkFont.Font(family='Times',size=10)
        self.pause_button.config(highlightbackground=br_color)
        self.pause_button["font"] = ft
        self.pause_button["justify"] = "center"
        self.pause_button["text"] = "Pause"
        self.pause_button["state"] = DISABLED
        self.pause_button.place(x=250,y=270,width=76,height=97)
        

        self.stop_button=tk.Button(root, highlightthickness=2)
        self.stop_button["bg"] = bg_color
        ft = tkFont.Font(family='Times',size=10)
        self.stop_button.config(highlightbackground=br_color)
        self.stop_button["font"] = ft
        self.stop_button["fg"] = font_color
        self.stop_button["justify"] = "center"
        self.stop_button["text"] = "Stop"
        self.stop_button["state"] = DISABLED
        self.stop_button.place(x=250,y=370,width=75,height=133)
        
        self.start_button["command"] = self.start
        self.stop_button["command"] = self.stop
        self.pause_button["command"] = self.pause


        self.paused = False
        self.started = False

        

    def start(self):
        self.link = self.link_entry.get()
        self.from_ep = self.from_entry.get()
        self.to_ep = self.to_entry.get()
        if 'animefox.io/anime/' not in self.link:
            self.output_box["text"] = self.output_box["text"] + '\nIvalid link'
        elif self.link == '' or self.from_ep == '' or self.to_ep == '':
            self.output_box["text"] = self.output_box["text"] + '\nNone of upper entries can be empty'
        elif self.from_ep>self.to_ep:
            self.output_box["text"] = self.output_box["text"] + '\nFirst episode to download\nhas to be larger number than the last one'
        elif self.paused:
            self.output_box["text"] = self.output_box["text"] + '\nResuming'
            self.paused = False
            self.start_button["state"] = DISABLED
            self.stop_button["state"] = NORMAL
            self.pause_button["state"] = NORMAL
            self.start()
        else:
            self.start_button["state"] = DISABLED
            self.stop_button["state"] = NORMAL
            self.pause_button["state"] = NORMAL
            self.started = True
            new_thread = threading.Thread(target=self._start, daemon=True)
            # Start the thread
            new_thread.start()
            # continue code or run this:
            while new_thread.is_alive():
                self.title_label.update()
                sleep(0.1)
            self.output_box["text"] = self.output_box["text"] + '\nDone!'
            self.start_button["state"] = NORMAL
            self.stop_button["state"] = DISABLED
            self.pause_button["state"] = DISABLED
    def _start(self):
            
            name = self.link.split('/')[-1]
            if isfloat(name):
                name = self.link.split('/')[-2]
            video_link = 'https://embed.animefox.io/player/' + name + '/'

            n = 1
            for i in range(int(self.from_ep), int(self.to_ep) + 1):
                download_link = video_link + str(i)
                response = requests.get(download_link)
                soup = bs4.BeautifulSoup(response.text, features="html.parser")
                links = str(soup.find("script", {"type": "text/javascript"}))
                
                while links.startswith('playlist') == False:
                    links = links[1:]    
                links = links[10:]  

                while links.endswith(']') == False:
                    links = links[:-1]
                
                json_dumps = json.dumps(links)
                
                json_loads = json.loads(json_dumps)
                
                list = json_loads.strip('][').split(', ')
                
                dict = demjson.decode(list[0])


                for i in dict['sources']:
                    if i['label'] == "High Speed":
                            final_link = i['file']
                            

                if os.path.isdir(path + '\\output\\' + name) == False:
                    os.mkdir(path + '\\output\\' + name)

                n += 1
                while self.paused:
                    o = 0
                    sleep(0.1)
                if self.started == 0:
                    break
                
                urllib.request.urlretrieve(str(final_link), path + '\\output\\' + name + '\\' + name + '_' + str(n) + '.mp4')
                
                
                n += 1
                while self.paused:
                    o = 0
                    sleep(0.1)
                if self.started == 0:
                    break
            
    def stop(self):
        self.started = False
        self.paused = False
        self.start_button["state"] = NORMAL
        self.stop_button["state"] = DISABLED
        self.pause_button["state"] = DISABLED
        self.output_box["text"] = self.output_box["text"] + '\nStopped.'


    def pause(self):
        self.paused = True
        self.start_button["state"] = NORMAL
        self.stop_button["state"] = NORMAL
        self.pause_button["state"] = DISABLED
        self.output_box["text"] = self.output_box["text"] + '\nPaused'
        


        
root = tk.Tk()
app = App(root)
root.mainloop()

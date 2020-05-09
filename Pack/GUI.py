# -*- coding: utf-8 -*-
"""
Created on Mon Apr 20 17:34:37 2020

@author: George
"""

import os
import tkinter as tk
from tkinter import messagebox

if os.getcwd() != os.path.dirname(os.path.abspath(__file__)):
    import get_albums
    import add_spotify

else:
    import Pack.get_albums as get_albums
    import Pack.add_spotify as add_spotify

num_rows = 6
num_cols = 1
row_min = 100
frame_bg = '#3DC461'

month = '2020-05'
page = 'https://downbeat.com/reviews/editorspicks/'


class Header:
    height = 3
    width = 35
    fg = '#3DC461'
    bg = '#000000'
    pady = 30
    padx = 80
    
    font = ("Bahnschrift SemiLight", 20, 'bold')
    


class SmallHeader(Header):
    bg = Header.fg
    fg = Header.bg
    
    font = ("Bahnschrift SemiLight", 16, 'bold') 
    
class Body(SmallHeader):
    ipadx = 50
    ipady = 50
    
    font = ("Bahnschrift SemiLight", 8) 
    
class BodyBold(Body):
    font = ("Bahnschrift SemiLight", 12, 'bold') 

    
class Button:
    fg = '#3DC461'
    bg = '#000000'
    
    font = ("Bahnschrift SemiLight", 16) 
    
class Checkbox:
    bg = '#3DC461'
    

class AdderApp(tk.Tk):
    
    def __init__(self, *args, **kwargs):
        
        tk.Tk.__init__(self, *args, **kwargs)       
        
        tk.Tk.wm_title(self, "Monthly Spotify Albums")
        
        container = tk.Frame(self)
        container.grid(sticky = 'nsew')
        container.grid_rowconfigure(0, weight = 1)
        container.grid_columnconfigure(0, weight = 1)
        
        self.frames = {}
        
        for F in (OpenPage,):         
            frame = F(container, self)
            self.frames[F] = frame             
            frame.grid(row=0, column = 0, sticky = 'nsew')
            
            self.rowconfigure(0, weight = 1)
            self.columnconfigure(0, weight = 1)
            

        self.show_frame(OpenPage)
        
    def show_frame(self, cont):
        
        frame = self.frames[cont]
        frame.tkraise()
        frame.event_generate("<<ShowFrame>>")
        
        
class OpenPage(tk.Frame):

    def __init__(self, parent, controller):                
       
        tk.Frame.__init__(self, parent, bg = frame_bg)
        
        for i in range(num_rows):                 
            self.rowconfigure(i, minsize=row_min, weight = 1) 
            
        
        for i in range(num_cols):
            self.columnconfigure(i, weight = 1) 
        
        header = tk.Label(self, text='Monthly Spotify Albums', 
                          bg=Header.bg, fg=Header.fg, font=Header.font)
        header.grid(row=1, padx=Header.padx, pady=Header.pady)
        header.config(height=Header.height, width=Header.width)
        
        header2 = tk.Label(self, text = "This month's top albums:",
                           bg=SmallHeader.bg, fg=SmallHeader.fg,
                           font=SmallHeader.font)
        
        header2.grid()
        
        body = tk.Label(self,
                        bg=SmallHeader.bg,
                        borderwidth=4, relief="solid",
                        font=Body.font)
        body.grid()

        self.check_dict = {}
        
        self.entries = self.retrieve_entries()

        for cat in enumerate(('Artist', 'Album', 'Genres')):     
            descriptor = tk.Label(body, text = cat[1],
                                bg=Body.bg, fg=Body.fg, font=BodyBold.font)
            descriptor.grid(row=0, column=cat[0], sticky='w')
            descriptor.config(anchor='w', )
            
        checkall = tk.Button(body, bg=Button.bg, fg=Button.fg,
                             command=self.check_all, text='Check All')                        
        
        checkall.grid(row=0, column=3)
        checkall.config(padx=10, width=10)
            
        self.cbs = []
        

        
        
        
        
        for entry in enumerate(self.entries, start=1):
            
            item1 = tk.Label(body, text = entry[1].artist,
                            bg=Body.bg, fg=Body.fg, font=Body.font)
            item1.grid(row=entry[0], column=0, sticky='w')
            item1.config(anchor='w', )
            
            item2 = tk.Label(body, text = entry[1].album,
                            bg=Body.bg, fg=Body.fg, font=Body.font)
            item2.grid(row=entry[0], column=1, sticky='w')
            item2.config(anchor='w', )
            
            item1 = tk.Label(body, text = entry[1].genres,
                            bg=Body.bg, fg=Body.fg, font=Body.font)
            item1.grid(row=entry[0], column=2, sticky='w')
            item1.config(anchor='w', )
            
            checkboxvar = tk.IntVar()          
            checkboxvar.set(1)
            
            self.check_dict[entry[1]] = checkboxvar
            
            
            checkbox = tk.Checkbutton(body, bg=Checkbox.bg, 
                                      variable=checkboxvar, 
                                      onvalue=1, offvalue=0)
            checkbox.grid(row=entry[0], column=3)
            checkbox.config(anchor='e', padx=10, width=10)
            
            self.cbs.append((checkbox, checkboxvar))
            
            
        
        button = tk.Button(self, text = 'Add albums',
                           bg=Button.bg, fg=Button.fg,
                           font=Button.font,
                           command=self.check_vals)
        button.grid()
            

    def retrieve_entries(self) :
        entries = get_albums.find_albums(page, month)
        entries = add_spotify.apply_extend(entries)
        
        return entries

        
    def check_vals(self):
        
        message = ''
        
        for k, v in self.check_dict.items():
            if v.get():
                try:
                    self.process_line(k)
                except (add_spotify.ArtistError, add_spotify.AlbumError) as ex:
                    message += (str(ex) + '\n') 
        
        if message:
            messagebox.showinfo('Warning', message)
            
    def process_line(self, line):
        
        track_ids = add_spotify.execute_search(line.artist, line.album)
        add_spotify.add_to_playlist(track_ids)
        
    def check_all(self):
        for cb in self.cbs:
            if not cb[1].get():
                for cb in self.cbs:
                    cb[0].select()
                break
        else:
            for cb in self.cbs:
                cb[0].deselect()
        

app = AdderApp()
width  = int(app.winfo_screenwidth()/1.6)
height = int(app.winfo_screenheight()/1.1)
w = app.winfo_reqwidth()
h = app.winfo_reqheight()

x = int((width/4) - (w))
y = int((height/4) - (h))

app.geometry(f'{width}x{height}+{x}+{y}')

app.mainloop()


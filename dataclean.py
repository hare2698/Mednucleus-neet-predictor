import pandas as pd #line:1
import tkinter as tk #line:2
from tkinter import filedialog ,messagebox #line:3
from tkinter import ttk #line:4
class CSVCleanerApp :#line:6
    def __init__ (O0OOO0O000O000O0O ,OO0O0000O0000O0O0 ):#line:7
        O0OOO0O000O000O0O .root =OO0O0000O0000O0O0 #line:8
        O0OOO0O000O000O0O .root .title ("CSV Cleaner | Haries Palaniappan")#line:9
        O0OOO0O000O000O0O .df =None #line:10
        O0OOO0O000O000O0O .style =ttk .Style ()#line:13
        O0OOO0O000O000O0O .style .theme_use ("clam")#line:14
        O0OOO0O000O000O0O .style .configure ("TButton",padding =6 ,relief ="flat",background ="#2E8B57",foreground ="white",font =('Arial',12 ))#line:17
        O0OOO0O000O000O0O .style .map ("TButton",background =[('active','#3CB371')])#line:18
        O0OOO0O000O000O0O .style .configure ("TCheckbutton",font =('Arial',11 ))#line:20
        O0OOO0O000O000O0O .create_widgets ()#line:23
    def create_widgets (O00OO0O0000OOOO0O ):#line:25
        OO000OOOO0O0OOO00 =ttk .Frame (O00OO0O0000OOOO0O .root ,padding ="10")#line:27
        OO000OOOO0O0OOO00 .pack (pady =10 )#line:28
        O00OO0O0000OOOO0O .load_button =ttk .Button (OO000OOOO0O0OOO00 ,text ="Load CSV",command =O00OO0O0000OOOO0O .load_csv )#line:31
        O00OO0O0000OOOO0O .load_button .grid (row =0 ,column =0 ,padx =5 ,pady =5 )#line:32
        O00OO0O0000OOOO0O .save_button =ttk .Button (OO000OOOO0O0OOO00 ,text ="Save CSV",command =O00OO0O0000OOOO0O .save_csv )#line:35
        O00OO0O0000OOOO0O .save_button .grid (row =0 ,column =1 ,padx =5 ,pady =5 )#line:36
        OO00O0O00OOO0O0OO =ttk .Frame (O00OO0O0000OOOO0O .root ,padding ="10")#line:39
        OO00O0O00OOO0O0OO .pack (pady =10 )#line:40
        O00OO0O0000OOOO0O .remove_duplicates_var =tk .BooleanVar ()#line:43
        O00OO0O0000OOOO0O .trim_whitespace_var =tk .BooleanVar ()#line:44
        O00OO0O0000OOOO0O .remove_symbols_var =tk .BooleanVar ()#line:45
        O00OO0O0000OOOO0O .remove_duplicates_check =ttk .Checkbutton (OO00O0O00OOO0O0OO ,text ="Remove Duplicates",variable =O00OO0O0000OOOO0O .remove_duplicates_var )#line:47
        O00OO0O0000OOOO0O .remove_duplicates_check .grid (row =0 ,column =0 ,sticky =tk .W ,padx =5 ,pady =5 )#line:48
        O00OO0O0000OOOO0O .trim_whitespace_check =ttk .Checkbutton (OO00O0O00OOO0O0OO ,text ="Trim Whitespace",variable =O00OO0O0000OOOO0O .trim_whitespace_var )#line:50
        O00OO0O0000OOOO0O .trim_whitespace_check .grid (row =1 ,column =0 ,sticky =tk .W ,padx =5 ,pady =5 )#line:51
        O00OO0O0000OOOO0O .remove_symbols_check =ttk .Checkbutton (OO00O0O00OOO0O0OO ,text ="Remove ₹, *, and ,",variable =O00OO0O0000OOOO0O .remove_symbols_var )#line:53
        O00OO0O0000OOOO0O .remove_symbols_check .grid (row =2 ,column =0 ,sticky =tk .W ,padx =5 ,pady =5 )#line:54
        O00OO0O0000OOOO0O .clean_button =ttk .Button (O00OO0O0000OOOO0O .root ,text ="Automatic Clean",command =O00OO0O0000OOOO0O .automatic_clean )#line:57
        O00OO0O0000OOOO0O .clean_button .pack (pady =10 )#line:58
        OO00O00O0OO0OOO0O =ttk .Frame (O00OO0O0000OOOO0O .root ,padding ="10")#line:61
        OO00O00O0OO0OOO0O .pack (pady =10 )#line:62
        O00OO0O0000OOOO0O .preview_text =tk .Text (OO00O00O0OO0OOO0O ,height =15 ,width =80 ,wrap =tk .NONE )#line:65
        O00OO0O0000OOOO0O .preview_text .grid (row =0 ,column =0 ,sticky =tk .W )#line:66
        O00O0000OO000OO0O =ttk .Scrollbar (OO00O00O0OO0OOO0O ,orient =tk .VERTICAL ,command =O00OO0O0000OOOO0O .preview_text .yview )#line:69
        O00O0000OO000OO0O .grid (row =0 ,column =1 ,sticky =tk .N +tk .S )#line:70
        OO00O00OO0OO0OOOO =ttk .Scrollbar (OO00O00O0OO0OOO0O ,orient =tk .HORIZONTAL ,command =O00OO0O0000OOOO0O .preview_text .xview )#line:72
        OO00O00OO0OO0OOOO .grid (row =1 ,column =0 ,sticky =tk .E +tk .W )#line:73
        O00OO0O0000OOOO0O .preview_text .config (yscrollcommand =O00O0000OO000OO0O .set ,xscrollcommand =OO00O00OO0OO0OOOO .set )#line:75
    def load_csv (OOO0O0O0000000OOO ):#line:77
        O000OOO0O0O0O00OO =filedialog .askopenfilename (filetypes =[("CSV Files","*.csv")])#line:78
        if O000OOO0O0O0O00OO :#line:79
            OOO0O0O0000000OOO .df =pd .read_csv (O000OOO0O0O0O00OO )#line:80
            OOO0O0O0000000OOO .show_preview ()#line:81
    def save_csv (OOOO0O00000O0OOOO ):#line:83
        if OOOO0O00000O0OOOO .df is not None :#line:84
            O0OO0O00OOO0OOOO0 =filedialog .asksaveasfilename (defaultextension =".csv",filetypes =[("CSV Files","*.csv")])#line:85
            if O0OO0O00OOO0OOOO0 :#line:86
                OOOO0O00000O0OOOO .df .to_csv (O0OO0O00OOO0OOOO0 ,index =False )#line:87
                messagebox .showinfo ("Info","File saved successfully!")#line:88
        else :#line:89
            messagebox .showwarning ("Warning","Please load a CSV file first!")#line:90
    def automatic_clean (O0OO00000OOO00OOO ):#line:92
        if O0OO00000OOO00OOO .df is not None :#line:93
            if O0OO00000OOO00OOO .remove_duplicates_var .get ():#line:95
                O0OO00000OOO00OOO .df .drop_duplicates (inplace =True )#line:96
            if O0OO00000OOO00OOO .trim_whitespace_var .get ():#line:98
                O0OO00000OOO00OOO .df =O0OO00000OOO00OOO .df .applymap (lambda O0O00OOO0000OOO00 :O0O00OOO0000OOO00 .strip ()if isinstance (O0O00OOO0000OOO00 ,str )else O0O00OOO0000OOO00 )#line:99
            if O0OO00000OOO00OOO .remove_symbols_var .get ():#line:101
                O0OO00000OOO00OOO .df .replace ({r'[₹,*,]':''},regex =True ,inplace =True )#line:102
            O0OO00000OOO00OOO .df .columns =pd .Index ([f"{OO000000OO0O0OOOO}_{OOO000OOO0O0OOOOO}"if O0OO00000OOO00OOO .df .columns .duplicated ()[OOO000OOO0O0OOOOO ]else OO000000OO0O0OOOO for OOO000OOO0O0OOOOO ,OO000000OO0O0OOOO in enumerate (O0OO00000OOO00OOO .df .columns )])#line:105
            O0OO00000OOO00OOO .df =O0OO00000OOO00OOO .df .applymap (lambda OO0OO00O00OOO0O00 :int (OO0OO00O00OOO0O00 )if isinstance (OO0OO00O00OOO0O00 ,str )and OO0OO00O00OOO0O00 .isdigit ()else OO0OO00O00OOO0O00 )#line:108
            O0OO00000OOO00OOO .show_preview ()#line:110
            messagebox .showinfo ("Info","Automatic Cleaning Done!")#line:111
        else :#line:112
            messagebox .showwarning ("Warning","Please load a CSV file first!")#line:113
    def show_preview (O00O0OOOO000O000O ):#line:115
        if O00O0OOOO000O000O .df is not None :#line:116
            O00O0OOOO000O000O .preview_text .delete (1.0 ,tk .END )#line:117
            O00O0OOOO000O000O .preview_text .insert (tk .END ,O00O0OOOO000O000O .df .head ().to_string (index =False ))#line:118
if __name__ =="__main__":#line:120
    root =tk .Tk ()#line:121
    app =CSVCleanerApp (root )#line:122
    root .mainloop ()#line:123

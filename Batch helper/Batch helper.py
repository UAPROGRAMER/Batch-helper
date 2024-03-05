#importing required packages and libraries

import re
from tkinter import *
from tkinter.ttk import *
from datetime import datetime
from tkinter import messagebox
from tkinter import filedialog,simpledialog
from tkinter.scrolledtext import ScrolledText

#the root widget
root = Tk()
root.title('Batch helper')
root.iconbitmap("Batch helper.ico")
root.resizable(0, 0)
#creating scrollable notepad window
notepad = ScrolledText(root, width = 60, height = 40)
fileName = ' '
is_echo_off = False
set_int_check = False
set_input_check = False

#defining functions for commands
def cmdNew(event):     #file menu New option
    global fileName
    if len(notepad.get('1.0', END+'-1c'))>0:
        if messagebox.askyesno("Notepad", "Do you want to save changes?"):
            cmdSave()
        else:
            notepad.delete(0.0, END)
    root.title("Notepad")
def cmdOpen(event):     #file menu Open option
    fd = filedialog.askopenfile(parent = root, mode = 'r')
    t = fd.read()     #t is the text read through filedialog
    notepad.delete(0.0, END)
    notepad.insert(0.0, t)
    
def cmdSave(event):     #file menu Save option
    fd = filedialog.asksaveasfile(mode = 'w', defaultextension = '.bat')
    if fd!= None:
        data = notepad.get('1.0', END)
    try:
        fd.write(data)
    except:
        messagebox.showerror(title="Error", message = "Not able to save file!")
     
def cmdSaveAs(event):     #file menu Save As option
    fd = filedialog.asksaveasfile(mode='w', defaultextension = '.bat')
    t = notepad.get(0.0, END)     #t stands for the text gotten from notepad
    try:
        fd.write(t.rstrip())
    except:
        messagebox.showerror(title="Error", message = "Not able to save file!")
def cmdExit():     #file menu Exit option
    if messagebox.askyesno("Notepad", "Are you sure you want to exit?"):
        root.destroy()
def cmdCut():     #edit menu Cut option
    notepad.event_generate("<<Cut>>")

def cmdCopy():     #edit menu Copy option
    notepad.event_generate("<<Copy>>")
def cmdPaste():     #edit menu Paste option
    notepad.event_generate("<<Paste>>")
def cmdClear():     #edit menu Clear option
    notepad.event_generate("<<Clear>>")
       
def cmdFind():     #edit menu Find option
    notepad.tag_remove("Found",'1.0', END)
    find = simpledialog.askstring("Find", "Find what:")
    if find:
        idx = '1.0'     #idx stands for index
    while 1:
        idx = notepad.search(find, idx, nocase = 1, stopindex = END)
        if not idx:
            break
        lastidx = '%s+%dc' %(idx, len(find))
        notepad.tag_add('Found', idx, lastidx)
        idx = lastidx
    notepad.tag_config('Found', foreground = 'white', background = 'blue')
    notepad.bind("<1>", click)
def click(event):     #handling click event
    notepad.tag_config('Found',background='white',foreground='black')
def cmdSelectAll():     #edit menu Select All option
    notepad.event_generate("<<SelectAll>>")
    
def cmdTimeDate():     #edit menu Time/Date option
    now = datetime.now()
    # dd/mm/YY H:M:S
    dtString = now.strftime("%d/%m/%Y %H:%M:%S")
    label = messagebox.showinfo("Time/Date", dtString)
def cmdAbout():     #help menu About option
    label = messagebox.showinfo("About Program", "Batch helper by...")
def cmdEchoOffCheckBox():
    global is_echo_off
    if is_echo_off:
        is_echo_off = False
        text_to_remove = "@echo off\n"
        start_pos = notepad.search(text_to_remove, "1.0", END)
        end_pos = f"{start_pos}+{len(text_to_remove)}c"
        notepad.delete(start_pos, end_pos)
    else:
        is_echo_off = True
        notepad.insert("1.0", "@echo off\n")
    
#batch commands buttons
def cmd_batch_setlocal():
    new_text = "setlocal\n"
    cursor_position = notepad.index(INSERT)
    notepad.insert(cursor_position, new_text)

def cmd_batch_endlocal():
    new_text = "endlocal\n"
    cursor_position = notepad.index(INSERT)
    notepad.insert(cursor_position, new_text)

def cmd_batch_start():
    new_text = "start " + start_text.get(1.0, "end-1c") + "\n"
    cursor_position = notepad.index(INSERT)
    notepad.insert(cursor_position, new_text)
    start_text.delete(1.0, "end-1c")

def cmd_batch_loop():
    new_text = "for /l %%x in (1, 1, " + loop_text.get(1.0, "end-1c") + ") do (\n  \n  )\n"
    cursor_position = notepad.index(INSERT)
    notepad.insert(cursor_position, new_text)
    loop_text.delete(1.0, "end-1c")

def cmd_batch_set():
    if set_int_check:
        if set_input_check:
            new_text = 'set /p /a "' + set_text.get(1.0, "end-1c") + '=' + set_text_v.get(1.0, "end-1c") + '"\n'
        else:
            new_text = 'set /a "' + set_text.get(1.0, "end-1c") + '=' + set_text_v.get(1.0, "end-1c") + '"\n'
    else:
        if set_input_check:
            new_text = 'set /p "' + set_text.get(1.0, "end-1c") + '=' + set_text_v.get(1.0, "end-1c") + '"\n'
        else:
            new_text = 'set "' + set_text.get(1.0, "end-1c") + '=' + set_text_v.get(1.0, "end-1c") + '"\n'
    cursor_position = notepad.index(INSERT)
    notepad.insert(cursor_position, new_text)
    set_text.delete(1.0, "end-1c")
    set_text_v.delete(1.0, "end-1c")

def cmd_batch_int_checkbox():
    global set_int_check
    set_int_check = not set_int_check

def cmd_batch_input_checkbox():
    global set_input_check
    set_input_check = not set_input_check

def on_enter_press(event):
    if event.keysym == "Return":
        return "break"

def cmd_batch_echo():
    new_text = "echo " + echo_text.get(1.0, "end-1c") + "\n"
    cursor_position = notepad.index(INSERT)
    notepad.insert(cursor_position, new_text)
    echo_text.delete(1.0, "end-1c")

def cmd_batch_label():
    new_text = ":" + label_text.get(1.0, "end-1c") + "\n"
    cursor_position = notepad.index(INSERT)
    notepad.insert(cursor_position, new_text)
    label_text.delete(1.0, "end-1c")

def cmd_batch_goto():
    new_text = "goto " + goto_text.get(1.0, "end-1c") + "\n"
    cursor_position = notepad.index(INSERT)
    notepad.insert(cursor_position, new_text)
    goto_text.delete(1.0, "end-1c")

def cmd_batch_cls():
    new_text = "cls\n"
    cursor_position = notepad.index(INSERT)
    notepad.insert(cursor_position, new_text)

def cmd_batch_if():
    new_text = 'if ' + if_text.get(1.0, "end-1c") + ' ' + if_text_v.get(1.0, "end-1c") + '\n'
    cursor_position = notepad.index(INSERT)
    notepad.insert(cursor_position, new_text)
    if_text.delete(1.0, "end-1c")
    if_text_v.delete(1.0, "end-1c")

def cmd_batch_timer():
    new_text = "pathping -h 1 -p 25564 -q 1 -w " + timer_text.get(1.0, "end-1c") + " 127.0.0.1>nul\n"
    cursor_position = notepad.index(INSERT)
    notepad.insert(cursor_position, new_text)
    timer_text.delete(1.0, "end-1c")

#buttons!
echo_checkbutton = Checkbutton(text="Echo off", command=cmdEchoOffCheckBox)
echo_checkbutton.grid(row=0, column=1)

setlocal_button = Button(text="setlocal", command=cmd_batch_setlocal)
setlocal_button.grid(row=0, column=2)

endlocal_button = Button(text="endlocal", command=cmd_batch_endlocal)
endlocal_button.grid(row=0, column=3)

start_button = Button(text="start", command=cmd_batch_start)
start_button.grid(row=1, column=1)

start_text = Text(root, height = 1, width = 20)
start_text.grid(row=1, column=2, columnspan=2)
start_text.bind("<KeyPress>", on_enter_press)

loop_button = Button(text="create loop", command=cmd_batch_loop)
loop_button.grid(row=2, column=1)

loop_text = Text(root, height = 1, width = 6)
loop_text.grid(row=2, column=2, columnspan=2)
loop_text.bind("<KeyPress>", on_enter_press)

set_button = Button(text="set", command=cmd_batch_set)
set_button.grid(row=3, column=1)

set_text = Text(root, height = 1, width = 10)
set_text.grid(row=3, column=2)
set_text.bind("<KeyPress>", on_enter_press)

set_text_v = Text(root, height = 1, width = 10)
set_text_v.grid(row=3, column=3)
set_text_v.bind("<KeyPress>", on_enter_press)

set_int_checkbutton = Checkbutton(text="is int", command=cmd_batch_int_checkbox)
set_int_checkbutton.grid(row=4, column=1, columnspan=2)

set_input_checkbutton = Checkbutton(text="is input", command=cmd_batch_input_checkbox)
set_input_checkbutton.grid(row=4, column=2, columnspan=2)

echo_button = Button(text="echo", command=cmd_batch_echo)
echo_button.grid(row=5, column=1)

echo_text = Text(root, height = 1, width = 20)
echo_text.grid(row=5, column=2, columnspan=2)
echo_text.bind("<KeyPress>", on_enter_press)

label_button = Button(text="create label", command=cmd_batch_label)
label_button.grid(row=6, column=1)

label_text = Text(root, height = 1, width = 10)
label_text.grid(row=6, column=2, columnspan=2)
label_text.bind("<KeyPress>", on_enter_press)

goto_button = Button(text="goto", command=cmd_batch_goto)
goto_button.grid(row=7, column=1)

goto_text = Text(root, height = 1, width = 10)
goto_text.grid(row=7, column=2, columnspan=2)
goto_text.bind("<KeyPress>", on_enter_press)

cls_button = Button(text="cls", command=cmd_batch_cls)
cls_button.grid(row=8, column=1)

if_button = Button(text="if", command=cmd_batch_if)
if_button.grid(row=9, column=1)

if_text = Text(root, height = 1, width = 10)
if_text.grid(row=9, column=2)
if_text.bind("<KeyPress>", on_enter_press)

if_text_v = Text(root, height = 1, width = 10)
if_text_v.grid(row=9, column=3)
if_text_v.bind("<KeyPress>", on_enter_press)

#pathping -h 1 -p 70 -q 1 -w 1 127.0.0.1>nul

timer_button = Button(text="timer", command=cmd_batch_timer)
timer_button.grid(row=10, column=1)

timer_text = Text(root, height = 1, width = 6)
timer_text.grid(row=10, column=2, columnspan=2)
timer_text.bind("<KeyPress>", on_enter_press)

#key binds

def on_alt_c(event):
    new_text = "start "
    cursor_position = notepad.index(INSERT)
    notepad.insert(cursor_position, new_text)

def on_alt_w(event):
    new_text = "for /l %%x in (1, 1, 10) do (\n  \n  )\n"
    cursor_position = notepad.index(INSERT)
    notepad.insert(cursor_position, new_text)

def on_alt_d(event):
    new_text = "goto "
    cursor_position = notepad.index(INSERT)
    notepad.insert(cursor_position, new_text)

root.bind("<Alt-s>", on_alt_c)

root.bind("<Alt-w>", on_alt_w)

root.bind("<Alt-d>", on_alt_d)

root.bind("<Alt-a>", cmd_batch_timer)

root.bind("<Control-s>", cmdSave)

root.bind("<Control-Alt-s>", cmdSaveAs)

root.bind("<Control-e>", cmdOpen)

root.bind("<Control-q>", cmdNew)

#notepad menu items
notepadMenu = Menu(root)
root.configure(menu=notepadMenu)
#file menu
fileMenu = Menu(notepadMenu, tearoff = False)
notepadMenu.add_cascade(label='File', menu = fileMenu)
#adding options in file menu
fileMenu.add_command(label='New', command = cmdNew)
fileMenu.add_command(label='Open...', command = cmdOpen)
fileMenu.add_command(label='Save', command = cmdSave)
fileMenu.add_command(label='Save As...', command = cmdSaveAs)
fileMenu.add_separator()
fileMenu.add_command(label='Exit', command = cmdExit)
#edit menu
editMenu = Menu(notepadMenu, tearoff = False)
notepadMenu.add_cascade(label='Edit', menu = editMenu)
#adding options in edit menu
editMenu.add_command(label='Cut', command = cmdCut)
editMenu.add_command(label='Copy', command = cmdCopy)
editMenu.add_command(label='Paste', command = cmdPaste)
editMenu.add_command(label='Delete', command = cmdClear)
editMenu.add_separator()
editMenu.add_command(label='Find...', command = cmdFind)
editMenu.add_separator()
editMenu.add_command(label='Select All', command = cmdSelectAll)
editMenu.add_command(label='Time/Date', command = cmdTimeDate)
#help menu
helpMenu = Menu(notepadMenu, tearoff = False)
notepadMenu.add_cascade(label='Help', menu = helpMenu)
#adding options in help menu
helpMenu.add_command(label='About Program', command = cmdAbout)

notepad.grid(row=0, rowspan=99, column=0, sticky="ew")
root.mainloop()
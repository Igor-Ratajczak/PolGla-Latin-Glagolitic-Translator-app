from tkinter import PhotoImage, messagebox, font, colorchooser
import pyperclip
from tkinter import *
from PIL import ImageTk, Image
import requests
import os
import re

VERSION = '1.1'
UPDATE_URL = 'https://raw.githubusercontent.com/Igor-Ratajczak/PolGla-Tlumacz/main/update/whatsnew.flag'
FLAG_FILE = 'https://raw.githubusercontent.com/Igor-Ratajczak/PolGla-Tlumacz/main/update/'
LATEST_VERSION = 'https://raw.githubusercontent.com/Igor-Ratajczak/PolGla-Tlumacz/main/update/version.flag'
INFO_VERSION = 'option/info.flag'
COLOR_FILE = 'option/color.txt'

root = Tk()
root.state("zoomed")
root.title(f"Tłumacz Polski na Głagolice {VERSION}v")
logo = PhotoImage(file="img/icon.png")
root.iconphoto(True, logo)

# Set default colors
DEFAULT_COLORS = ['#F0F0F0', '#FFFFFF', '#CCCCCC', '#000000']


def is_valid_hex(s):
    """
    Check if the given string s is a valid hexadecimal RGB color code of the form '#RRGGBB'
    """
    if s.startswith('#') and len(s) == 7:
        try:
            int(s[1:], 16)
            return True
        except ValueError:
            pass
    return False


def color_change(bg, trans, buttons, text_color):
    main.config(bg=bg)
    button_Copy_place.config(bg=bg)
    icon_canvas.config(bg=bg)
    name_logo.config(bg=bg)
    inputtext.config(bg=trans)
    text.config(bg=trans)
    button.config(bg=buttons)
    buttonCopy.config(bg=buttons)
    button_place.config(bg=buttons)
    lang1.config(bg=buttons)
    lang2.config(bg=buttons)
    name_logo.config(fg=text_color)
    inputtext.config(fg=text_color)
    text.config(fg=text_color)
    button.config(fg=text_color)
    buttonCopy.config(fg=text_color)
    lang1.config(fg=text_color)
    lang2.config(fg=text_color)


def load_color():
    # Check if background file exists and load colors
    if os.path.isfile(COLOR_FILE):
        # Read colors from file
        with open(COLOR_FILE, 'r') as f:
            lines = f.readlines()

            if len(lines) == 0:
                # if file is empty, use default colors
                bg = DEFAULT_COLORS[0]
                trans = DEFAULT_COLORS[1]
                buttons = DEFAULT_COLORS[2]
                text_color = DEFAULT_COLORS[3]
            else:
                # Check if line is empty or invalid
                bg = lines[0].strip()
                trans = lines[1].strip()
                buttons = lines[2].strip()
                text_color = lines[3].strip()

                # Check if RGB hex code is valid
                if not re.match(r'^#(?:[0-9a-fA-F]{3}){1,2}$', bg):
                    bg = DEFAULT_COLORS[0]
                if not re.match(r'^#(?:[0-9a-fA-F]{3}){1,2}$', trans):
                    trans = DEFAULT_COLORS[1]
                if not re.match(r'^#(?:[0-9a-fA-F]{3}){1,2}$', buttons):
                    buttons = DEFAULT_COLORS[2]
                if not re.match(r'^#(?:[0-9a-fA-F]{3}){1,2}$', text_color):
                    text_color = DEFAULT_COLORS[3]
        color_change(bg, trans, buttons, text_color)

    else:
        # If file does not exist, use default colors
        bg = DEFAULT_COLORS[0]
        trans = DEFAULT_COLORS[1]
        buttons = DEFAULT_COLORS[2]
        text_color = DEFAULT_COLORS[3]
        color_change(bg, trans, buttons, text_color)


# Define save_change_color function in the global scope
def save_change_color(nr):
    with open(COLOR_FILE, 'r+') as f:
        lines = f.readlines()
        if nr == 1:
            lines[0] = bg + '\n'
        elif nr == 2:
            lines[1] = trans + '\n'
        elif nr == 3:
            lines[2] = buttons + '\n'
        elif nr == 4:
            lines[3] = text_color + '\n'
        f.seek(0)
        f.writelines(lines)


def change_color(option):
    global bg, trans, buttons, text_color

    # Open color picker
    new_color = colorchooser.askcolor(title="Wybierz nowy kolor dla tła")

    if new_color[1]:
        # Update background color
        color = new_color[1]
        if option == 1:  # Change the background color
            main.config(bg=color)
            button_Copy_place.config(bg=color)
            icon_canvas.config(bg=color)
            name_logo.config(bg=color)
            bg = color
            save_change_color(1)
        if option == 2:  # Change the color of the translator
            inputtext.config(bg=color)
            text.config(bg=color)
            trans = color
            save_change_color(2)
        if option == 3:  # Change the color of the buttons
            button.config(bg=color)
            buttonCopy.config(bg=color)
            button_place.config(bg=color)
            lang1.config(bg=color)
            lang2.config(bg=color)
            buttons = color
            save_change_color(3)
        if option == 4:  # Change the color of the text
            name_logo.config(fg=color)
            inputtext.config(fg=color)
            text.config(fg=color)
            name_logo.config(fg=color)
            button.config(fg=color)
            buttonCopy.config(fg=color)
            lang1.config(fg=color)
            lang2.config(fg=color)
            text_color = color
            save_change_color(4)

def author():
    messagebox.showinfo(
        title='Informacje o autorze',
        message='Igor Ratajczak',
    )


def check_info_of_actual_version():
    with open(INFO_VERSION, encoding='utf-8') as file:
        contents = file.read()

    messagebox.showinfo(
        title='Informacje o wersji',
        message=f'{contents}',
    )


def check_for_updates(check):
    try:
        response_UPDATE_URL = requests.get(UPDATE_URL)
        response_UPDATE_URL.raise_for_status()
        latest_version = response_UPDATE_URL.text.strip()
        response_LATEST_VERSION = requests.get(LATEST_VERSION)
        response_LATEST_VERSION.raise_for_status()
        new_version = response_LATEST_VERSION.text.strip()
        print(check, 1)
        if new_version > VERSION:
            response = messagebox.askyesno(
                title='Dostępna aktualizacja',
                message=f'Dostępna jest nowa wersja {latest_version}.\n\nCzy chcesz ją teraz pobrać i zainstalować?',
            )
            if response:
                import webbrowser
                webbrowser.open('http://127.0.0.1/program/update/')
            else:
                messagebox.showinfo(
                    'Aktualizacja', 'Możesz pobrać i zainstalować nową wersję w dogodnym momencie.')
        elif check == 1:
            messagebox.showinfo(
                title='Brak aktualizacji',
                message='Nie ma nowej wersji programu.',
            )
    except requests.exceptions.RequestException:
        pass


#### dictionary ######
characters = (
    {"pl": "A", "gl": "\u2C00"},
    {"pl": "a", "gl": "\u2C30"},
    {"pl": "Ą", "gl": "\u2C28"},
    {"pl": "ą", "gl": "\u2C58"},
    {"pl": "B", "gl": "\u2C01"},
    {"pl": "b", "gl": "\u2C31"},
    {"pl": "C", "gl": "\u2C1C"},
    {"pl": "c", "gl": "\u2C4C"},
    {"pl": "Ć", "gl": "\u2C1C"},
    {"pl": "ć", "gl": "\u2C4C"},
    {"pl": "D", "gl": "\u2C04"},
    {"pl": "d", "gl": "\u2C34"},
    {"pl": "E", "gl": "\u2C05"},
    {"pl": "e", "gl": "\u2C35"},
    {"pl": "F", "gl": "\u2C2A"},
    {"pl": "f", "gl": "\u2C5A"},
    {"pl": "G", "gl": "\u2C03"},
    {"pl": "g", "gl": "\u2C33"},
    {"pl": "H", "gl": "\u2C22"},
    {"pl": "h", "gl": "\u2C52"},
    {"pl": "I", "gl": "\u2C0B"},
    {"pl": "i", "gl": "\u2C3B"},
    {"pl": "J", "gl": "\u2C0B"},
    {"pl": "j", "gl": "\u2C3B"},
    {"pl": "K", "gl": "\u2C0D"},
    {"pl": "k", "gl": "\u2C3D"},
    {"pl": "L", "gl": "\u2C0E"},
    {"pl": "l", "gl": "\u2C3E"},
    {"pl": "M", "gl": "\u2C0F"},
    {"pl": "m", "gl": "\u2C3F"},
    {"pl": "N", "gl": "\u2C10"},
    {"pl": "n", "gl": "\u2C40"},
    {"pl": "Ó", "gl": "\u2C11"},
    {"pl": "ó", "gl": "\u2C41"},
    {"pl": "O", "gl": "\u2C11"},
    {"pl": "o", "gl": "\u2C41"},
    {"pl": "P", "gl": "\u2C12"},
    {"pl": "p", "gl": "\u2C42"},
    {"pl": "R", "gl": "\u2C13"},
    {"pl": "r", "gl": "\u2C43"},
    {"pl": "S", "gl": "\u2C14"},
    {"pl": "s", "gl": "\u2C44"},
    {"pl": "T", "gl": "\u2C15"},
    {"pl": "t", "gl": "\u2C45"},
    {"pl": "U", "gl": "\u2C16"},
    {"pl": "u", "gl": "\u2C46"},
    {"pl": "W", "gl": "\u2C02"},
    {"pl": "w", "gl": "\u2C32"},
    {"pl": "V", "gl": "\u2C02"},
    {"pl": "v", "gl": "\u2C32"},
    {"pl": "X", "gl": "\u2C18"},
    {"pl": "x", "gl": "\u2C48"},
    {"pl": "Y", "gl": "\u2C1F\u2C09"},
    {"pl": "y", "gl": "\u2C4F\u2C39"},
    {"pl": "Z", "gl": "\u2C08"},
    {"pl": "z", "gl": "\u2C38"},
)
PLtoGL = {}
GLtoPL = {}
emptyInput = ('<p id="translate_text-input_empty">Tłumaczenie</p>')
for char in characters:
    PLtoGL[char["pl"]] = char["gl"]
    GLtoPL[char["gl"]] = char["pl"]


def translate_text(event):
    string = inputtext.get("1.0", "end-1c")
    word = string
    result = []
    dictionary = GLtoPL if lang1_name == "gl" else PLtoGL
    for i in range(len(word)):
        char = word[i]
        combined = char + word[i + 1] if i + 1 < len(word) else ""
        result.append(dictionary.get(combined, combined)
                      if combined in dictionary else dictionary.get(char, char))
    add_letters(result)
    return "".join(result)


def add_letters(result):
    text.configure(state="normal")
    text.delete("1.0", END)
    text.insert("1.0", "".join(result))
    text.yview(END)
    inputtext.yview(END)
    text.configure(state="disabled")


def copy():
    text.configure(state="normal")
    copyText = text.get("1.0", "end-1c")
    pyperclip.copy(copyText)
    text.configure(state="disabled")


lang1_name = ""
lang2_name = ""


def changeLang():
    global lang1_name
    global lang2_name
    if (lang1.cget("text") == "POLSKI"):
        lang1.configure(text="ⰃⰎⰀⰃⰑⰎⰋⰜⰀ", width=15)
        lang2.configure(text="POLSKI", width=7)
        text1 = text.get("1.0", "end-1c")
        text.configure(state="normal")
        root.title("Tłumacz Głagolica na Polski")
        lang1_name = "gl"
        lang2_name = "pl"
        inputtext.delete("1.0", "end")
        inputtext.insert("1.0", text1)
        inputtext.yview(END)
        text.yview(END)
        text.configure(state="disabled")
        translate_text(None)  # add this line to pass the "event" argument
    else:
        lang1.configure(text="POLSKI", width=7)
        lang2.configure(text="ⰃⰎⰀⰃⰑⰎⰋⰜⰀ", width=15)
        text1 = text.get("1.0", "end-1c")
        text.configure(state="normal")
        root.title("Tłumacz Polski na Głagolice")
        lang1_name = "pl"
        lang2_name = "gl"
        inputtext.delete("1.0", "end")
        inputtext.insert("1.0", text1)
        inputtext.yview(END)
        text.yview(END)
        text.configure(state="disabled")
        translate_text(None)  # add this line to pass the "event" argument


# create menu bar
menubar = Menu(root)

option_menu = Menu(menubar, tearoff=0)

change_color_menu = Menu(menubar, tearoff=0)

change_color_menu.add_command(label="Zmień kolor tła ",
                              command=lambda key=1: change_color(1))
change_color_menu.add_command(label="Zmień kolor tłumcza",
                              command=lambda key=2: change_color(2))
change_color_menu.add_command(label="Zmień kolor przycisków",
                              command=lambda key=3: change_color(3))
change_color_menu.add_command(label="Zmień kolor tekstu",
                              command=lambda key=4: change_color(4))

option_menu.add_cascade(
    label="Zmień kolor tła dla ...",
    menu=change_color_menu,
)
option_menu.add_command(label="Zmień język tłumaczenia", command=changeLang)
option_menu.add_command(label="Skopiuj tłumaczenie", command=copy)
option_menu.add_separator()
option_menu.add_command(label="Exit", command=root.quit)

menubar.add_cascade(label="Opcje", menu=option_menu)

info_menu = Menu(menubar, tearoff=0)
info_menu.add_command(label="Informacje o wersji",
                      command=check_info_of_actual_version)
info_menu.add_command(label="Sprawdź czy nie ma nowej wersji",
                      command=lambda key=1: check_for_updates(1))
info_menu.add_command(label="O twórcy", command=author)

menubar.add_cascade(label="Info", menu=info_menu)

# display the menu bar
root.config(menu=menubar)

def clickKey(key=None):
    if key:
        inputtext.insert("end", key)
        translate_text(None)


def keyboard(lang, characters_list):
    keyboard = LabelFrame(root, bg='#ffffff', bd=19)
    keyboard.place(relx=0.8, rely=0, relwidth=0.2, relheight=1)
    fontKeyboard = font.Font(size=65)
    canvas = Canvas(keyboard, bg='#000000')
    frame = Frame(canvas, bg='#000000')
    scrollbar = Scrollbar(keyboard, orient='vertical', command=canvas.yview)
    canvas.configure(yscrollcommand=scrollbar.set)
    scrollbar.pack(side='right', fill='y')
    for characters in characters_list:
        if lang == "GLtoPL":
            lang1 = characters["gl"]
            lang2 = characters["pl"]
        elif lang == "PLtoGL":
            lang1 = characters["pl"]
            lang2 = characters["gl"]
        else:
            print("We have a problem!!!")
        button_frame = Frame(frame, bg='#000000', bd=5)
        lang1 = Button(button_frame, text=lang1, width=2, height=1,
                       anchor="center", background="#00c1ff", font=fontKeyboard, command=lambda key=lang1: clickKey(key))
        lang2 = Button(button_frame, text=lang2, width=2, height=1,
                       anchor="center", background="#00c1ff", font=fontKeyboard, command=lambda key=lang2: clickKey(key))
        lang1.pack(side="left")
        lang2.pack(side="left")
        button_frame.pack(pady=5)
    canvas.create_window((0, 0), window=frame, anchor='nw')
    canvas.update_idletasks()
    canvas.bind("<Configure>", lambda e: canvas.configure(
        scrollregion=canvas.bbox("all")))
    canvas.bind_all("<MouseWheel>", lambda e: canvas.yview_scroll(
        int(-1*(e.delta/120)), "units"))
    canvas.configure(scrollregion=canvas.bbox('all'))
    canvas.pack(side='left', fill='both', expand=True)


main = Frame(root, bg='#00c1ff', bd=5)
main.place(relx=0, rely=0, relwidth=0.8, relheight=1)
# main.config(bg=bg)
# Create a photoimage object of the image in the path
icon_canvas = Canvas(main, bd=0, highlightthickness=0, bg='#00c1ff')
icon_canvas.place(relx=0.35, rely=0, relwidth=0.3, relheight=0.3)
img = ImageTk.PhotoImage(Image.open('img/keyNile.png').resize((420, 320)))
icon_canvas.delete("all")
icon_canvas.create_image(160, 160, anchor='center', image=img)
icon_canvas.image = img
font_name_logo = font.Font(size=25)
name_logo = Label(icon_canvas,
                  text="Klucz Nilu", font=font_name_logo, bg='#00c1ff')
name_logo.place(relx=0.52, rely=0.7, relwidth=0.5, relheight=0.3)

# text to translate
frame = Frame(main, bg='#80c1ff', bd=5)
frame.place(relx=0, rely=0.4, relwidth=0.5, relheight=0.5)

inputtext_font = font.Font(size=35)
inputtext = Text(frame, height=100, width=100,
                 font=inputtext_font, padx=30, pady=10, bd=20)
inputtext.pack()
root.bind_all("<Key>", lambda event: translate_text(event))

# button to change language
button_place = Frame(main, bg='#ffffff', bd=5)
button_place.place(relx=0, rely=0.32, relwidth=1, relheight=0.08)

Text_font = font.Font(size=35)
lang1_name = "pl"
lang1 = Label(button_place, text="POLSKI", width=7, height=5,
              font=("Helvetica", 36), name=lang1_name)
lang1.place(relx=0.2, rely=0.5, anchor="center")

button_font = font.Font(size=35)
button = Button(button_place, text="\u21C4", width=5, height=5,
                font=button_font, anchor="center", command=changeLang)
button.pack()

lang2_name = "gl"
lang2 = Label(button_place, text="ⰃⰎⰀⰃⰑⰎⰋⰜⰀ", width=15,
              height=1, font=Text_font, name=lang2_name, padx=2)
lang2.place(relx=0.8, rely=0.5, anchor="center")

# text translate
lower_frame = Frame(main, bg='#80c1ff', bd=5)
lower_frame.place(relx=0.5, rely=0.4, relwidth=0.5, relheight=0.5)

Text_font = font.Font(size=35)
text = Text(lower_frame, height=10, width=30, font=Text_font,
            state="disabled", padx=30, pady=10, bd=20)
text.pack()

button_Copy_place = Frame(main, bg='#ffffff', bd=6)
button_Copy_place.place(relx=0, rely=0.9, relwidth=1, relheight=0.05)

buttonCopy_font = font.Font(size=15)
buttonCopy = Button(button_Copy_place, text="Skopiuj tłumaczenie",
                    font=buttonCopy_font, justify="right", command=copy)
buttonCopy.pack()

keyboard("GLtoPL", characters)

load_color()

check_for_updates(0)

root.mainloop()

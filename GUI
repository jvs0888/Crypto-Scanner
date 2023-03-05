import customtkinter as ctk
from PIL import Image


def start_scanning():
    checkboxes = [checkbox_binance, checkbox_huobi, checkbox_bybit, checkbox_kucoin,
                    checkbox_gateio, checkbox_mexc, checkbox_okx]
    exchanges = ['binance', 'huobi', 'bybit', 'kucoin', 'gateio', 'mexc', 'okx']
    cex = list()
    cex_flag = False
    for i in range(len(checkboxes)):
        if checkboxes[i].get() == 1:
            cex.append(exchanges[i])
    if len(cex) > 1:
        cex_flag = True

    optionmenu = [optionmenu_btc, optionmenu_eth, optionmenu_usdt]
    crypto = ['BTC', 'ETH', 'USDT']
    traiding_pair = list()
    optionmenu_flag = False
    for i in range(len(crypto)):
        if optionmenu[i].get() != crypto[i]:
            if optionmenu[i].get() not in traiding_pair:
                traiding_pair.append(optionmenu[i].get().replace('/',''))
                optionmenu_flag = True

    entry_flag = False
    if entry.cget('state') == 'disabled':
        if entry.get() not in traiding_pair:
            traiding_pair.append(entry.get().upper())
            entry_flag = True

    textbox.configure(state='normal')
    textbox.delete(0.0, 'end')
    if cex_flag:
        if optionmenu_flag or entry_flag:
            textbox.insert(1.0, '') # output to the main screen
    else:
        textbox.insert(1.0, 'You must select at least 2 exchanges to compare')
    textbox.configure(state='disabled')

def clear_result():
    textbox.configure(state='normal')
    textbox.delete(0.0, 'end')
    textbox.configure(state='disabled')

def change_appearance_mode_event(new_appearance_mode: str):
    ctk.set_appearance_mode(new_appearance_mode)

def change_scaling_event(new_scaling: str):
    new_scaling_float = int(new_scaling.replace('%', '')) / 100
    ctk.set_widget_scaling(new_scaling_float)

def optionmenu_reset():
    optionmenu = [optionmenu_btc, optionmenu_eth, optionmenu_usdt]
    crypto = ['BTC', 'ETH', 'USDT']
    for i in range(len(crypto)):
        if optionmenu[i].get() != crypto[i]:
            optionmenu[i].set(crypto[i])
    for i in range(len(crypto)):
        optionmenu[i].configure(state='normal')
    entry.configure(state='normal')
    entry.delete(0, last_index='end')

def input_confirm():
    if entry.get():
        entry.configure(state='disabled')

def percent_set(value):
    progressbar.set(value)
    percent_value.configure(text=str(round(value * 100)) + ' %')

def switch_select():
    checkboxes = [checkbox_binance, checkbox_huobi, checkbox_bybit, checkbox_kucoin,
                    checkbox_gateio, checkbox_mexc, checkbox_okx]
    for i in checkboxes:
        if switch_var.get() == 'on':
            i.select()
        else:
            i.deselect()


app = ctk.CTk()
app.title("Crypto Scanner v. 1.0")
app.iconbitmap('images/windowicon.ico')
app.geometry('1280x720+150+50')
app.minsize(width=1280, height=720)

app.grid_columnconfigure(1, weight=1)
app.grid_columnconfigure((2, 3), weight=0)
app.grid_rowconfigure((0, 1, 2), weight=1)

font = ctk.CTkFont(slant='roman', size=20)

ctk.set_appearance_mode("Dark")
ctk.set_default_color_theme("blue")

sidebar_frame = ctk.CTkFrame(master=app, width=140, corner_radius=0)
sidebar_frame.grid(row=0, column=0, rowspan=4, sticky="nsew")
sidebar_frame.grid_rowconfigure(4, weight=1)

logo_img = ctk.CTkImage(light_image=Image.open("images/windowicon.png"), size=(150, 150))
logo_label = ctk.CTkLabel(master=sidebar_frame, image=logo_img, text='')
logo_label.grid(row=4, column=0, padx=0, pady=(0, 0))

start_scanning_button = ctk.CTkButton(master=sidebar_frame, command=start_scanning, text='Start scanning',
                                      font=('font', 15), height=50)
start_scanning_button.grid(row=0, column=0, padx=20, pady=(20, 10))

clear_button = ctk.CTkButton(master=sidebar_frame, command=clear_result, text='Clear result', font=('font', 15),
                             height=30)
clear_button.grid(row=1, column=0, padx=20, pady=(10, 10))

appearance_mode_label = ctk.CTkLabel(master=sidebar_frame, text="Appearance Mode:", anchor="w", font=('font', 15),
                                     height=30)
appearance_mode_label.grid(row=5, column=0, padx=20, pady=(10, 0))
appearance_mode_optionemenu = ctk.CTkOptionMenu(master=sidebar_frame, values=["Light", "Dark", "System"],
                                                command=change_appearance_mode_event, font=('font', 15),
                                                dropdown_font=('font', 15), height=30)
appearance_mode_optionemenu.grid(row=6, column=0, padx=20, pady=(10, 10))
appearance_mode_optionemenu.set("Dark")

scaling_label = ctk.CTkLabel(master=sidebar_frame, text="UI Scaling:", anchor="w", font=('font', 15))
scaling_label.grid(row=7, column=0, padx=20, pady=(10, 0))
scaling_optionemenu = ctk.CTkOptionMenu(master=sidebar_frame, values=["80%", "90%", "100%"],
                                        command=change_scaling_event, font=('font', 15), dropdown_font=('font', 15))
scaling_optionemenu.grid(row=8, column=0, padx=20, pady=(10, 20))
scaling_optionemenu.set("100%")

textbox = ctk.CTkTextbox(master=app, width=250, font=('font', 20))
textbox.grid(row=0, rowspan=3, column=1, padx=(20, 0), pady=(10, 10), sticky="nsew")


optionmenu_frame = ctk.CTkFrame(master=app)
optionmenu_frame.grid(row=0, column=3, padx=(20, 20), pady=(10, 0), sticky="nsew")

optionmenu_btc = ctk.CTkOptionMenu(master=optionmenu_frame, dynamic_resizing=False,
                                   values=["XMR/BTC", "DOGE/BTC", "LTC/BTC", "ADA/BTC",
                                           "XLM/BTC", "DASH/BTC", "EOS/BTC", "BTC/USDC",
                                           "BCH/BTC","XRP/BTC", "TRX/BTC", "LINK/BTC"],
                                   font=('font', 15), dropdown_font=('font', 15), height=30)
optionmenu_btc.grid(row=0, column=1, padx=(20, 10), pady=(14, 9), sticky='n')
optionmenu_btc.set("BTC")

btc_logo = ctk.CTkImage(light_image=Image.open("images/btc_logo.png"),
                                  size=(50, 50))
btc = ctk.CTkLabel(master=optionmenu_frame, image=btc_logo, text='')
btc.grid(row=0, column=0, padx=(10, 0), pady=(5, 0), sticky='n')

optionmenu_eth = ctk.CTkOptionMenu(master=optionmenu_frame, dynamic_resizing=False,
                                   values=["ETH/BTC", "ETH/BCH", "ETH/LINK", "ETH/ADA",
                                           "ETH/DOGE", "TRX/ETH", "XMR/ETH", "ZEC/ETH",
                                           "DASH/ETH", "ETH/USDC", "ETH/DAI"],
                                   font=('font', 15), dropdown_font=('font', 15), height=30)
optionmenu_eth.grid(row=1, column=1, padx=(20, 10), pady=(9.5, 9), sticky='n')
optionmenu_eth.set("ETH")

eth_logo = ctk.CTkImage(light_image=Image.open("images/eth_logo.png"),
                                  size=(50, 50))
eth = ctk.CTkLabel(master=optionmenu_frame, image=eth_logo, text='')
eth.grid(row=1, column=0, padx=(10, 0), pady=(0, 0), sticky='n')

optionmenu_usdt = ctk.CTkOptionMenu(master=optionmenu_frame, dynamic_resizing=True,
                                    values=["BTC/USDT", "ETH/USDT", "DOGE/USDT", "BCH/USDT",
                                            "LTC/USDT", "XRP/USDT", "EOS/USDT", "LINK/USDT",
                                            "BNB/USDT", "TRX/USDT", "DOT/USDT", "MATIC/USDT",
                                            "ATOM/USDT", "ADA/USDT", "SHIB/USDT", "WAVES/USDT",
                                            "AVAX/USDT", "SOL/USDT", "XMR/USDT", "1INCH/USDT",
                                            "XLM/USDT", "AAVE/USDT"],
                                    font=('font', 15), dropdown_font=('font', 15), height=30)
optionmenu_usdt.grid(row=3, column=1, padx=(20, 10), pady=(9.5, 10), sticky='n')
optionmenu_usdt.set("USDT")

usdt_logo = ctk.CTkImage(light_image=Image.open("images/usdt_logo.png"),
                                  size=(50, 50))
usdt = ctk.CTkLabel(master=optionmenu_frame, image=usdt_logo, text='')
usdt.grid(row=3, column=0, padx=(10, 0), pady=(0, 10), sticky='n')

entry = ctk.CTkEntry(master=optionmenu_frame, placeholder_text="Manual input", width=120, font=('font', 18), height=30)
entry.grid(row=4, column=0, columnspan=2, padx=(10, 5), pady=(0, 2.5), sticky="nw")

confirm_button = ctk.CTkButton(master=optionmenu_frame, fg_color="transparent",border_width=2,
                               text_color=("gray10", "#DCE4EE"), text='Confirm', command=input_confirm,
                               font=('font', 15), width=70, height=30)
confirm_button.grid(row=4, column=1, padx=(5, 10), pady=(0, 2.5), sticky="ne")

reset_button = ctk.CTkButton(master=optionmenu_frame, fg_color="transparent", border_width=2,
                             text_color=("gray10", "#DCE4EE"), text='Reset all', command=optionmenu_reset,
                             font=('font', 15), height=30)
reset_button.grid(row=5, column=0, columnspan=2, padx=(10, 10), pady=(10, 5), sticky="nsew")

progressbar_frame = ctk.CTkFrame(master=app)
progressbar_frame.grid(row=1, column=3, padx=(20, 20), pady=(10, 10), sticky="nsew")

progressbar= ctk.CTkProgressBar(master=progressbar_frame)
progressbar.grid(row=0, column=0, padx=(10, 5), pady=(20, 10), sticky="nsew")

percent_value = ctk.CTkLabel(master=progressbar_frame, text="50 %", font=('font', 20))
percent_value.grid(row=1, column=0, padx=(0, 0), pady=(5, 5), sticky='nsew')

slider_1 = ctk.CTkSlider(master=progressbar_frame, from_=0, to=1, number_of_steps=100, command=percent_set)
slider_1.grid(row=2, column=0, padx=(10, 5), pady=(10, 10), sticky="nsew")

checkbox_frame = ctk.CTkFrame(master=app)
checkbox_frame.grid(row=2, rowspan=3, column=3, padx=(20, 20), pady=(0, 10), sticky="nsew")

switch_var = ctk.StringVar(value="off")
switch_select = ctk.CTkSwitch(master=checkbox_frame, command=switch_select, text='Select All', font=('font', 15),
                              variable=switch_var, onvalue="on", offvalue="off")
switch_select.grid(row=0, column=0, padx=(30, 0), pady=(10, 10), sticky='nsew')

checkbox_binance = ctk.CTkCheckBox(master=checkbox_frame, text='Binance', font=('font', 15))
checkbox_binance.grid(row=1, column=0, padx=(30, 0), pady=(5, 5), sticky='nsew')

binance_logo = ctk.CTkImage(light_image=Image.open("images/binance_logo.png"), size=(25, 25))
binance = ctk.CTkLabel(master=checkbox_frame, image=binance_logo, text='')
binance.grid(row=1, column=1, padx=(30, 20), pady=(5, 2.5), sticky='nsew')

checkbox_huobi = ctk.CTkCheckBox(master=checkbox_frame, text='Huobi', font=('font', 15))
checkbox_huobi.grid(row=2, column=0, padx=(30, 0), pady=(5, 5), sticky='nsew')

huobi_logo = ctk.CTkImage(light_image=Image.open("images/huobi_logo.png"), size=(35, 30))
huobi = ctk.CTkLabel(master=checkbox_frame, image=huobi_logo, text='')
huobi.grid(row=2, column=1, padx=(30, 20), pady=(2.5, 2.5), sticky='nsew')

checkbox_bybit = ctk.CTkCheckBox(master=checkbox_frame, text='Bybit', font=('font', 15))
checkbox_bybit.grid(row=3, column=0, padx=(30, 0), pady=(5, 5), sticky='nsew')

bybit_logo = ctk.CTkImage(light_image=Image.open("images/bybit_logo.png"), size=(25, 25))
bybit = ctk.CTkLabel(master=checkbox_frame, image=bybit_logo, text='')
bybit.grid(row=3, column=1, padx=(30, 20), pady=(2.5, 2.5), sticky='nsew')

checkbox_kucoin = ctk.CTkCheckBox(master=checkbox_frame, text='Kucoin', font=('font', 15))
checkbox_kucoin.grid(row=4, column=0, padx=(30, 0), pady=(5, 5), sticky='nsew')

kucoin_logo = ctk.CTkImage(light_image=Image.open("images/kucoin_logo.png"), size=(25, 25))
kucoin = ctk.CTkLabel(master=checkbox_frame, image=kucoin_logo, text='')
kucoin.grid(row=4, column=1, padx=(30, 20), pady=(2.5, 2.5), sticky='nsew')

checkbox_gateio = ctk.CTkCheckBox(master=checkbox_frame, text='Gateio', font=('font', 15))
checkbox_gateio.grid(row=5, column=0, padx=(30, 0), pady=(5, 5), sticky='nsew')

gateio_logo = ctk.CTkImage(light_image=Image.open("images/gateio_logo.png"), size=(25, 25))
gateio = ctk.CTkLabel(master=checkbox_frame, image=gateio_logo, text='')
gateio.grid(row=5, column=1, padx=(30, 20), pady=(2.5, 2.5), sticky='nsew')

checkbox_mexc = ctk.CTkCheckBox(master=checkbox_frame, text='Mexc', font=('font', 15))
checkbox_mexc.grid(row=6, column=0, padx=(30, 0), pady=(5, 5), sticky='nsew')

mexc_logo = ctk.CTkImage(light_image=Image.open("images/mexc_logo.png"), size=(25, 20))
mexc = ctk.CTkLabel(master=checkbox_frame, image=mexc_logo, text='')
mexc.grid(row=6, column=1, padx=(30, 20), pady=(2.5, 2.5), sticky='nsew')

checkbox_okx = ctk.CTkCheckBox(master=checkbox_frame, text='Okx', font=('font', 15))
checkbox_okx.grid(row=7, column=0, padx=(30, 0), pady=(5, 10), sticky='nsew')

okx_logo = ctk.CTkImage(light_image=Image.open("images/okx_logo.png"), size=(25, 25))
okx = ctk.CTkLabel(master=checkbox_frame, image=okx_logo, text='')
okx.grid(row=7, column=1, padx=(30, 20), pady=(2.5, 10), sticky='nsew')

app.mainloop()

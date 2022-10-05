import numpy as np
import pandas as pd
from tkinter import Tk
from tkinter import messagebox
import threading
from scipy.signal import argrelextrema
import matplotlib.pyplot as plt
import requests
from colorama import Fore
import colorama
import os
from pystyle import Add, Center, Anime, Colors, Colorate, Write, System
import time
from datetime import datetime
from multiprocessing import Process


from numpy import *
from matplotlib.pyplot import *

class bcolors:
    OK = '\033[92m' #GREEN
    WARNING = '\033[93m' #YELLOW
    FAIL = '\033[91m' #RED
    RESET = '\033[0m' #RESET COLOR
    PURPLE = '\033[35m'  #PURPLE

w = Fore.WHITE
b = Fore.BLACK
g = Fore.LIGHTGREEN_EX
y = Fore.LIGHTYELLOW_EX
m = Fore.LIGHTMAGENTA_EX
c = Fore.LIGHTCYAN_EX
lr = Fore.LIGHTRED_EX
lb = Fore.LIGHTBLUE_EX

my_lock = threading.RLock()


end = str(pd.Timestamp.today() + pd.DateOffset(5))[0:10]
start_15m = str(pd.Timestamp.today() + pd.DateOffset(-1000))[0:10]
start_30m = str(pd.Timestamp.today() + pd.DateOffset(-3))[0:10]
start_1h = str(pd.Timestamp.today() + pd.DateOffset(-5))[0:10]
start_6h = str(pd.Timestamp.today() + pd.DateOffset(-20))[0:10]
start_1d = str(pd.Timestamp.today() + pd.DateOffset(-30))[0:10]
start_1week = str(pd.Timestamp.today() + pd.DateOffset(-120))[0:10]
start_1month = str(pd.Timestamp.today() + pd.DateOffset(-240))[0:10]
print(start_1week)
api_key = '1KsqKOh1pTAJyWZx6Qm9pvnaNcpKVh_8'



def graph(time1,time_name1,start1,time2,time_name2,start2):
	api_url_livePrice = f'https://api.polygon.io/v1/last/crypto/{tiker_live}?apiKey={api_key}'
	data = requests.get(api_url_livePrice).json()
	df_livePrice = pd.DataFrame(data)

	# api_url_OHLC = f'https://api.polygon.io/v2/aggs/ticker/{ticker}/range/15/minute/2022-07-01/2022-07-15?adjusted=true&sort=asc&limit=30000&apiKey={api_key}'
	api_url_OHLC = f'https://api.polygon.io/v2/aggs/ticker/{ticker}/range/{time1}/{time_name1}/{start1}/{end}?adjusted=true&limit=50000&apiKey={api_key}'
	api_url_OHLC2 = f'https://api.polygon.io/v2/aggs/ticker/{ticker}/range/{time2}/{time_name2}/{start2}/{end}?adjusted=true&limit=50000&apiKey={api_key}'

	data = requests.get(api_url_OHLC).json()
	df = pd.DataFrame(data['results'])


	data2 = requests.get(api_url_OHLC2).json()
	df2 = pd.DataFrame(data2['results'])

	fig1 = plt.figure(figsize=(10,7))
	fig1.patch.set_facecolor('#17abde')
	fig1.patch.set_alpha(0.3)



	plt.subplot(2, 1, 1)
	#a1 = plt.subplot(2,1,1)
	#a1.patch.set_facecolor('white')
	#a1.patch.set_alpha(0.5)






	supmax = len(df['c']) - 15
	df3 = df['c'][supmax:-1].tolist()
	#df3 = df[supmax:-1]
	df3 = pd.DataFrame(df3, columns=['c'])
	#tab = pd.DataFrame(tab, columns=['a'])

	#del df['c'].values[0:supmax]

	local_max = argrelextrema(df3['c'].values, np.greater, order=1, mode='clip')[0]
	local_min = argrelextrema(df3['c'].values, np.less, order=1, mode='clip')[0]

	highs = df3.iloc[local_max, :]
	lows = df3.iloc[local_min, :]
	df3['c'].plot(color=['blue'], lw=1.2, ls='-', label='Prix')
	plt.plot([], [])
	plt.title(f'{nom} | {time1} {time_name1}', fontweight="bold")


	plt.scatter(x=highs.index, y=highs['c'])
	plt.scatter(x=lows.index, y=lows['c'])
	plt.legend(loc='upper left')
	plt.grid(b=True, which='major', color='#666666', linestyle='-', alpha=0.1)
# le deuxieme


	#a2 = plt.subplot(3,1,2)
	#a2.patch.set_facecolor('#b2b2b2')
	#a2.patch.set_alpha(0.5)

	local_max2 = argrelextrema(df['c'].values, np.greater, order=1, mode='clip')[0]
	local_min2 = argrelextrema(df['c'].values, np.less, order=1, mode='clip')[0]
	local_max21 = argrelextrema(df2['c'].values, np.greater, order=1, mode='clip')[0]
	local_min21 = argrelextrema(df2['c'].values, np.less, order=1, mode='clip')[0]




	# BB indicateur





	#plt.subplot(3, 1, 3)
	a2 = plt.subplot(2, 1, 2)
	a2.axis('off')
	#a2.patch.set_facecolor('#b2b2b2')
	#a2.patch.set_alpha(0.5)

	local_max3 = argrelextrema(df['v'].values, np.greater, order=1, mode='clip')[0]
	local_min3 = argrelextrema(df['v'].values, np.less, order=1, mode='clip')[0]

	def sma(data, window):
		sma = data.rolling(window=window).mean()
		return sma

	df['sma_20'] = sma(df['c'], 20)
	df.tail()

	def bb(data, sma, window):
		std = data.rolling(window=window).std()
		upper_bb = sma + std * 2
		lower_bb = sma - std * 2
		return upper_bb, lower_bb

	df['upper_bb'], df['lower_bb'] = bb(df['c'], df['sma_20'], 20)
	df.tail()


	def createMACD(df):
		df['e26'] = pd.Series.ewm(df['c'], span=26).mean()
		df['e12'] = pd.Series.ewm(df['c'], span=12).mean()
		df['MACD'] = df['e12'] - df['e26']
		df['e9'] = pd.Series.ewm(df['MACD'], span=9).mean()
		df['HIST'] = df['MACD'] - df['e9']



	createMACD(df)

	def rsi(df, periods=14, ema=True):
		"""
        Returns a pd.Series with the relative strength index.
        """
		close_delta = df['c'].diff()

		# Make two series: one for lower closes and one for higher closes
		up = close_delta.clip(lower=0)
		down = -1 * close_delta.clip(upper=0)

		if ema == True:
			# Use exponential moving average
			ma_up = up.ewm(com=periods - 1, adjust=True, min_periods=periods).mean()
			ma_down = down.ewm(com=periods - 1, adjust=True, min_periods=periods).mean()
		else:
			# Use simple moving average
			ma_up = up.rolling(window=periods, adjust=False).mean()
			ma_down = down.rolling(window=periods, adjust=False).mean()

		rsi = ma_up / ma_down
		rsi = 100 - (100 / (1 + rsi))
		return rsi

	df['rsi'] = rsi(df)
	print(df)

	macd = ""
	volume = ""
	boolinger ="PAS DE BULLE BANDES DE BOLLINGER"
	tendance = ""





	if df['c'].values[-1] > df['upper_bb'].values[-1] and df['c'].values[local_max2[-1]] > df['upper_bb'].values[local_max2[-1]] :
		print('-- ATTENTION BULLE BANDES DE BOLLINGER --')
		boolinger = "BULLE BANDES DE BOLLINGER BAISSIERE"

	if df['c'].values[-1] < df['lower_bb'].values[-1] or df['c'].values[local_min2[-1]] < df['lower_bb'].values[
		local_min2[-1]]:
		print('-- EN BULLE DE BOLLINGER HAUSSIERE --')
		boolinger = "BULLE BANDES DE BOLLINGER HAUSSIERE"

	if local_max3[-1] > local_min3[-1] and df['v'].values[-1] < df['v'].values[local_max3[-1]]:
		print('-- LE VOLUME DESCEND --')
		volume = "DESCEND"
	else:
		print('-- LE VOLUME MONTE --')
		volume = "MONTE"


	if local_max2[-1] > local_min21[-1] and df2['c'].values[-1] > df2['c'].values[local_max21[-1]]:
		print('-- EN TENDANCE BAISSIERE --')
		tendance = "BAISSIERE"
	else:
		print('-- EN TENDANCE HAUSSIERE --')
		tendance = "HAUSSIERE"

	if df['HIST'].values[-1] > df['HIST'].values[-2]:
		print('-- MACD QUI MONTE --')
		macd = "MONTE"
	else:
		print('-- MACD QUI DESCEND --')
		macd = "DESCEND"

	#data = [['la macd :', macd],
	#		[5, 6]]
	#colors = [["#17abde", "#17abde"], ["#17abde", "#17abde"]]
	#a2.table(cellText=data, loc="center", cellColours = colors, cellLoc='center')

	plt.axis([0, 10, 0, 10])
	plt.text(0, 8, f" ▶ LA MACD : {macd}", ha='left', style='normal', size=9.5, color='black', wrap=True, alpha=1)
	plt.text(0, 6.5, f" ▶ LE VOLUME : {volume}", ha='left', style='normal', size=9.5, color='black', wrap=True, alpha=1)
	plt.text(0, 5, f" ▶ {boolinger}", ha='left', style='normal', size=9.5, color='black', wrap=True, alpha=1)
	plt.text(5, 8, f" ▶ LA TENDANCE EST : {tendance}", ha='left', style='normal', size=9.5, color='black', wrap=True, alpha=1)
	plt.text(5, 6.5, f" ▶ LE RSI EST DE : {int(df['rsi'].values[-1])}", ha='left', style='normal', size=9.5, color='black', alpha=1)
	plt.text(5, 5, " ▶ PAS DE FIGURE PRESENTE SUR LE GRAPH", ha='left', style='normal', size=9.5, color='black', wrap=True, alpha=1)

	#plt.savefig('images/figure.png')
	plt.show()





os.system('clear')


print(' ')
print(' ')
Write.Print("                                          /$$$$$$  /$$$$$$$  /$$      /$$  /$$$$$$  /$$$$$$$$\n", Colors.purple_to_blue, interval=0.000)
Write.Print("                                         /$$__  $$| $$__  $$| $$$    /$$$ /$$__  $$|__  $$__/\n", Colors.purple_to_blue, interval=0.000)
Write.Print("                                        | $$  \ $$| $$  \ $$| $$$$  /$$$$| $$  \ $$   | $$   \n", Colors.purple_to_blue, interval=0.000)
Write.Print("                                        | $$$$$$$$| $$  | $$| $$ $$/$$ $$| $$$$$$$$   | $$   \n", Colors.purple_to_blue, interval=0.000)
Write.Print("                                        | $$__  $$| $$  | $$| $$  $$$| $$| $$__  $$   | $$   \n", Colors.purple_to_blue, interval=0.000)
Write.Print("                                        | $$  | $$| $$  | $$| $$\  $ | $$| $$  | $$   | $$   \n", Colors.purple_to_blue, interval=0.000)
Write.Print("                                        | $$  | $$| $$$$$$$/| $$ \/  | $$| $$  | $$   | $$   \n", Colors.purple_to_blue, interval=0.000)
Write.Print(" > ADMAT Version 1.1                    |__/  |__/|_______/ |__/     |__/|__/  |__/   |__/   \n", Colors.purple_to_blue, interval=0.000)

Write.Print("════════════════════════════════════════════════════════════════════════════════════════════════════════════════════════", Colors.purple_to_blue, interval=0.000)
time.sleep(0.5)
print(' ')
print(f'''{m}'''.replace('$', f'{m}${w}') + f'''{m}[{w}1{Fore.RESET}{m}]{Fore.RESET} ADAUSD          {m}'''.replace('$', f'{m}${w}') + f'''{m}[{w}11{Fore.RESET}{m}]{Fore.RESET} LINKUSD          {m}'''.replace('$', f'{m}${w}') + f'''{m}[{w}21{Fore.RESET}{m}]{Fore.RESET}  XRPUSD ''')
print(f'''{m}'''.replace('$', f'{m}${w}') + f'''{m}[{w}2{Fore.RESET}{m}]{Fore.RESET} AVAXUSD         {m}'''.replace('$', f'{m}${w}') + f'''{m}[{w}12{Fore.RESET}{m}]{Fore.RESET} MANAUSD          {m}'''.replace('$', f'{m}${w}') + f'''{m}[{w}22{Fore.RESET}{m}]{Fore.RESET}  XTZUSD ''')
print(f'''{m}'''.replace('$', f'{m}${w}') + f'''{m}[{w}3{Fore.RESET}{m}]{Fore.RESET} BTCUSD          {m}'''.replace('$', f'{m}${w}') + f'''{m}[{w}13{Fore.RESET}{m}]{Fore.RESET} MATICUSD         {m}'''.replace('$', f'{m}${w}') + f'''{m}[{w}23{Fore.RESET}{m}]{Fore.RESET}  YFIUSD ''')
print(f'''{m}'''.replace('$', f'{m}${w}') + f'''{m}[{w}4{Fore.RESET}{m}]{Fore.RESET} CROUSD          {m}'''.replace('$', f'{m}${w}') + f'''{m}[{w}14{Fore.RESET}{m}]{Fore.RESET} SANDUSD          {m}'''.replace('$', f'{m}${w}') + f'''{m}[{w}24{Fore.RESET}{m}]{Fore.RESET}  DOTUSD ''')
print(f'''{m}'''.replace('$', f'{m}${w}') + f'''{m}[{w}5{Fore.RESET}{m}]{Fore.RESET} DOGEUSD         {m}'''.replace('$', f'{m}${w}') + f'''{m}[{w}15{Fore.RESET}{m}]{Fore.RESET} SHIBUSD ''')
print(f'''{m}'''.replace('$', f'{m}${w}') + f'''{m}[{w}6{Fore.RESET}{m}]{Fore.RESET} EGLDUSD         {m}'''.replace('$', f'{m}${w}') + f'''{m}[{w}16{Fore.RESET}{m}]{Fore.RESET} SOLUSD ''')
print(f'''{m}'''.replace('$', f'{m}${w}') + f'''{m}[{w}7{Fore.RESET}{m}]{Fore.RESET} EOSUSD          {m}'''.replace('$', f'{m}${w}') + f'''{m}[{w}17{Fore.RESET}{m}]{Fore.RESET} THETAUSD ''')
print(f'''{m}'''.replace('$', f'{m}${w}') + f'''{m}[{w}8{Fore.RESET}{m}]{Fore.RESET} ETHUSD          {m}'''.replace('$', f'{m}${w}') + f'''{m}[{w}18{Fore.RESET}{m}]{Fore.RESET} TRXUSD ''')
print(f'''{m}'''.replace('$', f'{m}${w}') + f'''{m}[{w}9{Fore.RESET}{m}]{Fore.RESET} FTMUSD          {m}'''.replace('$', f'{m}${w}') + f'''{m}[{w}19{Fore.RESET}{m}]{Fore.RESET} UNIUSD ''')
print(f'''{m}'''.replace('$', f'{m}${w}') + f'''{m}[{w}10{Fore.RESET}{m}]{Fore.RESET} GALAUSD        {m}'''.replace('$', f'{m}${w}') + f'''{m}[{w}20{Fore.RESET}{m}]{Fore.RESET} UOSUSD           {m}'''.replace('$', f'{m}${w}') + f'''{m}[{w}M{Fore.RESET}{m}]{Fore.RESET}{lb} RETOUR ''')
print(' ')
Write.Print("════════════════════════════════════════════════════════════════════════════════════════════════════════════════════════", Colors.purple_to_blue, interval=0.000)

print('                      ')
Write.Print(" CHOISSISEZ VOTRE MONNAIE : ", Colors.purple, interval=0.000)
time.sleep(0.5)
print(' ')

nom = ""


a = 0
while a != 1:
	monnaie = input(' >>\x1B[1m ')
	if monnaie == "1":
		nom = "ADA"
		a = 1
	if monnaie == "2":
		nom = "AVAX"
		a = 1
	if monnaie == "3":
		nom = "BTC"
		a = 1
	if monnaie == "4":
		nom = "CRO"
		a = 1
	if monnaie == "5":
		nom = "DOGE"
		a = 1
	if monnaie == "6":
		nom = "EGLD"
		a = 1
	if monnaie == "7":
		nom = "EOS"
		a = 1
	if monnaie == "8":
		nom = "ETH"
		a = 1
	if monnaie == "9":
		nom = "FTM"
		a = 1
	if monnaie == "10":
		nom = "GALA"
		a = 1
	if monnaie == "11":
		nom = "LINK"
		a = 1
	if monnaie == "12":
		nom = "MANA"
		a = 1
	if monnaie == "13":
		nom = "MATIC"
		a = 1
	if monnaie == "14":
		nom = "SAND"
		a = 1
	if monnaie == "15":
		nom = "SHIB"
		a = 1
	if monnaie == "16":
		nom = "SOL"
		a = 1
	if monnaie == "17":
		nom = "THETA"
		a = 1
	if monnaie == "18":
		nom = "TRX"
		a = 1
	if monnaie == "19":
		nom = "UNI"
		a = 1
	if monnaie == "20":
		nom = "UOS"
		a = 1
	if monnaie == "21":
		nom = "XRP"
		a = 1
	if monnaie == "22":
		nom = "XTZ"
		a = 1
	if monnaie == "23":
		nom = "YFI"
		a = 1
	if monnaie == "24":
		nom = "DOT"
		a = 1
	if monnaie == "m" or monnaie == "M":
		a = 1
		stream = os.system('python3 /home/yumin/Desktop/admatv2/Launcher.py')
	if monnaie != "1" and monnaie != "2" and monnaie != "3" and monnaie != "4" and monnaie != "5" and monnaie != "6" and monnaie != "7" and monnaie != "8" and monnaie != "9" and monnaie != "10" and monnaie != "11" and monnaie != "12" and monnaie != "13" and monnaie != "14" and monnaie != "15" and monnaie != "16" and monnaie != "17" and monnaie != "18" and monnaie != "19" and monnaie != "20" and monnaie != "21" and monnaie != "22" and monnaie != "23" and monnaie != "24" and monnaie != "m" and monnaie != "M":
		print(bcolors.FAIL + 'Choix non reconnu, veuillez recommencer' + bcolors.RESET)
ticker = f'X:{nom}USD'
tiker_live = f'{nom}/USD'

print(' ')
Write.Print(" CHOISSISEZ VOTRE TIME-FRAME ? : ", Colors.purple, interval=0.000)
print(' ')
print(' ')
time.sleep(0.5)

print(f'''{m}'''.replace('$', f'{m}${w}') + f'''{m}[{w}1{Fore.RESET}{m}]{Fore.RESET} NON ''')
print(f'''{m}'''.replace('$', f'{m}${w}') + f'''{m}[{w}2{Fore.RESET}{m}]{Fore.RESET} OUI ''')
print(' ')
print(' ')


b = 0
while b != 1:
	frame = input(' >>\x1B[1m ')

	if frame != "1" and frame != "2":
		print(bcolors.FAIL + 'Choix non reconnu, veuillez recommencer' + bcolors.RESET)


	if frame == "1":
		b = 1
		minute = "minute"
		hour = "hour"

		graph(5, minute, start_15m, 1, hour, start_1h)


	if frame == "2":

		b = 1
		print(' ')
		Write.Print(" CHOISSISEZ VOTRE TIME-FRAME  : ", Colors.purple, interval=0.000)
		print(' ')
		print(' ')
		time.sleep(0.5)

		print(f'''{m}'''.replace('$', f'{m}${w}') + f'''{m}[{w}1{Fore.RESET}{m}]{Fore.RESET} 1 MINUTE          ''')
		print(f'''{m}'''.replace('$', f'{m}${w}') + f'''{m}[{w}2{Fore.RESET}{m}]{Fore.RESET} 5 MINUTES          ''')
		print(f'''{m}'''.replace('$', f'{m}${w}') + f'''{m}[{w}3{Fore.RESET}{m}]{Fore.RESET} 15 MINUTES          ''')
		print(f'''{m}'''.replace('$', f'{m}${w}') + f'''{m}[{w}6{Fore.RESET}{m}]{Fore.RESET} 30 MINUTES          ''')
		print(f'''{m}'''.replace('$', f'{m}${w}') + f'''{m}[{w}4{Fore.RESET}{m}]{Fore.RESET} 1 HEURE          ''')
		print(f'''{m}'''.replace('$', f'{m}${w}') + f'''{m}[{w}5{Fore.RESET}{m}]{Fore.RESET} 6 HEURES          ''')
		print(f'''{m}'''.replace('$', f'{m}${w}') + f'''{m}[{w}7{Fore.RESET}{m}]{Fore.RESET} 1 JOUR          ''')
		print(f'''{m}'''.replace('$', f'{m}${w}') + f'''{m}[{w}8{Fore.RESET}{m}]{Fore.RESET} 1 MOI          ''')

		print(' ')
		print(' ')
		c = 0
		while c != 1:
			timea = input(' >>\x1B[1m ')

			if timea == "1":
				time1 = 1
				c = 1
				time_name1 = "minute"
			if timea == "2":
				time1 = 5
				c = 1
				time_name1 = "minute"
			if timea == "3":
				time1 = 15
				c = 1
				time_name1 = "minute"
			if timea == "4":
				time1 = 30
				c = 1
				time_name1 = "minute"
			if timea == "5":
				time1 = 1
				c = 1
				time_name1 = "hour"
			if timea == "6":
				time1 = 1
				c = 1
				time_name1 = "hour"
			if timea == "7":
				time1 = 1
				c = 1
				time_name1 = "day"
			if timea == "8":
				time1 = 1
				c = 1
				time_name1 = "month"
			if timea != "1" and timea != "2" and timea != "3" and timea != "4" and timea != "5" and timea != "6" and timea != "7" and timea != "8":
				print(bcolors.FAIL + 'Choix non reconnu, veuillez recommencer' + bcolors.RESET)

		print(' ')
		Write.Print(" CHOISSISEZ VOTRE TIME-FRAME 2  : ", Colors.purple, interval=0.000)
		print(' ')
		print(' ')
		time.sleep(0.5)

		print(f'''{m}'''.replace('$', f'{m}${w}') + f'''{m}[{w}1{Fore.RESET}{m}]{Fore.RESET} 1 MINUTE          ''')
		print(f'''{m}'''.replace('$', f'{m}${w}') + f'''{m}[{w}2{Fore.RESET}{m}]{Fore.RESET} 5 MINUTES          ''')
		print(f'''{m}'''.replace('$', f'{m}${w}') + f'''{m}[{w}3{Fore.RESET}{m}]{Fore.RESET} 15 MINUTES          ''')
		print(f'''{m}'''.replace('$', f'{m}${w}') + f'''{m}[{w}6{Fore.RESET}{m}]{Fore.RESET} 30 MINUTES          ''')
		print(f'''{m}'''.replace('$', f'{m}${w}') + f'''{m}[{w}4{Fore.RESET}{m}]{Fore.RESET} 1 HEURE          ''')
		print(f'''{m}'''.replace('$', f'{m}${w}') + f'''{m}[{w}5{Fore.RESET}{m}]{Fore.RESET} 6 HEURES          ''')
		print(f'''{m}'''.replace('$', f'{m}${w}') + f'''{m}[{w}7{Fore.RESET}{m}]{Fore.RESET} 1 JOUR          ''')
		print(f'''{m}'''.replace('$', f'{m}${w}') + f'''{m}[{w}8{Fore.RESET}{m}]{Fore.RESET} 1 MOI          ''')

		print(' ')
		print(' ')

		d = 0
		while d != 1:
			timeb = input(' >>\x1B[1m ')

			if timeb == "1":
				time2 = 1
				d = 1
				time_name2 = "minute"
			if timeb == "2":
				time2 = 5
				d = 1
				time_name2 = "minute"
			if timeb == "3":
				time2 = 15
				d = 1
				time_name2 = "minute"
			if timeb == "4":
				time2 = 30
				d = 1
				time_name2 = "minute"
			if timeb == "5":
				time2 = 1
				d = 1
				time_name2 = "hour"
			if timeb == "6":
				time2 = 1
				d = 1
				time_name2 = "hour"
			if timeb == "7":
				time2 = 1
				d = 1
				time_name2 = "day"
			if timeb == "8":
				time2 = 1
				d = 1
				time_name2 = "month"
			if timeb != "1" and  timeb != "2" and timeb != "3" and timeb != "4" and timeb != "5" and timeb != "6" and timeb != "7" and timeb != "8":
				print(bcolors.FAIL + 'Choix non reconnu, veuillez recommencer' + bcolors.RESET)

		print(' ')
		Write.Print(" CHOISSISEZ VOTRE DEPART 1: ", Colors.purple, interval=0.000)
		print(' ')
		print(' ')
		time.sleep(0.5)

		print(f'''{m}'''.replace('$', f'{m}${w}') + f'''{m}[{w}1{Fore.RESET}{m}]{Fore.RESET} START_15M          ''')
		print(f'''{m}'''.replace('$', f'{m}${w}') + f'''{m}[{w}2{Fore.RESET}{m}]{Fore.RESET} START_30M          ''')
		print(f'''{m}'''.replace('$', f'{m}${w}') + f'''{m}[{w}3{Fore.RESET}{m}]{Fore.RESET} START_1H          ''')
		print(f'''{m}'''.replace('$', f'{m}${w}') + f'''{m}[{w}6{Fore.RESET}{m}]{Fore.RESET} START_6H         ''')
		print(f'''{m}'''.replace('$', f'{m}${w}') + f'''{m}[{w}4{Fore.RESET}{m}]{Fore.RESET} START_1D          ''')
		print(f'''{m}'''.replace('$', f'{m}${w}') + f'''{m}[{w}5{Fore.RESET}{m}]{Fore.RESET} START_1WEEK          ''')
		print(f'''{m}'''.replace('$', f'{m}${w}') + f'''{m}[{w}7{Fore.RESET}{m}]{Fore.RESET} START_1MONTH          ''')

		print(' ')
		print(' ')

		e = 0
		while e != 1:
			timec = input(' >>\x1B[1m ')

			if timec == "1":
				start1 = start_15m
				e = 1
			if timec == "2":
				start1 = start_30m
				e = 1
			if timec == "3":
				start1 = start_1h
				e = 1
			if timec == "4":
				start1 = start_6h
				e = 1
			if timec == "5":
				start1 = start_1d
				e = 1
			if timec == "6":
				start1 = start_1week
				e = 1
			if timec == "7":
				start1 = start_1month
				e = 1
			if timec != "1" and  timec != "2" and timec != "3" and timec != "4" and timec != "5" and timec != "6" and timec != "7" and timec != "8":
				print(bcolors.FAIL + 'Choix non reconnu, veuillez recommencer' + bcolors.RESET)




		print(' ')
		Write.Print(" CHOISSISEZ VOTRE DEPART 2: ", Colors.purple, interval=0.000)
		print(' ')
		print(' ')
		time.sleep(0.5)

		print(f'''{m}'''.replace('$', f'{m}${w}') + f'''{m}[{w}1{Fore.RESET}{m}]{Fore.RESET} START_15M          ''')
		print(f'''{m}'''.replace('$', f'{m}${w}') + f'''{m}[{w}2{Fore.RESET}{m}]{Fore.RESET} START_30M          ''')
		print(f'''{m}'''.replace('$', f'{m}${w}') + f'''{m}[{w}3{Fore.RESET}{m}]{Fore.RESET} START_1H          ''')
		print(f'''{m}'''.replace('$', f'{m}${w}') + f'''{m}[{w}6{Fore.RESET}{m}]{Fore.RESET} START_6H         ''')
		print(f'''{m}'''.replace('$', f'{m}${w}') + f'''{m}[{w}4{Fore.RESET}{m}]{Fore.RESET} START_1D          ''')
		print(f'''{m}'''.replace('$', f'{m}${w}') + f'''{m}[{w}5{Fore.RESET}{m}]{Fore.RESET} START_1WEEK          ''')
		print(f'''{m}'''.replace('$', f'{m}${w}') + f'''{m}[{w}7{Fore.RESET}{m}]{Fore.RESET} START_1MONTH          ''')

		print(' ')
		print(' ')

		f = 0
		while f != 1:
			timed = input(' >>\x1B[1m ')

			if timed == "1":
				start2 = start_15m
				f = 1
			if timed == "2":
				start2 = start_30m
				f = 1
			if timed == "3":
				start2 = start_1h
				f = 1
			if timed == "4":
				start2 = start_6h
				f = 1
			if timed == "5":
				start2 = start_1d
				f = 1
			if timed == "6":
				start2 = start_1week
				f = 1
			if timed == "7":
				start2 = start_1month
				f = 1
			if timed != "1" and timed != "2" and timed != "3" and timed != "4" and timed != "5" and timed != "6" and timed != "7" and timed != "8":
				print(bcolors.FAIL + 'Choix non reconnu, veuillez recommencer' + bcolors.RESET)


		time.sleep(0.5)
		Write.Print(" LANCEMENT DU GRAPH  :    ", Colors.purple, interval=0.000)
		print(' ')
		print(' ')
		graph(time1, time_name1, start1, time2, time_name2, start2)





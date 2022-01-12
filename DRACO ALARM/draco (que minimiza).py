"""
import requests

url = 'https://economia.awesomeapi.com.br/json/all/USD-BRL'
url_draco = 'https://api.mir4global.com/wallet/prices/draco/lastest'
loop = 1

while loop == 1:
    response = requests.get(url).json()
    response_draco = requests.post(url_draco).json()

    print(f"Draco em dollar: {float(response_draco['Data']['USDDracoRate'])}\nDraco em reais: {float(response_draco['Data']['USDDracoRate']) * float(response['USD']['low'])}")
"""

import requests
import time
import vlc
import subprocess
import ctypes

url_draco = 'https://api.mir4global.com/wallet/prices/draco/lastest'
loop = 1
meta = float(input("Digite um valor em Draco>USD que você deseja vender: "))
metac = float(input("Digite um valor em Draco>Wemix que você deseja comprar: "))
opc = float(input("\n1- Me envie um e-mail quando o valor do draco chegar na meta;\n2- Tocar um alarme quando o valor do draco chegar na meta;\n3- Ambas;\nEscolha uma opção: "))
print ('\n')
p = vlc.MediaPlayer("./arquivos/alarm1.mp3")
p1 = vlc.MediaPlayer("./arquivos/alarm2.mp3")
kernel32 = ctypes.WinDLL('kernel32')
user32 = ctypes.WinDLL('user32')

SW_HIDE = 0
hWnd = kernel32.GetConsoleWindow()
if hWnd:
    user32.ShowWindow(hWnd, SW_HIDE)
    
while loop == 1:
    response_draco = requests.post(url_draco).json()

    print(time.strftime('%d-%m %H:%M:%S', time.localtime()))
    print(f"Draco em dólar: {float(response_draco['Data']['USDDracoRate'])}")
    print(f"Wemix em dólar: {float(response_draco['Data']['USDWemixRate'])}")
    print(f"Draco em wemix: {float(response_draco['Data']['DracoPriceWemix'])}")
    print(f'Meta venda/compra: {float(meta)} / {float(metac)}')
    if ((float(response_draco['Data']['USDDracoRate']) >= meta) or (float(response_draco['Data']['DracoPriceWemix']) <= metac)):
        SW_HIDE = 3
        if hWnd:
            user32.ShowWindow(hWnd, SW_HIDE)

        print('---ACIMA DA META!!!!!!!-------')
        if (opc == 1 or opc == 3):
            print('ENVIANDO EMAIL')
            subprocess.call([r'.\arquivos\draco.bat'])
            if (opc == 1):
                meta = 999
                metac = 0
        if (opc == 2 or opc == 3):
            print('TOCANDO ALARME')
            while loop == 1:
                p.play()
                time.sleep(30)
                p.stop()
                p1.play()
                time.sleep(30)
                p.stop()
    else:
        print('Não atingiu a meta\n')
    time.sleep(61)
    
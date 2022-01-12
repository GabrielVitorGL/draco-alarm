import requests
import time
import vlc
import subprocess
import ctypes
import sys
from PyQt5.QtWidgets import QApplication, QSystemTrayIcon, QMenu
from PyQt5.QtGui import QIcon

meta = float(input("Digite um valor em Draco>USD que você deseja vender: "))
metac = float(input("Digite um valor em Draco>Wemix que você deseja comprar: "))
opc = float(input("\n1- Me envie um e-mail quando o valor do draco chegar na meta;\n2- Tocar um alarme quando o valor do draco chegar na meta;\n3- Ambas;\nEscolha uma opção: "))
print ('\n')

url = 'https://economia.awesomeapi.com.br/json/all/USD-BRL'
url_draco = 'https://api.mir4global.com/wallet/prices/draco/lastest'
p = vlc.MediaPlayer("./arquivos/alarm1.mp3")
p1 = vlc.MediaPlayer("./arquivos/alarm2.mp3")
kernel32 = ctypes.WinDLL('kernel32')
user32 = ctypes.WinDLL('user32')
hWnd = kernel32.GetConsoleWindow()
app = QApplication(sys.argv)
trayIcon = QSystemTrayIcon(QIcon('./arquivos/draco.ico'), parent=app)
trayIcon.setToolTip('Obtendo valor, por favor aguarde')
trayIcon.show()
menu = QMenu()
exitAction = menu.addAction('Fechar')
exitAction.triggered.connect(app.quit)
trayIcon.setContextMenu(menu)

SW_HIDE = 0
if hWnd:
    user32.ShowWindow(hWnd, SW_HIDE)

loop = 1
while loop == 1:
    try:
        response = requests.get(url).json()
        response_draco = requests.post(url_draco).json()
    except:
        pass
    trayIcon.setToolTip(f"${round(float(response_draco['Data']['USDDracoRate']),2)} / R${round(float(response_draco['Data']['USDDracoRate']) * float(response['USD']['low']),2)}  R${round(297*(float(response_draco['Data']['USDDracoRate']) * float(response['USD']['low'])),2)}")

    if ((float(response_draco['Data']['USDDracoRate']) >= meta) or (float(response_draco['Data']['DracoPriceWemix']) <= metac)):
        SW_HIDE = 3
        if hWnd:
            user32.ShowWindow(hWnd, SW_HIDE)

        print(time.strftime('%d-%m %H:%M:%S', time.localtime()))
        print(f"Draco em dólar: {float(response_draco['Data']['USDDracoRate'])}")
        print(f"Wemix em dólar: {float(response_draco['Data']['USDWemixRate'])}")
        print(f"Draco em wemix: {float(response_draco['Data']['DracoPriceWemix'])}")
        print(f'Meta venda/compra: {float(meta)} / {float(metac)}')
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
    time.sleep(61)
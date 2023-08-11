import os, sys, platform, hashlib
import webbrowser
import json
import requests
import random
from PyQt6.QtCore import *
from PyQt6.QtWidgets import *
from PyQt6.QtGui import *
import secp256k1 as ice
from bloomfilter import BloomFilter
import multiprocessing
import numpy as np
import time
from mnemonic import Mnemonic
from hdwallet import HDWallet
import signal
is_windows = True if platform.system() == "Windows" else False

DEFAULT_SEED_RATIO = 45
GRID_SIZE = 16
CELL_SIZE = 30
ON_CELL_COLOR = QColor(255, 0, 0)
OFF_CELL_COLOR = QColor(255, 255, 255)

def open_web():
    webbrowser.open("https://mizogg.co.uk")

def open_telegram():
    webbrowser.open("https://t.me/CryptoCrackersUK")

mizogg = f'''
 Made by Mizogg Version 2.1  © mizogg.co.uk 2018 - 2023     

 {f"[>] Running with Python {sys.version_info[0]}.{sys.version_info[1]}.{sys.version_info[2]}"}
'''

if is_windows:
    os.system("title Mizogg @ github.com/Mizogg")
def red(text):
    os.system("")
    faded = ""
    for line in text.splitlines():
        green = 250
        for character in line:
            green -= 5
            if green < 0:
                green = 0
            faded += f"\033[38;2;255;{green};0m{character}\033[0m"
        faded += "\n"
    return faded

def win_colour(text):
    os.system("")
    faded = ""
    for line in text.splitlines():
        green = 20
        for character in line:
            green += 3
            if green < 0:
                green = 0
            faded += f"\033[38;2;255;{green};0m{character}\033[0m"
        faded += "\n"
    return faded


    os.system("")
    faded = ""
    for line in text.splitlines():
        green = 0
        for character in line:
            green += 3
            if green > 255:
                green = 255
            faded += f"\033[38;2;0;{green};255m{character}\033[0m"
        faded += "\n"
    return faded

def water(text):
    os.system("")
    faded = ""
    green = 10
    for line in text.splitlines():
        faded += f"\033[38;2;0;{green};255m{line}\033[0m\n"
        if not green == 255:
            green += 15
            if green > 255:
                green = 255
    return faded


    os.system("")
    faded = ""
    down = False

    for line in text.splitlines():
        red = 40
        for character in line:
            if down:
                red -= 3
            else:
                red += 3
            if red > 254:
                red = 255
                down = True
            elif red < 1:
                red = 30
                down = False
            faded += f"\033[38;2;{red};0;220m{character}\033[0m"
    return faded

try:
    with open('btc.bf', "rb") as fp:
        addfind = BloomFilter.load(fp)
except FileNotFoundError:
    try:
        filename = 'btc.txt'
        with open(filename) as file:
            addfind = file.read().split()
    except FileNotFoundError:
        addfind = ''

class DarkspaceScannerThread(QThread):
    btc_hunter_finished = pyqtSignal(str, str)
    grid_data_ready = pyqtSignal(list)

    def __init__(self, start_value, end_value, num_cpus):
        super().__init__()
        self.start_value = start_value
        self.end_value = end_value
        self.is_active = True
        self.num_cpus = num_cpus
        self.processes = []  # Initialize the processes list
        self.is_active = True
    
    def run(self):
        counter = 0
        is_active_flag = multiprocessing.Value('i', 1)  # 1 means active, 0 means inactive
        processes = []
        while is_active_flag.value:
            start = int(self.start_value)
            end = int(self.end_value)
            chunk_size = (end - start) // self.num_cpus
            ranges = [(start + i * chunk_size, start + (i + 1) * chunk_size) for i in range(self.num_cpus)]
            processes = []
            for i in range(self.num_cpus):
                cpu_start = ranges[i][0]
                cpu_end = ranges[i][1]
                p = multiprocessing.Process(target=generate_keys, args=(cpu_start, cpu_end, self.num_cpus, is_active_flag))
                processes.append(p)
                p.start()
            self.processes = processes  # Store the processes for later termination

            for process in processes:
                process.join()
    
    def stop(self):
        for process in self.processes:
            process.terminate()

        # Send SIGINT (Ctrl+C) signal to each process
        for process in self.processes:
            process.send_signal(signal.SIGINT)

        for process in self.processes:
            process.join()

        self.processes = []

def generate_keys(cpu_start, cpu_end, num_cpus, is_active_flag):
    try:
        keys_generated = 0
        total_keys_scanned = 0
        total_keys_scanned1 = 0
        start_time = time.time()
        group_size = 10000
        while is_active_flag.value:
            for i in range(cpu_start, cpu_end, group_size):
                private_key = random.randrange(cpu_start, cpu_end)
                P = ice.scalar_multiplication(private_key)
                current_pvk = private_key + 1
                
                Pv = ice.point_sequential_increment(group_size, P)
                keys_generated += 1*num_cpus
                
                for t in range(group_size):
                    this_btc = ice.pubkey_to_address(0, True, Pv[t*65:t*65+65])
                    process_address(this_btc, current_pvk+t)
                    total_keys_scanned += keys_generated
                    total_keys_scanned1 += keys_generated
                    
                    if time.time() - start_time >= 1 and multiprocessing.current_process()._identity[0] == 1:
                        elapsed_time = time.time() - start_time
                        speed = keys_generated / elapsed_time if elapsed_time > 0 else 0
                        formatted_speed = convert_int(speed)
                        speed1 = total_keys_scanned / elapsed_time if elapsed_time > 0 else 0
                        formatted_speed1 = convert_int(speed1)
                        description = f"CPU {num_cpus} Total/CPU={formatted_speed}Keys/Sec  GroupSize/CPU={formatted_speed1}Keys/Sec Total Keys: {total_keys_scanned1} HEX : {current_pvk+t}"
                        print(red(f"CPU {num_cpus} Total/CPU={formatted_speed}Keys/Sec  GroupSize/CPU={formatted_speed1}Keys/Sec Total Keys: {total_keys_scanned1} HEX : {current_pvk+t}"), end="")
                        keys_generated = 0
                        total_keys_scanned = 0
                        start_time = time.time()
                        
                P = Pv[-65:]
                current_pvk += group_size
                
    except KeyboardInterrupt:
        # If a Ctrl+C signal is received, exit the loop gracefully
        pass
            
def process_address(address, private_key):
    if address in addfind:
        print(win_colour(f'\nDarkFound!! Private Key: {hex(private_key)}\tAddress: {address}\n') + "")
        with open('DarkFound.txt', 'a') as result:
            result.write(f'Private Key: {hex(private_key)}\tAddress: {address}\n')   

def convert_int(num: int): 
    dict_suffix = {0: 'key', 1: 'Kkey/s', 2: 'Mkey/s', 3: 'Gkey/s', 4: 'Tkey/s', 5: 'Pkey/s', 6: 'Ekeys/s'} 
    num *= 1.0 
    idx = 0 
    for ii in range(len(dict_suffix) - 1): 
        if int(num / 1000) > 0: 
            idx += 1 
            num /= 1000 
        else: 
            break 
    return f"{num:.2f}", dict_suffix[idx]
    
class KeyspaceScannerThread(QThread):
    btc_hunter_finished = pyqtSignal(str, str)
    grid_data_ready = pyqtSignal(list)

    def __init__(self, start_value, end_value):
        super().__init__()
        self.start_value = start_value
        self.end_value = end_value
        self.is_active = True

    def stop(self):
        self.is_active = False

    def run(self):
        counter = 0
        while self.is_active:
            int_value = random.randint(self.start_value, self.end_value)
            dec = int(int_value)
            caddr = ice.privatekey_to_address(0, True, dec)  # Compressed address
            uaddr = ice.privatekey_to_address(0, False, dec)  # Uncompressed address
            p2sh = ice.privatekey_to_address(1, True, dec)  # p2sh address
            bech32 = ice.privatekey_to_address(2, True, dec)  # bech32 address
            HEX = "%064x" % dec  # Convert the decimal private key to a 64-character hexadecimal format
            wifc = ice.btc_pvk_to_wif(HEX)  # Convert the hexadecimal private key to WIF compressed format
            wifu = ice.btc_pvk_to_wif(HEX, False)  # Convert the hexadecimal private key to WIF uncompressed format
            data = (f"DEC Key: {dec}\nHEX Key: {HEX} \nBTC Address Compressed: {caddr} \nWIF Compressed: {wifc} \nBTC Address Uncompressed: {uaddr} \nWIF Uncompressed: {wifu} \nBTC Address p2sh: {p2sh} \nBTC Address Bc1: {bech32} \n")
            self.btc_hunter_finished.emit(data, 'scanning')
            counter += 1
            if caddr in addfind:
                WINTEXT = (f"DEC Key: {dec}\nHEX Key: {HEX} \nBTC Address Compressed: {caddr} \nWIF Compressed: {wifc} \n")
                self.btc_hunter_finished.emit(data, 'winner')
                with open("found.txt", "a") as f: # Write the matching information to the "found.txt" file
                    f.write(WINTEXT)
            if uaddr in addfind:
                WINTEXT = (f"DEC Key: {dec}\nHEX Key: {HEX} \nBTC Address Uncompressed: {uaddr} \nWIF Uncompressed: {wifu} \n")
                self.btc_hunter_finished.emit(data, 'winner')
                with open("found.txt", "a") as f:
                    f.write(WINTEXT)
            if p2sh in addfind:
                self.WINTEXT = (f"DEC Key: {dec}\nHEX Key: {HEX} \nBTC Address p2sh: {p2sh} \n")
                self.btc_hunter_finished.emit(data, 'winner')
                with open("found.txt", "a") as f:
                    f.write(WINTEXT)
            if bech32 in addfind:
                WINTEXT = (f"DEC Key: {dec}\nHEX Key: {HEX} \nBTC Address Bc1: {bech32} \n")
                self.btc_hunter_finished.emit(data, 'winner')
                with open("found.txt", "a") as f:
                    f.write(WINTEXT)
            if counter >= 1000:
                binstring = "{0:b}".format(int_value)
                binstring = binstring.rjust(16 * 16, "0")
                self.grid_data_ready.emit(self.grid_data(binstring))
                counter = 0

    def grid_data(self, binstring):
        grid = [[int(binstring[j]) for j in range(i * 16, (i + 1) * 16)] for i in range(16)]
        return grid

class BtcHunterThread(QThread):
    btc_hunter_finished = pyqtSignal(str, str)

    def __init__(self, grid):
        super().__init__()
        self.grid = grid

    def run(self):
        arr = np.array(self.grid)
        binstring = ''.join(''.join(map(str, l)) for l in arr)
        dec = int(binstring, 2)
        caddr = ice.privatekey_to_address(0, True, dec)  # Compressed address
        uaddr = ice.privatekey_to_address(0, False, dec)  # Uncompressed address
        p2sh = ice.privatekey_to_address(1, True, dec)  # p2sh address
        bech32 = ice.privatekey_to_address(2, True, dec)  # bech32 address
        HEX = "%064x" % dec  # Convert the decimal private key to a 64-character hexadecimal format
        wifc = ice.btc_pvk_to_wif(HEX)  # Convert the hexadecimal private key to WIF compressed format
        wifu = ice.btc_pvk_to_wif(HEX, False)  # Convert the hexadecimal private key to WIF uncompressed format
        data = (f"DEC Key: {dec}\nHEX Key: {HEX} \nBTC Address Compressed: {caddr} \nWIF Compressed: {wifc} \nBTC Address Uncompressed: {uaddr} \nWIF Uncompressed: {wifu} \nBTC Address p2sh: {p2sh} \nBTC Address Bc1: {bech32} \n")
        self.btc_hunter_finished.emit(data, 'scanning')
        if caddr in addfind:
            WINTEXT = (f"DEC Key: {dec}\nHEX Key: {HEX} \nBTC Address Compressed: {caddr} \nWIF Compressed: {wifc} \n")
            self.btc_hunter_finished.emit(data, 'winner')
            with open("found.txt", "a") as f:
                f.write(WINTEXT)
            pass
        if uaddr in addfind:
            WINTEXT = (f"DEC Key: {dec}\nHEX Key: {HEX} \nBTC Address Uncompressed: {uaddr} \nWIF Uncompressed: {wifu} \n")
            self.btc_hunter_finished.emit(data, 'winner')
            with open("found.txt", "a") as f:
                f.write(WINTEXT)
            pass
        if p2sh in addfind:
            self.WINTEXT = (f"DEC Key: {dec}\nHEX Key: {HEX} \nBTC Address p2sh: {p2sh} \n")
            self.btc_hunter_finished.emit(data, 'winner')
            with open("found.txt", "a") as f:
                f.write(WINTEXT)
            pass
        if bech32 in addfind:
            WINTEXT = (f"DEC Key: {dec}\nHEX Key: {HEX} \nBTC Address Bc1: {bech32} \n")
            self.btc_hunter_finished.emit(data, 'winner')
            with open("found.txt", "a") as f:
                f.write(WINTEXT)
            pass
    def stop(self):
        self.terminate()

    def finish(self):
        self.quit()
        self.wait()

class BtcHunterThread_online(QThread):
    btc_hunter_finished_online = pyqtSignal(str, str)

    def __init__(self, grid):
        super().__init__()
        self.grid = grid

    def run(self):
        arr = np.array(self.grid)
        binstring = ''.join(''.join(map(str, l)) for l in arr)
        dec = int(binstring, 2)
        caddr = ice.privatekey_to_address(0, True, dec)  # Compressed address
        uaddr = ice.privatekey_to_address(0, False, dec)  # Uncompressed address
        HEX = "%064x" % dec  # Convert the decimal private key to a 64-character hexadecimal format
        wifc = ice.btc_pvk_to_wif(HEX)  # Convert the hexadecimal private key to WIF compressed format
        wifu = ice.btc_pvk_to_wif(HEX, False)  # Convert the hexadecimal private key to WIF uncompressed format
        balance, totalReceived, totalSent, txs = check_balance(caddr)
        balanceu, totalReceivedu, totalSentu, txsu = check_balance(uaddr)
        data = (f"DEC Key: {dec}\nHEX Key: {HEX} \nBTC Address Compressed: {caddr} \nWIF Compressed: {wifc} \nBalance: {balance} \nTotalReceived: {totalReceived} \nTotalSent: {totalSent} \nTransactions: {txs}\n")
        data1 = (f"DEC Key: {dec}\nHEX Key: {HEX} \nBTC Address Uncompressed: {uaddr} \nWIF Uncompressed: {wifu} \nBalance: {balanceu} \nTotalReceived: {totalReceivedu} \nTotalSent: {totalSentu} \nTransactions: {txsu}\n")
        self.btc_hunter_finished_online.emit(data, 'scanning')
        self.btc_hunter_finished_online.emit(data1, 'scanningu')
        if int(txs) > 1:
            self.btc_hunter_finished_online.emit(data, 'winner')
            with open("found.txt", "a") as f:
                f.write(data)
        if int(txsu) > 1:
            self.btc_hunter_finished_online.emit(data1, 'winner')
            with open("found.txt", "a") as f:
                f.write(data1)

    def stop(self):
        self.terminate()

    def finish(self):
        self.quit()
        self.wait()
        
class KnightRiderWidget(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.timer = QTimer(self)
        self.timer.timeout.connect(self.update)
        self.position = 0
        self.direction = 1
        self.lightWidth = 20
        self.lightHeight = 10
        self.lightSpacing = 10
        self.lightColor = QColor(255, 0, 0)
        self.setContentsMargins(0, 0, 0, 0)
        self.setSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Fixed)

    def startAnimation(self):
        self.timer.start(1)

    def stopAnimation(self):
        self.timer.stop()

    def paintEvent(self, event):
        painter = QPainter(self)
        painter.setRenderHint(QPainter.RenderHint.Antialiasing)
        painter.setPen(Qt.PenStyle.NoPen)

        for i in range(12):
            lightX = self.position + i * (self.lightWidth + self.lightSpacing)
            lightRect = QRect(lightX, 0, self.lightWidth, self.lightHeight)
            painter.setBrush(self.lightColor)
            painter.drawRoundedRect(lightRect, 5, 5)

    def update(self):
        self.position += self.direction
        if self.position <= 0 or self.position >= self.width() - self.lightWidth - self.lightSpacing:
            self.direction *= -1
        self.repaint()

    def setLightColor(self, color):
        self.lightColor = color
        self.repaint()
        
class WinnerDialog(QDialog):
    def __init__(self, WINTEXT, parent=None):
        super().__init__(parent)
        self.setWindowTitle("BitcoinHunter 16x16.py")
        layout = QVBoxLayout(self)
        title_label = QLabel("⭐🔥⭐ !!!! CONGRATULATIONS !!!!! ⭐🔥⭐")
        layout.addWidget(title_label)
        informative_label = QLabel("© MIZOGG 2018 - 2023")
        layout.addWidget(informative_label)
        detail_label = QPlainTextEdit(WINTEXT)
        layout.addWidget(detail_label)
        ok_button = QPushButton("OK")
        ok_button.clicked.connect(self.accept)
        layout.addWidget(ok_button)
        self.setMinimumSize(640, 350) 

class MatrixDrop:
    def __init__(self, col, max_rows):
        self.col = col
        self.max_rows = max_rows
        self.row = random.randint(-10, -1)
        self.speed = random.randint(1, 3)

    def move(self):
        self.row += self.speed

    def is_visible(self):
        return 0 <= self.row < self.max_rows

class Smoke_up:
    def __init__(self, row, col, max_rows):
        self.row = row
        self.col = col
        self.max_rows = max_rows
        self.speed = random.randint(1, 5)
        self.ttl = random.randint(15, 30)

    def move(self):
        self.row -= self.speed
        self.ttl -= 1

    def is_visible(self):
        return 0 <= self.row < self.max_rows and self.ttl > 0

class LavaBubble:
    def __init__(self, row, col, max_rows):
        self.row = row
        self.col = col
        self.max_rows = max_rows
        self.direction = random.choice([-1, 1])
        self.speed = random.uniform(0.5, 2.0)
        self.size = random.randint(1, 3)
        self.ttl = random.randint(15, 30)

    def move(self):
        self.row += self.direction * self.speed
        self.ttl -= 1
        if random.random() < 0.1:
            self.direction *= -1

    def is_visible(self):
        return 0 <= self.row < self.max_rows and self.ttl > 0


class blocking_grid:
    def __init__(self, row, col, max_rows):
        self.row = row
        self.col = col
        self.max_rows = max_rows
        self.speed = random.randint(1, 5)
        self.ttl = random.randint(15, 30)
        self.direction = random.choice([(0, 1), (0, -1), (1, 0), (-1, 0)])

    def move(self):

        self.row += self.direction[0] * self.speed
        self.col += self.direction[1] * self.speed
        self.row = max(0, min(self.row, self.max_rows - 1))
        self.col = max(0, min(self.col, self.max_rows - 1))
        
        self.ttl -= 1

        if random.random() < 0.2:
            self.direction = random.choice([(0, 1), (0, -1), (1, 0), (-1, 0)])

    def is_visible(self):
        return 0 <= self.row < self.max_rows and self.ttl > 0
        
session = requests.Session()
session.headers.update({'User-Agent': 'Mozilla/5.0'})

def check_balance(address):
    try:
        response = session.get(f'https://btcbook.guarda.co/api/v2/address/{address}')
        if response.content:
            res = response.json()
            ress = json.dumps(res)
            resload = json.loads(ress)
            balance = resload['balance']
            totalReceived  = resload['totalReceived']
            totalSent  = resload['totalSent']
            txs = resload['txs']
            addressinfo = resload['address']
            return balance, totalReceived, totalSent, txs
        else:
            print('Empty response from API')
    except json.JSONDecodeError:
        print('Error decoding JSON response from API')
        
class App(QMainWindow):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.is_active = False
        self.in_tick = False
        self.cols = GRID_SIZE
        self.rows = GRID_SIZE
        self.size = CELL_SIZE
        self.grid = []
        self.initial_state = []
        self.tick_count = 0
        self.addr_count = 0
        self.off_cells = 0
        self.on_cells = 0
        self.count = 0
        self.off_cell_color = OFF_CELL_COLOR
        self.on_cell_color = ON_CELL_COLOR
        self.setWindowTitle('BitcoinHunter 16x16.py')
        self.setGeometry(70, 70, 900, 600)
        self.scanning = False
        self.btc_hunter_thread = None
        self.jump_forward_active = False
        self.jump_backward_active = False
        self.jump_forward_timer = QTimer(self)
        self.jump_backward_timer = QTimer(self)
        self.animation_timer = None
        self.keyspace_scanner_thread = None
        self.dark_scanner_thread = None
        self.online_check_balance = False
        self.matrix_drops = []
        self.matrix_bubbles = []
        self.blocks_work = []
        self.init_ui()

    def init_ui(self):
        self.setWindowIcon(QIcon('miz.ico'))
        self.setStyleSheet("font-size: 14px; font-family: Calibri;")
        cpu_count = multiprocessing.cpu_count()
        self.keyspace_scanner_thread = KeyspaceScannerThread(0, 0)
        self.keyspace_scanner_thread.btc_hunter_finished.connect(self.on_btc_hunter_finished)
        self.dark_scanner_thread = DarkspaceScannerThread(0, 0, 0)
        self.dark_scanner_thread.btc_hunter_finished.connect(self.on_btc_hunter_finished)
        self.matrix_timer = QTimer(self)
        self.matrix_timer.timeout.connect(self.matrix_rain)
        self.matrix_timer_random = QTimer(self)
        self.matrix_timer_random.timeout.connect(self.random_matrix)
        self.run_forever_timer = QTimer(self)
        self.run_forever_timer.timeout.connect(self.mnemonic_ran)
        self.Smoke_ups_timer = QTimer(self)
        self.Smoke_ups_timer.timeout.connect(self.Smoke_ups)
        self.Lava_bubbles_timer = QTimer(self)
        self.Lava_bubbles_timer.timeout.connect(self.Lava_bubbles)
        self.blocks_timer = QTimer(self)
        self.blocks_timer.timeout.connect(self.blocks_run)
        # Create a menu bar
        menubar = self.menuBar()
        file_menu = menubar.addMenu("File")
        # Add 'Load File' action
        load_file_action = QAction("Load File", self)
        load_file_action.triggered.connect(self.load_file)
        file_menu.addAction(load_file_action)
        file_menu.addAction("Exit", self.close)
        help_menu = menubar.addMenu("Help")
        help_menu.addAction("Help Telegram Group", open_telegram)
        help_menu.addAction("Mizogg Website", open_web)
        help_menu.addAction("About 16x16", self.show_about_dialog)

        main_layout = QVBoxLayout()
        self.centralWidget = QWidget(self)
        self.setCentralWidget(self.centralWidget)
        self.centralWidget.setSizePolicy(QSizePolicy.Policy.Fixed, QSizePolicy.Policy.Fixed)
        
        self.layout = QHBoxLayout(self.centralWidget)
        left_layout = QVBoxLayout()
        self.layout.addLayout(left_layout)
        left_layout.addLayout(main_layout)

        center_layout = QVBoxLayout()
        self.layout.addLayout(center_layout)

        image_label = QLabel(self)
        pixmap = QPixmap("mizogg.png")
        image_label.setPixmap(pixmap)
        image_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        main_layout.addWidget(image_label)
        self.welcome_label = QLabel('Welcome to ₿itcoinHunter 16x16 Crypto Scanner')
        self.welcome_label.setStyleSheet("font-size: 30px; font-weight: bold; color: red;")
        self.welcome_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        title_label = QLabel('<html><center><font size="6">❤️ Good Luck and Happy Hunting Mizogg ❤️</font></center></html>')
        title_label.setStyleSheet("QLabel { color: red; }")
        title_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        title_label1 = QLabel('<html><center><font size="6">⭐ https://mizogg.co.uk ⭐</font></center></html>')
        title_label1.setStyleSheet("QLabel { color: red; }")
        title_label1.setAlignment(Qt.AlignmentFlag.AlignCenter)
        main_layout.addWidget(self.welcome_label)
        main_layout.addWidget(title_label)
        main_layout.addWidget(title_label1)
        
        self.colourGroupBox = QGroupBox(self)
        self.colourGroupBox.setStyleSheet("QGroupBox { border: 3px solid red; padding: 7px; }")
        self.colourWidget = QWidget()
        self.colourLayout = QHBoxLayout(self.colourWidget)
        self.colorlable = QLabel('Pick Grid Colour', self)
        self.colorlable.setStyleSheet("font-size: 16px; font-weight: bold; color: red;")
        self.colorlable.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.colorlable.setAlignment(Qt.AlignmentFlag.AlignRight)
        self.colorComboBox = QComboBox(self)
        self.colorComboBox.addItem("Default Colour")
        self.colorComboBox.addItem("Option 1: White Background, Purple Box")
        self.colorComboBox.addItem("Option 2: Black Background, Green Box")
        self.colorComboBox.addItem("Option 3: White Background, Blue Box")
        self.colorComboBox.addItem("Option 4: Yellow Background, Blue Box")
        self.colorComboBox.addItem("Option 5: Red Background, Black Box")
        self.colorComboBox.addItem("Option 6: Black Background, Yellow Box")
        self.colorComboBox.currentIndexChanged.connect(self.update_knight_rider_color)
        self.colourLayout.addWidget(self.colorlable)
        self.colourLayout.addWidget(self.colorComboBox)
        self.colourGroupBox.setLayout(self.colourLayout)

        left_layout.addWidget(self.colourGroupBox)

        main_layout1 = QVBoxLayout()
        main_layout2 = QHBoxLayout()
        left_layout.addLayout(main_layout1)
        left_layout.addLayout(main_layout2)

        grid_layout = QGridLayout()
        main_layout2.addLayout(grid_layout)

        for i in range(GRID_SIZE):
            grid_layout.setColumnStretch(i, 1)
            grid_layout.setRowStretch(i, 1)

        self.scene = QGraphicsScene(self)
        self.canvas = QGraphicsView(self.scene)
        self.canvas.setSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Expanding)
        self.canvas.setVerticalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAlwaysOff)
        self.canvas.setHorizontalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAlwaysOff)
        self.canvas.setAlignment(Qt.AlignmentFlag.AlignTop | Qt.AlignmentFlag.AlignLeft)
        grid_layout.addWidget(self.canvas, 0, 0, 1, GRID_SIZE) 

        vertical_checkbox_layout = QHBoxLayout()

        self.vertical_blocking_checkboxes = []
        group_box = QGroupBox()
        group_box.setTitle("Columns")
        group_box.setStyleSheet("QGroupBox { border: 3px solid red; padding: 7px; font-size: 14px; font-weight: bold; color: black;}")

        for col in range(GRID_SIZE):
            checkboxc = QCheckBox()
            checkboxc.setStyleSheet("font-size: 14px; font-weight: bold; color: black;")
            checkboxc.setChecked(False)
            checkboxc.stateChanged.connect(self.block_lines_changed)
            col_layout = QVBoxLayout()
            label = QLabel(f"{col +1}")
            label.setAlignment(Qt.AlignmentFlag.AlignHCenter)
            col_layout.addWidget(label)
            col_layout.addWidget(checkboxc)
            self.vertical_blocking_checkboxes.append(checkboxc)
            vertical_checkbox_layout.addLayout(col_layout)
            vertical_checkbox_layout.addSpacing(10)
        self.clear_rows_checkbox = QPushButton("Clear")
        self.clear_rows_checkbox.setStyleSheet("color: blue")
        self.clear_rows_checkbox.clicked.connect(self.clear_rows)
        vertical_checkbox_layout.addWidget(self.clear_rows_checkbox) 

        vertical_checkbox_layout.addStretch(1)
        group_box.setLayout(vertical_checkbox_layout)
        main_layout1.addWidget(group_box)

        horizontal_checkbox_layout = QVBoxLayout()
        self.horizontal_blocking_checkboxes = []
        group_boxh = QGroupBox()
        group_boxh.setTitle("Rows")
        group_boxh.setStyleSheet("QGroupBox { border: 3px solid red; padding: 7px; font-size: 14px; font-weight: bold; color: black;}")
        for row in range(GRID_SIZE, 0, -1):
            checkbox = QCheckBox(f"{row}")
            checkbox.setStyleSheet("font-size: 14px; font-weight: bold; color: black;")
            checkbox.setChecked(False)
            checkbox.stateChanged.connect(self.block_lines_changed)
            self.horizontal_blocking_checkboxes.append(checkbox)
            horizontal_checkbox_layout.addWidget(checkbox)
        self.clear_columns_checkbox = QPushButton("Clear")
        self.clear_columns_checkbox.setStyleSheet("color: blue")
        self.clear_columns_checkbox.clicked.connect(self.clear_columns)
        horizontal_checkbox_layout.addWidget(self.clear_columns_checkbox)
        horizontal_checkbox_layout.addStretch(1)
        group_boxh.setLayout(horizontal_checkbox_layout)
        main_layout2.addWidget(group_boxh)

        seed_group_box = QGroupBox(self)
        seed_group_box.setTitle("Seed Configuration")
        seed_group_box.setStyleSheet("QGroupBox { border: 3px solid red; padding: 7px; font-size: 14px; font-weight: bold; color: black;}")
        seed_layout = QHBoxLayout(seed_group_box)
        self.lbl_edt_seed_ratio = QLabel('Seed Ratio % start On', self)
        seed_layout.addWidget(self.lbl_edt_seed_ratio)
        self.edt_seed_ratio = QComboBox(self)
        for i in range(1, 90):
            self.edt_seed_ratio.addItem(str(i))
        self.edt_seed_ratio.setCurrentIndex(DEFAULT_SEED_RATIO)
        seed_layout.addWidget(self.edt_seed_ratio)
        self.btn_seed = QPushButton('Seed', self)
        self.btn_seed.clicked.connect(self.seed)
        seed_layout.addWidget(self.btn_seed)
        center_layout.addWidget(seed_group_box)

        scanning_controls_group_box = QGroupBox(self)
        scanning_controls_group_box.setTitle("Scanning Controls (Inc Block Grid Lines)")
        scanning_controls_group_box.setStyleSheet("QGroupBox { border: 3px solid red; padding: 7px; font-size: 14px; font-weight: bold; color: black;}")
        scanning_controls_layout = QVBoxLayout(scanning_controls_group_box)
        buttons_layout = QVBoxLayout()
        self.inverse_button = QPushButton('Inverse Grid', self)
        self.inverse_button.setStyleSheet("color: orange")
        self.inverse_button.clicked.connect(self.inverse_grid)
        buttons_layout.addWidget(self.inverse_button)
        self.btn_clear = QPushButton('Clear')
        self.btn_clear.setStyleSheet("color: red")
        self.btn_clear.clicked.connect(self.clear_canvas)
        buttons_layout.addWidget(self.btn_clear)
        self.btn_start_stop = QPushButton('⭐Start Random Full Scan⭐ (Must click Seed First)')
        self.btn_start_stop.setStyleSheet("color: green")
        self.btn_start_stop.clicked.connect(self.start_stop)
        buttons_layout.addWidget(self.btn_start_stop)
        
        self.pattern_dropdown = QComboBox()
        self.pattern_dropdown.addItem("Conway")
        self.pattern_dropdown.addItem("High Life")
        self.pattern_dropdown.addItem("Maze")
        self.pattern_dropdown.addItem("Crystallization")
        self.pattern_dropdown.addItem("Castle Walls")
        buttons_layout.addWidget(self.pattern_dropdown)
        self.btn_game_of_life = QPushButton('Start Game of Life Patterns')
        self.btn_game_of_life.setStyleSheet("color: Green")
        self.btn_game_of_life.clicked.connect(self.start_game_of_life)
        buttons_layout.addWidget(self.btn_game_of_life)

        rain_layout = QHBoxLayout()
        rain_layout1 = QHBoxLayout()
        self.btn_matrix = QPushButton('Start Matrix Random')
        self.btn_matrix.setStyleSheet("color: green")
        self.btn_matrix.clicked.connect(self.start_stop_random)
        rain_layout.addWidget(self.btn_matrix)
        self.num_random_matrix = QComboBox()
        self.num_random_matrix.addItems(['1', '4', '6', '8', '10', '12', '14', '16'])
        self.num_random_matrix.setCurrentIndex(3)
        rain_layout.addWidget(self.num_random_matrix)
        self.btn_rain = QPushButton('Start Matrix Rain')
        self.btn_rain.setStyleSheet("color: green")
        self.btn_rain.clicked.connect(self.start_stop_matrix)
        rain_layout.addWidget(self.btn_rain)
        self.num_drops_selector = QComboBox()
        self.num_drops_selector.addItems(['1', '8', '32', '64', '128', '256', '512'])
        self.num_drops_selector.setCurrentIndex(3)
        rain_layout.addWidget(self.num_drops_selector)
        
        self.btn_Smoke_ups = QPushButton('Start Smoke')
        self.btn_Smoke_ups.setStyleSheet("color: green")
        self.btn_Smoke_ups.clicked.connect(self.start_stop_Smoke_ups)
        rain_layout.addWidget(self.btn_Smoke_ups)

        self.num_Smoke_ups_selector = QComboBox()
        self.num_Smoke_ups_selector.addItems(['1', '5', '10', '20', '30', '40', '50', '60'])
        self.num_Smoke_ups_selector.setCurrentIndex(3)
        rain_layout.addWidget(self.num_Smoke_ups_selector)
        
        self.btn_Lava_bubbles = QPushButton('Start Lava')
        self.btn_Lava_bubbles.setStyleSheet("color: green")
        self.btn_Lava_bubbles.clicked.connect(self.start_stop_Lava_bubbles)
        rain_layout1.addWidget(self.btn_Lava_bubbles)

        self.num_Lava_bubbles_selector = QComboBox()
        self.num_Lava_bubbles_selector.addItems(['1', '2', '4', '6', '8', '10', '20', '30'])
        self.num_Lava_bubbles_selector.setCurrentIndex(3)
        rain_layout1.addWidget(self.num_Lava_bubbles_selector)
        
        self.btn_blocks = QPushButton('Start Blocks')
        self.btn_blocks.setStyleSheet("color: green")
        self.btn_blocks.clicked.connect(self.start_stop_blocks)
        rain_layout1.addWidget(self.btn_blocks)

        self.num_block_selector = QComboBox()
        self.num_block_selector.addItems(['1', '2', '3', '4', '5', '6', '7', '8', '9', '10'])
        self.num_block_selector.setCurrentIndex(3)
        rain_layout1.addWidget(self.num_block_selector)
        
        scanning_controls_layout.addLayout(buttons_layout)
        scanning_controls_layout.addLayout(rain_layout)
        scanning_controls_layout.addLayout(rain_layout1)
        center_layout.addWidget(scanning_controls_group_box)

        forward_group_box = QGroupBox(self)
        forward_group_box.setTitle("Forward Scanning Configuration")
        forward_group_box.setStyleSheet("QGroupBox { border: 3px solid red; padding: 7px; font-size: 14px; font-weight: bold; color: black;}")
        forward_button_layout = QHBoxLayout(forward_group_box)
        self.forward_scaning = QComboBox(self)
        self.forward_scaning.addItems(['1', '10', '100', '1000', '10000', '100000', '1000000'])
        forward_button_layout.addWidget(self.forward_scaning)
        self.start_button_forward = QPushButton('✅Start Forward✅', self)
        self.start_button_forward.setStyleSheet("color: green")
        self.start_button_forward.clicked.connect(self.start_stop_jump_forward)
        forward_button_layout.addWidget(self.start_button_forward)

        center_layout.addWidget(forward_group_box)

        backward_group_box = QGroupBox(self)
        backward_group_box.setTitle("Backward Scanning Configuration")
        backward_group_box.setStyleSheet("QGroupBox { border: 3px solid red; padding: 7px; font-size: 14px; font-weight: bold; color: black;}")
        backward_button_layout = QHBoxLayout(backward_group_box)
        self.backwards_scaning = QComboBox(self)
        self.backwards_scaning.addItems(['1', '10', '100', '1000', '10000', '100000', '1000000'])
        backward_button_layout.addWidget(self.backwards_scaning)
        self.start_button_backward = QPushButton('✅Start Backwards✅', self)
        self.start_button_backward.setStyleSheet("color: green")
        self.start_button_backward.clicked.connect(self.start_stop_jump_backward)
        backward_button_layout.addWidget(self.start_button_backward)
        
        center_layout.addWidget(backward_group_box)
        
        self.speedGroupBox = QGroupBox(self)
        self.speedGroupBox.setTitle("Speed Left faster Right Slower")
        self.speedGroupBox.setStyleSheet("QGroupBox { border: 3px solid red; padding: 7px; font-size: 14px; font-weight: bold; color: black;}")
        speed_layout = QHBoxLayout(self.speedGroupBox)
        self.speed_slider = QSlider(Qt.Orientation.Horizontal)
        self.speed_slider.setMinimum(0)
        self.speed_slider.setMaximum(200)
        self.speed_slider_value_display = QLabel(self)
        speed_layout.addWidget(self.speed_slider)
        speed_layout.addWidget(self.speed_slider_value_display)
        center_layout.addWidget(self.speedGroupBox)
        self.speed_slider.valueChanged.connect(self.update_speed_label)
        
        self.knightRiderWidget = KnightRiderWidget(self)
        self.knightRiderWidget.setSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Fixed)
        self.knightRiderWidget.setMinimumHeight(25)
        self.knightRiderLayout = QHBoxLayout()
        self.knightRiderLayout.setContentsMargins(10, 10, 10, 10)
        self.knightRiderLayout.addWidget(self.knightRiderWidget)

        self.knightRiderGroupBox = QGroupBox(self)
        self.knightRiderGroupBox.setTitle("Running Process ")
        self.knightRiderGroupBox.setStyleSheet("QGroupBox { border: 3px solid red; padding: 7px; font-size: 14px; font-weight: bold; color: black;}")
        self.knightRiderGroupBox.setLayout(self.knightRiderLayout)
        self.mizogg_label = QLabel(mizogg, self)
        self.mizogg_label.setStyleSheet("font-size: 17px; font-weight: bold; color: red;")
        self.mizogg_label.setAlignment(Qt.AlignmentFlag.AlignCenter)

        right_layout = QVBoxLayout()
        self.layout.addLayout(right_layout)
        labels_starting = QHBoxLayout()
        self.add_count_label = QLabel(self.count_add())
        self.add_count_label.setStyleSheet("font-size: 14px; font-weight: bold; color: black;")
        self.online_check_box = QCheckBox("🔞Check Balance Online🔞")
        self.online_check_box.setStyleSheet("font-size: 14px; font-weight: bold; color: red;")
        self.online_check_box.setChecked(False)
        labels_starting.addWidget(self.add_count_label)
        labels_starting.addWidget(self.online_check_box)
        right_layout.addLayout(labels_starting)
        
        labels_layout = QVBoxLayout()
        self.lbl_tick_no = QLabel('🔑 Total Private Keys Scanned 🔑: 0')
        self.lbl_tick_no.setStyleSheet("font-size: 14px; font-weight: bold; color: black;")
        labels_layout.addWidget(self.lbl_tick_no)
        self.lbl_total_no = QLabel('₿ Total Addresses Scanned ₿: 0')
        self.lbl_total_no.setStyleSheet("font-size: 14px; font-weight: bold; color: black;")
        labels_layout.addWidget(self.lbl_total_no)
        right_layout.addLayout(labels_layout)

        self.keyspaceGroupBox = QGroupBox(self)
        self.keyspaceGroupBox.setTitle("Key Space Configuration")
        self.keyspaceGroupBox.setStyleSheet("QGroupBox { border: 3px solid red; padding: 7px; font-size: 14px; font-weight: bold; color: black;}")

        keyspaceMainLayout = QVBoxLayout(self.keyspaceGroupBox)
        keyspaceLayout = QHBoxLayout()
        self.keyspaceLabel = QLabel("Random Key Space Range:", self)
        keyspaceLayout.addWidget(self.keyspaceLabel)
        self.keyspaceLineEdit = QLineEdit("20000000000000000:3ffffffffffffffff", self)
        self.keyspaceLineEdit.setPlaceholderText('Example range for 66 = 20000000000000000:3ffffffffffffffff')
        self.btn_start_keyspace = QPushButton('⭐Start Key Space⭐')
        self.btn_start_keyspace.clicked.connect(self.keyspace)
        keyspaceLayout.addWidget(self.btn_start_keyspace)
        keyspaceLayout.addWidget(self.keyspaceLineEdit)
        
        keyspacerange_layout = QHBoxLayout()
        self.keyspace_slider = QSlider(Qt.Orientation.Horizontal)
        self.keyspace_slider.setMinimum(1)
        self.keyspace_slider.setMaximum(256)
        self.keyspace_slider.setValue(66)
        self.slider_value_display = QLabel(self)
        keyspacerange_layout.addWidget(self.keyspace_slider)
        keyspacerange_layout.addWidget(self.slider_value_display)
        
        keyspaceMainLayout.addLayout(keyspaceLayout)
        keyspaceMainLayout.addLayout(keyspacerange_layout)
        self.keyspace_slider.valueChanged.connect(self.update_keyspace_range)
        
        keyspaceLayout2 = QHBoxLayout()

        input_win = QLabel("Visualize Your Own Private Key:", self)
        keyspaceLayout2.addWidget(input_win)
        self._btc_bin = QPushButton("Start Visualize", self)
        self._btc_bin.clicked.connect(self.update_grid)
        keyspaceLayout2.addWidget(self._btc_bin)
        
        keyspaceLayout3 = QHBoxLayout()
        self._txt_inputhex = QLineEdit(self)
        self._txt_inputhex.setText('2ffffffffffffffff')
        self._txt_inputhex.setFocus()
        keyspaceLayout3.addWidget(self._txt_inputhex)

        keyspaceMainLayout.addLayout(keyspaceLayout2)
        keyspaceMainLayout.addLayout(keyspaceLayout3)

        self.keyspaceGroupBox1 = QGroupBox(self)
        self.keyspaceGroupBox1.setTitle("Visualize Brain Wallet or Mnemonic Words ")
        self.keyspaceGroupBox1.setStyleSheet("QGroupBox { border: 3px solid red; padding: 7px; font-size: 14px; font-weight: bold; color: black;}")
        keyspaceMainLayout1 = QVBoxLayout(self.keyspaceGroupBox1)
        self.brain_input = QLineEdit(self)
        self.brain_input.setPlaceholderText("Enter your words here...")
        keyspaceMainLayout1.addWidget(self.brain_input)
        self.enter_button = QPushButton("Brain Wallet Enter", self)
        self.enter_button.setStyleSheet("color: blue")
        self.enter_button.clicked.connect(self.brain_inc)
        keyspaceMainLayout1.addWidget(self.enter_button)

        Mnemonic_button_layout = QHBoxLayout()
        self.enter_button1 = QPushButton("Mnemonic Words Enter", self)
        self.enter_button1.setStyleSheet("color: blue")
        self.enter_button1.clicked.connect(self.mnemonic_inc)
        
        start_button = QPushButton('Random Mnemonic')
        start_button.setStyleSheet("color: blue")
        start_button.clicked.connect(self.mnemonic_ran)
        
        # Add the new button and connect it to the new slot
        self.forever_button = QPushButton("⭐Generate Mnemonic's⭐")
        self.forever_button.setStyleSheet("color: green")
        self.forever_button.clicked.connect(lambda: self.toggle_run_forever())
        Mnemonic_button_layout.addWidget(self.enter_button1)
        Mnemonic_button_layout.addWidget(start_button)
        Mnemonic_button_layout.addWidget(self.forever_button)
        keyspaceMainLayout1.addLayout(Mnemonic_button_layout)
        
        
        radio_button_layout = QHBoxLayout()
        ammount_words_label = QLabel('Amount of words:')
        radio_button_layout.addWidget(ammount_words_label)
        self.ammount_words = QComboBox()
        self.ammount_words.addItems(['random', '12', '15', '18', '21', '24'])
        self.ammount_words.setCurrentIndex(1)
        radio_button_layout.addWidget(self.ammount_words)
        lang_words_label = QLabel('Language:')
        radio_button_layout.addWidget(lang_words_label)
        self.lang_words = QComboBox()
        self.lang_words.addItems(['random', 'english', 'french', 'italian', 'spanish', 'chinese_simplified', 'chinese_traditional', 'japanese', 'korean'])
        self.lang_words.setCurrentIndex(1)
        radio_button_layout.addWidget(self.lang_words)
        div_label = QLabel('Derivations:')
        radio_button_layout.addWidget(div_label)
        self.derivation_choice = QComboBox()
        self.derivation_choice.addItems(['1', '2', '5', '10', '20', '50', '100'])
        radio_button_layout.addWidget(self.derivation_choice)
        keyspaceMainLayout1.addLayout(radio_button_layout)
        center_layout.addWidget(self.keyspaceGroupBox)
        center_layout.addWidget(self.keyspaceGroupBox1)

        hex_label = QLabel('Current HEX value:')
        hex_label.setStyleSheet("font-size: 14px; font-weight: bold; color: black;")
        self.value_edit_hex = QLineEdit()
        self.value_edit_hex.setReadOnly(True)
        
        address_layout_caddr = QHBoxLayout()
        bitcoin_address_label = QLabel('Current ₿itcoin Compressed:')
        bitcoin_address_label.setStyleSheet("font-size: 14px; font-weight: bold; color: black;")
        self.btc_address_edit = QLineEdit()
        self.btc_address_edit.setReadOnly(True)
        address_layout_caddr.addWidget(bitcoin_address_label)
        open_button = QPushButton("Open in Browser")
        open_button.setStyleSheet("color: blue")
        open_button.clicked.connect(lambda: self.open_browser(str(self.btc_address_edit.text())))
        address_layout_caddr.addWidget(open_button)
        
        address_layout_uaddr = QHBoxLayout()
        bitcoin_address_labelu = QLabel('Current ₿itcoin Uncompressed:')
        bitcoin_address_labelu.setStyleSheet("font-size: 14px; font-weight: bold; color: black;")
        self.btc_address_editu = QLineEdit()
        self.btc_address_editu.setReadOnly(True)
        address_layout_uaddr.addWidget(bitcoin_address_labelu)
        open_button = QPushButton("Open in Browser")
        open_button.setStyleSheet("color: blue")
        open_button.clicked.connect(lambda: self.open_browser(str(self.btc_address_editu.text())))
        address_layout_uaddr.addWidget(open_button)
        
        address_layout_p2sh = QHBoxLayout()
        bitcoin_address_labelp2sh = QLabel('Current ₿itcoin P2SH :')
        bitcoin_address_labelp2sh.setStyleSheet("font-size: 14px; font-weight: bold; color: black;")
        self.btc_address_editp2sh = QLineEdit()
        self.btc_address_editp2sh.setReadOnly(True)
        address_layout_p2sh.addWidget(bitcoin_address_labelp2sh)
        open_button = QPushButton("Open in Browser")
        open_button.setStyleSheet("color: blue")
        open_button.clicked.connect(lambda: self.open_browser(str(self.btc_address_editp2sh.text())))
        address_layout_p2sh.addWidget(open_button)
        
        address_layout_bc1 = QHBoxLayout()
        bitcoin_address_labelbc1 = QLabel('Current ₿itcoin Bc1 :')
        bitcoin_address_labelbc1.setStyleSheet("font-size: 14px; font-weight: bold; color: black;")
        self.btc_address_editbc1 = QLineEdit()
        self.btc_address_editbc1.setReadOnly(True)
        address_layout_bc1.addWidget(bitcoin_address_labelbc1)
        open_button = QPushButton("Open in Browser")
        open_button.setStyleSheet("color: blue")
        open_button.clicked.connect(lambda: self.open_browser(str(self.btc_address_editbc1.text())))
        address_layout_bc1.addWidget(open_button)

        dec_label = QLabel('Current DEC value:')
        dec_label.setStyleSheet("font-size: 14px; font-weight: bold; color: black;")
        self.value_edit_dec = QLineEdit()
        self.value_edit_dec.setReadOnly(True)
        wif_label = QLabel('Current Compressed WIF :')
        wif_label.setStyleSheet("font-size: 14px; font-weight: bold; color: black;")
        self.value_edit_wif = QLineEdit()
        self.value_edit_wif.setReadOnly(True)
        wif_labelu = QLabel('Current Unompressed WIF :')
        wif_labelu.setStyleSheet("font-size: 14px; font-weight: bold; color: black;")
        self.value_edit_wifu = QLineEdit()
        self.value_edit_wifu.setReadOnly(True)

        balance_transactions_layout = QHBoxLayout()
        balance_label = QLabel('Balance:')
        balance_label.setStyleSheet("font-size: 14px; font-weight: bold; color: black;")
        self.balance_label_edit = QLineEdit()
        self.balance_label_edit.setReadOnly(True)
        balance_transactions_layout.addWidget(balance_label)
        balance_transactions_layout.addWidget(self.balance_label_edit)

        transactions_label = QLabel('Transactions:')
        transactions_label.setStyleSheet("font-size: 14px; font-weight: bold; color: black;")
        self.transactions_label_edit = QLineEdit()
        self.transactions_label_edit.setReadOnly(True)
        balance_transactions_layout.addWidget(transactions_label)
        balance_transactions_layout.addWidget(self.transactions_label_edit)
        
        received_sent_layout = QHBoxLayout()
        totalReceived_label = QLabel('TotalReceived:')
        totalReceived_label.setStyleSheet("font-size: 14px; font-weight: bold; color: black;")
        self.totalReceived_label_edit = QLineEdit()
        self.totalReceived_label_edit.setReadOnly(True)
        received_sent_layout.addWidget(totalReceived_label)
        received_sent_layout.addWidget(self.totalReceived_label_edit)

        totalSent_label = QLabel('TotalSent:')
        totalSent_label.setStyleSheet("font-size: 14px; font-weight: bold; color: black;")
        self.totalSent_label_edit = QLineEdit()
        self.totalSent_label_edit.setReadOnly(True)
        received_sent_layout.addWidget(totalSent_label)
        received_sent_layout.addWidget(self.totalSent_label_edit)
        
        right_layout.addWidget(hex_label)
        right_layout.addWidget(self.value_edit_hex)
        right_layout.addWidget(dec_label)
        right_layout.addWidget(self.value_edit_dec)
        right_layout.addLayout(address_layout_caddr)
        right_layout.addWidget(self.btc_address_edit)
        right_layout.addWidget(wif_label)
        right_layout.addWidget(self.value_edit_wif)
        right_layout.addLayout(address_layout_uaddr)
        right_layout.addWidget(self.btc_address_editu)
        right_layout.addWidget(wif_labelu)
        right_layout.addWidget(self.value_edit_wifu)
        right_layout.addLayout(address_layout_p2sh)
        right_layout.addWidget(self.btc_address_editp2sh)
        right_layout.addLayout(address_layout_bc1)
        right_layout.addWidget(self.btc_address_editbc1)
        right_layout.addLayout(balance_transactions_layout)
        right_layout.addLayout(received_sent_layout)
        
        dark_button_layout = QHBoxLayout()
        self.dark_start_keyspace = QPushButton()
        self.dark_start_keyspace.setText('🔥Start Dark Space🔥')
        self.dark_start_keyspace.setStyleSheet("color: green")
        self.dark_start_keyspace.clicked.connect(self.darkspace)
        dark_button_layout.addWidget(self.dark_start_keyspace)
        cpu_label = QLabel('Number of CPUS :')
        cpu_label.setStyleSheet("color: blue")
        dark_button_layout.addWidget(cpu_label)
        self.cpu_box = QComboBox()
        for i in range(1, cpu_count + 1):
            self.cpu_box.addItem(str(i))
        dark_button_layout.addWidget(self.cpu_box)
        right_layout.addLayout(dark_button_layout)
        right_layout.addWidget(self.knightRiderGroupBox)
        right_layout.addWidget(self.mizogg_label)
        main_layout.addStretch()
        self.canvas.mousePressEvent = self.canvas_click
        self.canvas.mousePressEvent = self.canvas_mouse_press_event
        self.canvas.mouseMoveEvent = self.canvas_mouse_move_event
        self.canvas.mouseReleaseEvent = self.canvas_mouse_release_event
        self.show()
    
    def update_speed_label(self):
        actual_speed = self.speed_slider.value()
        self.speed_slider_value_display.setText(str(actual_speed))
    
    def open_browser(self, address):
        url = f'https://www.blockchain.com/explorer/addresses/btc/{address}'
        webbrowser.open(url)

    def inverse_grid(self):
        for rw in range(self.rows):
            for cl in range(self.cols):
                self.grid[rw][cl] = 1 - self.grid[rw][cl]
        self.update_canvas()

    def show_about_dialog(self):
        QMessageBox.about(self, "About 16x16Hunter", mizogg)
        pass

    def start(self):
        self.init_grid()
        self.clear_canvas()
        app.exec()
        pass
    
    def count_add(self):
        addr_data = len(addfind)
        addr_count_print = f'Total BTC Addresses Loaded and Checking : {addr_data}'
        return addr_count_print
        
    def update_grid_from_key(self, int_value):
        binstring = "{0:b}".format(int_value)
        binstring = binstring.rjust(self.rows * self.cols, "0")
        for i in range(self.rows):
            self.grid[i] = [int(binstring[j]) for j in range(i * self.cols, (i + 1) * self.cols)]
    
    @pyqtSlot(list)
    def grid_data_ready(self, grid_data):
        self.grid = grid_data
        self.update_canvas()
     
    def update_keyspace_range(self, value):
        start_range = hex(2**(value - 1))[2:]
        end_range = hex(2**value - 1)[2:]
        self.keyspaceLineEdit.setText(f"{start_range}:{end_range}")
        self._txt_inputhex.setText(f"{start_range}")
        self.slider_value_display.setText(str(value))
        self.update_grid()

    def keyspace(self):
        key_space_range = self.keyspaceLineEdit.text().strip()
        start_hex, end_hex = key_space_range.split(':')

        try:
            start_value = int(start_hex, 16)
            end_value = int(end_hex, 16)
        except InvalidOperation:
            self.pop_Result("⚠️Invalid key space range. Please enter a valid hexadecimal range.⚠️")
            return
        if start_value > end_value:
            self.pop_Result("⚠️Invalid key space range. Start value must be less than or equal to end value.⚠️")
            return
        if self.keyspace_scanner_thread and self.keyspace_scanner_thread.isRunning():
            self.keyspace_scanner_thread.stop()
            self.keyspace_scanner_thread.wait()
            self.keyspace_scanner_thread = None
            self.btn_start_keyspace.setText('⭐Start Key Space⭐')
            self.btn_start_keyspace.setStyleSheet("color: green")
            self.scanning = False
            self.knightRiderWidget.stopAnimation()
        else:
            self.keyspace_scanner_thread = KeyspaceScannerThread(start_value, end_value)
            self.keyspace_scanner_thread.btc_hunter_finished.connect(self.on_btc_hunter_finished)
            self.keyspace_scanner_thread.grid_data_ready.connect(self.grid_data_ready)
            self.keyspace_scanner_thread.start()
            self.btn_start_keyspace.setText('🚫Stop Key Space🚫')
            self.btn_start_keyspace.setStyleSheet("color: red")
            self.scanning = True
            self.knightRiderWidget.startAnimation()
        self.btn_start_stop.setEnabled(True)
        
    def darkspace(self):
        key_space_range = self.keyspaceLineEdit.text().strip()
        start_hex, end_hex = key_space_range.split(':')
        num_cpus = int(self.cpu_box.currentText())
        try:
            start_value = int(start_hex, 16)
            end_value = int(end_hex, 16)
        except InvalidOperation:
            self.pop_Result("Invalid key space range. Please enter a valid hexadecimal range.")
            return
        if start_value > end_value:
            self.pop_Result("Invalid key space range. Start value must be less than or equal to end value.")
            return
        if self.dark_scanner_thread and self.dark_scanner_thread.isRunning():
            self.dark_scanner_thread.stop()
            self.dark_scanner_thread.wait()
            self.dark_scanner_thread = None
            self.dark_start_keyspace.setText('🔥Start Dark Space🔥')
            self.dark_start_keyspace.setStyleSheet("color: green")
            self.scanning = False
            self.knightRiderWidget.stopAnimation()
        else:
            self.dark_scanner_thread = DarkspaceScannerThread(start_value, end_value, num_cpus)
            self.dark_scanner_thread.btc_hunter_finished.connect(self.on_btc_hunter_finished)
            self.dark_scanner_thread.grid_data_ready.connect(self.grid_data_ready)
            self.dark_scanner_thread.start()
            self.dark_start_keyspace.setText('🚫Stop Dark Space🚫 (Will Close GUI)')
            self.dark_start_keyspace.setStyleSheet("color: red")
            self.scanning = True
            self.knightRiderWidget.startAnimation()
        self.btn_start_stop.setEnabled(True)
        
    def seed_inc(self):
        if self.in_tick:
            return
        self.in_tick = True
        self.on_cells = 0
        self.off_cells = 0
        self.scene.clear()
        int_value = int(self._txt_inputhex.text(), 16)
        self.scanning_speed = self.speed_slider.value()
        self.update_grid_from_key(int_value)
        for rw in range(self.rows):
            for cl in range(self.cols):
                if self.grid[rw][cl]:
                    color = self.on_cell_color
                    self.on_cells += 1
                else:
                    color = self.off_cell_color
                    self.off_cells += 1
                self.put_rect(self.scene, rw, cl, color)

        self.update_canvas()
        self.in_tick = False

        if self.is_active:
            QTimer.singleShot(self.scanning_speed, self.seed_inc)
    
    def brain_inc(self):
        brainwords = self.brain_input.text().strip()

        if not brainwords:
            return

        try:
            int_value = int.from_bytes(hashlib.sha256(brainwords.encode()).digest(), byteorder='big')
            hex_value = "%064x" % int_value
            self._txt_inputhex.setText(hex_value)
            self.update_grid_from_key(int_value)
            self.seed_inc()
        except ValueError:
            self.pop_Result("Invalid Brainwords. Please enter a valid brainwords.")
            return
    
    def mnemonic_inc(self):
        if self.in_tick:
            return
        self.in_tick = True
        self.on_cells = 0
        self.off_cells = 0
        self.scene.clear()
        self.div_input = int(self.derivation_choice.currentText())
        derivation = "m/44'/0'/0'/0"
        words = self.brain_input.text().strip()
        self.scanning_speed = self.speed_slider.value()
        try:
            hdwallet = HDWallet().from_mnemonic(words)
            wallet = hdwallet.from_mnemonic(words)
            for p in range(0, self.div_input):
                path = f"{derivation}/{p}"
                hdwallet.from_path(path=path)
                path_read = hdwallet.path()
                private_key = hdwallet.private_key()
                int_value = int(private_key, 16)
                self._txt_inputhex.setText(private_key)
                self.update_grid_from_key(int_value)

                for rw in range(self.rows):
                    for cl in range(self.cols):
                        if self.grid[rw][cl]:
                            color = self.on_cell_color
                            self.on_cells += 1
                        else:
                            color = self.off_cell_color
                            self.off_cells += 1
                        self.put_rect(self.scene, rw, cl, color)

                self.update_canvas()
                self.in_tick = False
                self.update_labels()
                self.btc_hunter()

                if self.is_active:
                    QTimer.singleShot(self.scanning_speed, self.seed_inc)
        except Exception as e:
            self.pop_Result("Error: " + str(e))
    
    
    def start_run_forever(self):
        self.scanning_speed = self.speed_slider.value()
        self.run_forever_timer.start(self.scanning_speed)

    def stop_run_forever(self):
        # Stop the timer to halt the repeated execution of `mnemonic_ran`
        self.run_forever_timer.stop()

    def toggle_run_forever(self):
        if self.run_forever_timer.isActive():
            # Timer is active, stop it
            self.stop_run_forever()
            self.forever_button.setText("⭐Generate Mnemonic's⭐")
        else:
            # Timer is not active, start it
            self.start_run_forever()
            self.forever_button.setText("🚫Stop Mnemonic's🚫")

            
    def mnemonic_ran(self):
        if self.in_tick:
            return
        self.in_tick = True
        self.on_cells = 0
        self.off_cells = 0
        self.scene.clear()
        self.div_input = int(self.derivation_choice.currentText())
        self.scanning_speed = self.speed_slider.value()
        derivation = "m/44'/0'/0'/0"
        try:
            if self.lang_words.currentText() == 'random':
                lang = random.choice(['english', 'french', 'italian', 'spanish', 'chinese_simplified', 'chinese_traditional', 'japanese', 'korean'])
            else:
                lang = self.lang_words.currentText()
            
            if self.ammount_words.currentText() == 'random':
                word_length = random.choice([12, 15, 18, 21, 24])
            else:
                word_length = int(self.ammount_words.currentText())
            
            strengths = {
                12: 128,
                15: 160,
                18: 192,
                21: 224,
                24: 256
            }
            strength = strengths[word_length]
            mnemonic = Mnemonic(lang)
            words = mnemonic.generate(strength=strength)
            hdwallet = HDWallet().from_mnemonic(words)
            wallet = hdwallet.from_mnemonic(words)
            for p in range(0, self.div_input):
                path = f"{derivation}/{p}"
                hdwallet.from_path(path=path)
                path_read = hdwallet.path()
                private_key = hdwallet.private_key()
                int_value = int(private_key, 16)
                self._txt_inputhex.setText(private_key)
                self.update_grid_from_key(int_value)

                for rw in range(self.rows):
                    for cl in range(self.cols):
                        if self.grid[rw][cl]:
                            color = self.on_cell_color
                            self.on_cells += 1
                        else:
                            color = self.off_cell_color
                            self.off_cells += 1
                        self.put_rect(self.scene, rw, cl, color)
                self.brain_input.setText(words)
                self.update_canvas()
                self.in_tick = False
                self.update_labels()
                self.btc_hunter()

                if self.is_active:
                    QTimer.singleShot(self.scanning_speed, self.seed_inc)
            pass
        except Exception as e:
            self.pop_Result("Error: " + str(e))
            
    def start_stop_jump_forward(self):
        self.scanning_speed = self.speed_slider.value()
        if self.jump_forward_active:
            self.jump_forward_active = False
            self.jump_forward_timer.stop()
            self.start_button_forward.setText('✅Start Forward✅')
            self.start_button_forward.setStyleSheet("color: green")
            self.scanning = False
            self.knightRiderWidget.stopAnimation()
        else:
            selected_increment = int(self.forward_scaning.currentText())
            self.jump_forward_active = True
            self.jump_forward_timer.timeout.connect(lambda: self.seed_inc_increment(selected_increment))
            self.jump_forward_timer.start(self.scanning_speed)
            self.start_button_forward.setText('🚫Stop Forward🚫')
            self.start_button_forward.setStyleSheet("color: red")
            self.scanning = True
            self.knightRiderWidget.startAnimation()

    def start_stop_jump_backward(self):
        self.scanning_speed = self.speed_slider.value()
        if self.jump_backward_active:
            self.jump_backward_active = False
            self.jump_backward_timer.stop()
            self.start_button_backward.setText('✅Start Backwards✅')
            self.start_button_backward.setStyleSheet("color: green")
            self.scanning = False
            self.knightRiderWidget.stopAnimation()
        else:
            selected_increment = int(self.backwards_scaning.currentText())
            self.jump_backward_active = True
            self.jump_backward_timer.timeout.connect(lambda: self.seed_inc_increment(-selected_increment))
            self.jump_backward_timer.start(self.scanning_speed)
            self.start_button_backward.setText('🚫Stop Backwards🚫')
            self.start_button_backward.setStyleSheet("color: red")
            self.scanning = True
            self.knightRiderWidget.startAnimation()

    def seed_inc_increment(self, increment):
        try:
            hex_value = int(self._txt_inputhex.text(), 16)
            hex_value += increment
            self._txt_inputhex.setText(f"{hex_value:x}")
            self.update_grid_from_key(hex_value)
            self.seed_inc()
        except ValueError:
            self.pop_Result("Invalid Hex Value Please enter a valid hexadecimal value")

    def btc_hunter(self):
        if self.online_check_box.isChecked():
            if self.btc_hunter_thread:
                self.btc_hunter_thread.quit()
                self.btc_hunter_thread.wait()
            self.btc_hunter_thread = BtcHunterThread_online(self.grid)
            self.btc_hunter_thread.btc_hunter_finished_online.connect(self.on_btc_hunter_finished_online)
            self.btc_hunter_thread.start()
        else:
            if self.btc_hunter_thread:
                self.btc_hunter_thread.quit()
                self.btc_hunter_thread.wait()
            self.btc_hunter_thread = BtcHunterThread(self.grid)
            self.btc_hunter_thread.btc_hunter_finished.connect(self.on_btc_hunter_finished)
            self.btc_hunter_thread.start()

    def on_btc_hunter_finished(self, data, returncode):
        if returncode == 'scanning':
            self.value_edit_dec.setText(data.split("\n")[0].split(":")[1].strip())
            self.value_edit_hex.setText(data.split("\n")[1].split(":")[1].strip())
            self.btc_address_edit.setText(data.split("\n")[2].split(":")[1].strip())
            self.value_edit_wif.setText(data.split("\n")[3].split(":")[1].strip())
            self.btc_address_editu.setText(data.split("\n")[4].split(":")[1].strip())
            self.value_edit_wifu.setText(data.split("\n")[5].split(":")[1].strip())
            self.btc_address_editp2sh.setText(data.split("\n")[6].split(":")[1].strip())
            self.btc_address_editbc1.setText(data.split("\n")[7].split(":")[1].strip())
            self.balance_label_edit.setText('')
            self.transactions_label_edit.setText('')
            self.totalReceived_label_edit.setText('')
            self.totalSent_label_edit.setText('')
            self.tick_count += 1
            self.addr_count += 4
            self.update_labels()
        elif returncode == 'winner':
            winner_dialog = WinnerDialog(data, self)
            winner_dialog.exec()
        if self.btc_hunter_thread:
            self.btc_hunter_thread.finish()
            self.btc_hunter_thread.deleteLater()
        self.btc_hunter_thread = None
    
    def on_btc_hunter_finished_online(self, data, returncode):
        if returncode == 'scanning':
            self.value_edit_dec.setText(data.split("\n")[0].split(":")[1].strip())
            self.value_edit_hex.setText(data.split("\n")[1].split(":")[1].strip())
            self.btc_address_edit.setText(data.split("\n")[2].split(":")[1].strip())
            self.value_edit_wif.setText(data.split("\n")[3].split(":")[1].strip())
            self.btc_address_editp2sh.setText('')
            self.btc_address_editbc1.setText('')
            self.balance_label_edit.setText(data.split("\n")[4].split(":")[1].strip())
            self.transactions_label_edit.setText(data.split("\n")[7].split(":")[1].strip())
            self.totalReceived_label_edit.setText(data.split("\n")[5].split(":")[1].strip())
            self.totalSent_label_edit.setText(data.split("\n")[6].split(":")[1].strip())
            self.tick_count += 0.5
            self.addr_count += 1
            self.update_labels()
        elif returncode == 'scanningu':
            self.value_edit_dec.setText(data.split("\n")[0].split(":")[1].strip())
            self.value_edit_hex.setText(data.split("\n")[1].split(":")[1].strip())
            self.btc_address_editu.setText(data.split("\n")[2].split(":")[1].strip())
            self.value_edit_wifu.setText(data.split("\n")[3].split(":")[1].strip())
            self.btc_address_editp2sh.setText('')
            self.btc_address_editbc1.setText('')
            self.balance_label_edit.setText(data.split("\n")[4].split(":")[1].strip())
            self.transactions_label_edit.setText(data.split("\n")[7].split(":")[1].strip())
            self.totalReceived_label_edit.setText(data.split("\n")[5].split(":")[1].strip())
            self.totalSent_label_edit.setText(data.split("\n")[6].split(":")[1].strip())
            self.tick_count += 0.5
            self.addr_count += 1
            self.update_labels()
        elif returncode == 'winner':
            winner_dialog = WinnerDialog(data, self)
            winner_dialog.exec()
        if self.btc_hunter_thread:
            self.btc_hunter_thread.finish()
            self.btc_hunter_thread.deleteLater()
        self.btc_hunter_thread = None
        
    def init_grid(self):
        self.grid = [[0 for x in range(self.cols)] for y in range(self.rows)]

    def update_canvas(self):
        self.off_cells = 0
        self.on_cells = 0
        scene = self.canvas.scene()
        scene.clear()
        for rw in range(self.rows):
            for cl in range(self.cols):
                self.put_rect(scene, rw, cl, self.off_cell_color)

        for rw in range(self.rows):
            for cl in range(self.cols):
                if self.grid[rw][cl]:
                    color = self.on_cell_color
                    self.on_cells += 1
                else:
                    color = self.off_cell_color
                    self.off_cells += 1
                self.put_rect(scene, rw, cl, color)
        self.update_labels()
        self.btc_hunter()

    def canvas_mouse_press_event(self, event):
        self.is_drawing = True
        self.canvas_click(event)

    def canvas_mouse_move_event(self, event):
        if self.is_drawing:
            self.canvas_click(event)

    def canvas_mouse_release_event(self, event):
        self.is_drawing = False

    def canvas_click(self, e):
        if self.is_active is False:
            point = e.pos()
            cl = int(point.x() // self.size)
            rw = int(point.y() // self.size)

            if 0 <= rw < self.rows and 0 <= cl < self.cols:
                if self.grid[rw][cl]:
                    self.grid[rw][cl] = 0
                    color = self.off_cell_color
                    self.on_cells -= 1
                    self.off_cells += 1
                else:
                    self.grid[rw][cl] = 1
                    color = self.on_cell_color
                    self.on_cells += 1
                    self.off_cells -= 1

                self.put_rect(self.scene, rw, cl, color)
                self.update_labels()
                self.btc_hunter()
                if self.on_cells:
                    self.btn_start_stop.setEnabled(True)
                else:
                    self.btn_start_stop.setEnabled(False)
                
    def clear_columns(self, state):
        for checkbox in self.horizontal_blocking_checkboxes:
            checkbox.setChecked(False)

    def clear_rows(self, state):
        for checkbox in self.vertical_blocking_checkboxes:
            checkbox.setChecked(False)

    def block_lines_changed(self, state):
        sender = self.sender()
        if sender in self.horizontal_blocking_checkboxes:
            row = self.horizontal_blocking_checkboxes.index(sender)
            for col in range(GRID_SIZE):
                self.grid[row][col] = 0 if state else 1
        elif sender in self.vertical_blocking_checkboxes:
            col = self.vertical_blocking_checkboxes.index(sender)
            for row in range(GRID_SIZE):
                self.grid[row][col] = 0 if state else 1
        self.update_canvas()
        pass
        
    def put_rect(self, scene, rw, cl, color):
        x1 = cl * self.size
        y1 = rw * self.size
        x2 = x1 + self.size
        y2 = y1 + self.size
        scene.addRect(x1, y1, self.size, self.size, brush=QBrush(QColor(color)))

    def clear_canvas(self):
        self.seed_ratio = int(self.edt_seed_ratio.currentText())
        self.init_grid()
        self.canvas.setFixedSize(self.cols * self.size, self.rows * self.size)
        self.update_canvas()
        self.btn_start_stop.setDisabled(True)
        pass

    def seed(self):
        self.clear_canvas()
        for rw in range(self.rows):
            for cl in range(self.cols):
                seed_chance = random.randint(1, 100)
                if seed_chance <= self.seed_ratio:
                    self.grid[rw][cl] = 1
                else:
                    self.grid[rw][cl] = 0

        for row, blocked in enumerate(self.horizontal_blocking_checkboxes):
            if blocked.isChecked():
                for col in range(self.cols):
                    self.grid[row][col] = 0

        for col, blocked in enumerate(self.vertical_blocking_checkboxes):
            if blocked.isChecked():
                for row in range(self.rows):
                    self.grid[row][col] = 0

        for rw in range(self.rows):
            for cl in range(self.cols):
                if self.grid[rw][cl]:
                    color = self.on_cell_color
                    self.on_cells += 1
                else:
                    color = self.off_cell_color
                    self.off_cells += 1
                self.put_rect(self.scene, rw, cl, color)
        self.update_canvas()
        self.btn_start_stop.setEnabled(True)

    def start_stop(self):
        if self.is_active:
            #self.scanning_speed = self.speed_slider.value()
            self.is_active = False
            self.tick()
            self.btn_start_stop.setText('Start Random Full Scan (Must click Seed First)')
            self.btn_start_stop.setStyleSheet("color: green")
            self.btn_seed.setEnabled(True)
            self.btn_clear.setEnabled(True)
            self.scanning = False
            self.knightRiderWidget.stopAnimation()
        else:
            self.is_active = True
            self.tick()
            self.btn_start_stop.setText('🚫Stop Random Full Scan🚫')
            self.btn_start_stop.setStyleSheet("color: red")
            self.btn_seed.setEnabled(False)
            self.btn_clear.setEnabled(False)
            self.scanning = True
            self.knightRiderWidget.startAnimation()
            
    def start_game_of_life(self):
        self.scanning_speed = self.speed_slider.value()
        if self.is_active:
            self.is_active = False
            self.btn_game_of_life.setText('✅Start Game of Life Patterns✅')
            self.btn_game_of_life.setStyleSheet("color: Green")
            self.btn_game_of_life.setEnabled(True)
            self.btn_seed.setEnabled(True)
            self.btn_clear.setEnabled(True)
            if self.animation_timer is not None:
                self.animation_timer.stop()
                self.animation_timer = None
        else:
            self.is_active = True
            self.btn_game_of_life.setText('🚫Stop Game of Life Patterns🚫')
            self.btn_game_of_life.setStyleSheet("color: red")
            self.btn_game_of_life.setEnabled(True)
            self.btn_seed.setEnabled(False)
            self.btn_clear.setEnabled(False)
            self.game_of_life()
    
    def setup_animation_timer(self):
        self.animation_timer = QTimer()
        self.animation_timer.timeout.connect(self.game_of_life)
        self.animation_timer.start(self.scanning_speed)
    
    def game_of_life(self):
        selected_pattern = self.pattern_dropdown.currentText()
        self.scanning_speed = self.speed_slider.value()
        patterns = {
            'Conway': lambda neighbors: 1 if neighbors == 3 else (1 if neighbors == 2 and self.grid[rw][cl] else 0),
            'High Life': lambda neighbors: 1 if neighbors in (3, 6) else (1 if neighbors == 2 and self.grid[rw][cl] else 0),
            'Maze': lambda neighbors: 1 if neighbors in (1, 2, 3, 4, 5) else 0,
            'Crystallization': lambda neighbors: 1 if neighbors == 4 else (1 if neighbors == 3 or neighbors == 8 else 0),
            'Castle Walls': lambda neighbors: 1 if neighbors == 2 or neighbors == 3 else (1 if neighbors == 4 or neighbors == 5 else 0),
        }

        if selected_pattern in patterns:
            next_grid = [[0 for _ in range(self.cols)] for _ in range(self.rows)]

            for rw in range(self.rows):
                for cl in range(self.cols):
                    neighbors = self.count_neighbors(rw, cl)
                    next_grid[rw][cl] = patterns[selected_pattern](neighbors)

            for row, blocked in enumerate(self.horizontal_blocking_checkboxes):
                if blocked.isChecked():
                    for col in range(self.cols):
                        self.grid[row][col] = 0

            for col, blocked in enumerate(self.vertical_blocking_checkboxes):
                if blocked.isChecked():
                    for row in range(self.rows):
                        self.grid[row][col] = 0

            self.grid = next_grid
            self.update_canvas()
            self.btc_hunter()

            if any(any(cell == 1 for cell in row) for row in self.grid) and self.is_active:
                QTimer.singleShot(self.scanning_speed, self.game_of_life)
            else:
                self.is_active = False
                self.btn_game_of_life.setText('Start Game of Life Patterns')
                self.btn_game_of_life.setStyleSheet("color: green")
                self.btn_game_of_life.setEnabled(True)
                self.btn_seed.setEnabled(True)
                self.btn_clear.setEnabled(True)


    def count_neighbors(self, row, col):
        count = 0
        for dr in [-1, 0, 1]:
            for dc in [-1, 0, 1]:
                if dr == 0 and dc == 0:
                    continue
                nr, nc = row + dr, col + dc
                if 0 <= nr < self.rows and 0 <= nc < self.cols and self.grid[nr][nc] == 1:
                    count += 1
        return count
        
    def start_stop_random(self):
        self.scanning_speed = self.speed_slider.value()
        if self.matrix_timer_random.isActive():
            self.matrix_timer_random.stop()
            self.btn_matrix.setText('Start Matrix Random')
            self.btn_matrix.setStyleSheet("color: green")
            self.scanning = False
            self.knightRiderWidget.stopAnimation()
        else:
            self.matrix_timer_random.start(self.scanning_speed)
            self.btn_matrix.setText('🚫Stop Matrix Random🚫')
            self.btn_matrix.setStyleSheet("color: red")
            self.scanning = True
            self.knightRiderWidget.startAnimation()
            
    def random_matrix(self):
        num_new_drops = int(self.num_random_matrix.currentText())
        for rw in range(self.rows):
            if random.random() < 0.1:
                num_drops = random.randint(1, num_new_drops)
                drop_positions = random.sample(range(self.cols), num_drops)
                for cl in range(self.cols):
                    if cl in drop_positions:
                        self.grid[rw][cl] = 1
                    else:
                        self.grid[rw][cl] = 0

        for row, blocked in enumerate(self.horizontal_blocking_checkboxes):
            if blocked.isChecked():
                for col in range(self.cols):
                    self.grid[row][col] = 0

        for col, blocked in enumerate(self.vertical_blocking_checkboxes):
            if blocked.isChecked():
                for row in range(self.rows):
                    self.grid[row][col] = 0
        
        self.update_canvas()
    
    def start_stop_Smoke_ups(self):
        self.scanning_speed = self.speed_slider.value()
        if self.Smoke_ups_timer.isActive():
            self.Smoke_ups_timer.stop()
            self.btn_Smoke_ups.setText('Start Smoke')
            self.btn_Smoke_ups.setStyleSheet("color: green")
            self.scanning = False
            self.knightRiderWidget.stopAnimation()
        else:
            self.Smoke_ups_timer.start(self.scanning_speed)
            self.btn_Smoke_ups.setText('🚫Stop Smoke🚫')
            self.btn_Smoke_ups.setStyleSheet("color: red")
            self.scanning = True
            self.knightRiderWidget.startAnimation()

    def Smoke_ups(self):
        self.matrix_drops = [drop for drop in self.matrix_drops if drop.is_visible()]
        num_new_Smoke_ups = int(self.num_Smoke_ups_selector.currentText())
        for _ in range(num_new_Smoke_ups):
            row = random.randint(self.rows // 2, self.rows)
            col = random.randint(0, self.cols - 1)
            self.matrix_drops.append(Smoke_up(row, col, self.rows))

        for drop in self.matrix_drops:
            drop.move()

        self.init_grid()

        for drop in self.matrix_drops:
            if drop.is_visible():
                self.grid[drop.row][drop.col] = 1
        for row, blocked in enumerate(self.horizontal_blocking_checkboxes):
            if blocked.isChecked():
                for col in range(self.cols):
                    self.grid[row][col] = 0

        for col, blocked in enumerate(self.vertical_blocking_checkboxes):
            if blocked.isChecked():
                for row in range(self.rows):
                    self.grid[row][col] = 0
        self.update_canvas()
    
    def start_stop_Lava_bubbles(self):
        self.scanning_speed = self.speed_slider.value()
        if self.Lava_bubbles_timer.isActive():
            self.Lava_bubbles_timer.stop()
            self.btn_Lava_bubbles.setText('Start Lava')
            self.btn_Lava_bubbles.setStyleSheet("color: green")
            self.scanning = False
            self.knightRiderWidget.stopAnimation()
        else:
            self.Lava_bubbles_timer.start(self.scanning_speed)
            self.btn_Lava_bubbles.setText('🚫Stop Lava🚫')
            self.btn_Lava_bubbles.setStyleSheet("color: red")
            self.scanning = True
            self.knightRiderWidget.startAnimation()

    def Lava_bubbles(self):
        self.matrix_bubbles = [bubble for bubble in self.matrix_bubbles if bubble.is_visible()]
        num_new_Lava_bubbles = int(self.num_Lava_bubbles_selector.currentText())
        for _ in range(num_new_Lava_bubbles):
            row = random.randint(0, self.rows // 2)
            col = random.randint(0, self.cols - 1)
            self.matrix_bubbles.append(LavaBubble(row, col, self.rows))

        for bubble in self.matrix_bubbles:
            bubble.move()

        self.init_grid()

        for bubble in self.matrix_bubbles:
            if bubble.is_visible():
                for i in range(bubble.size):
                    row = int(bubble.row) + i
                    if 0 <= row < self.rows:
                        self.grid[row][bubble.col] = 1
        for row, blocked in enumerate(self.horizontal_blocking_checkboxes):
            if blocked.isChecked():
                for col in range(self.cols):
                    self.grid[row][col] = 0

        for col, blocked in enumerate(self.vertical_blocking_checkboxes):
            if blocked.isChecked():
                for row in range(self.rows):
                    self.grid[row][col] = 0
        self.update_canvas()

    def start_stop_blocks(self):
        self.scanning_speed = self.speed_slider.value()
        if self.blocks_timer.isActive():
            self.blocks_timer.stop()
            self.btn_blocks.setText('Start Blocks')
            self.btn_blocks.setStyleSheet("color: green")
            self.scanning = False
            self.knightRiderWidget.stopAnimation()
        else:
            self.blocks_timer.start(self.scanning_speed)
            self.btn_blocks.setText('🚫Stop Blocks🚫')
            self.btn_blocks.setStyleSheet("color: red")
            self.scanning = True
            self.knightRiderWidget.startAnimation()

    def blocks_run(self):
        self.blocks_work = [block for block in self.blocks_work if block.is_visible()]
        num_block_selector = int(self.num_block_selector.currentText())
        row = random.randint(0, self.rows // 2)
        col = random.randint(0, self.cols - 1)
        self.blocks_work.append(blocking_grid(row, col, self.rows))

        for block in self.blocks_work:
            block.move()

        self.init_grid()

        for block in self.blocks_work:
            if block.is_visible():
                for i in range(num_block_selector):
                    row = int(block.row) + i
                    if 0 <= row < self.rows:
                        self.grid[row][block.col] = 1
        for row, blocked in enumerate(self.horizontal_blocking_checkboxes):
            if blocked.isChecked():
                for col in range(self.cols):
                    self.grid[row][col] = 0

        for col, blocked in enumerate(self.vertical_blocking_checkboxes):
            if blocked.isChecked():
                for row in range(self.rows):
                    self.grid[row][col] = 0
        self.update_canvas()
        
    def start_stop_matrix(self):
        self.scanning_speed = self.speed_slider.value()
        if self.matrix_timer.isActive():
            self.matrix_timer.stop()
            self.btn_rain.setText('Start Matrix Rain')
            self.btn_rain.setStyleSheet("color: green")
            self.scanning = False
            self.knightRiderWidget.stopAnimation()
        else:
            self.matrix_timer.start(self.scanning_speed)
            self.btn_rain.setText('🚫Stop Matrix Rain🚫')
            self.btn_rain.setStyleSheet("color: red")
            self.scanning = True
            self.knightRiderWidget.startAnimation()
        
    def matrix_rain(self):
        self.matrix_drops = [drop for drop in self.matrix_drops if drop.is_visible()]
        num_new_drops = int(self.num_drops_selector.currentText())
        for _ in range(num_new_drops):
            if random.random() < 0.1:
                col = random.randint(0, self.cols - 1)
                self.matrix_drops.append(MatrixDrop(col, self.rows))

        for drop in self.matrix_drops:
            drop.move()

        self.init_grid()

        for drop in self.matrix_drops:
            if drop.is_visible():
                self.grid[drop.row][drop.col] = 1
        for row, blocked in enumerate(self.horizontal_blocking_checkboxes):
            if blocked.isChecked():
                for col in range(self.cols):
                    self.grid[row][col] = 0

        for col, blocked in enumerate(self.vertical_blocking_checkboxes):
            if blocked.isChecked():
                for row in range(self.rows):
                    self.grid[row][col] = 0
        self.update_canvas()
        
    def update_grid(self):
        hex_value = self._txt_inputhex.text()
        scene = self.canvas.scene()
        scene.clear()
        try:
            int_value = int(hex_value, 16)
            binstring = "{0:b}".format(int_value)
            binstring = binstring.rjust(self.rows * self.cols, "0")
            for i in range(self.rows):
                self.grid[i] = [int(binstring[j]) for j in range(i * self.cols, (i + 1) * self.cols)]
                for rw in range(self.rows):
                    for cl in range(self.cols):
                        if self.grid[rw][cl]:
                            color = self.on_cell_color
                            self.on_cells += 1
                        else:
                            color = self.off_cell_color
                            self.off_cells += 1
                        self.put_rect(scene, rw, cl, color)
            self.btc_hunter()
        except ValueError:
            self.pop_Result("Invalid Hex Value Please enter a valid hexadecimal value")
    
    def pop_Result(self, message_error):
        msg_box = QMessageBox()
        msg_box.setWindowTitle("Warning")
        msg_box.setText(message_error)
        msg_box.addButton(QMessageBox.StandardButton.Ok)
        msg_box.exec()
        
    def update_labels(self):
        self.lbl_tick_no.setText('🔑 Total Private Keys Scanned 🔑: %d' % self.tick_count)
        self.lbl_total_no.setText('₿ Total Addresses Scanned ₿: %d' % self.addr_count)
        
    def update_knight_rider_color(self, index):
        if index == 1:
            color = QColor(128, 0, 128)
            self.on_cell_color = QColor(128, 0, 128)
            self.off_cell_color = QColor(255, 255, 255)
        elif index == 2:
            color = QColor(0, 128, 0)
            self.on_cell_color = QColor(0, 128, 0)
            self.off_cell_color = QColor(0, 0, 0)
        elif index == 3:
            color = QColor(0, 0, 255)
            self.on_cell_color = QColor(0, 0, 255)
            self.off_cell_color = QColor(255, 255, 255)
        elif index == 4:
            color = QColor(0, 0, 255)
            self.on_cell_color = QColor(0, 0, 255)
            self.off_cell_color = QColor(255, 255, 0)
        elif index == 5:
            color = QColor(0, 0, 0)
            self.on_cell_color = QColor(0, 0, 0)
            self.off_cell_color = QColor(255, 0, 0)
        elif index == 6:
            color = QColor(0, 0, 0)
            self.on_cell_color = QColor(255, 255, 0)
            self.off_cell_color = QColor(0, 0, 0)
        else:
            color = QColor(255, 0, 0)
            self.on_cell_color = QColor(255, 0, 0)
            self.off_cell_color = QColor(255, 255, 255)

        self.update_canvas()

        border_color = f"border: 3px solid {color.name()};"
        style_sheet = f"QGroupBox {{ {border_color} padding: 7px; font-size: 14px; font-weight: bold; color: black;}}"
        for widget in self.findChildren(QGroupBox):
            widget.setStyleSheet(style_sheet)
        self.knightRiderGroupBox.setStyleSheet(style_sheet)
        miz = f"font-size: 17px; font-weight: bold; color: {color.name()};"
        self.mizogg_label.setStyleSheet(miz)
        color_lab = f"font-size: 16px; font-weight: bold; color: {color.name()};"
        self.colorlable.setStyleSheet(color_lab)
        welcome = f"font-size: 30px; font-weight: bold; color: {color.name()};"
        self.welcome_label.setStyleSheet(welcome)
        self.knightRiderWidget.setLightColor(color)

    def tick(self):
        if self.in_tick:
            return
        self.scanning_speed = self.speed_slider.value()
        self.in_tick = True
        self.on_cells = 0
        self.off_cells = 0
        self.scene.clear()
        for rw in range(self.rows):
            for cl in range(self.cols):
                seed_chance = random.randint(1, 100)
                if seed_chance <= self.seed_ratio:
                    self.grid[rw][cl] = 1
                else:
                    self.grid[rw][cl] = 0
        for row, blocked in enumerate(self.horizontal_blocking_checkboxes):
            if blocked.isChecked():
                for col in range(self.cols):
                    self.grid[row][col] = 0

        for col, blocked in enumerate(self.vertical_blocking_checkboxes):
            if blocked.isChecked():
                for row in range(self.rows):
                    self.grid[row][col] = 0
        for rw in range(self.rows):
            for cl in range(self.cols):
                if self.grid[rw][cl]:
                    color = self.on_cell_color
                    self.on_cells += 1
                else:
                    color = self.off_cell_color
                    self.off_cells += 1
                self.put_rect(self.scene, rw, cl, color)
        self.speed_slider_value_display.setText(str(self.scanning_speed))
        self.update_canvas()
        self.in_tick = False

        if self.is_active:
            QTimer.singleShot(self.scanning_speed, self.tick)
    
    def load_file(self):
        global addfind
        filePath, _ = QFileDialog.getOpenFileName(self, "Open File", "", "All Files (*);;BF Files (*.bf);;Text Files (*.txt)")
        
        if not filePath:  # If no file is selected, just return
            return

        if filePath.endswith('.bf'):
            try:
                with open(filePath, "rb") as fp:
                    addfind = BloomFilter.load(fp)
            except Exception as e:
                # Handle the exception (e.g., show a message box with an error)
                pass

        elif filePath.endswith('.txt'):
            with open(filePath) as file:
                addfind = file.read().split()
        addr_data = len(addfind)
        addr_count_print = f'Total BTC Addresses Loaded and Checking : {addr_data}'
        self.add_count_label.setText(addr_count_print)
            
if __name__ == '__main__':
    mizoggcmd= f'''
                      ___            ___
                     (o o)          (o o)
                    (  V  ) MIZOGG (  V  )
                    --m-m------------m-m--
                  © mizogg.co.uk 2018 - 2023
                   16x16.py CryptoHunter

                     VIP PROJECT Mizogg
                 
                {red(f"[>] Running with Python {sys.version_info[0]}.{sys.version_info[1]}.{sys.version_info[2]}")}


'''
    print(water(mizoggcmd), end="")
    app = QApplication([])
    hunter_16x16 = App()
    hunter_16x16.start()
import tkinter as tk
from tkinter import filedialog, messagebox
import time
import os

cellSize = 67
board = []
queen = []
ukuranBoard = 0
iterations = 0
inputFileName = ""
colorMap = {}
# Bernhard Aprillio Pramana - 13524074

# ===============================================================
def loadBoard():
    global board, ukuranBoard, queen, inputFileName, colorMap
    path = filedialog.askopenfilename(filetypes=[("SixSeven", "*.txt")])
    if not path:
        return
    inputFileName = path
    with open(path) as input:
        board = [list(line.strip()) for line in input if line.strip()]
    ukuranBoard = len(board)
    queen = [-1] * ukuranBoard
    canvas.config(width=ukuranBoard*cellSize, height=ukuranBoard*cellSize)
    colors = set(cell for row in board for cell in row)
    if len(colors) > ukuranBoard:
        messagebox.showerror("Invalid Board", f"Papan tidak valid: {len(colors)} region > ukuran papan {ukuranBoard}")
        board = []
        ukuranBoard = 0
        queen = []
        inputFileName = ""
        colorMap = {}
        return
    colorMap = {}
    for alphabet in colors:
        idx = ord(alphabet) - ord('A')
        color = (idx * 67) % 360
        r, g, b = coloring(color)
        colorMap[alphabet] = f"#{r:02x}{g:02x}{b:02x}"
    draw()

def saveOutput():
    if not board:
        return
    
    if inputFileName:
        name = os.path.splitext(os.path.basename(inputFileName))[0]
        filename = f"{name}_solusi.txt"
    else:
        filename = "output.txt"
    
    directory = os.path.join(os.path.dirname(__file__), "..", "test")
    outputPath = os.path.join(directory, filename)
    os.makedirs(directory, exist_ok=True)
    
    with open(outputPath, "w") as f:
        for i in range(ukuranBoard):
            f.write("".join("#" if queen[i] == j else board[i][j] for j in range(ukuranBoard)) + "\n")
    
    messagebox.showinfo("Saved", f"Tersimpan: {filename}")
# ===============================================================

# ===============================================================
def coloring(x):
    x %= 360
    target = 1 - abs((x / 60) % 2 - 1)
    if x < 60: # merah ke kuning
        r = 1
        g = target
        b = 0
    elif x < 120: # kuning ke hijau
        r = target
        g = 1
        b = 0
    elif x < 180: # hijau ke cyan
        r = 0
        g = 1
        b = target
    elif x < 240: # cyan ke biru
        r = 0
        g = target
        b = 1
    elif x < 300: # biru ke ungu
        r = target
        g = 0
        b = 1
    else: # ungu ke merah
        r = 1
        g = 0
        b = target
    return int(r*255), int(g*255), int(b*255)

def draw():
    canvas.delete("all")
    for i in range(ukuranBoard):
        for j in range(ukuranBoard):
            alphabet = board[i][j]
            x1, y1 = j * cellSize, i * cellSize
            canvas.create_rectangle(x1, y1, x1 + cellSize, y1 + cellSize, fill=colorMap.get(alphabet, "#ffffff"), outline="#f8c414") # hehehehehe those who know
            if queen[i] == j:
                canvas.create_text(x1 + cellSize//2, y1 + cellSize//2, text="#", font=("Arial", 20))
    myKisah.update()
# ===============================================================

# ===============================================================
def safe():
    for i in range(ukuranBoard):
        for j in range(i + 1, ukuranBoard):
            if queen[i] == queen[j]: # di kolom yang sama
                return False
            if abs(i - j) == 1 and abs(queen[i] - queen[j]) == 1: # bertetangga
                return False
            if board[i][queen[i]] == board[j][queen[j]]: # di warna yang sama
                return False
    return True

def solveHelper(x):
    global iterations
    if x == ukuranBoard:
        iterations += 1
        freqency = 10 ** (ukuranBoard // 2 + 2)
        finalFreq = freqency * (1 + iterations // (10 ** ukuranBoard)) + 67
        if iterations % max(1000, int(finalFreq)) == 0:
            draw()
            myKisah.update()
        if safe():
            return True
        return False
    
    for i in range(ukuranBoard):
        queen[x] = i
        if solveHelper(x + 1):
            return True
        queen[x] = -1
    return False

def solve():
    global iterations
    iterations = 0
    start = time.time()
    found = solveHelper(0)
    elapsed = int((time.time() - start) * 1000)
    if found:
        draw()
    status = "ditemukan" if found else "tidak ditemukan"
    messagebox.showinfo("Hasil", f"Solusi {status}\nWaktu: {elapsed} ms\nIterasi: {iterations}")
# ===============================================================

# ===============================================================
myKisah = tk.Tk()
myKisah.title("Tucil_13524074")
canvas = tk.Canvas(myKisah)
canvas.pack()

frame = tk.Frame(myKisah)
frame.pack(pady=5)

tk.Button(frame, text="Load Board", command=loadBoard).pack(side=tk.LEFT, padx=5)
tk.Button(frame, text="Solve", command=solve).pack(side=tk.LEFT, padx=5)
tk.Button(frame, text="Save", command=saveOutput).pack(side=tk.LEFT, padx=5)

myKisah.mainloop()
# ===============================================================
# ⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⣀⣀⣀⣀⣀⣀⣀⣀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀
# ⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⣠⣴⣶⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣶⣤⣀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀
# ⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⣠⣀⠀⠀⠀⢀⣴⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⠻⣿⣿⣿⣿⣦⣄⠀⠀⠠⠰⠶⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀
# ⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⢀⣠⣤⣤⡤⢀⣴⣿⣿⣿⠏⠀⠋⢉⣠⣿⣿⣿⣿⣿⣿⣿⣤⣄⡀⠈⠙⢿⣿⣿⣿⣧⡀⠐⠻⣶⣶⣄⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀
# ⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⣰⣿⠟⠁⠉⢠⣾⣿⣿⡿⠁⠀⣠⣾⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣦⣄⠈⠻⣿⣿⣿⣷⡄⠀⢀⠙⢿⡆⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀
# ⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⢰⠟⢁⡔⠀⣠⣿⣿⣿⡿⠁⣠⣾⣿⣿⠛⣻⣿⣿⡿⠁⠹⣿⣿⣿⣿⣿⣿⣿⣦⡀⠹⣿⣿⣿⣿⡀⠈⢧⡈⢳⡀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀
# ⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⡟⢠⡿⠀⢰⣿⣿⣿⡿⠁⣼⣿⣿⡿⠃⣼⣿⠏⠀⠁⣴⣆⠈⠉⠙⢿⣿⣿⣿⣿⣷⡄⢹⣿⣿⣿⣷⠀⠀⢷⡈⣧⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀
# ⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠐⢠⣿⠃⠀⣿⣿⣿⣿⠃⣸⣿⣿⠟⢀⣾⠿⠋⠀⢠⣾⣿⣿⣷⣄⠀⠀⠙⢿⣿⣿⣿⣷⠀⣿⣿⣿⣿⡄⢣⠘⣇⠘⡆⠀⠀⠀⠀⠀⠀⠀⠀⠀
# ⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⣼⡟⠀⢰⣿⣿⣿⡟⢀⣿⠟⠀⠰⠛⠋⠀⢠⣾⣿⣿⣿⣿⣿⡿⠟⠂⣀⠀⠉⠙⢿⣿⡇⢸⣿⣿⣿⣇⠘⡄⢹⡀⣿⠀⠀⠀⠀⠀⠀⠀⠀⠀
# ⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⢰⣿⡇⠀⠸⣿⣿⣿⡇⠈⠁⠀⠀⡀⠀⢀⣀⣤⣿⣿⣿⣿⣿⣿⣷⣤⣍⣉⣁⣤⣤⣀⠙⠓⠘⣿⣿⣿⣿⠀⣇⢸⣿⣿⡆⠀⠀⠀⠀⠀⠀⠀⠀
# ⠀⠀⠀⠀⠀⠀⠀⠀⠀⢰⣾⣿⠁⠀⠀⣿⣿⣿⡇⢠⣶⣾⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣦⠀⣿⠻⣿⠛⡆⢻⠸⣿⣿⣇⠀⠀⠀⠀⠀⠀⠀⠀
# ⠀⠀⠀⠀⠀⠀⠀⠀⠀⢸⣿⣿⠀⡆⠀⣿⣿⠙⡇⢸⣿⣿⡿⠿⠟⠋⠙⢻⣿⣿⣿⣿⣿⣿⣿⣿⠛⠙⠛⠿⢿⣿⣿⣿⠀⡟⠀⣿⠀⡇⢈⣀⠛⠛⠻⠀⠀⠀⠀⠀⠀⠀⠀
# ⠀⠀⡀⠀⠀⠀⠀⠀⠀⠀⣀⣀⡀⠀⠀⢻⣿⡆⢁⠘⣿⣿⣇⣀⣀⣀⣠⣼⣿⣿⣿⣿⣿⣿⣿⣿⣦⣀⣀⠀⢠⣿⣿⣿⠀⠇⢰⣿⠀⡇⢠⣌⣉⣉⠓⠒⠶⠶⠤⠤⣤⣀⠀
# ⠀⠈⠓⠶⢄⠐⠲⠀⡄⢾⣿⣿⣿⣧⠀⠘⣿⡇⠘⠀⢿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⡟⠀⠀⢸⣿⠀⠁⢸⣿⣿⣿⠇⢰⣀⣄⠠⠒⠉⠀⠀
# ⠀⠀⠀⠀⠀⠀⠘⠛⠇⠀⠹⣿⣿⣿⡄⠀⠹⣷⠀⠁⠘⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⠃⠀⠀⣿⡏⠀⠀⣾⡿⠟⠋⠀⠀⠉⠀⠀⠀⠀⠀⠀
# ⠀⠀⠀⠀⠀⠀⠀⠀⠀⢀⡀⠀⠉⣙⠛⠀⠀⠙⡆⠀⠀⢻⣿⣿⣿⣿⣿⣿⡿⠿⣿⠿⠿⣿⠿⣿⣿⣿⣿⣿⣿⣿⣇⢀⡾⠀⠇⠀⠀⢀⡠⠄⢀⣠⣶⡇⠀⠀⠀⠀⠀⠀⠀
# ⠀⠀⠀⠀⠀⠀⠀⠀⠀⢸⣿⣷⡆⠉⠀⠀⠀⠀⠀⠀⠀⢺⣿⣿⣿⣿⣿⣿⣿⣶⣶⣶⣶⣶⣶⣿⣿⣿⣿⣿⣿⣿⣿⡿⠁⠀⠀⠀⠀⠈⢠⣶⣿⣿⣿⣷⠀⠀⠀⠀⠀⠀⠀
# ⠀⠀⠀⠀⠀⠀⠀⠀⠀⢸⣿⣿⣿⡄⠀⠀⠸⣿⠀⠀⠀⠻⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⡿⠟⠀⠀⠀⣾⠁⠀⣠⣿⣿⣿⣿⣿⣿⠀⠀⠀⠀⠀⠀⠀
# ⠀⠀⠀⠀⠀⠀⠀⠀⠀⢸⣿⣿⣿⣷⠀⠘⡀⢻⡀⠀⠀⠀⠈⠙⠿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⡿⠟⠉⠀⠀⠀⠀⠀⠃⠀⢰⣿⣿⣿⠀⣿⣿⣿⠀⠀⠀⠀⠀⠀⠀
# ⠀⠀⠀⠀⠀⠀⠀⠀⠀⢸⣿⠸⣿⣿⡀⠀⣧⠘⡇⠀⠀⠀⠀⠀⠀⠀⠀⠉⠛⠿⠿⢿⣿⠿⠿⠛⠋⠁⠀⠀⠀⠀⣀⣀⡀⠀⠀⠀⢸⣿⣿⡿⢰⣿⣿⡿⠀⠀⠀⠀⠀⠀⠀
# ⠀⠀⠀⠀⠀⠀⠀⠀⠀⠘⣿⡀⣿⣿⣇⠀⢿⡄⠃⢸⣿⣿⠀⣄⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⣀⣠⣤⣾⡇⠈⣿⣿⣿⠀⠀⠀⢸⣿⣿⡇⢸⣿⡟⠀⠀⠀⠀⠀⠀⠀⠀
# ⠀⠀⠀⠀⠀⠀⠀⠀⠘⠀⣿⡇⣿⣿⣿⡆⠸⣧⠀⠀⣿⡇⠀⠀⠀⠀⠀⠀⠀⠐⣶⣶⣶⣿⣿⣿⣿⣿⡿⠋⠁⠀⣿⣿⡇⠀⠀⠀⣼⣿⣿⡇⠈⠟⠀⠀⠀⠀⠀⠀⠀⠀⠀
# ⠀⠀⠀⠀⠀⠀⠀⠀⠘⠀⣿⡇⣿⣿⣿⣷⠀⢿⡀⠀⣿⣇⠀⠱⠀⠀⠀⠀⠀⠀⣿⣿⣿⣿⣿⠿⠛⢉⡠⠚⠀⢰⣿⣿⡇⠀⠀⠀⣿⣿⣿⡇⠀⠀⣠⡀⠀⠀⠀⠀⠀⠀⠀
# ⠀⠀⠀⠀⠀⠀⠀⢰⡆⠀⢹⡇⢹⣿⣿⣿⡇⠸⡇⠀⢸⣿⡄⠀⢄⣉⠛⠒⠒⠦⠤⠤⠤⠤⠒⠒⠉⣁⣤⠂⠀⣸⣿⣿⠇⢨⡰⢀⣿⣿⣿⡇⠀⣰⣿⣷⡀⠀⠀⠀⠀⠀⠀
# ⠀⠀⠀⠀⠀⠀⢠⣿⡇⠀⠸⡇⢸⣿⣿⣿⣿⠀⣿⠀⢸⣿⣷⠀⠘⣿⣿⡏⡠⠀⣴⠂⣤⠀⣶⠈⣆⠸⠃⠈⢠⣿⣿⣿⠀⣿⡇⢸⣿⣿⣿⡇⢠⣿⣿⣿⣧⠀⠀⠀⠀⠀⠀
# ⠀⠀⠀⠀⠀⢠⣿⣿⣿⠀⠀⣧⠸⣿⣿⣿⣿⡇⢸⡇⠀⣿⣿⣇⠀⠘⣿⡇⡇⢸⣿⢠⣿⠄⢿⠀⣿⠀⠀⣠⣿⣿⣿⡟⢠⣿⠃⣼⣿⣿⣿⡇⣾⣿⣿⣿⣿⣧⠀⠀⠀⠀⠀
# ⠀⠀⠀⠀⠀⣼⣿⣿⣿⡇⠀⢸⠀⣿⣿⣿⣿⣿⠈⣿⠀⢿⣿⣿⣄⠁⢘⠀⡄⢸⣿⠈⢀⠀⢘⡀⢻⠀⣴⣿⣿⣿⣿⡇⢸⣿⣤⣿⣿⣿⣿⡇⣿⣿⠛⣿⣿⣿⣆⠀⠀⠀⠀
# ⠀⠀⠀⠀⢠⣿⣿⠃⣸⣿⠀⠸⡄⢻⣿⣿⣿⣿⡄⢻⡆⢸⣿⣿⣿⣿⣿⠀⠃⢈⡇⠀⢸⡄⠈⣇⠘⡆⢻⣿⣿⣿⣿⠁⣾⠇⣼⣿⣿⣿⣿⡇⣿⣿⡆⠘⣿⣿⣿⡆⠀⠀⠀
# ⠀⠀⠀⢀⣾⣿⡏⢀⣿⣿⡇⠀⡇⠸⣿⣿⣿⣿⣇⠸⣧⢸⣿⣿⣿⣿⡇⢸⠀⣿⠇⠀⠉⠉⠀⢿⡀⢳⠸⣿⣿⣿⣿⠀⡿⠀⣿⣿⣿⡏⢹⡇⣿⣿⣧⠀⠸⣿⣿⣿⡄⠀⠀
# ⠀⠀⠀⣼⣿⡿⠀⣼⣿⣿⣿⠀⢱⣶⣿⣿⣿⣿⣿⠀⣿⠈⣿⣿⣿⣿⡇⠈⠀⣿⠀⠀⠀⠀⠀⠸⡇⠸⡀⢿⣿⣿⡏⢰⠃⠀⣿⣿⣿⣧⢸⡇⣿⣿⣿⡆⠀⢹⣿⣿⣿⡀⠀
# ⠀⠀⢠⣿⣿⠁⢠⣿⣿⣿⣿⡄⢸⡇⢻⣿⣿⣿⣿⡆⠀⠃⣿⣿⣿⣿⠀⣾⢸⡿⢀⣤⣤⣤⣤⠀⢿⠀⡇⠸⣿⣿⡇⠘⢠⠀⣿⣿⣿⣿⢸⡇⢹⣿⣿⣷⡀⠀⢿⣿⣿⣧⠀
# ⠀⠀⣾⣿⠏⠀⣼⣿⣿⣿⣿⡇⢸⡇⢸⣿⣿⣿⣿⡇⠀⠀⢻⣿⣿⣿⠀⠉⢸⡇⢸⣿⣿⣿⣿⡇⠸⡇⢻⡀⢿⣿⡇⠀⠀⠀⣿⣿⣿⡇⢸⡇⣼⣿⣿⣿⣇⠀⠘⣿⣿⣿⣧
# ⠀⣸⣿⡟⠀⢠⣿⣿⣿⣿⣿⣿⠈⡇⠈⣿⣿⣿⣿⣷⡆⠀⢸⣿⣿⡏⢠⡇⣼⠃⠀⠀⠀⠀⠀⠀⠀⣷⠘⡇⠸⣿⡇⢀⠀⠀⣿⣿⣿⡇⠈⡇⣿⣿⣿⣿⣿⡄⢆⠸⣿⣿⣿
# ⢠⣿⣿⠁⡌⢸⣿⣿⣿⣿⣿⣿⠀⡇⠀⢿⣿⣿⣿⣿⡇⠀⢸⣿⣿⡇⢘⠇⣿⠀⠀⠀⠀⠀⠀⠀⠀⠸⡀⢻⠀⢿⣷⠈⠀⠀⣿⣿⣿⠇⠀⡇⣿⣿⣿⣿⣿⣷⠘⡄⢹⣿⣿
# ⣿⣿⠇⢸⠇⣿⣿⣿⣿⣿⣿⣿⠀⡇⠀⠸⣿⣿⣿⣿⡇⠀⢸⣿⣿⠇⣘⠀⡟⢠⣤⣤⣤⣤⣤⣴⣶⠀⡇⠸⡇⢸⣿⡀⠀⠀⢿⣿⣿⠀⠀⠃⣿⣿⣿⣿⣿⣿⡄⢹⡀⢿⣿
# ⠙⠿⢠⣿⠀⣿⣿⣿⣿⣿⣿⣿⡇⠀⠀⠀⢻⣿⣿⣿⠀⠀⣾⣿⣿⠀⣿⠀⡇⢸⣿⣿⣿⣿⠿⠿⠿⡇⢸⠀⢻⠈⣿⣧⠀⠀⢸⣿⡏⠠⠀⢰⣿⣿⣿⣿⣿⣿⣷⠀⢷⣸⠟
# ⠷⠄⠈⠋⢠⣿⣿⣿⣿⣿⣿⣿⣷⠀⠀⠀⠈⢿⣿⡟⠀⠀⣿⣿⣿⠀⠋⢀⠃⠀⠀⠀⠀⠀⠀⠀⠀⠀⠸⡇⠸⡇⢻⣿⣷⡄⠀⣿⠃⠀⠀⢸⣿⣿⣿⣿⣿⣿⣿⣇⠈⠀⠲
# ⣦⠀⠀⠀⢸⣿⣿⣿⣿⣿⣿⣿⣿⣧⠀⢰⡄⠈⢻⠇⠀⢸⣿⣿⣿⠸⡇⢸⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⢿⠀⢧⠈⣿⣿⣷⡄⠘⢠⡆⢀⣿⣿⣿⣿⣿⣿⣿⣿⡟⠀⠀⠀
# ⠉⠀⠀⠀⠸⣿⣿⣿⣿⣿⣿⣿⣿⣿⣇⠈⢿⣦⡈⠀⣠⣿⣿⣿⡟⢠⠇⠘⠀⣤⣤⣤⣤⣤⣤⣤⣤⣴⡆⠸⡇⢸⡄⢹⣿⣿⡷⠀⣿⣧⣼⣿⣿⣿⣿⣿⡿⠟⢉⣤⠂⠀⠀
# ⠀⠀⠀⠀⠲⢤⣉⠛⠻⠿⣿⣿⣿⣿⣿⣶⣼⣿⣷⣀⣹⣿⣿⣿⡇⣼⠀⣿⠀⠛⠛⠛⠛⠋⠋⠉⠉⠉⠉⠀⢿⠈⣧⠈⣿⣿⣿⣿⣿⣿⣿⣿⠿⠟⠋⣁⣤⠶⠋⣀⠴⠀⠀
# ⠀⠀⠀⠀⠐⠂⠌⠉⠓⠒⠦⠤⠍⠉⠉⠙⠛⠛⠛⠻⠿⠿⠿⠿⠇⠿⠀⠿⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠸⠇⠹⠄⠹⠿⠿⠿⠟⠋⠉⠤⠶⠚⠋⠉⠤⠔⠊⠁⠀⠀⠀
# my kisah ini woy (diambil dari https://emojicombos.com/frieren)
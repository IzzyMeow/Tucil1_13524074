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

# ===============================================================
def loadBoard():
    global board, ukuranBoard, queen, inputFileName
    path = filedialog.askopenfilename(filetypes=[("SixSeven", "*.txt")])
    if not path:
        return
    inputFileName = path
    with open(path) as input:
        board = [list(line.strip()) for line in input if line.strip()]
    ukuranBoard = len(board)
    queen = [-1] * ukuranBoard
    canvas.config(width=ukuranBoard*cellSize, height=ukuranBoard*cellSize)
    draw()

def saveOutput():
    if inputFileName:
        input = os.path.basename(inputFileName)
        fileName = os.path.splitext(input)[0]
        output_path = f"../test/{fileName}_solusi.txt"
    with open(output_path, "w") as output:
        for i in range(ukuranBoard):
            for j in range(ukuranBoard):
                if queen[i] == j:
                    output.write("#")
                else:
                    output.write(board[i][j])
            output.write("\n")
    messagebox.showinfo("Saved", f"Tersimpan dengan nama file {output_path}")
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
    colors = {}
    for i in range(ukuranBoard):
        for j in range(ukuranBoard):
            alphabet = board[i][j]

            if alphabet not in colors:
                idx = ord(alphabet) - ord('A')
                color = (idx * 67) % 360
                r, g, b = coloring(color)
                colors[alphabet] = f"#{r:02x}{g:02x}{b:02x}" # ubah ke format hex
            
            x1 = j * cellSize
            y1 = i * cellSize
            x2 = x1 + cellSize
            y2 = y1 + cellSize

            canvas.create_rectangle(x1, y1, x2, y2, fill=colors[alphabet], outline="#f8c414")
            if queen[i] == j:
                canvas.create_text(x1 + cellSize//2, y1 + cellSize//2, text="#", font=("Arial", 20)) # menampilkan queen
    myKisah.update_idletasks()
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
        update_freq = (ukuranBoard ** ((ukuranBoard//2) + 2)) + 67
        if iterations % update_freq == 0:
            draw()
            myKisah.update()
        if safe():
            draw()  # Solusi akhir
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
    end = int((time.time() - start) * 1000)
    if found:
        msg = "Solusi ditemukan\nWaktu: " + str(end) + " ms\nIterasi: " + str(iterations)
    else:
        msg = "Solusi tidak ditemukan\nWaktu: " + str(end) + " ms\nIterasi: " + str(iterations)
    messagebox.showinfo("Hasil", msg)
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
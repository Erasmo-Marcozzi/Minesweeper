import numpy as np
import itertools
import tkinter as tk
from tkinter import ttk
import argparse
import time
import sys

parser = argparse.ArgumentParser('Minesweeper')
parser.add_argument('-x', '--x', help='x direction size.', type=int)
parser.add_argument('-y', '--y', help='y direction size.', type=int)
parser.add_argument('-b', '--bombs', help='Number of bombs.', type=int)
args = parser.parse_args()

x=args.x
y=args.y
b=args.bombs
k = 'y'
butts = {}
imgs = {}
m = []
root = ''

def create_map(y,x,b):
    '''
    Creates a map of dimension x times y with b bombs.
    '''
    global k
    if b <= 0:
        print('This will not generate a playable map! (No bombs)')
        k = 'n'
        return
    if b != int(b):
        print('This will not generate a playable map! (No such thing as a fractional bomb)')
        k = 'n'
        return
    if x != int(x) or y != int(y):
        print('This will not generate a playable map! (x, y need to be ints)')
        k = 'n'
        return
    if b > x*y:
        print('This will not generate a playable map! (Too many bombs)')
        k = 'n'
        return
    if x < 4 or y < 4:
        print('This will not generate a playable map! (Too small)')
        k = 'n'
        return
    if b == x*y:
        print("This will technically generate a map, but it won't be very fun to play... (Oops! All bombs)")
        print("Continue (y/n)?")
        k = input()
        helped = False
        if k.lower() == 'help':
            print('What? Are you in danger? The program has a help command if you need it, but if you are in actual danger, I suggest you get out of it BEFORE playing Minesweeper.')
            time.sleep(6)
            print("I'll still be waiting here once you're safe, I promise.")
            time.sleep(10)
            print("Done? You're ok? Great, now just put in y or n.")
            helped = True
        if k.lower() == 'zork':
            print('You have been eaten by a grue.')
            time.sleep(3)
            print("Nah, I'm kidding. Just put down y or n please. Don't you want to play Minesweeper?")
            helped = True
        if k.lower() == '0451':
            print("I can see you know ball. Still, that isn't going to help you with Minesweeper, I promise.")
            time.sleep(3)
            print("Please just put down y or n. The game doesn't start otherwise.")
            helped = True
        if k.lower() == 'run mla':
            print("I can probably do a passable Milton Library Assistant impression if you give me a second.")
            time.sleep(3)
            print("Blah blah blah you're stupid, yadda yadda yadda, I know you're wrong and I am so much smarter than you.")
            time.sleep(6)
            print("What? Oh, right. Minesweeper. Press y and then enter or n and then enter. Super easy.")
            time.sleep(4)
            print("Also, humans are worth more than frogs. Don't forget that.")
            time.sleep(4)
            print("Do you think a frog could have coded this? I don't think so.")
            helped = True
        if k.lower() == 'gostak':
            print("The gostak distims the doshes.")
            time.sleep(10)
            print("Glauds! How rorm it would be to pell back to the bewl and distunk them, distunk the whole delcot, let the drokes discren them.")
            time.sleep(10)
            print("Jallon, dermin y or n on the lossad.")
            time.sleep(6)
            print("Yeah, this is super niche. Do you think I care? Do you have any idea how much fun I'm having?")
            time.sleep(3)
            print("Not that much. Still.")
            helped = True
        while k.lower() != 'y' and k.lower() != 'n':
            if helped == False:
                print('No, the answers are y or n. Nothing else.')
            else:
                helped = False
            k = input()
        if k.lower() == 'n':
            return
    map = np.zeros((x,y), dtype=str)
    xb = np.random.randint(0, x, b)
    yb = np.random.randint(0, y, b)
    for q in range(b):
        while map[xb[q], yb[q]] == 'X':
            xb[q] = np.random.randint(0, x)
            yb[q] = np.random.randint(0, y)
        map[xb[q], yb[q]] = 'X'
    for a in range(x):
        for b in range(y):
            if map[a,b] == 'X':
                continue
            else:
                count = 0
                s1 = [a-1, a, a+1]
                s2 = [b-1, b, b+1]
                s = list(itertools.product(s1, s2))
                for t in s:
                    if -1 in t or t[0] == x or t[1] == y:
                        continue
                    if map[t[0], t[1]] == 'X':
                        count += 1
                map[a,b] = str(count)
    return map
def clear(xer,yer):
    rx = [xer-1, xer, xer+1]
    ry = [yer-1, yer, yer+1]
    arr = list(itertools.product(rx, ry))
    for e in arr:
        if e[0] >= 0 and e[1] >= 0 and e[1] < x and e[0] < y:
            if imgs['('+str(e[1])+', '+str(e[0])+')'] != 'flag':
                if m[e[0], e[1]] == '0':
                    butts['('+str(e[1])+', '+str(e[0])+')'].destroy()
                    m[e[0], e[1]] = 'p'
                    clear(e[0], e[1])
                elif m[e[0], e[1]] != 'X':
                    butts['('+str(e[1])+', '+str(e[0])+')'].destroy()
                    if m[e[0], e[1]] != 'p':
                        nt = ttk.Label(root, text=str(m[e[0],e[1]]), image=i2, compound='center')
                        nt.grid(row=e[0], column=e[1])
                    elif m[e[0], e[1]] == 'p':
                        nt = ttk.Label(root, image=i2)
                        nt.grid(row=e[0], column=e[1])
def click(event):
    widget = event.widget
    grid_info = widget.grid_info()
    if imgs['('+str(grid_info['column'])+', '+str(grid_info['row'])+')'] == 'flag':
        return
    widget.destroy()
    if m[grid_info['row'],grid_info['column']] != '0':
        nt = ttk.Label(root, text=str(m[grid_info['row'],grid_info['column']]), image=i2, compound='center')
        nt.grid(row=grid_info['row'], column=grid_info['column'])
    if m[grid_info['row'],grid_info['column']] == '0':
        nt = ttk.Label(root, image=i2)
        nt.grid(row=grid_info['row'], column=grid_info['column'])
        m[grid_info['row'],grid_info['column']] = 'p'
        clear(grid_info['row'],grid_info['column'])
    if m[grid_info['row'],grid_info['column']] == 'X':
        global vic, res
        vic = ttk.Label(root, text='You Lose! :-{', image=iv, compound='center', background = '#c40234')
        vic.grid(row = y+1, columnspan = x)
def mark(event):
    global fl
    widget = event.widget
    grid_info = widget.grid_info()
    if imgs['('+str(grid_info['column'])+', '+str(grid_info['row'])+')'] == 'i':
        widget.config(image=flag)
        imgs['('+str(grid_info['column'])+', '+str(grid_info['row'])+')'] = 'flag'
        fl += 1
        flag_placements[grid_info['row'], grid_info['column']] = 'f'
    elif imgs['('+str(grid_info['column'])+', '+str(grid_info['row'])+')'] == 'flag':
        widget.config(image=i)
        imgs['('+str(grid_info['column'])+', '+str(grid_info['row'])+')'] = 'i'
        fl -= 1
        flag_placements[grid_info['row'], grid_info['column']] = 'f'
    global vic
    if fl == b:
        if np.where(flag_placements == 'f')[0].all() == np.where(m == 'X')[0].all():
            vic = ttk.Label(root, text='You Win! Congrats! :-3', image=iv, compound='center', background = '#00ad83')
            vic.grid(row = y+1, columnspan = x)
        else:
            vic = ttk.Label(root, text=str(fl)+'/'+str(b), image=iv, compound='center')
            vic.grid(row = y+1, columnspan = x)
    else:
        vic = ttk.Label(root, text=str(fl)+'/'+str(b), image=iv, compound='center')
        vic.grid(row = y+1, columnspan = x)
def leave(holder):
    root.after(200, root.destroy())
    sys.exit()
    return
def restart(holder):
    root.destroy()
    main()

def main():
    global imgs, butts, m, root, xr, yr, i, i2, flag, fl, flag_placements, iv, vic, func, res, q
    m = create_map(x,y,b)
    if k.lower() != 'n':
        root = tk.Tk()
        root.title('Minesweeper')
        root.resizable(0, 0)

        xr = range(x)
        yr = range(y)
        r = list(itertools.product(xr,yr))

        flag = tk.PhotoImage(file='flag.png')
        fl = 0
        flag_placements = np.zeros_like(m, dtype=str)

        iv = tk.PhotoImage(width=85*y, height=50)
        vic = ttk.Label(root, text=str(fl)+'/'+str(b), image=iv, compound='center')
        vic.grid(row = y+1, columnspan = x)

        func = tk.PhotoImage(width=130, height=30)    
        res = ttk.Button(root, text='Restart', image=func, compound='center')
        res.grid(row=y+2,column=0, columnspan=2)
        res.bind('<Button-1>', restart)

        q = ttk.Button(root, text='Quit', image=func, compound='center')
        q.grid(row=y+2,column=x-2,columnspan=2)
        q.bind('<Button-1>', leave)

        i = tk.PhotoImage(width=70, height=70)
        i2 = tk.PhotoImage(width=85, height=85)
        for l in r:
            butts[str(l)] = ttk.Button(root, image=i)
            butts[str(l)].grid(row=l[1], column=l[0])
            butts[str(l)].bind('<Button-1>', click)
            butts[str(l)].bind('<Button-3>', mark)
            imgs[str(l)] = 'i'

        root.mainloop()

main()
import subprocess
from Tkinter import *

root = Tk.Tk()

canvas1 = Tk.Canvas(root, width=1280, height=720)
canvas1.pack()

def start_batch():
    subprocess.call([r'C:\Users\remlab\Desktop\G4SAC_Testing\SSD LTSSM.bat'])

# def lounchLTSSMTests():
#     with open('C:\TestSuite\LTSSM\LTSSM.txt', 'r')as f:
#         list = []
#         for i in f:
#             list.append(i.split('::'))
#         for x in list:
#             print x[1]


# buttonRun = tk.Button(root, text='Run The LTSSM ', command=start_batch)
# canvas1.create_window(270, 230, window=buttonRun)

buttonRun = Tk.Button(root, text='Run Selected Test ', command=start_batch)
canvas1.create_window(110, 600, window=buttonRun)

buttonRun = Tk.Button(root, text='Run Selected Test ', command=start_batch)
canvas1.create_window(250, 600, window=buttonRun)

buttonRun = Tk.Button(root, text='Run Selected Test ', command=start_batch)
canvas1.create_window(390, 600, window=buttonRun)

buttonLTSSM = Tk.Button(root, text='LTSSM ')
canvas1.create_window(100, 70, window=buttonLTSSM)

buttonIO = Tk.Button(root, text='IO \n Bandwidth ')
canvas1.create_window(220, 70, window=buttonIO)

buttonDataIntegrity = Tk.Button(root, text='Data \n Integrity ')
canvas1.create_window(340, 70, window=buttonDataIntegrity)

buttonRAID = Tk.Button(root, text='RAID ')
canvas1.create_window(460, 70, window=buttonRAID)

buttonConfigSpace = Tk.Button(root, text='Config \n Space ')
canvas1.create_window(100, 140, window=buttonConfigSpace)

buttonResets = Tk.Button(root, text='Resets ')
canvas1.create_window(220, 140, window=buttonResets)

buttonHotplug = Tk.Button(root, text='Hotplug ')
canvas1.create_window(340, 140, window=buttonHotplug)

buttonPTC = Tk.Button(root, text='PTC ')
canvas1.create_window(460, 140, window=buttonPTC)

root.mainloop()




























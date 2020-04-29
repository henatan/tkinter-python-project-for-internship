#Henok Belete Assefa
import tkinter
#from TestLTSSM_Multi import *
from multiprocessing import Process
from subprocess import Popen, PIPE
import sys
from itertools import islice
from subprocess import Popen, PIPE
from textwrap import dedent
from threading import Thread
#from PIL import ImageTk, Image
#import New_
from tempfile import mkstemp
from shutil import move
from os import fdopen, remove
import csv

# This class is used to redirect whatever the stdout result in our program
# should pass an argument of object which we want to display

class TextRedirector(object):
    def __init__(self, widget):
        self.terminal = sys.stdout
        self.widget = widget

    def write(self, str):
        self.widget.configure(state="normal")
        self.widget.insert("end", str)
        self.widget.configure(state="disabled")

# class TextRedirector(object):
# replace the old config file by the new one created on the UI
def replace(configFile,subst):
    with open(configFile, 'r+') as f:
        read=f.read()
        adiswa = read.split('\n')
        lela= adiswa[6]
    #Create temp file
    fh, abs_path = mkstemp()
    with fdopen(fh,'w') as new_file:
        with open(configFile) as old_file:
            for line in old_file:
                new_file.write(line.replace(lela[12], subst))
    #Remove original file
    remove(configFile)
    #Move new file
    move(abs_path, configFile)
# #         pass

# thid function is used to replace the run time in IObandwidth test
# the fundtion will edit whaat every config file is passing
# only minute and cinfug files are passing. The others are 0 by default

def replace(configFile,hour,minute,second):
    newLine = '	' + hour + '          ' + minute + '          ' + second
    with open(configFile, 'r+') as f:
        read=f.read()
        adiswa = read.split('\n')
        lela= adiswa[6]
    #Create temp file
    fh, abs_path = mkstemp()
    with fdopen(fh,'w') as new_file:
        with open(configFile) as old_file:
            for line in old_file:
                new_file.write(line.replace(lela,newLine))
    #Remove original file
    remove(configFile)
    #Move new file
    move(abs_path, configFile)

##########################################################################


# this function reads the IObandwidth result and display it to the display area
# We can display whatever we want from the csv file, this is just the default


##############################################################################################

#the function is a pop message for tests in progress(not completed)

def popupmsg(msg):
    popup = Tk()
    popup.geometry('300x200')
    popup.wm_title("!")
    label = Label(popup, text=msg, font=('Lucida Bright',12,'bold'),bg='sky blue')
    label.pack(side="top", fill="x", pady=10)
    B1 = Button(popup, text="Okay", command = popup.destroy,bg='sky blue', font=('Lucida Bright',12,'bold'))
    B1.pack()
    popup.configure(background='sky blue')
    popup.mainloop()


#this folder will save the csv file result from the IObandwith test

def parseLog(self, logFolder):

    errFound = False
    errLine = ""
    globalErr = False

    flist = glob.glob(os.path.join(os.getcwd(), 'ioMeter results', logFolder, '*.csv'))

    if not flist:
        print ("\n-W- No log files to parse in folder : {0}").format(os.path.join(os.getcwd(), 'ioMeter results', logFolder))
        sys.exit(0)

    for fn in flist:
        err = False
        errType = []
        errDict = {}

        with open(fn, 'r') as f:
            for linum, line in enumerate(f):
                # print line
                if line.startswith("ERROR!!"):
                    errFound = True
                    errLine = line
                elif errFound:
                    errFound = False
                    line = errLine.split("\n")[0] + " " + line

                    globalErr = True
                    err = True
                    if line.split("\n")[0] not in errType:
                        errType.append(line.split("\n")[0])
                        if errDict.get(line.split("\n")[0]):
                            val = int(errDict.get(line.split("\n")[0]))
                            errDict[line.split("\n")[0]] = val + 1
                        else:
                            errDict[line.split("\n")[0]] = 1

                    else:
                        if errDict.get(line.split("\n")[0]):
                            val = int(errDict.get(line.split("\n")[0]))
                            errDict[line.split("\n")[0]] = val + 1
                        else:
                            errDict[line.split("\n")[0]] = 1

        if err:
            print ("--- Error found in : {0} ---").format(fn)
            for key, val in errDict.items():
                print ("{0} = {1} times").format(key, val)
            print ("\n\n")
    if not globalErr:
        print ("\n\n*****  No error seen in IO test.. !  ******")
        print ("\nParsing of all log file complted...!")

# Application class is the main class of the UI,
# it contains all the main frams of the GUI

class Application(Frame):

    def __init__(self, master=None):
        Frame.__init__(self, master)
        self.grid()
        self.master.title("Platform Connected Test Suite")

# A buttoon which clear the display window after one test is finished and displayed
# I chose to put it down below but can be edited

        for r in range(1):
            self.master.rowconfigure(r, weight=1)
        for c in range(1):
            self.master.columnconfigure(c, weight=1)
            Button(master, text="            Clear Test Result".format(c),fg='yellow',  bg='dodgerBlue3', command=self.clearTest,font=('Lucida Bright',10,'bold')).grid(row=10,column=c,sticky=W)

################################################################
        global FrameMain
        FrameMain = Frame(master, bg="dodgerBlue3")
        FrameMain.grid(row = 0, column = 0, rowspan = 1, columnspan = 2,sticky='nswe', padx=5,pady=5)

# attached intel image on the first frame called FrameMain

        path = "degeteshale.png"
        img = ImageTk.PhotoImage(Image.open(path))
        panel = Label(FrameMain, image=img, borderwidth= 0)
        panel.photo = img
        panel.pack()

# scroll bar which will controll the y of the tests
        # it will help for the future when we have more tests coming

        scroll = Scrollbar(FrameMain)
        scroll.pack(side=RIGHT, fill=Y)

        self.dispayy = Canvas(FrameMain, yscrollcommand=scroll.set, bg='dodgerBlue3', borderwidth= 0)
        self.dispayy.pack(fill=Y)


# all the tests button are attached on the frameTests frame

        FrameTests = Frame(self.dispayy, bg="dodgerBlue3", borderwidth= 0)
        FrameTests.pack( expand=1)
        scroll.config(command=self.dispayy.yview)

        # --- create canvas with scrollbar ---
        # global frame
        # frame = Frame(master)
        # frame.grid(row=0, column=2, rowspan=12, columnspan=4, pady=5, padx=5, sticky='nswe')
        #
        # scroll = Scrollbar(frame)
        # scroll.pack(side=RIGHT, fill=Y)
        #
        # # Text Widget
        # global eula
        # self.eula = Text(frame, wrap=WORD, yscrollcommand=scroll.set, bg='lemon chiffon', padx=5, pady=5,
        #             font=('Lucida Bright', 10, 'bold'))
        #
        # self.eula.insert("1.0", "TEST RESULT \n\n")
        # self.eula.pack(side=LEFT, fill=Y)
        #
        # # Configure the scrollbars
        # scroll.config(command=self.eula.yview)



        FrameDevice = Frame(master, bg="dodgerBlue3")
        FrameDevice.grid(row = 1, column = 0, rowspan = 1, columnspan = 2, sticky = W+E+N+S, padx=5,pady=5)

        buttonSe = Button(FrameDevice, fg='white',text="Devices :",font=('Lucida Bright',8,'bold'), bg= 'dodgerBlue3', borderwidth= 0)
        #buttonSe.grid(column=2, row=0, padx=5)
        buttonSe.grid(column=0, row=0, sticky=E + W, pady=5)

        # buttonSe2 = Button(FrameDevice, text="Devices :",font=('Lucida Bright',10,'bold'), bg= 'sky blue')
        # buttonSe2.grid(column=1, row=0, padx=7)

        # I get the device name from the config file name ssd.cfg
        # It is usefull for the user to select different devices and work on

        if os.path.exists('ssd.cfg'):
            f = open('ssd.cfg', 'r')
            ispeed = f.readline().strip().split(":")[1]
            iwidth = f.readline().strip().split(":")[1]
            iven_id = f.readline().strip().split(":")[1]
            idev_id = f.readline().strip().split(":")[1]
            f.close()
        device_list = str(New_.getBDF(idev_id))
        Dev = device_list + ' - Intel(R) Solid-State Drive ArbordalePlus'


        device = StringVar(FrameDevice)
        device.set("choose device")  # default value
        #
        w = OptionMenu(FrameDevice, device, Dev)
       # w.grid(column=3, row=0, padx=3)
        w.grid(column=1, row=0,padx=3)
        w.config(fg='white', bg="dodgerBlue3",font=('Lucida Bright',8,'bold'))

# I use grid to set up the buttons for the tests

        button1 = Button(FrameTests, text="LTSSM", bg='deep sky blue', command=self.LTSSMtests,font=('Lucida Bright',8,'bold'),height = 2, width = 9, borderwidth= 10)
        button1.grid(column=2, row=6, padx=5, pady=15)

        button2 = Button(FrameTests, text="IO\nBandwidth", bg='deep sky blue',command=self.IOmeter,font=('Lucida Bright',8,'bold'),height = 2, width = 9, borderwidth= 10)
        button2.grid(column=3, row=6, padx=15, pady=15)

        button3 = Button(FrameTests, text="RAID",bg='deep sky blue',command=self.Raid,font=('Lucida Bright',8,'bold'),height = 2, width = 9, borderwidth= 10)
        button3.grid(column=4, row=6, padx=15, pady=15)

        button4 = Button(FrameTests, text="Config\nSpace", bg='deep sky blue',command=self.configSpace,font=('Lucida Bright',8,'bold'),height = 2, width = 9, borderwidth= 10)
        button4.grid(column=5, row=6, padx=15, pady=15)

        button5 = Button(FrameTests, text="Hotplug",bg='deep sky blue',command=self.Hotplug,font=('Lucida Bright',8,'bold'),height = 2, width = 9, borderwidth= 10)
        button5.grid(column=2, row=7, padx=15, pady=15)

        button6 = Button(FrameTests, text="Resets",bg='deep sky blue',command=self.Resets,font=('Lucida Bright',8,'bold'),height = 2, width = 9, borderwidth= 10)
        button6.grid(column=3, row=7, padx=15, pady=15)

        button7 = Button(FrameTests, text="PCLMT",bg='deep sky blue',command=self.lanemargining,font=('Lucida Bright',8,'bold'),height = 2,width = 9, borderwidth= 10)
        button7.grid(column=4, row=7, padx=15, pady=15)

        button8 = Button(FrameTests, text="Data\nIntegrity", bg='deep sky blue',command=self.dataIntegrity,font=('Lucida Bright',8,'bold'),height = 2,width = 9, borderwidth= 10)
        button8.grid(column=5, row=7)

##########################################################

        FrameSelected = Frame(master, bg="dodgerBlue3")
        FrameSelected.grid(row = 2, column = 0, rowspan = 1, columnspan = 2, sticky = N+W+E+S,padx=5,pady=5)

        buttonSelected = Button(FrameSelected, fg='white',text="       Selected Test :",font=('Lucida Bright',8,'bold'), bg= 'dodgerBlue3', borderwidth= 0)
        buttonSelected.grid(column=0, row=0,  pady=5,sticky=N+S+E+W)

        buttonSelected2 = Button(FrameSelected, fg='white',text="      Supported OS :",font=('Lucida Bright',8,'bold'),  bg= 'dodgerBlue3', borderwidth= 0)
        buttonSelected2.grid(column=2, row=0, padx=7,sticky=E+W)

        buttonSelected3 = Button(FrameSelected,fg='white', text="      Duration :",font=('Lucida Bright',8,'bold'),  bg= 'dodgerBlue3', borderwidth= 0)
        buttonSelected3.grid(column=0, row=1,sticky=N+S+E+W)

        global entry_varSelected
        self.entry_varSelected = StringVar()
        entrySelected = Entry(FrameSelected,textvariable=self.entry_varSelected,font=('Lucida Bright',8,'bold'))
        entrySelected.grid(column=1, row=0, padx=7)
        entrySelected.configure(state="disabled")

        self.entry_varOS = StringVar()
        entrySelected2 = Entry(FrameSelected, textvariable=self.entry_varOS,font=('Lucida Bright',8,'bold'))
        entrySelected2.grid(column=3, row=0)
        entrySelected2.configure(state="disabled")

        self.entry_varDuuration = StringVar()
        entrySelected3 = Entry(FrameSelected, textvariable=self.entry_varDuuration,font=('Lucida Bright',8,'bold'))
        entrySelected3.grid(column=1, row=1)
        entrySelected3.configure(state="disabled")


        # selected_label = Label(FrameSelected, text='Selected Test',bg='dodger blue',font=('Lucida Bright',10))
        # duration_label = Label(FrameSelected, text='Duration:',bg='dodger blue',font=('Lucida Bright',12))
        # support_label = Label(FrameSelected, text='Support OS:',bg='dodger blue',font=('Lucida Bright',12))
        # entry_Selected = Entry(FrameSelected, background='light blue')
        # entry_Duration = Entry(FrameSelected)
        # entry_OS = Entry(FrameSelected, background='light blue')
        #
        # selected_label.grid(row=1, columnspan=1)
        # duration_label.grid(row=2, columnspan=1)
        # support_label.grid(row=3, columnspan=1 )
        # entry_Selected.grid(row=1, column=2)
        # entry_Duration.grid(row=2, column=2)
        # entry_OS.grid(row=3, column=2)
###################################################
        dispayyy = Frame(master, bg="light blue")
        dispayyy.grid(row = 4, column = 0, rowspan = 3, columnspan = 2, sticky = W+E+N+S, padx=5,pady=5)

        FrameTable0= Canvas(dispayyy, bg='light blue', borderwidth= 0)
        FrameTable0.pack(fill=Y)

        global FrameTable
        FrameTable = Frame(FrameTable0, bg='light blue', borderwidth=0)
        FrameTable.pack( expand=1)
        # entry5 = Entry(FrameTable, textvariable=self.entry_varr1, font=('Lucida Bright', 10, 'bold'))
        self.entry_TestName = StringVar()
        self.entry_Duration = StringVar()
        self.entry_Support = StringVar()

        button9 = Entry(FrameTable, textvariable=self.entry_TestName,font=('Arial',11,'bold'),state="disabled")
        button9.grid(column=4, row=8, padx=0, pady=0,sticky=N+S+E+W)
        button10 = Entry(FrameTable, textvariable=self.entry_Duration,font=('Arial',11,'bold'),state="disabled")
        button10.grid(column=6, row=8, padx=0, pady=0,sticky=N+S+E+W)
        button11 = Entry(FrameTable, textvariable=self.entry_Support,font=('Arial',11,'bold'),state="disabled")
        button11.grid(column=8, row=8, padx=0, pady=0,sticky=N+S+E+W)

        self.entry_varLinkDisable = StringVar()
        self.entry_varSbr = StringVar()
        self.entry_varSpeedChange = StringVar()
        self.entry_varLinkRetrain = StringVar()
        self.entry_varTxEqRedo = StringVar()
        self.entry_varPm11 = StringVar()
        self.entry_var4 = StringVar()

        self.entry_varr1 = StringVar()
        self.entry_varr2 = StringVar()
        self.entry_varr3 = StringVar()
        self.entry_varr4 = StringVar()
        self.entry_varr5 = StringVar()
        self.entry_varr6 = StringVar()
        self.entry_varr7 = StringVar()

        self.entry_varrr1 = StringVar()
        self.entry_varrr2 = StringVar()
        self.entry_varrr3 = StringVar()
        self.entry_varrr4 = StringVar()
        self.entry_varrr5 = StringVar()
        self.entry_varrr6 = StringVar()
        self.entry_varrr7 = StringVar()

        self.entry_var6 = StringVar()

        # IO entries
        self.entry_var = StringVar()
        # coming soon entry
        self.entry_varsoon = StringVar()

        ########################################################################################################################################################################
        # entry00Ck = Label(FrameTable, background='light blue')
        # entry00Ck.grid(column=3, row=8, padx=0, pady=0,sticky=N+S+E+W)
        entry1 = Label(FrameTable, textvariable=self.entry_varLinkDisable, background='light blue',font=('Lucida Bright',9,'bold'))
        entry1.grid(column=4, row=9, padx=0, pady=0,sticky=N+S+E+W)
        global linkDisable,linkSpeed,linkRetrain,sbr,TxEqRedo,pm11,h
        linkDisable=IntVar()
        self.entry1Ck = Checkbutton(FrameTable, background='light blue',variable=linkDisable,font=('Lucida Bright',9,'bold'))

        entry2 = Label(FrameTable, textvariable=self.entry_varSpeedChange,font=('Lucida Bright',9,'bold'), background='light blue')
        entry2.grid(column=4, row=10, padx=0, pady=0,sticky=N+S+E+W)
        linkSpeed=IntVar()
        self.entry2Ck = Checkbutton(FrameTable, background='light blue',variable=linkSpeed)


        entry3 = Label(FrameTable, textvariable=self.entry_varLinkRetrain, background='light blue',font=('Lucida Bright',9,'bold'))
        entry3.grid(column=4, row=11, padx=0, pady=0,sticky=N+S+E+W)
        linkRetrain=IntVar()
        self.entry3Ck = Checkbutton(FrameTable, background='light blue',variable=linkRetrain)


        entry4 = Label(FrameTable, textvariable=self.entry_varSbr,font=('Lucida Bright',9,'bold'), background='light blue')
        entry4.grid(column=4, row=12, padx=0, pady=0,sticky=N+S+E+W)
        sbr=IntVar()
        self.entry4Ck = Checkbutton(FrameTable, background='light blue',variable=sbr)


        entry8 = Label(FrameTable, background='light blue',textvariable=self.entry_varTxEqRedo,font=('Lucida Bright',9,'bold'))
        entry8.grid(column=4, row=13, padx=0, pady=0,sticky=N+S+E+W)
        TxEqRedo=IntVar()
        self.entry8Ck = Checkbutton(FrameTable, background='light blue',variable=TxEqRedo)


        entry9 = Label(FrameTable,font=('Lucida Bright',9,'bold'),textvariable=self.entry_varPm11, background='light blue')
        entry9.grid(column=4, row=14, padx=0, pady=0,sticky=N+S+E+W)
        pm11=IntVar()


        entry10 = Label(FrameTable, background='light blue',font=('Lucida Bright',9,'bold'))
        entry10.grid(column=4, row=15, padx=0, pady=0,sticky=N+S+E+W)
        h=IntVar()
        self.entry10Ck = Label(FrameTable, background='light blue')


#####################################################################

        FrameRun = Frame(master, bg="dodgerBlue3")
        FrameRun.grid(row = 7, column = 0, rowspan = 3, columnspan = 2, sticky = W+E+N+S, padx=5,pady=5)

        self.entry_varTime = StringVar()
        entryTime = Label(FrameRun, bg='light blue',textvariable=self.entry_varTime,font=('Lucida Bright', 10,'bold'), borderwidth= 1)
        entryTime.grid(column=1, row=0, padx=0.5, pady=15,sticky=N+S+E+W)
        global iteration
        iteration=IntVar()

        entryIteration = Entry(FrameRun, background='light blue',font=('Lucida Bright',10,'bold'),textvariable=iteration)
        entryIteration.grid(column=2, row=0,padx=0.5, pady=15,sticky=N+S+E+W)

        button1 = Button(FrameRun, text="            Run Selected Test", bg='gold',command=self.RUNtests,font=('Lucida Bright',8,'bold'))
        button1.grid(column=1, row=1, padx=0.5, pady=15)
        button1 = Button(FrameRun, text="            Run All Test",command=self.RunAllTests, bg='gold',font=('Lucida Bright', 8,'bold'))
        button1.grid(column=2, row=1, padx=0.5, pady=15)
        button1 = Button(FrameRun, text="            Run Entire Suit", bg='gold',font=('Lucida Bright', 8,'bold'))
        button1.grid(column=3, row=1)


##########################################################
        global frame
        frame = Frame(master)
        frame.grid(row=0, column=2, rowspan=12, columnspan=4, pady=5, padx=5, sticky='nswe')
        # global canvas
        # canvas = Canvas(frame, bg='sky blue',scrollregion=frame.bbox("all"))

        # vbar = Scrollbar(frame, orient=VERTICAL)
        # vbar.pack(side=RIGHT, fill=Y)
        # canvas.config( yscrollcommand=vbar.set)
        # canvas.pack(side=LEFT, expand=True, fill=BOTH)\

        scroll = Scrollbar(frame)
        scroll.pack(side=RIGHT, fill=Y)

        # Text Widget
        global eula
        self.eula = Text(frame, wrap=WORD, yscrollcommand=scroll.set, bg='lemon chiffon', padx=5, pady=5,
                    font=('Lucida Bright', 10, 'bold'))
        # eula.grid(row=0, column=3, rowspan=10, columnspan=3, sticky=W + N + S + E, padx=5, pady=5)
        self.eula.insert("1.0", "TEST RESULT \n\n")
        self.eula.pack(side=LEFT, fill=Y)
        self.eula.configure(state="disabled")

        # Configure the scrollbars
        scroll.config(command=self.eula.yview)

    global table
    def table(self):
        entry5 = Label(FrameTable, textvariable=self.entry_varr1, background='light blue',font=('Lucida Bright', 10, 'bold'))
        entry5.grid(column=6, row=9, padx=0, pady=0, sticky=N + S + E + W)
        entry6 = Label(FrameTable, textvariable=self.entry_varr2, font=('Lucida Bright', 10, 'bold'),background='light blue')
        entry6.grid(column=6, row=10, padx=0, pady=0, sticky=N + S + E + W)
        entry7 = Label(FrameTable, textvariable=self.entry_varr3, background='light blue',font=('Lucida Bright', 10, 'bold'))
        entry7.grid(column=6, row=11, padx=0, pady=0, sticky=N + S + E + W)
        entry8 = Label(FrameTable, textvariable=self.entry_varr4, font=('Lucida Bright', 10, 'bold'), background='light blue')
        entry8.grid(column=6, row=12, padx=0, pady=0, sticky=N + S + E + W)
        entry16 = Label(FrameTable, textvariable=self.entry_varr5, background='light blue',font=('Lucida Bright', 10, 'bold'))
        entry16.grid(column=6, row=13, padx=0, pady=0, sticky=N + S + E + W)
        entry17 = Label(FrameTable, textvariable=self.entry_varr6, font=('Lucida Bright', 10, 'bold'),background='light blue')
        entry17.grid(column=6, row=14, padx=0, pady=0, sticky=N + S + E + W)
        entry18 = Label(FrameTable, textvariable=self.entry_varr7, background='light blue',font=('Lucida Bright', 10, 'bold'))
        entry18.grid(column=6, row=15, padx=0, pady=0, sticky=N + S + E + W)

        ############################
        entry9 = Label(FrameTable, textvariable=self.entry_varrr1, background='light blue',font=('Lucida Bright', 10, 'bold'))
        entry9.grid(column=8, row=9, padx=0, pady=0, sticky=N + S + E + W)
        entry10 = Label(FrameTable, textvariable=self.entry_varrr2, font=('Lucida Bright', 10, 'bold'),background='light blue')
        entry10.grid(column=8, row=10, padx=0, pady=0, sticky=N + S + E + W)
        entry11 = Label(FrameTable, textvariable=self.entry_varrr3, background='light blue',font=('Lucida Bright', 10, 'bold'))
        entry11.grid(column=8, row=11, padx=0, pady=0, sticky=N + S + E + W)
        entry12 = Label(FrameTable, textvariable=self.entry_varrr4, font=('Lucida Bright', 10, 'bold'),background='light blue')
        entry12.grid(column=8, row=12, padx=0, pady=0, sticky=N + S + E + W)
        entry13 = Label(FrameTable, textvariable=self.entry_varrr5, background='light blue',font=('Lucida Bright', 10, 'bold'))
        entry13.grid(column=8, row=13, padx=0, pady=0, sticky=N + S + E + W)
        entry14 = Label(FrameTable, textvariable=self.entry_varrr6, font=('Lucida Bright', 10, 'bold'), background='light blue')
        entry14.grid(column=8, row=14, padx=0, pady=0, sticky=N + S + E + W)
        entry15 = Label(FrameTable, textvariable=self.entry_varrr7, background='light blue',font=('Lucida Bright', 10, 'bold'))
        entry15.grid(column=8, row=15, padx=0, pady=0, sticky=N + S + E + W)
    global coming
    def coming(self,name):
        self.entry_varSelected.set(name)
        self.currentTest = name
        self.entry_varOS.set('Windows')
        self.entry_varLinkDisable.set('')
        self.entry_varSpeedChange.set('')
        self.entry_varLinkRetrain.set('')
        self.entry_varSbr.set('')
        self.entry_varPm11.set('')
        self.entry_varTxEqRedo.set('')
########################################################
    def LTSSMtests(self):
        self.entry_varLinkDisable.set('Link disable')
        self.entry_varSpeedChange.set('Speed Change')
        self.entry_varLinkRetrain.set('link Retrain')
        self.entry_varSbr.set('SBR')
        self.entry_varPm11.set('pmll')
        self.entry_varTxEqRedo.set('TxEqRedo')
        self.entry_varSelected.set('LTSSM')
        self.entry_varOS.set('Windows')
        self.entry_varDuuration.set('2 sec(each)')
        # self.entry_varS2.set('4')
        self.currentTest= 'LTSSM'
        self.eula.delete('1.0', END)
        self.eula.insert("1.0", "TEST RESULT . . . \n\n")
        table(self)

        self.entry_varr1.set('2'),self.entry_varr2.set('2'),self.entry_varr3.set('2'),self.entry_varr4.set('2'),self.entry_varr5.set('2'),self.entry_varr6.set('2'),self.entry_varr7.set('')
        self.entry_varrr1.set('Yes'),self.entry_varrr2.set('Yes'),self.entry_varrr3.set('Yes'),self.entry_varrr4.set('Yes'),self.entry_varrr5.set('Yes'),self.entry_varrr6.set('Yes'),self.entry_varrr7.set('')
        self.entry_varTime.set('    Iteration')
        iteration.set(1)
        self.entry9Ck = Checkbutton(FrameTable, background='light blue', variable=pm11)
        button11 = Entry(FrameTable, textvariable=self.entry_Support,font=('Arial',11,'bold'),state="disabled")
        button11.grid(column=8, row=8, padx=0, pady=0,sticky=N+S+E+W)
        self.entry_TestName.set('          Test Names'), self.entry_Duration.set('            Duration(sec)'), self.entry_Support.set('            Support')

        self.entry1Ck.grid(column=3, row=9, padx=0, pady=0, sticky=N + S + E + W),self.entry2Ck.grid(column=3, row=10, padx=0, pady=0,sticky=N+S+E+W),self.entry3Ck.grid(column=3, row=11, padx=0, pady=0,
                        sticky=N+S+E+W),self.entry4Ck.grid(column=3, row=12, padx=0, pady=0,sticky=N+S+E+W),self.entry8Ck.grid(column=3, row=13, padx=0, pady=0,sticky=N+S+E+W),
        self.entry9Ck.grid(column=3, row=14, padx=0, pady=0, sticky=N + S + E + W),self.entry10Ck.grid(column=3, row=15, padx=0, pady=0,sticky=N+S+E+W)
        entry9 = Label(FrameTable, font=('Lucida Bright', 9, 'bold'), background='light blue',textvariable=self.entry_varPm11)
        entry9.grid(column=4, row=14, padx=0, pady=0, sticky=N + S + E + W)
############################################################################
    def IOmeter(self):
        self.entry_varSelected.set('IO Bandwidth')
        self.currentTest = 'IO Bandwidth'
        self.entry_varOS.set('Windows')
        self.entry_varLinkDisable.set('(3)iometer')
        self.entry_varSpeedChange.set('iometer')
        self.entry_varLinkRetrain.set('Gen4_SpeedTest')
        self.entry_varSbr.set('')
        self.entry_varPm11.set('')
        self.entry_varTxEqRedo.set('')
        self.entry_varDuuration.set('5min(default)')
        self.eula.delete('1.0', END)
        self.eula.insert("1.0", "TEST RESULT . . . \n\n")
        self.entry_varr6.set(''),self.entry_varr5.set(''),self.entry_varr4.set(''),self.entry_varr1.set('5'),self.entry_varr2.set('5'),self.entry_varr3.set('5')
        self.entry_varrr5.set(''),self.entry_varrr6.set(''),self.entry_varrr4.set(''),self.entry_varrr1.set('Yes'),self.entry_varrr2.set('Yes'),self.entry_varrr3.set('Yes')
        table(self)
        button11 = Entry(FrameTable, textvariable=self.entry_Support,font=('Arial',11,'bold'),state="disabled")
        button11.grid(column=8, row=8, padx=0, pady=0,sticky=N+S+E+W)
        self.entry_varTime.set('   Run Time (min)'),self.entry_TestName.set('            Config Files'),self.entry_Duration.set('          Duration (Min)'),self.entry_Support.set('            Support')
        iteration.set(1)
        self.entry1Ck.grid(column=3, row=9, padx=0, pady=0, sticky=N + S + E + W),self.entry2Ck.grid(column=3, row=10, padx=0, pady=0,sticky=N+S+E+W),self.entry3Ck.grid(column=3, row=11, padx=0, pady=0,sticky=N+S+E+W)

        entry9 = Label(FrameTable, font=('Lucida Bright', 9, 'bold'), background='light blue', textvariable=self.entry_varPm11)
        entry9.grid(column=4, row=14, padx=0, pady=0, sticky=N + S + E + W)
############################################################################
    def Raid(self):
        coming(self, 'Raid')
        popupmsg("COMING SOON . . .")

############################################################################
    def configSpace(self):
        coming(self, 'configSpace')
        popupmsg("COMING SOON . . .")

############################################################################
    def Hotplug(self):
        coming(self, 'Hotplug')
        popupmsg("COMING SOON . . .")

############################################################################
    def Resets(self):
        coming(self, 'Resets')
        popupmsg("COMING SOON . . .")

############################################################################
    def dataIntegrity(self):
        coming(self, 'Data Integrity')
        popupmsg("COMING SOON . . .")

############################################################################
    def lanemargining(self):
        self.entry_varSelected.set('lane margining')
        self.currentTest = 'lane margining'
        self.entry_varOS.set('Windows')
        self.entry_varLinkDisable.set('LinkDown Linkup')
        self.entry_varLinkRetrain.set('link Retrain')
        self.entry_varSpeedChange.set('Speed Change')
        self.entry_varSbr.set('SBR')

        self.entry_varTxEqRedo.set('All')
        table(self)
        self.entry_varr1.set(''),self.entry_varr2.set(''),self.entry_varr3.set(''),self.entry_varr4.set(''),self.entry_varr5.set(''),self.entry_varr6.set(''),self.entry_varr7.set('')
        self.entry_varrr1.set(''),self.entry_varrr2.set(''),self.entry_varrr3.set(''),self.entry_varrr4.set(''),self.entry_varrr5.set(''),self.entry_varrr6.set(''),self.entry_varrr7.set('')

        entry9 = Label(FrameTable,font=('Arial',10,'bold'),background='gold',textvariable=self.entry_varPm11)
        entry9.grid(column=4, row=14, padx=0, pady=0,sticky=N+S+E+W)
        self.entry_varPm11.set('RUN DRIVE SIDE MARGINING')

        self.entry1Ck.grid(column=3, row=9, padx=0, pady=0, sticky=N + S + E + W)
        self.entry_varr6.set('')

        self.entry9Ck = Checkbutton(FrameTable, background='light blue', variable=pm11)
        self.entry_TestName.set('         Test Names'),self.entry_Duration.set('     Customer name -')
        self.entry2Ck.grid(column=3, row=10, padx=0, pady=0, sticky=N + S + E + W), self.entry3Ck.grid(column=3, row=11,padx=0, pady=0,sticky=N + S + E + W),
        self.entry4Ck.grid(column=3, row=12, padx=0, pady=0, sticky=N + S + E + W), self.entry8Ck.grid(column=3, row=13, padx=0,pady=0, sticky=N + S + E + W),
        self.entry9Ck.grid(column=3, row=14, padx=0, pady=0, sticky=N + S + E + W)
        self.entry_varTime.set('   Test cycle')
        entryCustomer = Entry(FrameTable,font=('Lucida Bright',9,'bold'),background='light blue')
        entryCustomer.grid(column=8, row=8, padx=0, pady=0,sticky=N+S+E+W)
############################################################################

    def RunAllTests(self):
        input = iteration.get()
        if self.currentTest == 'LTSSM':
            for i in range(1, 6):
                sys.stdout = TextRedirector(self.eula)
                New_.runTest(input, i)
        # proc = subprocess.Popen(['SSD LTSSM.bat'], stdin=subprocess.PIPE, shell=True, stderr=subprocess.PIPE,stdout=subprocess.PIPE)  # working code
        # out, err = proc.communicate()


    global IO
    def IO(self, configFile):
        input = iteration.get()
        exeFile = r'C:\\TestSuite\\IOBandwidth\\IOMeter.exe'
        logFolder = datetime.now().strftime('%Y.%m.%d.%H.%M.%S')
        os.mkdir(os.path.join(os.getcwd(), "ioMeter results", logFolder))
        resultFile = "TempLog.csv"



        for csv_file in glob.glob(os.getcwd() + "\\*.csv"):
            shutil.move(csv_file, os.path.join(os.getcwd(), "ioMeter results", logFolder))
        # resultFile = exeFile.join("\\Logs\\".join("_result.csv"));
        # subprocess.call(resultFile)
        # print (exeFile + " /c " + configFile + " /r " + resultFile);

        #builder = os.path.join(exeFile, configFile, resultFile)

        builder = r'C:\\TestSuite\\IOBandwidth\\IOMeter.exe -c {0} -r {1}'.format(configFile, resultFile)
        cmd_out = os.system(builder)

#################################################################################
    def RUNtests(self):
        input = iteration.get()
        if self.currentTest == 'LTSSM':
            if sbr.get():
                sys.stdout = TextRedirector(self.eula)
                New_.runTest(input, 1)
            if linkRetrain.get():
                sys.stdout = TextRedirector(self.eula)
                New_.runTest(input, 2)
            if linkDisable.get():
                sys.stdout = TextRedirector(self.eula)
                New_.runTest(input, 3)
            if linkSpeed.get():
                sys.stdout = TextRedirector(self.eula)
                New_.runTest(input, 4)
            if TxEqRedo.get():
                sys.stdout = TextRedirector(self.eula)
                New_.runTest(input, 5)
            if pm11.get():
                sys.stdout = TextRedirector(self.eula)
                New_.runTest(input, 6)

######################################################################
        if self.currentTest == 'IO Bandwidth':
            input = iteration.get()


            sys.stdout = TextRedirector(self.eula)
            # print 'please select Drive and Run time and hit <Start task> on IO application'
            exeFile = r'C:\\TestSuite\\IOBandwidth\\IOMeter.exe'
            your_module_address1 = r'C:\TestSuite\IOBandwidth\Configs\iometer.icf'
            your_module_address2 = r'C:\TestSuite\IOBandwidth\Configs\(3)iometer.icf'
            your_module_address3 = r'C:\TestSuite\IOBandwidth\Configs\Gen4_SpeedTest_ConfigFile.icf'

            if linkDisable.get():
                replace(your_module_address1,'0',str(input),'0')
                if input>=1:
                    sys.stdout = TextRedirector(self.eula)
                    IO(self, your_module_address1)
                    IOdisplay()
            if linkSpeed.get():
                replace(your_module_address2, '0', str(input), '0')
                if input >= 1:
                    sys.stdout = TextRedirector(self.eula)
                    IO(self, your_module_address2)
                    IOdisplay()
            if linkRetrain.get():
                replace(your_module_address3, '0', str(input), '0')
                if input >= 1:
                    sys.stdout = TextRedirector(self.eula)
                    IO(self, your_module_address3)
                    IOdisplay()
                # sys.stdout = TextRedirector(self.eula)


################################################################
        if self.currentTest =='lane margining':
            sys.stdout = TextRedirector(self.eula)
            os.system("LTSSM_Program_version2.py")

################################################################

# this function will clear whatever we have on the display frame

    def clearTest(self):

        sys.stdout = TextRedirector(self.eula.delete('1.0',END))
        # sys.stdout = TextRedirector.delete('1.0', END)
        # self.eula.delete('1.0', END)
        # print "TEST RESULT \n\n"

############################################################################



root = Tk()
RWidth=root.winfo_screenwidth()
RWidth=RWidth/1.08
       # /1.40
RHeight=root.winfo_screenheight()
RHeight=RHeight/1.1
        # /1.50
root.geometry(("%dx%d")%(RWidth,RHeight))
root.configure(background='light blue')
root.iconbitmap(r'intel.ico')





app = Application(master=root)
app.mainloop()
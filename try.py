from Tkinter import *
from TestLTSSM_Multi import *
from multiprocessing import Process
from subprocess import Popen, PIPE
import sys
from itertools import islice
from subprocess import Popen, PIPE
from textwrap import dedent
from threading import Thread
from PIL import ImageTk, Image
import New_
from tempfile import mkstemp
from shutil import move
from os import fdopen, remove
import csv

class TextRedirector(object):
    def __init__(self, widget):
        self.terminal = sys.stdout
        self.widget = widget

    def write(self, str):
        self.widget.configure(state="normal")
        self.widget.insert("end", str)
        self.widget.configure(state="disabled")

# class TextRedirector(object):
# def replace(configFile,subst):
#     with open(configFile, 'r+') as f:
#         read=f.read()
#         adiswa = read.split('\n')
#         lela= adiswa[6]
#     #Create temp file
#     fh, abs_path = mkstemp()
#     with fdopen(fh,'w') as new_file:
#         with open(configFile) as old_file:
#             for line in old_file:
#                 new_file.write(line.replace(lela[12], subst))
#     #Remove original file
#     remove(configFile)
#     #Move new file
#     move(abs_path, configFile)
# #         pass
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

def IOdisplay():
    output = []

    with open('TempLog.csv', 'r') as f:
        reader = csv.reader(f)
        read = f.read()
        adiswa = read.split('\n')

        for i in range(0, 13):
            print (adiswa[i].replace("'", ' '))
        print '\n'
        for i in range(13, 17):
            print (adiswa[i].split(',')[15])
            # print (adiswa[i].split(',')[16])

##############################################################################################
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



def parseLog(self, logFolder):

    errFound = False
    errLine = ""
    globalErr = False

    flist = glob.glob(os.path.join(os.getcwd(), 'ioMeter results', logFolder, '*.csv'))

    if not flist:
        print "\n-W- No log files to parse in folder : {0}".format(os.path.join(os.getcwd(), 'ioMeter results', logFolder))
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
            print "--- Error found in : {0} ---".format(fn)
            for key, val in errDict.items():
                print "{0} = {1} times".format(key, val)
            print "\n\n"
    if not globalErr:
        print "\n\n*****  No error seen in IO test.. !  ******"
        print "\nParsing of all log file complted...!"


class Application(Frame):
    def __init__(self, master=None):
        Frame.__init__(self, master)
        self.grid()
        self.master.title("Platform Connected Test Suite")

        for r in range(1):
            self.master.rowconfigure(r, weight=1)
        for c in range(1):
            self.master.columnconfigure(c, weight=1)
            Button(master, text="            Clear Test Result".format(c),fg='yellow',  bg='dodgerBlue3', command=self.clearTest,font=('Lucida Bright',10,'bold')).grid(row=10,column=c,sticky=W)

################################################################
        FrameMain = Canvas(master, bg="dodgerBlue3")
        FrameMain.grid(row = 0, column = 0, rowspan = 1, columnspan = 2, sticky = W+E+N+S, padx=5,pady=5)

        path = "degeteshale.png"
        img = ImageTk.PhotoImage(Image.open(path))
        panel = Label(FrameMain, image=img, borderwidth= 0)
        panel.photo = img
        panel.pack()

        scroll = Scrollbar(FrameMain)
        scroll.pack(side=RIGHT, fill=Y)

        self.dispayy = Canvas(FrameMain, yscrollcommand=scroll.set, bg='dodgerBlue3', borderwidth= 0,width=500,height=500,scrollregion=(0,0,500,800))
        self.dispayy.pack(fill=Y)

        scroll.config(command=self.dispayy.yview)

        FrameTests = Frame(self.dispayy, bg="dodgerBlue3")
        FrameTests.pack( expand=1)


        FrameDevice = Frame(master, bg="light blue")
        FrameDevice.grid(row = 1, column = 0, rowspan = 1, columnspan = 2, sticky = W+E+N+S, padx=5,pady=5)

        buttonSe = Button(FrameDevice, text="Devices :",font=('Lucida Bright',8,'bold'), bg= 'light blue', borderwidth= 0)
        #buttonSe.grid(column=2, row=0, padx=5)
        buttonSe.grid(column=0, row=0, sticky=E + W, pady=5)

        # buttonSe2 = Button(FrameDevice, text="Devices :",font=('Lucida Bright',10,'bold'), bg= 'sky blue')
        # buttonSe2.grid(column=1, row=0, padx=7)
        #
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
        w.config(bg="light blue",font=('Lucida Bright',8,'bold'))


        button1 = Button(FrameTests, text="LTSSM", bg='deep sky blue', command=self.LTSSMtests,font=('Lucida Bright',8,'bold'),height = 3, width = 9, borderwidth= 10)
        button1.grid(column=2, row=6, padx=5, pady=20)

        button2 = Button(FrameTests, text="IO\nBandwidth", bg='deep sky blue',command=self.IOmeter,font=('Lucida Bright',8,'bold'),height = 3, width = 9, borderwidth= 10)
        button2.grid(column=3, row=6, padx=15, pady=20)

        button3 = Button(FrameTests, text="RAID",bg='deep sky blue',command=self.Raid,font=('Lucida Bright',8,'bold'),height = 3, width = 9, borderwidth= 10)
        button3.grid(column=4, row=6, padx=15, pady=20)

        button4 = Button(FrameTests, text="Config\nSpace", bg='deep sky blue',command=self.configSpace,font=('Lucida Bright',8,'bold'),height = 3, width = 9, borderwidth= 10)
        button4.grid(column=5, row=6, padx=15, pady=20)

        button5 = Button(FrameTests, text="Hotplug",bg='deep sky blue',command=self.Hotplug,font=('Lucida Bright',8,'bold'),height = 3, width = 9, borderwidth= 10)
        button5.grid(column=2, row=7, padx=15, pady=20)

        button6 = Button(FrameTests, text="Resets",bg='deep sky blue',command=self.Resets,font=('Lucida Bright',8,'bold'),height = 3, width = 9, borderwidth= 10)
        button6.grid(column=3, row=7, padx=15, pady=20)

        button7 = Button(FrameTests, text="lane\nmargining",bg='deep sky blue',command=self.lanemargining,font=('Lucida Bright',8,'bold'),height = 3,width = 9, borderwidth= 10)
        button7.grid(column=4, row=7, padx=15, pady=20)

        button8 = Button(FrameTests, text="Data\nIntegrity", bg='deep sky blue',command=self.dataIntegrity,font=('Lucida Bright',8,'bold'),height = 3,width = 9, borderwidth= 10)
        button8.grid(column=5, row=7)

###########################################################
        FrameSelected = Frame(master, bg="lemon chiffon")
        FrameSelected.grid(row = 2, column = 0, rowspan = 1, columnspan = 2, sticky = N+W+E+S,padx=5,pady=5)

        buttonSelected = Button(FrameSelected, text="       Selected Test :",font=('Lucida Bright',8,'bold'), bg= 'lemon chiffon', borderwidth= 0)
        buttonSelected.grid(column=0, row=0,  pady=5,sticky=N+S+E+W)

        buttonSelected2 = Button(FrameSelected, text="      Supported OS :",font=('Lucida Bright',8,'bold'),  bg= 'lemon chiffon', borderwidth= 0)
        buttonSelected2.grid(column=2, row=0, padx=7,sticky=E+W)

        buttonSelected3 = Button(FrameSelected, text="      Duration :",font=('Lucida Bright',8,'bold'),  bg= 'lemon chiffon', borderwidth= 0)
        buttonSelected3.grid(column=0, row=1,sticky=N+S+E+W)

        global entry_varSelected
        self.entry_varSelected = StringVar()
        entrySelected = Entry(FrameSelected,textvariable=self.entry_varSelected, background='light blue',font=('Lucida Bright',8,'bold'))
        entrySelected.grid(column=1, row=0, padx=7)

        self.entry_varOS = StringVar()
        entrySelected2 = Entry(FrameSelected, textvariable=self.entry_varOS, background='light blue',font=('Lucida Bright',8,'bold'))
        entrySelected2.grid(column=3, row=0)

        self.entry_varDuuration = StringVar()
        entrySelected3 = Entry(FrameSelected, textvariable=self.entry_varDuuration, background='light blue',font=('Lucida Bright',8,'bold'))
        entrySelected3.grid(column=1, row=1)


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
        FrameTable = Frame(master, bg="light blue")
        FrameTable.grid(row = 4, column = 0, rowspan = 3, columnspan = 2, sticky = W+E+N+S, padx=5,pady=5)

        button9 = Button(FrameTable, text="Test Names", bg= 'light blue',font=('Lucida Bright',11,'bold'))
        button9.grid(column=4, row=8, padx=0, pady=0,sticky=N+S+E+W)
        button10 = Button(FrameTable, text="Duration (In Minutes)", bg= 'light blue',font=('Lucida Bright',11,'bold'))
        button10.grid(column=6, row=8, padx=0, pady=0,sticky=N+S+E+W)
        button11 = Button(FrameTable, text="Support", bg= 'light blue',font=('Lucida Bright',11,'bold'))
        button11.grid(column=8, row=8, padx=0, pady=0,sticky=N+S+E+W)

        self.entry_varLinkDisable = StringVar()
        self.entry_varSbr = StringVar()
        self.entry_varSpeedChange = StringVar()
        self.entry_varLinkRetrain = StringVar()
        self.entry_varTxEqRedo = StringVar()
        self.entry_varPm11 = StringVar()
        self.entry_var4 = StringVar()
        self.entry_var5 = StringVar()

        self.entry_var6 = StringVar()

        # IO entries
        self.entry_var = StringVar()
        # coming soon entry
        self.entry_varsoon = StringVar()

        entry5 = Entry(FrameTable, background='light blue', textvariable=self.entry_var5,font=('Lucida Bright',10,'bold'))
        entry5.grid(column=6, row=9, padx=0, pady=0,sticky=N+S+E+W)
        self.entry_var5.set('5 Min(s)')
        entry6 = Entry(FrameTable, textvariable=self.entry_var5,font=('Lucida Bright',10,'bold'))
        entry6.grid(column=6, row=10, padx=0, pady=0,sticky=N+S+E+W)
        self.entry_var5.set('5 Min(s)')
        entry7 = Entry(FrameTable, background='light blue', textvariable=self.entry_var5,font=('Lucida Bright',10,'bold'))
        entry7.grid(column=6, row=11, padx=0, pady=0,sticky=N+S+E+W)
        self.entry_var5.set('5 Min(s)')
        entry8 = Entry(FrameTable, textvariable=self.entry_var5,font=('Lucida Bright',10,'bold'))
        entry8.grid(column=6, row=12, padx=0, pady=0,sticky=N+S+E+W)
        self.entry_var5.set('5 Min(s)')
        entry16 = Entry(FrameTable, background='light blue', textvariable=self.entry_var5,font=('Lucida Bright',10,'bold'))
        entry16.grid(column=6, row=13, padx=0, pady=0,sticky=N+S+E+W)
        self.entry_var5.set('5 Min(s)')
        entry17 = Entry(FrameTable, textvariable=self.entry_var5,font=('Lucida Bright',10,'bold'))
        entry17.grid(column=6, row=14, padx=0, pady=0,sticky=N+S+E+W)
        self.entry_var5.set('5 Min(s)')
        entry18 = Entry(FrameTable, background='light blue', textvariable=self.entry_var5,font=('Lucida Bright',10,'bold'))
        entry18.grid(column=6, row=15, padx=0, pady=0,sticky=N+S+E+W)
        self.entry_var5.set('5 Min(s)')
        ############################
        entry9 = Entry(FrameTable, background='light blue', textvariable=self.entry_var6,font=('Lucida Bright',10,'bold'))
        entry9.grid(column=8, row=9, padx=0, pady=0,sticky=N+S+E+W)
        self.entry_var6.set('YES')
        entry10 = Entry(FrameTable, textvariable=self.entry_var6,font=('Lucida Bright',10,'bold'))
        entry10.grid(column=8, row=10, padx=0, pady=0,sticky=N+S+E+W)
        self.entry_var6.set('YES')
        entry11 = Entry(FrameTable, background='light blue', textvariable=self.entry_var6,font=('Lucida Bright',10,'bold'))
        entry11.grid(column=8, row=11, padx=0, pady=0,sticky=N+S+E+W)
        self.entry_var6.set('YES')
        entry12 = Entry(FrameTable, textvariable=self.entry_var6,font=('Lucida Bright',10,'bold'))
        entry12.grid(column=8, row=12, padx=0, pady=0,sticky=N+S+E+W)
        self.entry_var6.set('YES')
        entry13 = Entry(FrameTable, background='light blue', textvariable=self.entry_var6,font=('Lucida Bright',10,'bold'))
        entry13.grid(column=8, row=13, padx=0, pady=0,sticky=N+S+E+W)
        self.entry_var6.set('YES')
        entry14 = Entry(FrameTable, textvariable=self.entry_var6,font=('Lucida Bright',10,'bold'))
        entry14.grid(column=8, row=14, padx=0, pady=0,sticky=N+S+E+W)
        self.entry_var6.set('YES')
        entry15 = Entry(FrameTable, background='light blue', textvariable=self.entry_var6,font=('Lucida Bright',10,'bold'))
        entry15.grid(column=8, row=15, padx=0, pady=0,sticky=N+S+E+W)
        ########################################################################################################################################################################
        entry1 = Entry(FrameTable, textvariable=self.entry_varLinkDisable, background='light blue',font=('Lucida Bright',10,'bold'))
        entry1.grid(column=4, row=9, padx=0, pady=0,sticky=N+S+E+W)
        global linkDisable,linkSpeed,linkRetrain,sbr,TxEqRedo,pm11,h
        linkDisable=IntVar()
        entry1Ck = Checkbutton(FrameTable, background='light blue',variable=linkDisable,font=('Lucida Bright',10,'bold'))
        entry1Ck.grid(column=3, row=9, padx=0, pady=0)



        entry2 = Entry(FrameTable, textvariable=self.entry_varSpeedChange,font=('Lucida Bright',10,'bold'))
        entry2.grid(column=4, row=10, padx=0, pady=0,sticky=N+S+E+W)
        linkSpeed=IntVar()
        entry2Ck = Checkbutton(FrameTable,variable=linkSpeed)
        entry2Ck.grid(column=3, row=10, padx=0, pady=0)


        entry3 = Entry(FrameTable, textvariable=self.entry_varLinkRetrain, background='light blue',font=('Lucida Bright',10,'bold'))
        entry3.grid(column=4, row=11, padx=0, pady=0,sticky=N+S+E+W)
        linkRetrain=IntVar()
        entry3Ck = Checkbutton(FrameTable, background='light blue',variable=linkRetrain)
        entry3Ck.grid(column=3, row=11, padx=0, pady=0)

        entry4 = Entry(FrameTable, textvariable=self.entry_varSbr,font=('Lucida Bright',10,'bold'))
        entry4.grid(column=4, row=12, padx=0, pady=0,sticky=N+S+E+W)
        sbr=IntVar()
        entry4Ck = Checkbutton(FrameTable,variable=sbr)
        entry4Ck.grid(column=3, row=12, padx=0, pady=0)


        entry8 = Entry(FrameTable, background='light blue',textvariable=self.entry_varTxEqRedo,font=('Lucida Bright',10,'bold'))
        entry8.grid(column=4, row=13, padx=0, pady=0,sticky=N+S+E+W)
        TxEqRedo=IntVar()
        entry8Ck = Checkbutton(FrameTable, background='light blue',variable=TxEqRedo)
        entry8Ck.grid(column=3, row=13, padx=0, pady=0)

        entry9 = Entry(FrameTable,font=('Lucida Bright',10,'bold'),textvariable=self.entry_varPm11)
        entry9.grid(column=4, row=14, padx=0, pady=0,sticky=N+S+E+W)
        pm11=IntVar()
        entry9Ck = Checkbutton(FrameTable,variable=pm11)
        entry9Ck.grid(column=3, row=14, padx=0, pady=0)

        entry10 = Entry(FrameTable, background='light blue',font=('Lucida Bright',10,'bold'))
        entry10.grid(column=4, row=15, padx=0, pady=0,sticky=N+S+E+W)
        h=IntVar()
        entry10Ck = Checkbutton(FrameTable, background='light blue',variable=h)
        entry10Ck.grid(column=3, row=15, padx=0, pady=0)

#####################################################################

        FrameRun = Frame(master, bg="dodgerBlue3")
        FrameRun.grid(row = 7, column = 0, rowspan = 3, columnspan = 2, sticky = W+E+N+S, padx=5,pady=5)

        buttonIteration = Button(FrameRun, text="           Iteration", bg='sky blue',command=self.RUNtests,font=('Lucida Bright', 10,'bold'), borderwidth= 1)
        buttonIteration.grid(column=1, row=0, padx=0.5, pady=15,sticky=N+S+E+W)
        global iteration
        iteration=IntVar()
        iteration.set(1)
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

        # Configure the scrollbars
        scroll.config(command=self.eula.yview)



################################################################

    def clearTest(self):

        sys.stdout = TextRedirector(self.eula.delete('1.0',END))
        # sys.stdout = TextRedirector.delete('1.0', END)
        # self.eula.delete('1.0', END)
        # print "TEST RESULT \n\n"


########################################################
    def LTSSMtests(self):
        self.entry_varLinkDisable.set('Link disable')
        self.entry_varSpeedChange.set('Speed Change')
        self.entry_varLinkRetrain.set('link Retrain')
        self.entry_varSbr.set('SBR')
        self.entry_varPm11.set('pmll')
        self.entry_varTxEqRedo.set('TxEqRedo')
        self.entry_varSelected.set('LTSSM G3')
        self.entry_varOS.set('Windows')
        self.entry_varDuuration.set('1 min')
        # self.entry_varS2.set('4')
        self.currentTest= 'LTSSM G3'
        self.eula.delete('1.0', END)
        self.eula.insert("1.0", "TEST RESULT . . . \n\n")

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
        self.eula.delete('1.0', END)
        self.eula.insert("1.0", "TEST RESULT . . . \n\n")

############################################################################
    def Raid(self):
        self.entry_varSelected.set('Raid')
        self.currentTest = 'Raid'
        self.entry_varOS.set('Windows')
        self.entry_varLinkDisable.set('')
        self.entry_varSpeedChange.set('')
        self.entry_varLinkRetrain.set('')
        self.entry_varSbr.set('')
        self.entry_varPm11.set('')
        self.entry_varTxEqRedo.set('')
        # self.eula.delete('1.0', END)
        # self.eula.insert("1.0", "COMING SOON . . . \n\n")
        popupmsg("COMING SOON . . .")

############################################################################
    def configSpace(self):
        self.entry_varSelected.set('Config Space')
        self.currentTest = 'Config Space'
        self.entry_varOS.set('Windows')
        self.entry_varLinkDisable.set('')
        self.entry_varSpeedChange.set('')
        self.entry_varLinkRetrain.set('')
        self.entry_varSbr.set('')
        self.entry_varPm11.set('')
        self.entry_varTxEqRedo.set('')
        popupmsg("COMING SOON . . .")

############################################################################
    def Hotplug(self):
        self.entry_varSelected.set('Hotplug')
        self.currentTest = 'Hotplug'
        self.entry_varOS.set('Windows')
        self.entry_varLinkDisable.set('')
        self.entry_varSpeedChange.set('')
        self.entry_varLinkRetrain.set('')
        self.entry_varSbr.set('')
        self.entry_varPm11.set('')
        self.entry_varTxEqRedo.set('')
        popupmsg("COMING SOON . . .")

############################################################################
    def Resets(self):
        self.entry_varSelected.set('Resets')
        self.currentTest = 'Resets'
        self.entry_varOS.set('Windows')
        self.entry_varLinkDisable.set('')
        self.entry_varSpeedChange.set('')
        self.entry_varLinkRetrain.set('')
        self.entry_varSbr.set('')
        self.entry_varPm11.set('')
        self.entry_varTxEqRedo.set('')
        popupmsg("COMING SOON . . .")

############################################################################
    def dataIntegrity(self):
        self.entry_varSelected.set('Data Integrity')
        self.currentTest = 'Data Integrity'
        self.entry_varOS.set('Windows')
        self.entry_varLinkDisable.set('')
        self.entry_varSpeedChange.set('')
        self.entry_varLinkRetrain.set('')
        self.entry_varSbr.set('')
        self.entry_varPm11.set('')
        self.entry_varTxEqRedo.set('')
        popupmsg("COMING SOON . . .")

############################################################################
    def lanemargining(self):
        self.entry_varSelected.set('lane margining ')
        self.currentTest = 'lane margining'
        self.entry_varOS.set('Windows')
        self.entry_varLinkDisable.set('')
        self.entry_varSpeedChange.set('')
        self.entry_varLinkRetrain.set('')
        self.entry_varSbr.set('')
        self.entry_varPm11.set('')
        self.entry_varTxEqRedo.set('')
        popupmsg("COMING SOON . . .")
############################################################################

    def RunAllTests(self):
        input = iteration.get()
        if self.currentTest == 'LTSSM G3':
            sys.stdout = TextRedirector(self.eula)
            New_.runTest(input, 0)
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
        if self.currentTest == 'LTSSM G3':
            if sbr.get():
                sys.stdout = TextRedirector(self.eula)
                New_.runTest(input, 1)
            if linkRetrain.get() :
                sys.stdout = TextRedirector(self.eula)
                New_.runTest(input, 2)
            if linkDisable.get() :
                sys.stdout = TextRedirector(self.eula)
                New_.runTest(input, 3)
            if linkSpeed.get() :
                sys.stdout = TextRedirector(self.eula)
                New_.runTest(input, 4)
            if TxEqRedo.get() :
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
            your_command = "minutes 5"

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
                #
                #

############################################################################



############################################################################



root = Tk()
RWidth=root.winfo_screenwidth()
RWidth=RWidth/1.40
RHeight=root.winfo_screenheight()
RHeight=RHeight/1.50
root.geometry(("%dx%d")%(RWidth,RHeight))
root.configure(background='light blue')
root.iconbitmap(r'intel.ico')





app = Application(master=root)
app.mainloop()
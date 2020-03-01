import tkinter as tk
import felicaidm as fe
import nfcWithJson as nfJ
from time import sleep
import threading
import  gsUpdate
import sys

class Application(tk.Frame):
    def __init__(self, master=None):
        super().__init__(master=master)
        self.master = master
        self.pack()
        self.create_widgets()
        
    def create_widgets(self):
        self.textLabel = tk.Label(text="カードをタッチしてください。")
        self.exitSystemButton = tk.Button(text="Exit", command=sys.exit)
        self.textLabel.pack(side="top", expand=1)
        self.exitSystemButton.pack()
        self.startReadNfc()

    def startReadNfc(self):
        thread1 = threading.Thread(target=self.Attend)
        thread1.setDaemon(True)
        thread1.start()
        

    def Attend(self):
        cardID = fe.inputCard()
        if cardID == None:
            displayText = "対応していないカードです。"
            self.openMessageDialog(displayText)
            return

        authInfo = nfJ.importJson()
        if not cardID in authInfo:
            displayText = "登録されていないカードです。別のカードを試してください。"
            self.openMessageDialog(displayText)
        else:
            name = authInfo[cardID]
            displayText = f"{name}さん。出退勤を選んでください。"
            self.openSelectDialog(displayText, name)
        

    def openDialog(self):
        self.dialog = tk.Toplevel(self)
        self.dialog.title("勤怠管理システム")
        self.dialog.state("zoomed")
        self.dialog.grab_set_global()

    def openMessageDialog(self, displayText):
        self.openDialog()
        overrider(self.dialog)
        self.textLabel = tk.Label(self.dialog, text=displayText)
        self.textLabel.pack(expand=1, fill="both", padx="30", pady="10")
        self.closeButton = tk.Button(self.dialog, text="キャンセル", command=self.destroyDialog)
        self.closeButton.pack(expand=1, fill="both", padx="30", pady="10")

        
    def openSelectDialog(self, displayText, name):
        self.openMessageDialog(displayText)
        self.AttendButton = tk.Button(self.dialog, text="出勤", command=lambda: self.shukkin(name, "出勤"))
        self.AbsentButton = tk.Button(self.dialog, text="退勤", command=lambda: self.shukkin(name, "退勤"))
        self.AttendButton.pack(expand=1, fill="both", padx="30", pady="10")
        self.AbsentButton.pack(expand=1, fill="both", padx="30", pady="10")

    def destroyDialog(self):
        self.dialog.destroy()
        self.startReadNfc()
        self.master.grab_set_global()

    def shukkin(self, name, select):
        date, time = gsUpdate.addShuttaikin(name, select)
        self.dialog.destroy()
        self.openMessageDialog(f"{name}さんの{select}を{date}{time}に登録しました。")
    

def osIdentifier():
    osName = platform.system()
    if osName in ['Windows', 'Darwin', 'Linux']:
        return osName

def overrider(winObj):
    winObj.overrideredirect(True)
    if osIdentifier() == 'Darwin':
        """
        Darwinの場合のみ
        overrideredirect(True)に続けて
        overrideredirect(False)を実行しないと
        ウィンドウのベゼルが消えない。
        """
        winObj.overrideredirect(False)

root = tk.Tk()
root.title('勤怠管理システム')

root.state('zoomed')
overrider(root)

#root.overrideredirect(True)

app = Application(master=root)
app.mainloop()
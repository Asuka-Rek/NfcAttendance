from time import sleep
import sys, platform, threading
import tkinter as tk
import datetime
from pytz import timezone
# private modules
import gsUpdate
import felicaidm as fe
import nfcWithJson as nfJ
import azure_sql as azsql

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
            self.openMessageDialog(displayText=displayText, buttonText="閉じる")
            return

        authInfo = azsql.resolve_crew(card_hash=cardID)
        if authInfo is None:
            displayText = "登録されていないカードです。別のカードを試してください。"
            self.openMessageDialog(displayText=displayText, buttonText="閉じる")
        else:
            name = authInfo["name"]
            displayText = f"{name}さん。出退勤を選んでください。"
            self.openSelectDialog(displayText=displayText, name=name, authInfo=authInfo)
        

    def openDialog(self):
        self.dialog = tk.Toplevel(self)
        self.dialog.title("勤怠管理dialog")
        zoomer(self.dialog)
        self.dialog.grab_set()

    def openMessageDialog(self, displayText, buttonText):
        self.openDialog()
        overrider(self.dialog)
        self.textLabel = tk.Label(self.dialog, text=displayText)
        self.textLabel.pack(expand=1, fill="both", padx="30", pady="10")
        self.closeButton = tk.Button(self.dialog, text=buttonText, command=self.destroyDialog)
        self.closeButton.pack(expand=1, fill="both", padx="30", pady="10")

        
    def openSelectDialog(self, displayText, name, authInfo):
        self.openMessageDialog(displayText=displayText, buttonText="キャンセル")
        self.AttendButton = tk.Button(self.dialog, text="出勤", command=lambda: self.shukkin(name, "出勤", authInfo=authInfo))
        self.AbsentButton = tk.Button(self.dialog, text="退勤", command=lambda: self.shukkin(name, "退勤", authInfo=authInfo))
        self.AttendButton.pack(expand=1, fill="both", padx="30", pady="10")
        self.AbsentButton.pack(expand=1, fill="both", padx="30", pady="10")

    def destroyDialog(self):
        self.dialog.destroy()
        self.startReadNfc()
        self.master.grab_set_global()

    def shukkin(self, name, select, authInfo):
        # 現在時刻を取得
        dataNow = datetime.datetime.now(tz=timezone('Asia/Tokyo'))
        datestr = f'{dataNow.year}-{dataNow.month:02d}-{dataNow.day:02d}'
        timestr = f'{dataNow.hour:02d}:{dataNow.minute:02d}'
        # 勤怠をクラウドストレージに登録する
        azsql.shukkin(attendance=select, date_attend=f"{datestr} {timestr}", crew_data=authInfo)
        gsUpdate.addShuttaikin(workerName=name, attendance=select, dataNow=dataNow, datestr=datestr, timestr=timestr)
        # 完了メッセージの表示
        displayText = f"{name}さんの{select}を{datestr} {timestr}に登録しました。"
        self.dialog.destroy()
        self.openMessageDialog(displayText=displayText, buttonText="閉じる")
    

def osIdentifier():
    osName = platform.system()
    if osName in ['Windows', 'Darwin', 'Linux']:
        return osName
    else:
        return None

def overrider(winObj):
    osName = osIdentifier()
    if osName in ['Linux', 'Darwin']:
        return
    else:
        winObj.overrideredirect(True)


def zoomer(winObj):
    """
    OSごとの処理の違いを吸収して画面をフルスクリーン化する
    """
    osName = osIdentifier()
    if osName in ['Linux', 'Darwin']:
        winObj.attributes('-fullscreen', True)
    elif osName == 'Windows':
        winObj.state('zoomed')
        overrider(winObj=winObj)
        return


root = tk.Tk()
root.title('勤怠管理システム')

zoomer(root)

app = Application(master=root)
app.mainloop()
from time import sleep
import sys, platform, threading
import tkinter as tk
import tkinter.font as tkFont
import datetime
from pytz import timezone
# private modules
import gsUpdate
import felicaidm as fe
import azure_sql as azsql

class Application(tk.Frame):
    def __init__(self, master=None):
        super().__init__(master=master)
        self.master = master
        self.pack()
        self.create_widgets()
        
    def create_widgets(self):
        self.fontStyle = tkFont.Font(family="System", size=70)
        self.fontStyle2 = tkFont.Font(family="System", size=55)
        self.textLabel = tk.Label(text="カードをタッチしてください。", font=self.fontStyle)
        self.textLabel.pack(side="top", expand=1)
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
            displayText = "登録されていないカードです。\n別のカードを試してください。"
            self.openMessageDialog(displayText=displayText, buttonText="閉じる")
        else:
            name = authInfo["name"]
            adminOrNot = authInfo["admin"]
            displayText = f"{name}さん。\n{['出退勤','動作'][adminOrNot==1]}を選んでください。"
            self.openSelectDialog(displayText=displayText, name=name, authInfo=authInfo)
        

    def openDialog(self):
        self.dialog = tk.Toplevel(self)
        self.dialog.title("勤怠管理dialog")
        zoomer(self.dialog)
        self.dialog.grab_set()

    def openMessageDialog(self, displayText, buttonText):
        self.openDialog()
        self.textLabel = tk.Label(self.dialog, text=displayText, font=self.fontStyle2)
        self.textLabel.pack(expand=1, fill="both", padx="30", pady="10")
        self.closeButton = tk.Button(self.dialog, text=buttonText, command=self.destroyDialog, font=self.fontStyle)
        self.closeButton.pack(expand=1, fill="both", padx="30", pady="10")

        
    def openSelectDialog(self, displayText, name, authInfo):
        self.openMessageDialog(displayText=displayText, buttonText="キャンセル")
        self.AttendButton = tk.Button(self.dialog, text="出勤", command=lambda: self.shukkin(name, "出勤", authInfo=authInfo), font=self.fontStyle)
        self.AbsentButton = tk.Button(self.dialog, text="退勤", command=lambda: self.shukkin(name, "退勤", authInfo=authInfo), font=self.fontStyle)
        self.AttendButton.pack(expand=1, fill="both", padx="30", pady="10")
        self.AbsentButton.pack(expand=1, fill="both", padx="30", pady="10")
        if authInfo["admin"] == 1:
            self.finishButton = tk.Button(self.dialog, text="プログラム終了", command=sys.exit, font=self.fontStyle)
            self.finishButton.pack(expand=1, fill="both", padx="30", pady="10")

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
        thread2 = threading.Thread(target=gsUpdate.addShuttaikin(workerName=name,\
                attendance=select, dataNow=dataNow, datestr=datestr, timestr=timestr))
        thread2.start()
        # 完了メッセージの表示
        displayText = f"{name}さんの\n{select}を{datestr} {timestr}に登録しました。"
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
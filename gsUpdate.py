import gspread, random, json, datetime
from pytz import timezone
from oauth2client.service_account import ServiceAccountCredentials

scope = ['https://spreadsheets.google.com/feeds',
         'https://www.googleapis.com/auth/drive']

fileName = '勤怠管理テスト'
credentials = ServiceAccountCredentials.from_json_keyfile_name('My Project 97003-3496c907305d.json', scope)
gc = gspread.authorize(credentials)
wks = gc.open(fileName).sheet1


def searchSheet(searchTitle):
    """
    'title'の名前のシートが存在するか確認する
    
    Parameters
    ----------
    title : str

    Return
    ----------
    True  : シートがあるとき
    False : シートがないとき
    """
    sheetfile = gc.open(fileName)
    for i in sheetfile.worksheets(): # シートが既存かどうかの判定
        if i.title == searchTitle:
            return True
    return False

def createNewSheet(year, month):
    """スプレッドシートにシート「{year}_{month}」が存在するか調べ、無いときは追加する。
    
    Parameters
    ----------
    year : int
        追加するシートの年
    month : [type]
        追加するシートの月
    
    Returns
    -------
    newTitle : str
        追加または存在確認したシートのタイトル
    """
    year = int(year)
    month = int(month)
    sheetfile = gc.open(fileName)
    newTitle = f'{year}_{month:02d}'
    if searchSheet(searchTitle=newTitle) is True: # シートが既存かどうか確認する
        return newTitle
    # 存在しないとき作る
    sheetfile.add_worksheet(title=newTitle,rows=1000 , cols=5)
    sps = sheetfile.worksheet(newTitle)
    koumoku = ['日付', '氏名', '時刻', '出退勤', '備考']
    sps.append_row(values=koumoku)
    print(f'新規シート{newTitle}を作成しました。')
    return newTitle


def addShuttaikin(workerName, attendance, dataNow ,datestr, timestr):
    """スプレッドシートに出退勤を追記する
    Parameters
    ----------
    workerName : str
        出退勤者の名前
    attendance : str
        '出勤'または'退勤'
    dataNow : datetime
        現在時刻
    datestr : str
        dataNowの加工済みの日付データ。YYYY-MM-DD
    timestr : str
        dataNowの加工済み時刻データ。HH:MM
    """

    sheetTitle = createNewSheet(year=dataNow.year, month=dataNow.month)
    sheet2Add = gc.open(fileName).worksheet(sheetTitle)
    sheet2Add.append_row(values=[datestr, workerName, timestr, attendance])
    return
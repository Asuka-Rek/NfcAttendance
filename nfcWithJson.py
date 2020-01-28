import json, nfc, sys
import felicaidm as fe
import gsUpdate

def importJson():
    try:
        with open('authInfo.json') as f:
            authInfo = json.load(f)
    except FileNotFoundError: # ファイルがないとき
        print('json file is not exsist.\nCreate new...')
        authInfo = {}
    except json.decoder.JSONDecodeError: # ファイルが空の時
        print('json file is empty')
        authInfo = {}
    except:
        import traceback
        traceback.print_exc()
        sys.exit()
    return authInfo


def outputJson(authInfo):
    with open('authInfo.json', 'w') as f:
        json.dump(authInfo, f, indent=4)


def addNfc(newCardHolder):
    authInfo = importJson()

    if newCardHolder in authInfo.values():
        print('その名前は登録済みです。別の名前で登録してください。')
        return
    
    newCardSddRes = fe.inputCard()
    if newCardSddRes in authInfo:
        print('そのカードは既に登録されています。別のカードを試してください。')
        return
    if newCardSddRes == None:
        print('対応していないカードです。別のカードを試してください。')
        return
    authInfo[newCardSddRes] = newCardHolder
    
    outputJson(authInfo=authInfo)
    print('登録が完了しました。')


def shuttaikin():
    authInfo = importJson()
    print('出勤なら[1],退勤なら[2]を入力してください。')
    inputNum = input()
    if inputNum == '1' or inputNum == '2':
        attendance = ['出勤', '退勤'][inputNum == '2']
        cardID = fe.inputCard()
        if cardID == None:
            print('対応していないカードです。')
            return
        if not cardID in authInfo:
            print('登録されていないカードです。別のカードを試してください。')
            return
        
        # ログ出力
        #Gスプレッドシート出力
        gsUpdate.addShuttaikin(authInfo[cardID], attendance)
        print('登録が完了しました。')
    else:
        print('値エラー。予期せぬ値です。')
        return


shuttaikin()
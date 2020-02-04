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


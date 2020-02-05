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
    """
    新しいカードと持ち主を登録するときに使う関数。
    登録済みの名前もしくはカード、または非対応種カードのときは追加しない。
    
    Parameters
    ----------
    newCardHolder : str
        カードの所有者として登録する名前
    authInfo : dict
        カード登録情報
        {keys : values} = {'カードのidm()' : {カード所有者名}

    Return
    ----------
    常にbool値と変数messageを返す。
    bool値について
        True  : カード情報の登録に成功したとき
        False : カード情報が何らかの事情で登録できないとき
    message : str
        GUI画面に表示するためのメッセージを返す。
        カード登録成功ならその旨、失敗ならその詳細。
    """

    # 現在のカード登録情報を読み込み
    authInfo = importJson()
    if newCardHolder in authInfo.values():
        message = 'その名前は登録済みです。別の名前で登録してください。'
        return False, message
    
    newCard_idm = fe.inputCard()
    if newCard_idm in authInfo:
        message = 'そのカードは既に登録されています。別のカードを試してください。'
        return False, message
    if newCard_idm == None:
        message = '対応していないカードです。別のカードを試してください。'
        return False, message

    authInfo[newCard_idm] = newCardHolder
    outputJson(authInfo=authInfo)
    message = '登録が完了しました。'
    return True, message


import binascii
import nfc

class MyCardReader(object):

    def on_connect(self, tag):
        print("touched")
        #print(">>>>> ",end='')
        #print(tag)
        #print('tag.identifier = ' + str(tag.identifier))
        #print('tag.target = ' + str(tag.target))
        try:
            self.idm = binascii.hexlify(tag.target.sensf_res).decode('UTF-8')
        except:
            print("対応していないカードです")
            self.idm = None
        else:
            print('読み取り完了。カードを離してください。')
        return True

    def read_id(self):
        clf = nfc.ContactlessFrontend('usb')
        try:
            clf.connect(rdwr={'on-connect': self.on_connect})
        finally:
            clf.close()


def mugenCardRead(): # カード情報無限に読み取りたいとき（テスト用）
    
    cr = MyCardReader()
    while True:
        """
        inputL = input()
        if inputL == 'f':
            print(li)
            break
        else:
            pass
        """
        print("-----------------------------------------")
        print("タッチしてください:")
        cr.read_id()
        print("離されました")
        


def inputCard():
    cr = MyCardReader()
    print("カードをタッチしてください。")
    cr.read_id()
    return cr.idｍ

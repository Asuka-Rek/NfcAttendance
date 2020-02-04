import binascii
import nfc

class MyCardReader(object):

    def on_connect(self, tag):
        try:
            self.idm = binascii.hexlify(tag.target.sensf_res).decode('UTF-8')
        except:
            self.idm = None
        else:
            print('読み取り完了。カードを離してください。')
        return True

    def read_id(self):
        clf = nfc.ContactlessFrontend('usb')

        self.idm = None
        # clf.connectのterminate用
        # これがないとカードのタッチ後、離すまで次の処理が始まらない。
        forKill = lambda: self.idm is not None 

        try:
            clf.connect(rdwr={'on-connect': self.on_connect}, terminate=forKill)
        finally:
            clf.close()


def inputCard():
    cr = MyCardReader()
    cr.read_id()
    return cr.idｍ

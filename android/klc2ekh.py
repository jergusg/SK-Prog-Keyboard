#! python3
#
# converts windows klc layout format to android External Keyboard Helper layout format
# use: python klc2ekh.py sk-prog.klc
# generates: ekh_backup.dat
#
import sys

def conv(word):
    if word == '-1':
        return '0x0000'
    else:
        return '0x' + word[:4]

if __name__ == "__main__":
    klcFile = open(sys.argv[1], encoding='utf-16-le', mode='r')
    ekhFile = open("ekh_backup.dat", 'w', newline='\n')

    tr = {'-1': '0x0000'}

    rel = False
    for line in klcFile:
        if rel:
            code = line.split('//')[0]
            l = code.split()
            if len(l) == 0:
                continue
            else:
                try:
                    sc = int(l[0],16)
                except:
                    break
            if len(l) < 8:
                continue
            s = ""
            s += str(sc)
            s += " 1 0x0000 0x0000 "

            things = list(map(conv, l[6:8]))
            if things[0] == things[1] == '0x0000':
                continue
            s += ' '.join(things)
            ekhFile.write(s+'\n')
        if line.startswith('LAYOUT'):
            rel = True

    ekhFile.write('58 2 58\n') # CapsLock to AltGr
    klcFile.close()
    ekhFile.close()

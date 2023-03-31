import pyautogui
from PIL import Image
import pytesseract
import argparse
from cv2 import cv2
import os

class Screenie:
    def __init__(self,name,setregion,path):
        self.name = name
        self.setregion = setregion
        self.path = path 

    def scshot(self): # screenshot function. 
        identifiers = [0,0]
        image = pyautogui.screenshot(region=self.setregion)
        name_new = "{}.png".format(self.name)
        path_new = self.path + name_new
        image.save(path_new)
        identifiers[0] = image
        identifiers[1] = path_new
        self.path = path_new
        self.name = name_new
        return identifiers

    def imagetext(self): 
        imagepath = self.path    
        ap = argparse.ArgumentParser()
        ap.add_argument("-p", "--preprocess", type=str, default="thresh",
            help="type of preprocessing to be done")
        args = vars(ap.parse_args())

        image = cv2.imread(imagepath)
        gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

        if args["preprocess"] == "thresh":
            gray = cv2.threshold(gray, 0, 255,
                cv2.THRESH_BINARY | cv2.THRESH_OTSU)[1]

        elif args["preprocess"] == "blur":
            gray = cv2.medianBlur(gray, 3)

        filename = "{}.png".format(os.getpid())
        cv2.imwrite(filename, gray)
        # load image as PIL->OCR it-->Delete the temp file. 
        text = pytesseract.image_to_string(Image.open(filename))
        os.remove(filename)
        return text

class TextCheck:
    def __init__(self,text,bankl,banku,countl,countu,unknown):
        self.text = text
        self.bankl = bankl
        self.banku = banku
        self.countl = countl
        self.countu = countu
        self.unknown = unknown
        self.transfer = []

    def words(self):
        wordlist = self.text.replace("\n"," ")
        wordlist = wordlist.split(" ")
        pop = []
        for i in range(len(wordlist)):
            if len(wordlist[i]) == 1:
                if not wordlist[i] in self.bankl and not wordlist[i] in self.banku:
                    pop.append(i)
            elif len(wordlist[i]) == 0:
                pop.append(i)
        wordlist_edit = wordlist
        j = 0
        k = len(pop)
        for i in range(k):
            index = (k - 1) - j
            wordlist.pop(pop[index])
            j = j + 1
        return(wordlist_edit,wordlist)

    def counting(self):
        run_countl = self.countl
        run_countu = self.countu
        low = filter(str.islower,self.text)
        up = filter(str.isupper,self.text)


        for char in low:
            if char in self.bankl:
                index = self.bankl.index(char)
                run_countl[index] = 1 + run_countl[index]
            elif not char in self.bankl and not char == "," and not char == "." and not char == " " and not char == "\n":
                self.unknown.append(char)
            else:
                pass
        for char in up:
            if char in self.banku:
                index = self.banku.index(char)
                run_countu[index] = 1 + run_countu[index]
            elif not char in self.banku and not char == "," and not char == "." and not char == " " and not char == "\n":
                self.unknown.append(char)
            else:
                pass
        lenl = sum(run_countl)
        lenu = sum(run_countu)
        out = [run_countl, run_countu, lenl, lenu]
        return out

    def __iter__(self):
        return iter(self.counting())


class Math: #this is all character tracking. 
    def __init__(self, count_1l, count_2l, count_1u, count_2u,prevoutcome):
        self, count_1l, count_2l, count_1u, count_2u,prevoutcome, 
        self.count_1l = count_1l
        self.count_2l = count_2l
        self.count_1u = count_1u
        self.count_2u = count_2u
        self.prevoutcome = prevoutcome
    
    def char_spec_change(self):
        y, Y = 0,0
        z, Z = 0,0
        n, N = 0,0
        zn, Zn = 0,0
        outcome = 0

        sl1 = sum(self.count_1l)
        su1 = sum(self.count_1u)
        sl2 = sum(self.count_2l)
        su2 = sum(self.count_2u)

        for i in self.count_1l:
            if i == self.count_2l[n]:
                n = n + 1
            elif i > self.count_2l[n]:
                y = y + 1
                n = n + 1
            elif i < self.count_2l[n]:
                zn = zn + (self.count_2l[n]-i)
                z = z + 1
                n = n + 1
        for j in self.count_1u:
            if j == self.count_2u[N]:
                N = N + 1
            elif j > self.count_2u[N]:
                Y = Y + 1
                N = N + 1
            elif j < self.count_2u[N]:
                Zn = Zn + (self.count_2u[N]-j)
                Z = Z + 1
                N = N + 1

            #y: from 1->2 the instances decreased
            #z: from 1->2 the instances increased
        if sl2 and su2 == 0:
            outcome = 3
            cause = '0 char in string'
        elif not outcome == 3:
            if Y > 0 or y > 3:                   #loss (uppercase)
                if sl2 == 0:
                    outcome = 3                             #repeat
                    cause = ['prevented loss threshold mislabing', (y, Y), (z, Z), (n, N), (zn, Zn)]
                else:
                    outcome = 0                             #new
                    cause = ['first loss threshold', (y, Y), (z, Z), (n, N), (zn, Zn)]
            else:
                if zn > 0 or Zn > 0:                    #gain
                    if y > 3 or Y > 0:                      #gain -> loss
                        outcome = 0                          #new
                        cause = ['gain --> loss', (y, Y), (z, Z), (n, N), (zn, Zn)]
                    elif y < 4 and Y == 0:              #gain -> no loss
                        if self.prevoutcome == 3:           #gain after outcome 3
                            outcome = 0                     #new
                            cause = ['gained after an o:3 skip', (y, Y), (z, Z), (n, N), (zn, Zn)]
                        elif not self.prevoutcome == 3:
                            outcome = 1                     #same
                            cause = ['gain --> no loss', (y, Y), (z, Z), (n, N), (zn, Zn)]
                        outcome = 0                         #new
                    else:
                        outcome = 4
                        cause = ['error inside 1', (y, Y), (z, Z), (n, N), (zn, Zn)]
                elif zn == 0 or Zn == 0:                #no gain
                    if y > 3 or Y > 0:                  #no gain -> loss
                        outcome = 0                         #new
                        cause = ['no gain --> loss', (y, Y), (z, Z), (n, N), (zn, Zn)]
                    elif y < 4 and Y == 0:              #no gain --> no loss
                        if self.prevoutcome == 3:       #no gain no loss after outcome 3
                            outcome = 3                     #repeat
                            cause = ['no gain/no loss after outcome 3',  (y, Y), (z, Z), (n, N), (zn, Zn)]
                        elif not self.prevoutcome == 3:                        
                            outcome = 1                     #same
                            cause = ['no gain --> no loss', (y, Y), (z, Z), (n, N), (zn, Zn)]
                    else:
                        outcome = 4
                        cause = ["error inside 2", (y, Y), (z, Z), (n, N), (zn, Zn)]
                elif zn < 0 or Zn < 0:
                    outcome = 3
                    cause = 'prevented negative zn error'

                elif y == 0 and z == 0 and Y == 0 and Z == 0:
                    outcome = 1
                    cause = '0,0,0,0'
                else:
                    outcome = 4
                    cause = ["error outside", (y, Y), (z, Z), (n, N), (zn, Zn)]
        h = (sl1,su1)
        g = (sl2, su2)
        return outcome, cause, h,g,self.prevoutcome

    def __iter__(self):
        return iter(self.char_spec_change())

class NotMath: 
    def __init__(self, word1, word2):
        self.word1 = word1
        self.word2 = word2

    def wordchange(self):
        nonmatch = [x for x in self.word1 + self.word2 if x not in self.word1 or x not in self.word2]
        if not nonmatch:
            return 'same'
        else:
            if self.word1 and self.word2 == []:
                return 'double empty lists?'
            elif self.word1 == []:
                return 'empty list 1' 
            elif self.word2 == []:
                return 'empty list 2'
            else:
                return nonmatch

class Saves:
    def __init__(self,path_current,folder_new,title):
        self.path_current = path_current
        self.folder_new = folder_new
        self.title = title

    def moving(self):
        path_new = self.folder_new + self.title
        os.rename(self.path_current, path_new)
        return path_new
    def __str__(self):
        return str('saved new image at:\n%s' % self.moving())

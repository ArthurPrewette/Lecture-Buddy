lectname = "hist_L19"  #!!!                 Update me every time.
lectlen = '39:23'                           #Exact lecture length if asynchronous. 
speed =2.8                                  #This is your playback speed multiplier. 
path = 'THIS FOLDER CONTAINING THIS FILE'   #update me on first use. 
save_folder = 'UPDATE ME ONCE'              #update me on first use.
pytesseract.pytesseract.tesseract_cmd = r'C:\\Program Files (x86)\\Tesseract-OCR\\tesseract.exe'#confirm/update me once.
##########################################################################################################################################################
# When you press run, put your cursor on the top left corner of the lecture area until prompted to move it to the bottom right corner of the lecture area. 
##########################################################################################################################################################
import time
import pytesseract
import os
import SS_ORC as SS_OCR
import errno
from ctypes import windll, Structure, c_long, byref


ss_path1 = path+"\\"+"check1.png"
ss_path2 = path+"\\"+"check2.png"
save_folder = save_folder +'\\'+ lectname
try:
    os.makedirs(save_folder)
except OSError as e:
    if e.errno != errno.EEXIST:
        raise

# This is to prevent overwriting a file when you forget to change the lecture name. 
# If you forget, it will append to the historical file.
filename = 'Screenshots\\%s\\transcript.txt' % lectname
file_exists = os.path.isfile(filename)
if file_exists:
    pass 
else:
    new = open(filename, "w")
    new.close()

# This section is to determing lecture area. 
# I'm not going to write the code to automatically determine the size/location of a videoplayer. 
class POINT(Structure):
    _fields_ = [("x", c_long), ("y", c_long)]
def MousePosition():
    pt = POINT()
    windll.user32.GetCursorPos(byref(pt))
    return (pt.x,pt.y)
print("place your mouse on the top left corner of lecture window.")
for i in range(5):
    count = 5-i
    time.sleep(1)
    print('Pos1:\t%is' % count)      
pos1 = MousePosition()
print("place your mouse on the bottom right corner of lecture window.")
for i in range(5):
    count = 5-i
    time.sleep(1)
    print('Pos2:\t%is'% count)       
pos2 = MousePosition()
print("Done.\n Move your mouse away from lecture window.") 

print(pos1)
print(pos2) #printed so you can check with windowspy and restart before lecture starts if you messed it up. 
regx2 = pos2[0]-pos1[0]
regy2 = pos2[1]-pos1[1]
ss_region = (pos1[0],pos1[1],regx2,regy2)


#These are the characters we want to track. (we dont want to track noise from inaccurate OCR processing)
charlistl = ['a','b','c','d','e','f','g','h','i','j','k','l','m','n','o','p','q','r','s','t','u','v','w','x','y','z']
charlistu = ['A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'I', 'J', 'K', 'L', 'M', 'N', 'O', 'P', 'Q', 'R', 'S', 'T', 'U', 'V', 'W', 'X', 'Y', 'Z']
charcount1l = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
charcount1u = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
charcount2l = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
charcount2u = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
unknowna = []
unknownb = []
outcome = 0
outloop = 0

#Below is an example pattern of how the image referencing progresses throughout the script.
#Where for [xn-yn], x is the reference image and y the comparison image. 
#a1-b1, b1-a2, a2-b2, b2-a3, a3-b3
run = 1 
namea = 'check_a'
nameb = 'check_b'
start_t = time.time()
t = 0

#Total Runtime.
def update(s_time):
    curr = time.time()
    t = curr - s_time
    return t

#accounting for speed multiplier effects. 
def timer(lectlen,speed):
    lectlen = lectlen.split(':')
    second = int(lectlen[1]) / speed
    minute = int(lectlen[0]) * 60 / speed
    length = minute + second
    return length

#Removing illegal characters in file title. 
def titler(text):
    tit = text.replace('\n','+')
    tit = tit.replace(" ","_")
    tit = tit.replace(">","}")
    tit = tit.replace("<","{")
    tit = tit.replace(":","_")
    tit = tit.replace("|","I")
    tit = tit.replace("?","_")
    tit = tit.replace("*","_")
    tit = tit.replace('"',"_")
    tit = tit.replace('\\',"_")
    tit = tit.replace('/',"_")
    tit = tit.replace('\x0c',"_")
    tit = tit.replace('\x0b',"_")
    tit = tit.replace('\f',"_")
    tit = tit.replace('\v',"_")
    tit = tit[:10]
    return tit

length = timer(lectlen, speed)
print(length)
while t < length:
    t = update(start_t)

    if run == 1:
#Reference Screenshot
#This is what is saved if it is determined that the comparison screenshot contains less data
        print('run 1: %i' % run)
        load_a = SS_OCR.Screenie('check_a',ss_region,path)  
        check_a = load_a.scshot()
        path_a = check_a[1]
        image_a = check_a[0]
        text1 = load_a.imagetext()
        tc_load_a = SS_OCR.TextCheck(text1,charlistl,charlistu,charcount1l,charcount1u,unknownb)
        tc_a = tc_load_a.counting()
        tc_a = list(tc_a)
        count_a_l, count_a_u, len_a_l, len_a_u = tc_a
        #print(text1)
        words = tc_load_a.words()
        words_edit_a = words[0]
        words_orig_a = words[1]
        time.sleep(5)
        
#Comparison Screenshot
#This turns into reference screenshot if it is determined that no data was lost, i.e. both that:
#1: Text was not swapped with other text (slide change) or erased (partial or full slide change). 
#2: No handwriting was erased.
        load_b = SS_OCR.Screenie('check_b',ss_region,path)
        check_b = load_b.scshot()
        path_b = check_b[1]
        image_b = check_b[0]

        text2 = load_b.imagetext()    

        tc_load_b = SS_OCR.TextCheck(text2,charlistl,charlistu,charcount2l,charcount2u,unknownb)
        tc_b = tc_load_b.counting()
        tc_b = list(tc_b)
        count_b_l, count_b_u, len_b_l, len_b_u = tc_b

        words = tc_load_b.words()
        words_edit_b = words[0]
        words_orig_b = words[1]
        
        #print(text1)
        #print(text2)
        #print(tc_a)
        #print(tc_b)
    elif not run == 1 and not outloop == 3:
        
        print('run: %i' % run)
        path_a = check_b[1]
        image_a = check_b[0]
        text1 = text2
        count_a_l, count_a_u, len_a_l, len_a_u = count_b_l,count_b_u,len_b_l,len_b_u
        time.sleep(3)
        words_edit_a = words_edit_b
        words_orig_a = words_orig_b

        unknownb = []
        charcount2l = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
        charcount2l = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]

        name = "check%i" % run 
        load_b = SS_OCR.Screenie(name,ss_region,path)
        check_b = load_b.scshot()
        path_b = check_b[1]
        image_b = check_b[0]

        text2 = load_b.imagetext()     

        tc_load_b = SS_OCR.TextCheck(text2,charlistl,charlistu,charcount2l,charcount2u,unknownb)
        tc_b = tc_load_b.counting()
        tc_b = list(tc_b)
        count_b_l, count_b_u, len_b_l, len_b_u = tc_b

        words = tc_load_b.words()
        words_edit_b = words[0]
        words_orig_b = words[1]
        #print(tc_b)
        #print(tc_a)

    elif outloop == 3:
        time.sleep(5)
        print('run: %i' % run)

        unknownb = []
        charcount2l = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
        charcount2l = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]

        name = "check%i" % run 
        load_b = SS_OCR.Screenie(name,ss_region,path)
        check_b = load_b.scshot()
        path_b = check_b[1]
        image_b = check_b[0]

        text2 = load_b.imagetext()     

        
        tc_load_b = SS_OCR.TextCheck(text2,charlistl,charlistu,charcount2l,charcount2u,unknownb)
        tc_b = tc_load_b.counting()
        tc_b = list(tc_b)
        count_b_l, count_b_u, len_b_l, len_b_u = tc_b
        #print(tc_b)
        #print(tc_a)


    z = SS_OCR.Math(count_a_l,count_b_l,count_a_u,count_b_u, outloop)
    outcome = list(z.char_spec_change())
    outloop = outcome[0]
    #print(outcome)
    if outcome[0] == 1:
        print('Same Image')
        #print('*1*: %s\t%s\t%s' % (outcome[1],outcome[2],outcome[3]))
        cause = outcome[1]
        st1 = outcome[2]
        st2 = outcome[3]
        prev = outcome[4]
        print('*1*: %ls\t %s\n\t%s\t%s' % (cause, prev, st1, st2))

        os.remove(path_a)
    elif outcome[0] == 0:
        
        print('New image')
        #print('*0*: %s\t%s\t%s' % (outcome[1],outcome[2],outcome[3]))
        cause = outcome[1]
        st1 = outcome[2]
        st2 = outcome[3]
        prev = outcome[4]
        print('*0*: %ls\t %s\n\t%s\t%s' % (cause, prev, st1, st2))

        text1 = str(text1)
        with open(filename, 'a', encoding='utf-8') as f:
            f.write('\n\n~~~~~~~~~~~~~~~~~~\n\n')
            f.write(text1)
            f.close()

        tit = titler(text1)

        tim = update(start_t)

        t = update(start_t)
        t_s = str(t)
        t_s = t_s[:5]
        t_s = t_s.replace('.',"(")
        t = float(t)
        
        title = ('\\%s_%s.png' % (tit,t_s))
        #print('\n')
        #print(title)
        #print('\n')
        saved = SS_OCR.Saves(path_a,save_folder,title)
        move = saved.moving()
        #print(move)
    elif outcome[0] == 3:
        print('Skip')        
        #print('*3*: %s\t%s\t%s' % (outcome[1],outcome[2],outcome[3]))
        cause = outcome[1]
        st1 = outcome[2]
        st2 = outcome[3]
        prev = outcome[4]
        print('*3*: %ls\t %s\n\t%s\t%s' % (cause, prev, st1, st2))
        os.remove(path_b)
    elif outcome[0] == 666:
        print('logic is a construct')
        cause = outcome[1]
        st1 = outcome[2]
        st2 = outcome[3]
        prev = outcome[4]
        print('*666*: %ls\t %s\n\t%s\t%s' % (cause, prev, st1, st2))
    else:
        print('Something went HORRIBLY wrong.')
    run = run + 1

    print("%ls\n%ls" % (words_edit_a, words_orig_a))
    print("\n%ls\n%ls" % (words_edit_b, words_orig_b))
if outloop == 3:
    print('END OF LOOP: saving last confirmed image')
    print('*0*: %s\n%s' % (outcome[1],outcome[2]))

    text1 = str(text1)
    with open(filename, 'a', encoding='utf-8') as f:
        f.write('\n\n~~~~~~~~~~~~~~~~~~\n\n')
        f.write(text1)
        f.close()

        tit = titler(text1)

    tit = tit[:13]
    tim = update(start_t)

    t = update(start_t)
    t_s = str(t)
    t_s = t_s[:5]
    t_s = t_s.replace('.',"(")
    #print(t)
    t = float(t)
    
    title = ('\\%s_%s.png' % (tit,t_s))
    saved = SS_OCR.Saves(path_a,save_folder,title)
    move = saved.moving()
else:
    print('timer end')

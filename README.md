# Automatic-Note-Taker
# Generates OCR-enabled PDF's, Audio transcriptions, and Text Records of online lectures. 

~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
# Contextual information:
#  I wrote this program in March of 2021 during Covid when lectures were all online and professors wouldn't record lectures or post lecture material.
#  This program is best if used in addition to taking notes during lectures so you can go back for reference.
#      It is entirely possible to start this program with your phone using a RAT tool while you are off doing god knows what, but that is not the intended/reccomended 
#      use of this program. In reality, why skip a 1h lecture just to have to spend 2-3h to figure out what you missed.
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
#Code information:
# The file "main.py" is the control center for this, there are important variables that must be updated on first-time, and every use of the program. 
# The variables that need to be changed exist in the very top of "main.py".
# There are some QOL modifications that can be made to this program to increase the ease of adding additional functionality; But, at the time of posting, I no longer 
# have any use for this program so I have no intention of writing these modifications. 
    
#Required Libraries: 
# time, os, errno, ctypes, pyautogui, PIL/Pillow, argparse, cv2
# pytesseract, python wrapper for Google Tesseract: https://github.com/madmaze/pytesseract

#   This was developed using OCR as it's basis for a few main reasons:
#    1: Production of Searchable PDF's is a major W, obviously.
#    2: I used Image-identification for previous attempts as it is my go-to method for most automated processes. However, no matter how complex the processing and                verification is, image-idenfication techniques performed poorly in the context of automated note-taking as some pen colors are not possible to drown out and              false-positives occur very often. 
#       - OCR shines in this context as character outputs allow for mathematical analysis to be used concurrently with character-tracking as a verification process. 

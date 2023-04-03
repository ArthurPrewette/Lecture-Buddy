Lecture-Buddy
=====================
Generates lecture transcriptions and OCR-enabled PDF's of online lectures. 

Detects Full/Partial Slide Changes and Erased handwriting inside videoplayer regions. 

Dependencies
============
Supports python 3.(7-10)

The following libraries, which have their own dependencies, must be installed:

* Pillow
* errno
* pyautogui 
* argparse 
* cv2 
* shutil 
* pytesseract

Before Using 
============
The top of the file "main.py" contains variables that must be updated before use.

Detailed instructions are present as comments in the "main.py" file. 

How It Works
============

Takes screenshots at specified intervals, deleting the 3rd oldest image and keeping the two most recent images at each iteration:

A copy of each new image is processed for accurate optical character recognition. When applied, OCR output is read into python. 

Characters are sorted into lists containing all known written and digital character types, with common "noisy" OCR character types being sorted into their own categories. 

Mathematical analyis is used to determine whether slide changes occurred, internet connection is suffering (larger thresholds are used), handwriting is erased, or OCR incorrectly classified data types (character is reclassified as a "noisy" type for both images and analysis is repeated).

The original image preceeding a slide change or erased handwriting is processed, less intensely than before, and optical character recognition is applied to it before creating/appending-to the searchable pdf file created for that lecture. 

All files and lists created by the script are deleted/cleared after use, leaving only the pdf and transcription file after completion.

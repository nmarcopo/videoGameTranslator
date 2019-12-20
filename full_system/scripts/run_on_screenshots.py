from PIL import Image
import subprocess
import xml.etree.ElementTree as ET
from collections import namedtuple
from itertools import combinations
import glob
import os
from time import sleep
# import googletrans
from translation_client import Translator

# GLOBALS
tesseract_binary = '/usr/local/bin/tesseract' # Edit this to your local tessearct path
tessdata_dir = '../pxj_output/'
tessconfig_dir = '../tesseract_config/'
tessconfig_file = 'jpnconf'
translation_dir = '../translation_model/'
screenshot_dir = '/Users/chanhee/Desktop/'  # Edit this to your local screenshot saving path


def getOCRString(ocr_info):
    tree = ET.fromstring(ocr_info)
    existWord = False
    string = ''
    for line in tree.findall(".//*[@class='ocrx_word']/.."):
        for word in line:
            for char in word:
                if char.text.strip() != '':
                    existWord = True
                    # make sure algorithm is confident
                    if float(char.attrib['title'].split('; ')[1].split()[1]) > 90:
                        string += char.text
        if existWord == True:
            string += '\n' # print newline between lines that aren't blank
            existWord = False
    return string

def get_ocr_info(img_path, trainedTess=True):
    invert = False
    if float(subprocess.check_output(['convert', img_path, '-colorspace', 'Gray', '-format', '"%[fx:image.mean]"', 'info:']).decode('utf-8').replace('"', '')) < .3:
        invert = True

    with open('stderr.txt', 'w') as f:
        if not trainedTess:
            # quick and dirty way to test the original, untrained tesseract
            if invert:
                # convert image to light background dark text if it isn't already
                invertedImage = subprocess.Popen(('convert', img_path, '-channel', 'RGB', '-negate', '-'), stdout=subprocess.PIPE)
                out = subprocess.check_output([tesseract_binary, '-', 'stdout', '-l', 'jpn', tessconfig_dir + tessconfig_file, '--psm', '11'], stdin=invertedImage.stdout, stderr=f).decode('utf-8')
                invertedImage.wait()
                return out
            else:
                return subprocess.check_output([tesseract_binary, img_path, 'stdout', '-l', 'jpn', tessconfig_dir + tessconfig_file, '--psm', '11'], stderr=f).decode('utf-8')
        else:
            if invert:
                # convert image to light background dark text if it isn't already
                invertedImage = subprocess.Popen(('convert', img_path, '-channel', 'RGB', '-negate', '-'), stdout=subprocess.PIPE)
                out = subprocess.check_output([tesseract_binary, '--tessdata-dir', tessdata_dir, '-', 'stdout', '-l', 'pxj', tessconfig_dir + tessconfig_file, '--psm', '11'], stdin=invertedImage.stdout, stderr=f).decode('utf-8')
                invertedImage.wait()
                return out
            else:
                return subprocess.check_output([tesseract_binary, '--tessdata-dir', tessdata_dir, img_path, 'stdout', '-l', 'pxj', tessconfig_dir + tessconfig_file, '--psm', '11'], stderr=f).decode('utf-8')

if __name__ == "__main__":
    # img_path = 'images/image2.png'
    # ocr_info = get_ocr_info(img_path)
    # print(getOCRString(ocr_info))

    print("Waiting for a new screenshot...")
    # screenshot_dir = '/home/nmarcopo/snap/retroarch/318/.config/retroarch/screenshots/'
    list_of_files = glob.glob(screenshot_dir + '*')
    print(list_of_files)
    try:
        existing_file = max(list_of_files, key=os.path.getctime)
    except ValueError:
        existing_file = None
    # translator = googletrans.Translator()
    translator = Translator(translation_dir)
    while True:
        list_of_files = glob.glob(screenshot_dir + '*')
        try:
            latest_file = max(list_of_files, key=os.path.getctime)
        except ValueError:
            latest_file = None
        if latest_file != existing_file:
            print('NEW SCREENSHOT:')
            try:
                ocr_info = get_ocr_info(latest_file)
            except subprocess.CalledProcessError:
                print('Failed to run Tesseract, trying again...')
                continue
            ocr_string = getOCRString(ocr_info)
            if ocr_string:
                print('source:\n',ocr_string)
                print('translation:\n',translator.translate([''.join(ocr_string.split())]))
            else:
                print('No text found in screenshot...')
            existing_file = latest_file
        sleep(2)

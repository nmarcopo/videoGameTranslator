from PIL import Image
import subprocess
import xml.etree.ElementTree as ET
from collections import namedtuple
from itertools import combinations
import glob
import os
from time import sleep
from cer import cer
from translation_client import Translator
from tqdm import tqdm

# GLOBALS
tesseract_binary = '/home/nmarcopo/local/bin/tesseract'
tessdata_dir = '../pxj_output/'
tessconfig_dir = '../tesseract_config/'
tessconfig_file = 'jpnconf'
translation_dir = '../translation_model/'
output_dir = 'output/'
confidence = 0

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
                    if float(char.attrib['title'].split('; ')[1].split()[1]) > confidence:
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
    testDir = '../test/'
    allGameTrainedResults = {}
    allGameUntrainedResults = {}
    translator = Translator(translation_dir)
    os.makedirs(os.path.dirname(output_dir), exist_ok=True)

    for game in ['ffiv', 'ffvi']:
        print("getting metrics for the game", game, "...")
        for trained in [True, False]:
            parallels = {}
            trainedText = 'trained' if trained else 'untrained'
            print("running", game, "on", trainedText, "ocr")
            for root, dirs, files in os.walk(testDir + game + '/'):
                for img_path in tqdm(files):
                    ocr_info = get_ocr_info(root + img_path, trained)
                    ocr_string = getOCRString(ocr_info).replace('\n', '')
                    # format string by removing all whitespace and file type
                    img_path = img_path.replace('.png', '') + '\n'

                    # translate the OCR'd characters
                    try:
                        [ocr_string] = translator.translate([ocr_string])
                    except Exception as e:
                        print("EXCEPTION HAPPENED ON", img_path, ", text is", ocr_string)
                        raise(e)
                    ocr_string += '\n'

                    parallels[img_path] = ocr_string
                    if trained:
                        allGameTrainedResults[img_path] = ocr_string
                    else:
                        allGameUntrainedResults[img_path] = ocr_string

                break # don't go more than one directory deep
            print("creating", game + '_' + trainedText + '.ref', 'and', game + '_' + trainedText + '.hyp...')
            jpnFile = open(output_dir + game + '_' + trainedText + '.ref', 'w')
            engFile = open(output_dir + game + '_' + trainedText + '.hyp', 'w')
            jpnFile.writelines(parallels.keys())
            engFile.writelines(parallels.values())
            jpnFile.close()
            engFile.close()
        print()

    print("creating final_trained.ref and final_trained.hyp...")
    jpnFile = open(output_dir + 'final_trained.ref', 'w')
    engFile = open(output_dir + 'final_trained.hyp', 'w')
    jpnFile.writelines(allGameTrainedResults.keys())
    engFile.writelines(allGameTrainedResults.values())
    jpnFile.close()
    engFile.close()

    print("creating final_untrained.ref and final_untrained.hyp...")
    jpnFile = open(output_dir + 'final_untrained.ref', 'w')
    engFile = open(output_dir + 'final_untrained.hyp', 'w')
    jpnFile.writelines(allGameUntrainedResults.keys())
    engFile.writelines(allGameUntrainedResults.values())
    jpnFile.close()
    engFile.close()
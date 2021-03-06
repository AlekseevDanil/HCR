import cv2
from path import Path
import os
from DetectingWordsNN.src.infer import get_img_files, extract_words_sorted, line_box
from HTR.src.main import recognition
import matplotlib.pyplot as plt
import time
import numpy as np


def resizing(img):
    try:
        height, width = img.shape
        if height < 340 or width < 1200:
            return img
        elif height > width:
            f = 340 / height
            img = cv2.resize(img, None, fx=f, fy=f, interpolation=cv2.INTER_LINEAR)
            return img
        elif width >= height:
            f = 1200 / width
            img = cv2.resize(img, None, fx=f, fy=f, interpolation=cv2.INTER_LINEAR)
            return img
    except:
        return img


def extract_text(input_path, output_path):
    if os.path.isdir(Path(input_path)):
        if len(get_img_files(Path(input_path))) == 0:
            print('Изображений для обработки не обнаружено. проверьте путь')
        else:
            print(f"Найдено {len(get_img_files(Path(input_path)))} изображений для обработки.")
    else:
        print(f'директория {input_path} не существует')
    # проверяем папку ку складываем
    if os.path.isdir(output_path):
        print(f'директория {output_path} уже существует')
    else:
        os.makedirs(output_path)
        print(f'директория {output_path} создана')
    # получили список файлов
    files = get_img_files(input_path)
    for_recognition = extract_words_sorted(input_path)
    index = 0
    for DetectItem in for_recognition:
        text = ''
        img = cv2.imread(DetectItem.img_name, cv2.IMREAD_GRAYSCALE)
        for line in DetectItem.lines:
            for word in line:
                delta_y = 0.20 * (word.ymax - word.ymin)
                delta_x = 0.10 * (word.xmax - word.xmin)
                crop_word = img[int(word.ymin - delta_y):int(word.ymax + delta_y),
                            int(word.xmin - delta_x):int(word.xmax + delta_x)]
                crop_word = resizing(crop_word)
                # crop_word = cv2.threshold(crop_word, 0, 255, cv2.THRESH_BINARY + cv2.THRESH_OTSU)[1]
                try:
                    Smoothing = cv2.GaussianBlur(crop_word, (3, 3), 0)
                    crop_word = cv2.addWeighted(crop_word, 0.5, Smoothing, 0, 0)
                except:
                    print('Cant Smoothing')

                crop_word = cv2.threshold(crop_word, 0, 255, cv2.THRESH_BINARY + cv2.THRESH_OTSU)[1]
                #
                index += 1
                # plt.imshow(crop_word, cmap='gray')
                # plt.show()
                # следующая строка нужна для бинаризации на случай если используется
                # модель обученная на бинаризированных картинках

                try:
                    characters = recognition(crop_word)
                    print(characters)
                    text += ' ' + characters[0]
                except:
                    print('Cant recognize')
            text += ' \n '
        f_name = output_path + '/' + DetectItem.img_name.split('/')[-1] + '.txt'
        with open(f_name, 'a') as my_file:
            my_file.write(text)
            my_file.close()


extract_text('/Users/danilmovika/Desktop/projects/HCR/HTR/data/archive',
             '/Users/danilmovika/Desktop/projects/HCR/HTR/data/output')

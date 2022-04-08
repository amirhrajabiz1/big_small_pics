import os
import numpy as np
import cv2
from tqdm import tqdm
import imutils
import sys
import math
from pympler import asizeof
import shutil
import subprocess
import random


def make_image_memory_less(cache_address = r'.', primary_image_address=r'./prime.jpg', directroy_address_of_images=r'images', output=r'./primeout.jpg', split_size=100, chance_to_repeat=0.5):
    
    def most_common_used_color(img):
        b, g, r = cv2.split(img)
        r_total = round(np.average(np.average(r, axis=1), axis=0), 2)
        g_total = round(np.average(np.average(g, axis=1), axis=0), 2)
        b_total = round(np.average(np.average(b, axis=1), axis=0), 2)
        return(r_total, g_total, b_total)
    
    common_colors_resized_imgs = []
    size_of_divided_for_all = split_size
    imgs = []
    resized_images = []
    cache_address += '\cache'
    subprocess.check_call(["attrib", "+h", cache_address])
    if(os.path.exists(cache_address)):
        shutil.rmtree(cache_address)
    os.mkdir(cache_address)
    counter = 0
    print("Read small images and resize them and save them.")
    for count, filename in enumerate(tqdm(os.listdir(fr'{directroy_address_of_images}'))):
        imgs.append(cv2.imread(fr'{directroy_address_of_images}/{filename}'))
        if count % 300 == 0 and count != 0:
            for i in imgs:
                try:
                    resized_images.append(cv2.resize(i, (size_of_divided_for_all, size_of_divided_for_all)))
                except:
                    pass
            for i in resized_images:
                common_colors_resized_imgs.append(most_common_used_color(i))
                cv2.imwrite(fr"{cache_address}/{counter}.png", i)
                counter += 1
            resized_images = []
            imgs = []
    
    original_primaryImage = cv2.imread(primary_image_address)
    original_height = original_primaryImage.shape[0]
    original_width = original_primaryImage.shape[1]
    height = (original_height//size_of_divided_for_all)*size_of_divided_for_all
    width  = (original_width//size_of_divided_for_all) *size_of_divided_for_all
    primaryImage = cv2.resize(original_primaryImage, (width, height))
    del original_primaryImage
      
    divided_image = []
    for j in range(0, primaryImage.shape[0], size_of_divided_for_all):
        for i in range(0, primaryImage.shape[1], size_of_divided_for_all):
            divided_image.append(primaryImage[j:j+size_of_divided_for_all, i:i+size_of_divided_for_all])
     
    common_colors_divided_primary_image = []
    for i in divided_image:
        common_colors_divided_primary_image.append(most_common_used_color(i))

        
    def erdis5(v1, v2):
        dist = [(a - b) ** 2 for a, b in zip(v1, v2)]
        dist = math.sqrt(sum(dist))
        return dist
    primary_image_with_resized_indexes = []
    index_set = set()
    print("Calculate the best pairs.")
    for i in tqdm(common_colors_divided_primary_image):
        dst = 0
        smallest_dst = 100000
        for index, j in enumerate(common_colors_resized_imgs):
            dst = erdis5(i, j)
            if dst < 5 and index not in index_set:
                best_index_per_dst = index
                break
            if dst < smallest_dst and index not in index_set:
                smallest_dst = dst
                best_index_per_dst = index

        if best_index_per_dst in index_set:
            index_set = set()
        if random.random() > chance_to_repeat:
            index_set.add(best_index_per_dst)
        primary_image_with_resized_indexes.append(best_index_per_dst)
        
    k = 0
    height = primaryImage.shape[0]
    width  = primaryImage.shape[1]
    print("write the output image row by row")
    for j in tqdm(range(0, height, size_of_divided_for_all)):
        for i in range(0, width, size_of_divided_for_all):
            primaryImage[j:j+size_of_divided_for_all, i:i+size_of_divided_for_all] = cv2.imread(fr"{cache_address}/{primary_image_with_resized_indexes[k]}.png")
            k += 1
    cv2.imwrite(output, primaryImage)
    
    shutil.rmtree(cache_address)

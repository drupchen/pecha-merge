import numpy as np
import os
from PIL import Image as Img
from itertools import zip_longest

img_mode = ''


# Open Images and load it using Image Module
def open_img_triplet(img1, img2, img3):
    images_list = [img1, img2, img3]
    opened = [Img.open(i) for i in images_list]
    return opened


# resize the other images to match smaller image
def resize_n_merge_triplet(imgs, min_shape):
    # Merge the images using vstack and save the Vertially merged images
    new_imgs = []
    img_merge = np.vstack((np.asarray(i.resize(min_shape, Img.ANTIALIAS)) for i in imgs))
    img_merge = Img.fromarray(img_merge)
    return img_merge


def triplet_to_pdf(merged_triplet, out):
    merged_triplet.save(out + '.pdf', 'PDF')


def create_triplets(l, fillvalue):
    def fill(current):
        total = []
        triplet = []
        for c in current:
            if len(triplet) < 3:
                triplet.append(c)
            elif len(triplet) == 3:
                total.append(triplet)
                triplet = []
                triplet.append(c)
        if triplet != []:
            if len(triplet) == 1:
                triplet.append(fillvalue)
                triplet.append(fillvalue)
            elif len(triplet) == 2:
                triplet.append(fillvalue)
            total.append(triplet)
        return total

    current_odd = l[1:][::2]
    current_even = l[0:][::2]
    odd_triplets = fill(current_odd)
    even_triplets = fill(current_even)
    return odd_triplets, even_triplets


def find_min_img_size(files):
    imgs = [Img.open(i) for i in files]
    min_img_shape = sorted([(np.sum(i.size), i.size) for i in imgs])[0][1]
    return min_img_shape


def create_blank_page(min_shape):
    blank_min_img = Img.new('L', min_shape, 'white')
    blank_min_img.save('cache/blank.jpg')


def merge_pecha_jpg_folder(folder_name, jpg_name):
    files = sorted(['{}/{}'.format(folder_name, a) for a in os.listdir(folder_name)])

    min_shape = find_min_img_size(files)

    create_blank_page(min_shape)

    odd_triplets, even_triplets = create_triplets(files, fillvalue='cache/blank.jpg')

    for num, triplet in enumerate(odd_triplets):
        opened = open_img_triplet(triplet[0], triplet[1], triplet[2])
        merged = resize_n_merge_triplet(opened, min_shape)
        triplet_to_pdf(merged, '{}/{}_{}'.format('cache/jpg_output/odd', jpg_name, num + 1))

    for num, triplet in enumerate(even_triplets):
        opened = open_img_triplet(triplet[2], triplet[1], triplet[0])
        merged = resize_n_merge_triplet(opened, min_shape)
        merged = merged.transpose(Img.FLIP_LEFT_RIGHT)
        merged = merged.transpose(Img.FLIP_TOP_BOTTOM)
        triplet_to_pdf(merged, '{}/{}_{}'.format('cache/jpg_output/even', jpg_name, num+1))


if __name__ == '__main__':
    in_folder = './cache/jpg_input'
    out_name = 'jpg_merged'
    merge_pecha_jpg_folder(in_folder, out_name)

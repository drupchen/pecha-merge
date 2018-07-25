from merge_folios_into_pages import merge_pecha_jpg_folder
from wand.image import Image as Wimg
from PyPDF2 import PdfFileMerger, PdfFileReader
import os


def extract_jpgs(f_name):
    with open("input_pdf/"+f_name, 'rb') as f:
        all_pages = Wimg(blob=f.read(), resolution=1000)

    for num, img in enumerate(all_pages.sequence):
        with Wimg(img) as i:
            i.format = 'jpg'
            i.compression_quality = 99
            i.save(filename='{}/{}'.format('cache/jpg_input', f_name.split('.')[0] + '_' + str(num+1).zfill(3) + '.jpg'))


def generate_print_ready_pdf(side, name):
    file_names = sorted(["cache/jpg_output/{}/{}".format(side, a) for a in os.listdir('cache/jpg_output/'+side)])
    merger = PdfFileMerger()
    for f in file_names:
        merger.append(PdfFileReader(open(f, 'rb')))
    merger.write('output_pdfs/{}_{}.pdf'.format(name, side))


def empty_tmp_files():
    try:
        os.remove('cache/blank.jpg')
    except:
        pass

    folders = ['cache/jpg_input/', 'cache/jpg_output/even', 'cache/jpg_output/odd']
    for folder in folders:
        full = ['{}/{}'.format(folder, a) for a in os.listdir(folder)]
        for f in full:
            try:
                os.remove(f)
            except:
                pass


def process_pdf(pdf):
    filename = pdf.split('.')[0]
    empty_tmp_files()
    extract_jpgs(pdf)
    merge_pecha_jpg_folder('./cache/jpg_input', 'jpg_merged')
    generate_print_ready_pdf('even', filename)
    generate_print_ready_pdf('odd', filename)
    empty_tmp_files()


if __name__ == '__main__':
    for f in os.listdir('./input_pdf'):
        print(f)
        process_pdf(f)



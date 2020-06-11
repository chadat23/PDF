# https://imagemagick.org/script/download.php#windows
# https://www.ghostscript.com/download/gsdnld.html

# http://gauravvichare.com/how-to-password-protect-pdf-file-using-python/

import argparse
import datetime
import os
from pathlib import Path
import uuid

import PyPDF2


def set_password(input_path, master_password, user_password):
    t0 = datetime.datetime.now()
    input_path = Path(input_path)
    temp_png = Path(f'{uuid.uuid4()}.png')
    temp_pdf = Path(f'{uuid.uuid4()}.pdf')
    temp_pdf2 = Path(f'{uuid.uuid4()}.pdf')

    # larger density numbers increase png file size for better resolution but makes things slower
    # pdf_to_png = f'magick -density 100 {input_path} -strip -background white {temp_png}'  # 0.7 sec
    # pdf_to_png = f'magick -density 200 {input_path} -strip -background white {temp_png}'  # 1.3 sec looks different but clear
    pdf_to_png = f'magick -density 400 {input_path} -strip -background white {temp_png}'  # 2.9 sec
    # pdf_to_png = f'magick -density 800 {input_path} -strip -background white {temp_png}'  # 10 sec
    # pdf_to_png = f'magick -density 1000 {input_path} -strip -background white {temp_png}'  # 15 sec

    # larger scale makes better resolution but larger file sizes and slower
    # png_to_pdf = f'magick {temp_png} -scale 1000 -units pixelsperinch -density 72 -page letter {temp_pdf}'  # 10 sec
    # png_to_pdf = f'magick {temp_png} -scale 1200 -units pixelsperinch -density 72 -page letter {temp_pdf}'  # 11 sec
    png_to_pdf = f'magick {temp_png} -scale 1500 -units pixelsperinch -density 72 -page letter {temp_pdf}'  # 9 sec Looks different but pretty cleaar
    # png_to_pdf = f'magick {temp_png} -scale 2000 -units pixelsperinch -density 72 -page letter {temp_pdf}'  # 17 sec
    # png_to_pdf = f'magick {temp_png} -scale 4000 -units pixelsperinch -density 72 -page letter {temp_pdf}'  # 45 sec
    # png_to_pdf = f'magick {temp_png} {temp_pdf}'

    os.system(pdf_to_png)
    t1 = datetime.datetime.now()
    print(t1 - t0)
    os.system(png_to_pdf)
    t2 = datetime.datetime.now()
    print(t2 - t0, t2 - t1)
    os.system(png_to_pdf)
    # os.remove(temp_png)

    # output = PyPDF2.PdfFileWriter()
    #
    # with open(temp_pdf, 'rb') as pdf:
    #     input_stream = PyPDF2.PdfFileReader(pdf)
    #     for p in range(input_stream.getNumPages()):
    #         output.addPage(input_stream.getPage(p))
    #
    #     with open(temp_pdf2, 'wb') as output_stream:
    #         # output.encrypt(user_password, master_password, use_128bit=True)
    #         output.write(output_stream)
    t3 = datetime.datetime.now()
    print(t3 - t0, t3 - t1, t3 - t2)

    # os.remove(temp_pdf)
    # os.remove(input_path)
    # os.rename(temp_pdf2, input_path)


def user_inputs():
    parser = argparse.ArgumentParser()
    parser.add_argument('-i', '--input_pdf', required=True,
                        help='Input pdf file')
    parser.add_argument('-m', '--master_password', required=False, default=None,
                        help='Master/Owner Password, Allows opening, editing, copying, etc.')
    parser.add_argument('-p', '--user_password', required=True,
                        help='User Password, Allows opening with restrictions.')
    return parser.parse_args()


def main():
    args = user_inputs()
    set_password(args.input_pdf, args.master_password, args.user_password)


if __name__ == '__main__':
    main()

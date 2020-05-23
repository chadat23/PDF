# https://imagemagick.org/script/download.php#windows
# https://www.ghostscript.com/download/gsdnld.html

import argparse
import os
from pathlib import Path
import uuid

import PyPDF2


def set_password(input_path, master_password, user_password):
    input_path = Path(input_path)
    temp_png = Path(f'{uuid.uuid4()}.png')
    temp_pdf = Path(f'{uuid.uuid4()}.pdf')
    temp_pdf2 = Path(f'{uuid.uuid4()}.pdf')

    pdf_to_png = f'magick {input_path} {temp_png}'
    png_to_pdf = f'magick {temp_png} {temp_pdf}'

    os.system(pdf_to_png)
    os.system(png_to_pdf)
    os.remove(temp_png)

    output = PyPDF2.PdfFileWriter()

    with open(temp_pdf, 'rb') as pdf:
        input_stream = PyPDF2.PdfFileReader(pdf)
        for p in range(input_stream.getNumPages()):
            output.addPage(input_stream.getPage(p))

        with open(temp_pdf2, 'wb') as output_stream:
            output.encrypt(user_password, master_password, use_128bit=True)
            output.write(output_stream)

    os.remove(temp_pdf)
    os.remove(input_path)
    os.rename(temp_pdf2, input_path)


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

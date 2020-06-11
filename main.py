# https://imagemagick.org/script/download.php#windows
# https://www.ghostscript.com/download/gsdnld.html

# http://gauravvichare.com/how-to-password-protect-pdf-file-using-python/

import argparse
import os
from pathlib import Path
import uuid


def set_password(input_path):
    input_path = Path(input_path)
    temp_png = Path(f'{uuid.uuid4()}.png')
    temp_pdf = Path(f'{uuid.uuid4()}.pdf')

    # larger density numbers increase png file size for better resolution but makes things slower
    pdf_to_png = f'magick -density 400 {input_path} -strip -background white {temp_png}'

    # larger scale makes better resolution but larger file sizes and slower
    png_to_pdf = f'magick {temp_png} -scale 1500 -units pixelsperinch -density 72 -page letter {temp_pdf}'

    os.system(pdf_to_png)
    os.system(png_to_pdf)

    os.remove(temp_png)
    os.remove(input_path)
    os.rename(temp_pdf, input_path)


def user_inputs():
    parser = argparse.ArgumentParser()
    parser.add_argument('-i', '--input_pdf', required=True, help='Input pdf file')
    return parser.parse_args()


def main():
    args = user_inputs()
    set_password(args.input_pdf)


if __name__ == '__main__':
    main()

#!/usr/bin/python3.11
from PIL import Image, UnidentifiedImageError
from sys import argv
from pathlib import Path

USAGE = """> images2pdf
Usage:
    images2pdf.py <image1> <image2> ...
    images2pdf.py -o "output_file_name" <image1> <image2> ...

When -o flag is not used, output file will be named after the first image file.
If output_file_name does not end with ".pdf", the extensions will be added automatically.
"""


def main():

    # Remove script path
    argv.pop(0) 

    # Check if the USAGE message should be displayed
    if "--help" in argv\
        or len(argv) == 0:

        print(USAGE)
        return
    

    filename: str = None

    # Check if filename is given
    if "-o" in argv:
        dashOIndex = argv.index("-o")
        filename = argv.pop(dashOIndex + 1)
        argv.pop(dashOIndex)

    # Converting file paths to Path objects
    imagePaths = [Path(strPath) for strPath in argv]

    # If filename was not given
    if filename is None:
        filename = imagePaths[0].stem

    # Append .pdf if necessary
    filename = filename if filename.endswith(".pdf") else filename + ".pdf"

    # Check if file will not be overwritten
    outputPath = Path(filename)

    if outputPath.exists():
        print(f'[ERROR]: File "{outputPath.absolute()}" already exists')
        return


    # Opening images and handling potential errors
    images: list[Image.Image] = []

    for path in imagePaths:
        
        try:
            images.append(Image.open(path).convert("RGB"))

        except FileNotFoundError:
            print(f'[x] Skipping "{path.absolute()}": File does not exist')

        except UnidentifiedImageError:
            print(f'[x] Skipping "{path.absolute()}": File is not an image')


    # Quick check if there is anything left
    if len(images) == 0:
        print(f'[WARN]: No images left to convert. Exiting the program.')
        return


    # Saving PDF file and handling a potential error
    try:
        images[0].save(filename, save_all=True, append_images=images[1:], format="pdf")
        print(f'[✓]: File "{outputPath.absolute()}" was successfuly created')

    except OSError:
        print(f'[ERROR]: File "{outputPath.absolute()}" could not be written')



if __name__ == "__main__":
    main()
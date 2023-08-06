**File-Editor**:

A python package to convert a file to different file format.

*Example* :

png to pdf

pdf to png

jpeg to pdf

pdf to jpeg

tiff to pdf

pdf to tiff

Note : if input is 2 page pdf document and output specified as .png format. it will split the pdf document into two png files.

**Required Packages**:

Python-pil and pdf2image

>>> sudo apt-get install python-pil
>>> pip install pdf2image 

**Usage**:

Following commands will convert the input file to output file format.

*First argument* : Input file path

*Second argument* : Output file format


>>> from file_editor.editor import image
>>> image("example.png",".pdf")

**Supported File Fromats**

*BMP, PDF, EPS, GIF, ICNS, ICO, IM, JPEG, JPEG 2000, MSP, PCX, PNG, PPM, SGI, SPIDER, TIFF, WebP and XBM*



# ExifViewer

Simple PyQt5 project for Human Computer Interaction course. It consists in a `.jpeg` files viewer with **exif** informations. 
This program allows you to:

- **Visualize** all images in the same `.py` directory and switch previous/next image in the list.
- **Get** all _exif_ informations in a table.
- **Rotate** images.
- **Open** image _geolocalization_ with Google Maps API Url.

<div>
<p align="center">
<img src="/documents/screen.png" width=auto height=480px></img>
</p>
<div/>

### How to install
To build and run the files, you will need the following libraries:

- pyqt 5.12.1
- pillow 7.0.0

Put images in the directory and run `exifReader.py`.

This code was tested with Ubuntu 19.10 and Mac OS 10.15.3. It presents some lags with Mac operative systems due to PyQt 
framework, probably.

### Report
A copy of the report (italian) can be found 
<a href="https://github.com/FrancescoGradi/ExifViewer/documents/report.pdf" download="report.pdf">here</a>.
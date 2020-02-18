import PIL.Image
import PIL.ExifTags

from fractions import Fraction


def getExif(imagePath):
    try:
        img = PIL.Image.open(imagePath)
        exif = {
            PIL.ExifTags.TAGS[k]: v
            for k, v in img._getexif().items()
            if k in PIL.ExifTags.TAGS
        }
        return cleanExif(exif)
    except:
        return None


def convertToDegree(value):
    d, m, s = value

    d = float(d[0]) / float(d[1])
    m = float(m[0]) / float(m[1])
    s = float(s[0]) / float(s[1])

    return d + (m / 60.0) + (s / 3600.0)


def cleanExif(exif):
    try:
        exif['ShutterSpeedValue'] = str(Fraction(exif['ShutterSpeedValue'][0], exif['ShutterSpeedValue'][1]))
        exif['ApertureValue'] = float(exif['ApertureValue'][0]) / float(exif['ApertureValue'][1])
        exif['BrightnessValue'] = float(exif['BrightnessValue'][0]) / float(exif['BrightnessValue'][1])
        exif['ExposureBiasValue'] = float(exif['ExposureBiasValue'][0]) / float(exif['ExposureBiasValue'][1])
        exif['FocalLength'] = float(exif['FocalLength'][0]) / float(exif['FocalLength'][1])
        exif['ExposureTime'] = str(Fraction(exif['ExposureTime'][0], exif['ExposureTime'][1]))
        exif['XResolution'] = float(exif['XResolution'][0]) / float(exif['XResolution'][1])
        exif['FNumber'] = float(exif['FNumber'][0]) / float(exif['FNumber'][1])
        exif['YResolution'] = float(exif['YResolution'][0]) / float(exif['YResolution'][1])
        return exif
    except:
        return exif
import PIL.Image
import PIL.ExifTags


def getExif(imagePath):
    try:
        img = PIL.Image.open(imagePath)
        exif = {
            PIL.ExifTags.TAGS[k]: v
            for k, v in img._getexif().items()
            if k in PIL.ExifTags.TAGS
        }
        return exif
    except:
        return None


def convertToDegree(value):
    d, m, s = value

    d = float(d[0]) / float(d[1])
    m = float(m[0]) / float(m[1])
    s = float(s[0]) / float(s[1])

    return d + (m / 60.0) + (s / 3600.0)

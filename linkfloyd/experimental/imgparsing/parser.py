from urllib2 import urlopen, HTTPError
from PIL.ImageFile import Parser as ImageParser
from pickle import load
from multiprocessing import Pool

MIN_LINK_THUMB_WIDTH = 350
MIN_LINK_THUMB_HEIGHT = 200

def size_filter(image_url):
    try:
        file = urlopen(image_url)
    except HTTPError:
        return None
    data = file.read(1024)
    file.close()
    parser = ImageParser()
    parser.feed(data)
    if parser.image:
        if parser.image.size[0] > MIN_LINK_THUMB_WIDTH and \
            parser.image.size[1] > MIN_LINK_THUMB_HEIGHT:
            print image_url, parser.image.size
            return image_url

def get_size_filtered_images(image_urls, min_width=0, min_height=0):
    pool = Pool(processes=10)
    urls = pool.map(size_filter, image_urls)
    return filter(lambda x: x != None, urls)

if __name__ == "__main__":
    urls = load(open("urls.pkl", "rb"))
    print get_size_filtered_images(urls)

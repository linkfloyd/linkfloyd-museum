from urllib2 import urlopen, URLError
from BeautifulSoup import BeautifulSoup, BeautifulStoneSoup
from sorl.thumbnail import get_thumbnail
from django.contrib.sites.models import Site
from urlparse import urljoin

def get_info(url):
    """Fetches the contents of url and extracts (and utf-8 encodes)
       the contents of <title>"""

    resp_dict = {} # response dict

    if not url or not (url.startswith('http://') or url.startswith('https://')):
        return resp_dict

    try:
        opener = urlopen(url, None, timeout=15)
    except URLError:
        return resp_dict

    print opener.info().getheaders('content-type')

    if "text/html" in opener.info().getheaders('content-type')[0]:
        data = opener.read(8096)
        opener.close()
        bs = BeautifulSoup(data)

        if not bs:
            return {}

        og_title_bs = bs.find("meta", attrs={"property": "og:title"})

        if og_title_bs:
            resp_dict['title'] = og_title_bs['content']
        else:
            del(og_title_bs) # i like working sooo clean :)
            title_bs = bs.html.head.title
            if title_bs and title_bs.string:
                resp_dict['title'] = title_bs.string

        desc_bs = bs.find("meta", attrs={"name": "description"})

        if desc_bs and desc_bs.has_key('content'):
            resp_dict['description'] = desc_bs['content']

        img_bs = bs.find("meta", attrs={"property": "og:image"})

        if img_bs and img_bs.has_key('content'):
            resp_dict['image'] = img_bs['content']
        else:
            del(img_bs)
            img_src_bs = bs.find("link", attrs={"rel": "image_src"})
            if img_src_bs:
                resp_dict['image'] = img_src_bs['href']
            else:
                first_img_bs = bs.find("img")
                if first_img_bs:
                    resp_dict['image'] = first_img_bs['src']

    if "image" in opener.info().getheaders('content-type')[0]:
        resp_dict['image'] = url

    # cleanup title and description

    if resp_dict.has_key('title'):
        resp_dict['title'] = resp_dict['title'].strip()
        print resp_dict['title']
        try:
            resp_dict['title'] = BeautifulStoneSoup(resp_dict['title'],
                convertEntities=BeautifulStoneSoup.HTML_ENTITIES).contents[0]
        except IndexError:
            pass

    if resp_dict.has_key('description'):
        resp_dict['description'] == resp_dict['description'].strip()
        try:
            resp_dict['description'] = BeautifulStoneSoup(resp_dict['description'],
                convertEntities=BeautifulStoneSoup.HTML_ENTITIES).contents[0]
        except IndexError:
            pass

    # if thumbnail url is relative, make it absolute url.

    if resp_dict.has_key('image'):
        if  not resp_dict['image'].startswith("http") or \
            resp_dict['image'].startswith("ftp"):
            resp_dict['image'] = urljoin(url, resp_dict['image'])

    opener.close()
    return resp_dict

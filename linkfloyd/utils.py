from BeautifulSoup import BeautifulSoup, BeautifulStoneSoup
from django.http import HttpResponse
from django.utils.html_parser import HTMLParser
from urllib2 import build_opener, URLError, urlopen
from urlparse import urljoin
from django.db.models import aggregates
from django.db.models.sql import aggregates as sql_aggregates
from django.utils import simplejson

client = build_opener()
client.addheaders = [('User-agent', 'Mozilla/5.0')]
urlopen = client.open

def get_info(url):
    """Fetches the contents of url and extracts (and utf-8 encodes)
       the contents of title, description and embed data
    """

    resp_dict = {} # response dict

    if not url or not (url.startswith('http://') or url.startswith('https://')):
        return resp_dict

    try:
        opener = urlopen(url, None, timeout=15)
    except URLError:
        return resp_dict

    resp_dict = {"url": url}


    if "text/html" in opener.info().getheaders('content-type')[0]:
        data = opener.read()
        opener.close()

        bs = BeautifulSoup(data)

        if not bs:
            return {}

        og_title_bs = bs.find("meta", attrs={"property": "og:title"})

        if og_title_bs:
            resp_dict['title'] = og_title_bs['content']
        else:
            del(og_title_bs) # i like working sooo clean :)
            try:
                title_bs = bs.html.head.title
            except AttributeError:
                title_bs = None
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
                resp_dict['player'] = "<img src='%s' class='embed' />" \
                    % img_src_bs['href']
            else:
                first_img_bs = bs.find("img")
                if first_img_bs:
                    resp_dict['image'] = first_img_bs['src']

        # cleanup title and description

        if resp_dict.has_key('title'):
            resp_dict['title'] = resp_dict['title'].strip()

            try:
                resp_dict['title'] = BeautifulStoneSoup(
                    resp_dict['title'],
                    convertEntities=BeautifulStoneSoup.HTML_ENTITIES
                ).contents[0]
            except IndexError:
                pass

            if resp_dict.has_key('description'):
                resp_dict['description'] == resp_dict['description'].strip()
            try:
                resp_dict['description'] = BeautifulStoneSoup(
                    resp_dict['description'],
                    convertEntities=BeautifulStoneSoup.HTML_ENTITIES
                ).contents[0]
            except KeyError:
                pass
            except IndexError:
                pass

        # if thumbnail url is relative, make it absolute url.

        if resp_dict.has_key('image'):
            if  not resp_dict['image'].startswith("http") or \
                resp_dict['image'].startswith("ftp"):
                resp_dict['image'] = urljoin(url, resp_dict['image'])

        # if there is a embed link:
        embed_bs = bs.find('link', attrs={'type': 'application/json+oembed'})

        if embed_bs:
            print embed_bs['href']
            try:
                embed_link_opener = urlopen(embed_bs['href'], None, timeout=15)
            except URLError:
                embed_link_opener = None
                print "i could'nt open embed link", embed_bs['href']
                exit

            if embed_link_opener:
                try:
                    embed_data = simplejson.loads(embed_link_opener.read())
                except ValueError:
                    embed_data = None

                if embed_data:
                    try:
                        resp_dict['player'] = embed_data['html']
                    except IndexError:
                        exit
        else: # there is no oembed

            og_video_bs = bs.find("meta", attrs={"property": "og:video"})

            if og_video_bs:
                resp_dict['player'] = "<embed src='%s'/>" % og_video_bs['content']


    if "image" in opener.info().getheaders('content-type')[0]:
        resp_dict['image'] = url
        resp_dict['player'] = "<img src='%s' class='embed' />" % url

    opener.close()
    return resp_dict

# -----------------------------------------------------------------------------

class SumWithDefault(aggregates.Aggregate):
    name = 'SumWithDefault'

class SQLSumWithDefault(sql_aggregates.Sum):
    sql_template = 'COALESCE(%(function)s(%(field)s), %(default)s)'

setattr(sql_aggregates, 'SumWithDefault', SQLSumWithDefault)

# -----------------------------------------------------------------------------

def reduced_markdown(text, *args, **kwargs):
    """
    Monkey patch for standart markdown library, removes heading tag support
    and adds prettyprint to pre tags. (for google code prettyfy
    """

    from markdown import blockprocessors as bp
    from markdown import util
    from markdown import markdown

    def run_with_prettify(self, parent, blocks):
        """ Run method is overriden to render pre tag with prettify class """

        sibling = self.lastChild(parent)
        block = blocks.pop(0)
        theRest = ''
        if sibling and sibling.tag == "pre" and len(sibling) \
            and sibling[0].tag == "code":
            # The previous block was a code block. As blank lines do not start
            # new code blocks, append this block to the previous, adding back
            # linebreaks removed from the split into a list.
            code = sibling[0]
            block, theRest = self.detab(block)
            code.text = util.AtomicString('%s\n%s\n' % \
                (code.text, block.rstrip()))
        else:
            # This is a new codeblock. Create the elements and insert text.
            pre = util.etree.SubElement(parent, 'pre')
            pre.attrib['class'] = 'prettyprint'
            code = util.etree.SubElement(pre, 'code')
            block, theRest = self.detab(block)
            code.text = util.AtomicString('%s\n' % block.rstrip())
        if theRest:
            # This block contained unindented line(s) after the first indented
            # line. Insert these lines as the first block of the master blocks
            # list for future processing.
            blocks.insert(0, theRest)

    def build_block_parser(md_instance, **kwargs):
        """ Build reduced block parser used by Markdown. """
        parser = bp.BlockParser(md_instance)
        parser.blockprocessors['empty'] = bp.EmptyBlockProcessor(parser)
        parser.blockprocessors['code'] = bp.CodeBlockProcessor(parser)
        parser.blockprocessors['olist'] = bp.OListProcessor(parser)
        parser.blockprocessors['ulist'] = bp.UListProcessor(parser)
        parser.blockprocessors['quote'] = bp.BlockQuoteProcessor(parser)
        parser.blockprocessors['paragraph'] = bp.ParagraphProcessor(parser)
        return parser

    bp.build_block_parser = build_block_parser
    bp.CodeBlockProcessor.run = run_with_prettify

    return markdown(text, *args, **kwargs)


def get_object_or_403(klass, *args, **kwargs):
    from django.shortcuts import _get_queryset
    queryset = _get_queryset(klass)
    try:
        return queryset.get(*args, **kwargs)
    except queryset.model.DoesNotExist:
        return HttpResponse(status=403)

class HTMLImageParser(HTMLParser):
    """
    It's wrapper class for parsing images from HTML content. I found this idea
    from a stackoverflow page:

    http://stackoverflow.com/questions/4295139/
    """
    image_urls = []

    def handle_starttag(self, tag, attrs):
        if tag == 'img':
            src = dict(attrs)['src']
            self.image_urls.append(src)


class CustomHTMLParser(object):
    """
    This class includes some tools for parsing images, header objects from url.
    """
    def __init__(self, url, min_size=None):
        self.url = url
        self.min_size = min_size

    def check_size(self, url):
        """
        Checks media size for url header info or buffer size.
        """
        if self.min_size:
            content = urlopen(url)
            content_length_header = content.info().getheaders('Content-Length')
            try:
                # first try to read content length
                content_length = int(content_length_header[0])
            except IndexError:
                # if content length doesn't exist, download for min_size and
                # check the size.
                content_length = len(content.read(self.min_size))

            # compare content length with expected size
            if content_length < self.min_size:
                return False

        return True

    def get_images(self):
        """
        Returns all image urls from url content.
        """
        content = urlopen(self.url)
        encoding = content.headers.getparam('charset')
        data = content.read().decode(encoding)

        p = HTMLImageParser()
        p.feed(data)
        image_urls = p.image_urls
        p.close()

        for image_url in image_urls:
            # fix image path
            image_url = urljoin(self.url, image_url).replace('/..', '/')

            # check minimal size if argument determined
            if not self.check_size(image_url):
                continue

            yield image_url

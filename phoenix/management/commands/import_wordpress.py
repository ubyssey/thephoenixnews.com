import re
import os
import urllib
import StringIO
import hashlib
from datetime import datetime
from multiprocessing import Pool
from multiprocessing.pool import ThreadPool
from sets import Set

from bs4 import BeautifulSoup

from django.core.management.base import BaseCommand
from django.conf import settings

from dispatch.models import Article, Image, Section, Person, Author, Tag

def process_caption(line, content):
    soup = BeautifulSoup(content, 'html.parser')

    def get_caption(soup):
        caption = soup.text.strip()
        return caption if caption else None

    def get_id():
        code = re.match(r'.*id="attachment_([0-9]*)"', line)
        if code:
            return int(code.group(1))
        return None

    return {
        'type': 'image',
        'data': {
            'image_id': get_id(),
            'caption': get_caption(soup),
        }
    }

def match_caption(line):
    code = re.match(r'\[([^\[\]|]*)\](.*)\[/[^|]*', line)

    if code:
        func = code.group(1).split(" ")
        content = code.group(2)
        if func[0] == 'caption':
            return process_caption(line, content)

def process_inline_image(line):
    caption = match_caption(line)

    if caption:
        return caption

    code = re.match(r'.*wp-image-([0-9]*)', line)

    if code:
        return {
            'type': 'image',
            'data': {
                'image_id': int(code.group(1)),
            }
        }

    return None

def process_shortcodes(line):
    inline_image = process_inline_image(line)

    if inline_image:
        return inline_image

    soup = BeautifulSoup(line, 'html.parser')

    return {
        'type': 'paragraph',
        'data': line.replace('<content:encoded>', '').replace('</content:encoded>', ''),
    }

def is_image(item):
    return item.find('post_type').text == 'attachment'

def is_article(item):
    return item.find('post_type') and item.find('post_type').text == 'post' and item.find('status').text == 'publish'

def parse_content(item):
    blocks = str(item.find('encoded').text.encode("utf-8")).split('\n')
    blocks = filter(lambda b: b != '', blocks)
    blocks = [process_shortcodes(b) for b in blocks]
    return blocks

def parse_image(item):
    return {
        'id': int(item.find('post_id').text),
        'title': item.title.text,
        'url': item.find('attachment_url').text
    }

def parse_article(item):
    return {
        # 'id': int(item.find('post_id').text),
        # 'title': item.title.text,
        'slug': item.find('post_name').text,
        'tags': Set([i.text for i in item.find_all(domain='sub_category')]).union(Set([i.text for i in item.find_all(domain='post_tag')])).difference(Set([i.text for i in item.find_all(domain='contributor')])),
        # 'section': item.find(domain='category').text,
        # 'featured_image': parse_featured_image(item),
        # 'published_at': datetime.strptime(item.find('post_date').text,'%Y-%m-%d %H:%M:%S'),
        # 'authors': [i.text for i in item.find_all(domain='contributor')],
        # 'tags': [i.text for i in item.find_all(domain='post_tag')],
        # 'item': item,
    }

def parse_featured_image(item):
    keys = item.find_all('meta_key')

    meta = None
    for key in keys:
        if key.text == '_thumbnail_id':
            meta = key.parent

    if meta:
        return int(meta.find('meta_value').text)
    else:
        return None

def save_image(item):

    filename = item['url'].replace('http://www.thephoenixnews.com/wp-content/uploads/', 'images/')
    filename, extension = os.path.splitext(filename)

    # Convert tif to tiff
    if extension == '.tif':
        extension = '.tiff'

    filename = filename + extension

    try:
        try:
            image = Image.objects.get(img=filename)
            # if not image.height:
            #     image.save()
            #     print 'Re-saving: %d - %s' % (item['id'], filename)
            #     return True
            return False
        except:
            print 'Saving: %d - %s' % (item['id'], filename)

            image = Image()
            image.id = item['id']
            image.title = item['title']
            image.img = filename

            path = os.path.join(settings.MEDIA_ROOT, filename)
            dirname = os.path.dirname(path)
            if not os.path.exists(dirname):
                os.makedirs(dirname)

            urllib.urlretrieve(item['url'], path)

            image.img = filename

            image.save()

            return True
    except:
        return True

def add_image_to_tsv(tsv_file, item):

    f = StringIO.StringIO(urllib.urlopen(item['url']).read())

    hash_md5 = hashlib.md5()
    for chunk in iter(lambda: f.read(4096), b""):
        hash_md5.update(chunk)

    tsv_str = "%s  %s  %s\n" % (item['url'], str(f.len), hash_md5.hexdigest())
    print item['url']

    tsv_file.write(tsv_str)

    f.close()

def save_article(item):

    section, created = Section.objects.get_or_create(name=item.get('section'), slug=item.get('section','').lower())
    try:
        article, created = Article.objects.get_or_create(head=True, slug=item.get('slug'), section=section)
    except:
        articles = Article.objects.filter(slug=item.get('slug'))
        if len(articles) > 1:
            for article in articles[1:]:
                article.delete()
            print 'Skipping %s - %s' % (item.get('slug'), item.get('published_at'))
        return

    if not created:
        print 'Skipping %s - %s' % (item.get('slug'), item.get('published_at'))
        return

    article.id = item.get('id')
    article.head = True
    article.is_published = True
    article.headline = item.get('title')
    article.published_at = item.get('published_at')

    article.content = parse_content(item.get('item'))

    article.parent = None
    article.save(revision=False)

    def get_author(name):
        person, created = Person.objects.get_or_create(full_name=name)
        return {
            'person': person.id,
            'type': 'author'
        }

    def get_tag(name):
        tag, created = Tag.objects.get_or_create(name=name)
        return tag.id

    authors = [get_author(name) for name in item.get('authors', [])]
    article.save_authors(authors, is_publishable=True)

    tags = [get_tag(name) for name in item.get('tags', [])]
    article.save_tags(tags)

    if item['featured_image']:
        try:
            Image.objects.get(id=item['featured_image'])

            featured_image = {
                'image_id': item['featured_image']
            }
            article.save_featured_image(featured_image)
            article.save(update_fields=['featured_image'], revision=False)
        except:
            print 'cannot save featured image %d' % item['featured_image']

    print 'Saved: %s ' % article.headline

def save_article2(item):

    article = Article.objects.get(head=True, is_published=True, slug=item.get('slug'))

    def get_tag(name):
        tag, created = Tag.objects.get_or_create(name=name)
        return tag.id

    tags = [get_tag(name) for name in item.get('tags', [])]

    article.save_tags(tags)

    article.save(revision=False)

    print 'Saved: %s - %s' % (article.headline, item['tags'])

def map_image(item):
    save_image(parse_image(item))

def map_article(item):
    save_article(parse_article(item))

class Command(BaseCommand):
    def handle(self, **options):
        # for image in Image.objects.all():
        #     if not image.height:
        #         try:
        #             image.save()
        #             print 'Saved %s' % image.img
        #         except IOError:
        #             image.delete()
        #         except Exception as e:
        #             print 'error: %s - %s' % (image.img, str(e))

        with open('./thephoenixnews.wordpress.2018-04-16.xml', 'U') as f:
            soup = BeautifulSoup(f.read(), 'xml')

            items = soup.find_all('item')
            #
            # images = filter(is_image, items)
            #
            # pool = ThreadPool(5)
            # results = pool.map(map_image, images)
            # pool.close()

            articles = reversed(filter(is_article, items))
            for item in articles:
                save_article2(parse_article(item))

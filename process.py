from pymongo import MongoClient
from bs4 import BeautifulSoup
from ftfy import fix_text
import unicodedata
from pprint import pprint
import re
import os

# SAFE REFUGE FOR WAYWARD VARIABLES #
MONGO_URI = 'localhost'
MONGO_DB = 'nuliterature'
client = MongoClient(MONGO_URI, 27017)
db = client[MONGO_DB]
collection = db['raw']


def remove_html_tags(text):
    import re
    clean = re.compile('<.*?>')
    return re.sub(clean, '', text)


jewishworldreview_patterns = [('var( )?_ndnq( )?=( )?_ndnq( )?\|\|( )?\[\];( )?_ndnq.push\(\["embed"\]\);', ' '),
                ('SIGN UP FOR OUR NEWSLETTER', ''),
                ('""', '"'),
                ('\.\.', '.'),
                ('\.(?=[A-Z])', '. '),
                ('  ', ' '),
                ('\."(?=[A-Z])', '." '),
                ('^ ', '')
                ]
def jewishworldreview_body(article):
    html = open(os.path.join(os.path.abspath("."), 'profiles', 'jewishworldreview', article['uri'].replace('./', '')),
                'r').read()
    # Scheme 1
    begin = html.find('<!-- BEGIN ARTICLE BODY -->')
    end = html.find('<!-- END ARTICLE BODY -->')

    # Scheme 2
    if begin == -1 or end == -1:
        begin = html.find('JewishWorldReview.com |')
        end = html.find(' Comment by clicking ')

    content = html[begin:end]

    # Sanitize (non-Unicode)
    for rep in ['\n','\r','\t']:
        content = content.replace(rep,'')

    return content


breitbart_patterns = [('var( )?_ndnq( )?=( )?_ndnq( )?\|\|( )?\[\];( )?_ndnq.push\(\["embed"\]\);', ' '),
                ('SIGN UP FOR OUR NEWSLETTER', ''),
                ('""', '"'),
                ('\.\.', '.'),
                ('\.(?=[A-Z])', '. '),
                ('  ', ' '),
                ('\."(?=[A-Z])', '." '),
                ('^ ', '')
                ]
def breitbart_body(article):
    html = open(os.path.join(os.path.abspath("."), 'profiles', 'breitbart', article['uri'].replace('./', '')), 'r')
    soup = BeautifulSoup(html, 'html.parser')

    # TODO: check all retrieved, not just [0]
    content = soup.select('.entry-content')[0].get_text()

    # Magic (UNICODE ONLY) sanitization
    content = unicodedata.normalize('NFKD', fix_text(content)).replace('\n', '').replace('\u2026', '. . .')

    # Remove weirdness
    for vp in breitbart_patterns:
        content = re.sub(vp[0], vp[1], content)

    return content


jws_pattern = re.compile('([a-zA-Z]{2,})([0-9a-z-_]+)(?:\.html)')
def run_jewishworldreview():
    print('Working on JewishWorldreview. . .')
    man = [m.replace('\n', '') for m in open(os.path.join(os.path.abspath('.'),'profiles','jewishworldreview','manifest'), 'r').readlines()]

    print('{} found'.format(len(man)))
    print('----------')

    goods = dict()
    bads = list()

    for m in man:
        try:
            article = {'source': 'jewishworldreview'}

            mx = re.search(jws_pattern, m).group()
            name = re.search(jws_pattern, mx).group(1).lower()
            article['uri'] = m
            article['name'] = name
            # number = re.search(pattern2,mx).group(2)
            if name not in goods.keys():
                goods[name] = [article]
            else:
                goods[name].append(article)
        except Exception as e:
            bads.append(m)

    totalgoods = sum([len(goods[g]) for g in goods])

    print('{} succeeded, {} failed ({}%)'.format(
        totalgoods, len(bads), len(bads) / len(goods) * 100))

    # False for most numerous last
    # for k in sorted(goods, key=lambda k: len(goods[k]), reverse=False):
    #    print('{}: {}'.format(k, len(goods[k])))

    subcollection = collection.initialize_ordered_bulk_op()

    for author,articles in goods.iteritems():
        if len(articles) > 100:             # Only select prolific authors
            for article in articles:
                try:
                    article['content'] = jewishworldreview_body(article)
                    subcollection.find({'uri': article['uri']}).upsert().replace_one(article)
                except Exception as e:
                    bads.append(article)
                    print(e)


def run_breitbart():
    print('Working on Breitbart. . .')
    author = source = 'breitbart'

    subcollection = collection.initialize_ordered_bulk_op()

    # Read agenda
    uris = [u.replace('\n', '') for u in open(os.path.join('profiles','breitbart','manifest', 'r')).readlines()]
    print('{} found'.format(str(len(uris))))
    print('----------')

    # Capture content
    for idx, u in enumerate(uris):
        # N.B.:
        # I tried, for the life of me, to instantiate a template and then allow the loop to change the relevant
        # properties but something about submitting the first (0th) document to the database assigns, in perpetuity,
        # the resultant ObjectID, which is carried across articles and thus results in an immediate
        #   'batch op errors occurred'
        # or more specifically:
        #   E11000 duplicate key error collection: nuliterature.raw index: _id_ dup key: { : ObjectId('############') }

        article = {'author': author, 'source': source}

        # This is pretty messy
        article['uri'] = os.path.join(os.path.abspath('.'), 'profiles', article['source'], u.replace('./', ''))

        try:
            article['content'] = breitbart_body(article)
            subcollection.find({'uri': article['uri']}).upsert().replace_one(article)

            if idx % 100 == 0:
                print('... {} of {}'.format(str(idx),str(len(uris))))
            if idx % 1000 == 0:
                print('>>> executing subcollection')
                result = subcollection.execute()
                pprint(result)
                subcollection = collection.initialize_ordered_bulk_op()

        except Exception as e:
            print(e.message)
            pass


if __name__ == '__main__':
    run_jewishworldreview()
    run_breitbart()
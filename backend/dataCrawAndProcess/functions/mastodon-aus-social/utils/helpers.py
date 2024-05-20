import re
import string
from bs4 import BeautifulSoup
from textblob import TextBlob

def search_params(key_list):
    p = '&'.join([f'q={x}' for x in key_list])
    return p

def split_with_punc(s):
    r = re.split(r'[\W_]+', s)
    return [a.strip() for a in r if a.strip()]

def remove_unicode(s):
    a = s.encode("ascii", "ignore")
    return a.decode().strip().lower()

def split_with_space(s):
    return [a for a in s.split(" ") if a]

def remove_invalid(s):
    return re.sub(r'(@\S+|http\S+|https\S+|#\S+|\d+)', '', s).strip()

def remove_punc(s):
    return ''.join(c for c in s if c not in string.punctuation)

def concat_all(s_list):
    return [j for i in s_list for j in i]

def remove_short(s_list):
    return [a for a in s_list if len(a) > 2]

def remove_html_tags(text):
    return BeautifulSoup(text, "html.parser").get_text()

def get_tokens(content):
    content = remove_unicode(content)
    content = remove_invalid(content)
    tokens = split_with_space(content)
    tokens = concat_all(list(map(split_with_punc, tokens)))
    return list(set(remove_short(tokens)))

def extract_info(status):
    s = {}
    s['id'] = str(status.get('id'))
    s['created_at'] = status.get('created_at')
    s['lang'] = status.get('language')
    s['sentiment'] = TextBlob(status.get('content')).sentiment.polarity
    s['tokens'] = get_tokens(remove_html_tags(status.get('content')))
    s['tags'] = [tag.get('name') for tag in status.get('tags', [])]
    if not s['tags'] and not s['tokens']:
        return None
    return s

def create_timelines_url(instance_url, max_id=None, local=False):
    params = f"max_id={max_id}" if max_id else ""
    params += "&local=true" if local else ""
    return f"{instance_url}/api/v1/timelines/public?{params}"
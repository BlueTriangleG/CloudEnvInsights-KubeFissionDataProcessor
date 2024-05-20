import asyncio
import aiohttp
import time
import json
import re
import string
from datetime import datetime, timedelta
from textblob import TextBlob
from bs4 import BeautifulSoup

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
    # Uncomment this line if you want to keep the original content
    # s['content'] = remove_html_tags(status.get('content'))
    s['tags'] = [tag.get('name') for tag in status.get('tags', [])]
    if not s['tags'] and not s['tokens']:
        return None
    return s

def create_timelines_url(instance_url, max_id=None, local=False):
    params = f"max_id={max_id}" if max_id else ""
    params += "&local=true" if local else ""
    return f"{instance_url}/api/v1/timelines/public?{params}"

async def fetch_timeline(session, url, headers):
    async with session.get(url, headers=headers) as response:
        return await response.json()

async def get_timelines(access_token, instance_url, years, output_file, local=False):
    headers = {'Authorization': f'Bearer {access_token}'}
    date_limit = datetime.now() - timedelta(days=365*years)
    max_id = None
    count = 0

    async with aiohttp.ClientSession() as session:
        while True:
            search_url = create_timelines_url(instance_url, max_id, local)
            try:
                data = await fetch_timeline(session, search_url, headers)
            except Exception as e:
                print(f"Error requesting timelines: {str(e)}")
                await asyncio.sleep(1)
                continue

            if data:
                if "error" in data:
                    print(f"Error requesting timelines: {data['error']}")
                    if data["error"] == "Too many requests":
                        await asyncio.sleep(10)
                    continue
                try:
                    with open(output_file, 'a') as f:
                        for status in data:
                            created_at = datetime.strptime(status['created_at'], '%Y-%m-%dT%H:%M:%S.%fZ')
                            if created_at >= date_limit:
                                info = extract_info(status)
                                if info:
                                    count += 1
                                    json.dump(info, f)
                                    f.write("\n")
                            else:
                                print(f"ID: {status['id']} reached date limit")
                                return count
                    max_id = data[-1]['id']
                except Exception as e:
                    print(f"Error setting status data: {str(e)}")
                    print("Data:", json.dumps(data))
                    continue
            else:
                print("No data returned")
                break
            await asyncio.sleep(1)  # Reduced sleep interval
    return count

# Example usage
if __name__ == "__main__":
    access_token = 'iq2gpUooJ10hAFXm19ifTGXitRWKs8KResFM-uMgEOY'
    instance_url = 'https://mastodon.social/'
    years = 1
    output_file = 'output.json'
    local = False

    loop = asyncio.get_event_loop()
    count = loop.run_until_complete(get_timelines(access_token, instance_url, years, output_file, local))
    print(f"Total statuses fetched: {count}")

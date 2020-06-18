import re
import pandas as pd
from requests_html import HTMLSession
from fake_useragent import UserAgent
import random
import time


def googlescraper(query):
    print('關鍵字：', query)

    query = query.replace(' ', '+')

    ua = UserAgent()
    session = HTMLSession()
    results = []
    for num in range(0, 1000, 10):
        URL = f"https://www.google.com/search?q={query}&start={num}"
        headers = {'User-Agent': ua.random}
        r = session.get(URL, headers=headers)
        r_response = int(str(r)[11:14])

        if '找不到符合搜尋字詞' in r.html.html:
            print('找不到符合搜尋字詞')
            break

        if r_response == 200:
            time.sleep(random.uniform(0, 2))
            print('正在處理：', num, '/1000')
            links = r.html.absolute_links
            linktolist = []
            for i in range(len(links)):
                linktolist.append(links.pop())
            for i in range(len(linktolist)):
                if 'google' not in linktolist[i]:
                    results.append(linktolist[i])

    return results


query = input('輸入關鍵字：')
url = googlescraper(query)
print(pd.Series(url))
EMAIL_REGEX = r"""(?:[a-z0-9!#$%&'*+/=?^_`{|}~-]+(?:\.[a-z0-9!#$%&'*+/=?^_`{|}~-]+)*|"(?:[\x01-\x08\x0b\x0c\x0e-\x1f\x21\x23-\x5b\x5d-\x7f]|\\[\x01-\x09\x0b\x0c\x0e-\x7f])*")@(?:(?:[a-z0-9](?:[a-z0-9-]*[a-z0-9])?\.)+[a-z0-9](?:[a-z0-9-]*[a-z0-9])?|\[(?:(?:(2(5[0-5]|[0-4][0-9])|1[0-9][0-9]|[1-9]?[0-9]))\.){3}(?:(2(5[0-5]|[0-4][0-9])|1[0-9][0-9]|[1-9]?[0-9])|[a-z0-9-]*[a-z0-9]:(?:[\x01-\x08\x0b\x0c\x0e-\x1f\x21-\x5a\x53-\x7f]|\\[\x01-\x09\x0b\x0c\x0e-\x7f])+)\])"""
ua = UserAgent()
session = HTMLSession()
res = pd.DataFrame(columns=['Title', 'Email'])
for i in range(len(url)):
    try:
        headers = {'User-Agent': ua.random}
        r = session.get(url[i], headers=headers)
        print(r)
        # r.html.render()
        e = r.html.find("title", first=True)

        n = 0
        for re_match in re.finditer(EMAIL_REGEX, r.html.raw_html.decode()):
            res.loc[len(res)] = [e.text, re_match.group()]
            print('writting:', e.text, re_match.group())
            n += 1
    except Exception:
        print(r)
        print('Except')
        pass


print(res)
res.to_csv('res.csv', encoding='utf_8_sig')

"""Functions to fetch parsed data from yellowpages.com.my."""
import time
import urllib

from random import randint
from django.utils.text import slugify
from lib.parser.constants import INDUSTRIES
from lib.parser.utils import istag, cleanstr, connect

DOMAIN = 'http://www.yellowpages.com.my'

CITIES = (
    'Kuala Lumpur',
    'Shah Alam',
    'Petaling Jaya',
    'Subang Jaya',
    'Pulau Pinang',
    'Johor Bahru',
    'Pasir Gudang',
    'Kajang',
    'Cheras',
    'Ampang',
    'Klang',
    'Ipoh',
    'Batu Gajah',
    'Selayang',
    'Rawang',
    'Kuching',
    'Seremban',
    'Georgetown',
    'Malacca',
    'Kota Bahru',
    'Kota Kinabalu',
    'Kuantan',
    'Sungai Petani',
    'Batu Pahat',
    'Tawau',
    'Sandakan',
    'Bukit Mertajam',
    'Alor Setar',
    'Kuala Terengganu',
    'Taiping',
    'Miri',
    'Kluang',
    'Butterworth',
    'Kulim',
    'Kulai',
    'Sibu',
    'Muar',
    'Sitiawan',
    'Kangar',
    'Banting',
    'Jitra',
    'Sepang',
    'Kuala Selangor',
    'Teluk Intan',
    'Lahad Datu',
    'Bayan Lepas',
    'Kuala Kubu Bharu',
    'Kota Tinggi',
    'Segamat',
    'Pasir Mas',
    'Bintulu',
    'Alor Gajah',
    'Parit Buntar',
    'Tanjung Malim',
    'Tapah',
    'Keningau',
    'Chukai',
    'Nibong Tebal',
    'Sungai Jawi',
    'Temerioh',
)


def _fetch_details(url):
    """Fetch and parse company's details."""
    soup = connect(url)
    data = dict()
    # Get company name.
    cont = soup.find(id='result')
    if cont is not None:
        name_tag = cont.find('h2')
        if name_tag is not None:
            data['name'] = cleanstr(cont.find('h2').string)
        table = cont.find('table')
        if table is not None:
            rows = table.find_all('tr')
            if len(rows) > 1:
                row = rows[1]
                for col in row.children:
                    if istag(col):
                        s = str()
                        for el in col.contents:
                            if el.string is not None:
                                if istag(el):
                                    s += cleanstr(el.string)
                                else:
                                    s += cleanstr(el)
                        if 'Tel:' in s:
                            # Get phone number.
                            phone = ''
                            for d in s[5:17]:
                                if d.isdigit():
                                    phone += d
                            if len(phone) == 10:
                                data['phone'] = phone
                        else:
                            # Get city.
                            for city in CITIES:
                                if city.lower() in s.lower():
                                    data['city'] = city
    if 'name' in data and 'phone' in data and 'city' in data:
        return data
    return None


def fetch(industry=None, limit=10):
    """Entry point for fetching company list."""
    def _parse(industry, delay=False):
        """Parse data for industry. Use recursive call when the page
        isn't available or we haven't receive enough data.
        """
        if delay:
            time.sleep(20)  # in order to avoid ban

        slug = slugify(industry)
        url_pattern = '{domain}/category/{category}/?p={page}'
        url = url_pattern.format(domain=DOMAIN, category=slug,
                                 page=randint(1, 10))
        try:
            soup = connect(url)
        except urllib.error.HTTPError:
            _parse(industry, delay=True)

        list_ = list()
        ul = soup.find(id='result')
        if ul is not None:
            for li in ul.find_all(class_='listing'):
                if len(list_) == limit:
                    break
                if istag(li):
                    link = li.find('a')['href']
                    profile_url = '{domain}{link}'.format(
                        domain=DOMAIN, link=link)
                    try:
                        data = _fetch_details(profile_url)
                    except urllib.error.HTTPError:
                        continue
                    else:
                        if data is None:  # incomplete information
                            continue
                        data.update(dict(industry=industry,
                                         country='Malaysia'))
                        list_.append(data)
        else:
            # Probably we got banned.
            return []
        # Continue searching for records if we haven't got enough.
        if len(list_) < limit:
            _parse(industry, delay=True)
        return list_

    if industry is not None:
        res = _parse(industry)
    else:
        res = list()
        for key, list_ in INDUSTRIES.items():
            for v in list_:
                if len(res) == limit:
                    break
                res.extend(_parse(v, delay=True))
    return res

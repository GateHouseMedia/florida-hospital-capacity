# Initial code from the great Jeremy Bowers!
# CSV pull from Aric Chokey

# Dashboard here https://bi.ahca.myflorida.com/t/ABICC/views/Public/HospitalBedsCounty?%3AshowAppBanner=false&%3Adisplay_count=n&%3AshowVizHome=n&%3Aorigin=viz_share_link&%3AisGuestRedirectFromVizportal=y&%3Aembed=y

from bs4 import BeautifulSoup
import requests

import datetime
import json
import os

timestamp = datetime.datetime.now().strftime("%Y-%m-%d_%H%M")
rawdir = "raw/"
basefilename = "FL-hospital-"

basecsvurl = "https://bi.ahca.myflorida.com/t/ABICC/views/Public/"

corefilenames = [
    "HospitalBedsHospital",
    "HospitalBedsCounty",
    "ICUBedsCounty",
    "ICUBedsHospital"
    ]

os.makedirs(rawdir, exist_ok=True)

headers = {
    'sec-fetch-mode': 'cors',
    'origin': 'https://bi.ahca.myflorida.com',
    'accept-encoding': 'gzip, deflate, br',
    'accept-language': 'en-US,en;q=0.9',
    'cookie': 'tableau_locale=en',
    'x-tsi-active-tab': 'Hospital%20BedsCounty',
    'user-agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_4) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/77.0.3865.90 Safari/537.36',
    'content-type': 'application/x-www-form-urlencoded',
    'accept': 'text/javascript',
    'referer': 'https://bi.ahca.myflorida.com/t/ABICC/views/Public/HospitalBedsCounty?%3AshowAppBanner=false&%3Adisplay_count=n&%3AshowVizHome=n&%3Aorigin=viz_share_link&%3AisGuestRedirectFromVizportal=y&%3Aembed=y',
    'authority': 'bi.ahca.myflorida.com',
    'sec-fetch-site': 'same-origin',
    'dnt': '1',
}
data = {
  'worksheetPortSize': '{"w":1680,"h":536}',
  'dashboardPortSize': '{"w":1680,"h":536}',
  'clientDimension': '{"w":1680,"h":220}',
  'renderMapsClientSide': 'true',
  'isBrowserRendering': 'true',
  'browserRenderingThreshold': '100',
  'formatDataValueLocally': 'false',
  'clientNum': '',
  'navType': 'Reload',
  'navSrc': 'Top',
  'devicePixelRatio': '2',
  'clientRenderPixelLimit': '25000000',
  'allowAutogenWorksheetPhoneLayouts': 'true',
  'sheet_id': 'Hospital%20BedsCounty',
  'showParams': '{"checkpoint":false,"refresh":false,"refreshUnmodified":false}',
  'stickySessionKey': '{"featureFlags":"{}","isAuthoring":false,"isOfflineMode":false,"lastUpdatedAt":1585873049792,"workbookId":1770}',
  'filterTileSize': '200',
  'locale': 'en_US',
  'language': 'en',
  'verboseMode': 'false',
  ':session_feature_flags': '{}',
  'keychain_version': '1'
}
baseurl = "https://bi.ahca.myflorida.com/t/ABICC/views/Public/HospitalBedsCounty?%3AshowAppBanner=false&%3Adisplay_count=n&%3AshowVizHome=n&%3Aorigin=viz_share_link&%3AisGuestRedirectFromVizportal=y&%3Aembed=y"
r = requests.get(baseurl, headers=headers)
soup = BeautifulSoup(r.text, 'lxml')
config = json.loads(soup.select('#tsConfigContainer')[0].text)
sessionid = config['sessionid']
response = requests.post(f'https://bi.ahca.myflorida.com/vizql/t/ABICC/w/Public/v/HospitalBedsCounty/bootstrapSession/sessions/{sessionid}', headers=headers, data=data)

if response.status_code == 200:
    with open(f"{rawdir}{basefilename}{timestamp}.raw", "wb") as f:
        f.write(response.content)

for corefilename in corefilenames:
    r = requests.get(f"{basecsvurl}{corefilename}.csv", headers=headers)
    if r.status_code == 200:
        with open(f"{rawdir}{corefilename}_{timestamp}.csv", "wb") as outfile:
            outfile.write(r.content)
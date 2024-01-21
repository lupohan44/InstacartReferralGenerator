import json
import os
import random
import re
import urllib.parse

import requests
from bs4 import BeautifulSoup
from flask import Flask
from random_user_agent.user_agent import UserAgent
from random_user_agent.params import SoftwareName, OperatingSystem

app = Flask(__name__)


@app.route('/')
def ref():
    try:
        code, offer_detail, advertisement = get_ref()
        if code and offer_detail and advertisement:
            # add a link to advertisement
            regex = r'(http|ftp|https):\/\/([\w_-]+(?:(?:\.[\w_-]+)+))([\w.,@?^=%&:\/~+#-]*[\w@?^=%&\/~+#-])'
            matches = re.finditer(regex, advertisement, re.MULTILINE | re.IGNORECASE)
            for matchNum, match in enumerate(matches, start=1):
                advertisement = advertisement.replace(match.group(), f'<a href="{match.group()}">{match.group()}</a>')
            return f'<h1>Code: {code}</h1><p>{offer_detail}</p><p>{advertisement}</p>'
        else:
            return '<h1>No code found</h1>'
    except Exception as e:
        print(e)
        return '<h1>Something went wrong</h1>'


def get_ref():
    url = 'https://www.instacart.com/store/referrals'
    software_names = [SoftwareName.CHROME.value]
    operating_systems = [OperatingSystem.WINDOWS.value, OperatingSystem.LINUX.value]

    user_agent_rotator = UserAgent(software_names=software_names, operating_systems=operating_systems, limit=100)
    cookies = []
    cookies_folder = 'cookies'
    files = os.listdir(cookies_folder)
    for file in files:
        if file.endswith('.txt'):
            with open(os.path.join(cookies_folder, file), 'r') as f:
                cookies.append(f.read())
    if not cookies:
        raise Exception('No cookies found')
    headers = {
        'Referer': 'https://www.instacart.com/store/referrals',
        'Cookie': random.choice(cookies),
        'User-Agent': user_agent_rotator.get_random_user_agent()
    }
    response = requests.get(url, headers=headers)
    if response.ok:
        try:
            bs = BeautifulSoup(response.text, 'html.parser')
            script_data = bs.find('script', id='node-apollo-state')
            # url decode text
            script_data_decode = urllib.parse.unquote(script_data.text)
            json_data = json.loads(script_data_decode)
            for key in json_data.keys():
                if key.startswith('ReferralPage'):
                    referral_details = json_data[key][list(json_data[key].keys())[0]]['referralDetails']
                    code = referral_details['shareCode']
                    offer_detail = referral_details['viewSection']['offerDetails']['headerString'].replace('\n', ' ')
                    advertisement = referral_details['viewSection']['referralShareInfo']['emailContentString']
                    return code, offer_detail, advertisement
        except Exception as e:
            print(e)
            return None, None, None
    return None, None, None


if __name__ == '__main__':
    app.run(port=19320)

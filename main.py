import time
from tqdm import tqdm
from pprint import pprint
import json
import requests
from urllib.parse import urlencode
ydtoken = open('ydtoken').read()
APP_ID = '51724525'
OAUTH_BASE_URL = 'https://oauth.vk.com/authorize'
params = {
    'client_id': APP_ID,
    'redirect_uri': 'https://oauth.vk.com/blank.html',
    'display': 'page',
    'scope': 'photos',
    'response_type': 'token'
          }
oauth_url = f'{OAUTH_BASE_URL}?{urlencode(params)}'
# print(oauth_url)
VKTOKEN = 'vk1.a.vBhyyqOIrrXUPyH9m1L8udFvO2EXuCzbwDtTPxjFaiEqnLUOrZNIkGdzrX4x-2HnuwXsYHERPh1AjvydezIRVS3ZPst2hF0aBZG0JpLA3H9fYZTBF33txcCdX_S06y44SCchGvAPq4LO5M5JwpCVPsKcENgxn9Yow2GMJSIO-ZY7CFyJDPz6tz2WtSUb_crv'


class VKAPIClient:
    API_BASE_URL = 'https://api.vk.com/method/'


    def __init__(self, token, user_id):
        self.token = token
        self.user_id = user_id


    def common_params(self):
        return {
            'access_token': self.token,
            'v': '5.131',
            'extended': '1'
        }


    def get_photos(self):
        params = self.common_params()
        params.update({'owner_id': self.user_id, 'album_id': 'profile'})
        response = requests.get(f'{self.API_BASE_URL}photos.get', params=params)
        return response.json()


    def savephoto(self):
        photo_json = []
        photos = self.get_photos()['response']['items']
        total_photos = len(photos)
        for i, photo in tqdm(enumerate(photos, 1), total=total_photos, desc='Saving photos'):
            sizes = photo['sizes'][-1]
            url = sizes['url']
            response = requests.get(url)
            filename = f'{photo["likes"]["count"]}.jpg'
            with open(filename, 'wb') as file:
                file.write(response.content)
            album = 'NT'
            url = 'https://cloud-api.yandex.net/v1/disk/resources/upload'
            params = {'path': f'/{album}/{filename}'}
            headers = {'Authorization': f'OAuth {ydtoken}'}
            response = requests.get(url, params=params, headers=headers)
            data = response.json()
            url = data['href']
            with open(filename, 'rb') as f:
                response = requests.post(url, files={'file': f})
            photo_json.append({
                                "file_name": filename,
                                "size": sizes['type']
                              })
            with open("photo_info.json", "w") as file:
                json.dump(photo_json, file, indent=1)


client = VKAPIClient(VKTOKEN, 260829155)
photos = client.savephoto()




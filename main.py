import requests, ctypes, os, sys
from dotenv import load_dotenv

load_dotenv()

current_dir = os.path.dirname(os.path.abspath(__file__))
daily_image_file_name = 'daily_image.jpg'
full_path = os.path.join(current_dir, daily_image_file_name)

api_url = 'https://api.unsplash.com/photos/random'
access_key = os.getenv('UNSPLASH_ACCESS_KEY')
headers = {
    'Authorization': f'Client-ID {access_key}'
}

def download_image_from_url_and_save(image_url):
    response = requests.get(image_url)

    if response.status_code == 200:
        image_data = response.content

        with open(daily_image_file_name, 'wb') as image_file:
            image_file.write(image_data)
    else:
        print(f'Failed to download image: {response.reason} \nStatus Code: {response.status_code}')
        sys.exit(1)


def set_desktop_wallpaper():
    SPI_SETDESKWALLPAPER = 0x0014
    ctypes.windll.user32.SystemParametersInfoW(SPI_SETDESKWALLPAPER, 0, full_path, 3)

response = requests.get(api_url, headers=headers)

if response.status_code == 200:
    data = response.json()

    raw_image_url = data['urls']['raw']

    download_image_from_url_and_save(raw_image_url)
    set_desktop_wallpaper()

    print('Your daily wallpaper has been successfully set!')
else:
    print(f'Failed to call the api: {response.reason} \nStatus Code: {response.status_code}')
    sys.exit(1)
  
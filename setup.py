import os, sys, requests, zipfile, tarfile
from os.path import join, dirname, abspath

if sys.version_info[0] < 3 and sys.version_info[1] < 6:
    sys.exit(' - Error, please run the setup with Python 3.6 or higher.')

def download(src, dest):
    '''
    Downloads a file
    '''

    if not os.path.isfile(dest):
        with requests.get(src) as req:
            with open(dest, 'wb') as fd:
                fd.write(req.content)

def decompress(src, dest):
    '''
    Decompresses a zip, or anything else, compressed file
    '''

    if not os.path.exists(src): print(f' - {src} does not exist'); return

    if src.endswith('.zip'):
        with zipfile.ZipFile(src, "r") as zip_ref:
            zip_ref.extractall(dest)
    else:
        with tarfile.open(src) as tar:
            tar.extractall(dest)

def main():
    '''
    Main function
    '''

    print('Setting Cerberus up, please be patient')
    if sys.platform == 'windows':
        #print(' - Windows detected, Cerberus will use "requests" instead of "PyCurl".')

        chrome_url = 'https://chromedriver.storage.googleapis.com/104.0.5112.20/chromedriver_win32.zip'
        gecko_url = 'https://github.com/mozilla/geckodriver/releases/download/v0.31.0/geckodriver-v0.31.0-win64.zip'

    elif sys.platform == 'linux':
        #print(' + Linux detected, Cerberus will favor the usage of "PyCurl" over "requests", but will use "requests" as backup')

        #print(' + Installing PyCurl')
        #os.system('sudo apt install python3-pycurl -y')

        chrome_url = 'https://chromedriver.storage.googleapis.com/104.0.5112.20/chromedriver_linux64.zip'
        gecko_url = 'https://github.com/mozilla/geckodriver/releases/download/v0.31.0/geckodriver-v0.31.0-linux64.tar.gz'
    else:
        sys.exit(' - Sorry, only Windows and Linux are supported :/')

    target_dir = join(dirname(abspath(__file__)), 'src', 'files')
    chrome_dst = 'chrome_driver.' + chrome_url.split('.')[-1] if not chrome_url.endswith('.tar.gz') else 'tar.gz'
    gecko_dst = f'gecko_driver.' + gecko_url.split('.')[-1] if not gecko_url.endswith('.tar.gz') else 'tar.gz'

    print(' + Installing chrome driver')
    download(chrome_url, chrome_dst) # chrome uses zip compression for both windows and linux
    decompress(chrome_dst, target_dir)

    print(' + Installing gecko driver')
    download(gecko_url, gecko_dst)
    decompress(gecko_dst, target_dir)

    print(' + Installing python depencies')
    os.system('python3 -m pip install -r requirements.txt')

    print(' + Cleaning up.')
    os.remove(chrome_dst)
    os.remove(gecko_dst)
    os.system('sudo apt autoremove -y; sudo apt autoclean -y')

    print(' + Done')

if __name__ == '__main__':
    main()
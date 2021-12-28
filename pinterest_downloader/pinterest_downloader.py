import argparse
import m3u8
import requests
from version import __version__

def get_master(url: str):
    """
    Extracts the m3u8 master url from the webpage.
    :param url: pinterest web url
    :return: url of the master file
    """
    # TODO: Extract .m3u8 from pinterest webpage


def download_image(url: str):
    """
    Downloads an image from pinterest
    :param url: pinterest web url
    """
    # TODO: download image


def download_video(master_url: str):
    """
    Downloads the blob: video
    :param master_url: url of the m3u8 master file.
    """
    # Get the website request
    m3u8_request = requests.get(master_url)
    m3u8_master = m3u8.loads(m3u8_request.text)
    m3u8_location = master_url[0:master_url.rfind('/') + 1]

    # Get initial playlist
    playlist_url = m3u8_master.data['playlists'][0]['uri']
    play_r = requests.get(m3u8_location + playlist_url)
    m3u8_master_play = m3u8.loads(play_r.text)
    m3_data = (m3u8_master_play.data)
    m3_datas = m3_data['segments'][0]['uri']

    # Combine stream segments
    with open('video.ts', 'wb') as fs:
        for segments in m3_data['segments']:
            uri = segments['uri']
            print(uri)
            m3u8_request = requests.get(m3u8_location + uri)
            fs.write(m3u8_request.content)


def parse_options():
    """
    :return:
    """
    parser = argparse.ArgumentParser(description='Discord channel scraper')

    requiredNamed = parser.add_argument_group('Required arguments:')
    requiredNamed.add_argument('-m', '--master', type=str, required=True,
                               help='A link to the master file located on a pinterest link. In the form of *.m3u8')
    requiredNamed.add_argument('-o', '--output', type=str, required=True,
                               help='Output file name in the form of *.ts or *.png')

    return parser.parse_args()


if __name__ == "__main__":
    print("Pinterest Downloader version", __version__)
    args = parse_options()

    if '.ts' in args.output:
        download_video(args.master)
    # else:
    #     download_image(args.master)

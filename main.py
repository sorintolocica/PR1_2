import os
import re
import socket
import ssl
import threading

import requests

sem = threading.Semaphore(2)
with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as mysocket:
    mysocket.connect(("utm.md", 443))
    mysocket = ssl.wrap_socket(mysocket, keyfile=None, certfile=None, server_side=False, cert_reqs=ssl.CERT_NONE,
                               ssl_version=ssl.PROTOCOL_SSLv23)
    mysocket.sendall(b"GET / HTTP/1.1\r\nHost: utm.md\r\n\r\n")

    print(str(mysocket.recv(52), 'utf-8'))


def get_url_images_in_text(source):

    urls = []
    results = re.findall("[^\"']*\\.(?:png|jpg|gif)", source)

    for x in results:
        if 'https://' not in x:
            x = 'https://utm.md' + x
        urls.append(x)
    urls = list(set(urls))
    print('Links of images detected: ' + str(len(urls)))
    return urls


def get_images_from_url(url):
    resp = requests.get(url)
    urls = get_url_images_in_text(resp.text)
    print('\nUrls:\n', urls)
    return urls




def download_images(path):
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as mysocket:
        mysocket.connect(("utm.md", 443))
        mysocket = ssl.wrap_socket(mysocket, keyfile=None, certfile=None, server_side=False, cert_reqs=ssl.CERT_NONE,
                                   ssl_version=ssl.PROTOCOL_SSLv23)
        mysocket.sendall("GET {0} HTTP/1.1\r\nHost: utm.md\r\nConnection: close\r\n\r\n".format(path).encode("latin1"))

        images = b''

        while True:

            data = mysocket.recv(1024)
            if not data:
                images = images.split(b"\r\n\r\n")
                if "200" not in images[0].decode("latin1"):
                    print(path)
                image_path = os.path.join(os.getcwd(), "ima", path.rpartition("/")[-1])
                with open(image_path, "wb") as fcont:
                    fcont.write(images[-1])
                break

            images += data


img_list = get_images_from_url('https://utm.md/')



thread_list = []
threads = 4

for i in img_list:
    t = threading.Thread(target=download_images, args=(i,))
    thread_list.append(t)
    t.start()


for i in thread_list:
    i.join()




print("Download Done")
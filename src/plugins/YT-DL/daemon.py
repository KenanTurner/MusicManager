#!/usr/bin/env python3
import socket
import threading
import daemon
import json
from yt_dlp import YoutubeDL, parse_options

#run this script with the following command:
#nohup python3 daemon.py > /dev/null 2> /dev/null &

#test urls
#url = 'https://www.youtube.com/watch?v=Pi-MRZBP91I'
#url = 'https://soundcloud.com/ubiktune/fearofdark-rolling-down-the-street-in-my-katamari'
#url = 'https://the8bitbigband.bandcamp.com/track/metaknights-revenge-feat-buttonmasher-from-kirby-super-star'

ydl_opts = {
    'format': 'bestaudio',
    'quiet': True,
    'no_warnings': True,
}

def handle_client(sock,ydl):
    try:
        data = sock.recv(8192)#.decode('utf-8')
        track = json.loads(data.decode('utf-8'))
        info = ydl.extract_info(track['src'], download=False)
        #sources = [{"audio_ext":x['audio_ext'],"url":x['fragment_base_url'] if "fragment_base_url" in x else x['url']} for x in info['formats'] if x['acodec'] != "none" and x['vcodec'] == "none"]
        sources = [{
            "ext":x['ext'] if "ext" in x else None,
            "codec":x['acodec'] if "acodec" in x else None,
            "abr":x['abr'] if "abr" in x else None,
            "asr":x['asr'] if "asr" in x else None,
            "src":x['fragment_base_url'] if "fragment_base_url" in x else x['url']}
        for x in info['formats'] if x['resolution'] == "audio only"]
        sources.reverse()
        #print(sources)
        track['sources'] = sources
        track['src'] = info['url']
        sock.sendall(json.dumps(track).encode('utf-8'))
        #print(info['audio_ext'])
    except Exception as e:
        print(e)
        sock.sendall("ERROR: Invalid URL!".encode('utf-8'))
    finally:
        sock.close()

def serve_forever(ydl):
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as server:
        server.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        server.bind(('localhost', 4200))
        server.listen(1)
        while True:
            conn, address = server.accept()
            thread = threading.Thread(target=handle_client, args=[conn,ydl])
            thread.daemon = True
            thread.start()

with YoutubeDL(ydl_opts) as ydl:
    serve_forever(ydl)
    
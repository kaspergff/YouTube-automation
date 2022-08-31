import json
from venv import create
from TikTokApi import TikTokApi
from pathlib import Path
from moviepy.editor import *
import os


# Const
VIDEO_LENGTH = 60
TAGS = [
    # "Soccer",
    # "Volleyball",
    # "Cricket",
    "Baseball",
    "Basketball",
    "Tennis"
]

def get_cookies_from_file():
    with open('C:/Users/krdeg/dev/YouTube-automation/videoDownloader/exported-cookies.json') as f:
        cookies = json.load(f)

    cookies_kv = {}
    for cookie in cookies:
        cookies_kv[cookie['name']] = cookie['value']

    return cookies_kv


cookies = get_cookies_from_file()


def get_cookies(**kwargs):
    return cookies


def download_video(id:str,api:TikTokApi,path:str):
    video = api.video(id=id)
    # Bytes of the TikTok video
    video_data = video.bytes()
    name = id + ".mp4"
    full_path = path + "/" + name
    with open(full_path, "wb") as out_file:
        out_file.write(video_data)
    return full_path
    

def videos_downloader(video_length:int,video_tag:str,path:str):
    with TikTokApi() as api:
        total_time = 0
        counter = 0
        api._get_cookies = get_cookies
        tag = api.hashtag(name=video_tag)
        vids = tag.videos(count=50)
        for v in vids:
            if total_time > video_length:
                break
            print("Downloading video nr: " + str(counter))
            video = download_video(v.id,api,path)
            total_time += get_length(video)
            print("Total time: ",str(total_time) + " seconds")
            counter += 1
        print("Videos downloaded")
            


# function to get the length of a video in seconds
def get_length(filename):
    clip = VideoFileClip(filename)
    return clip.duration


def create_compilation(name:str):
    print("Start: " + name)
    project_name = "tag_" + name
    print("Creating folder")
    path = "C:/Users/krdeg/dev/YouTube-automation/videoDownloader/projects/"+project_name
    Path(path).mkdir(parents=True, exist_ok=True)
    videos = VIDEO_LENGTH
    videos_downloader(videos,name,path)   
    print("Creating video")

    L = []
    for root, dirs,files in os.walk(path):
        for file in files:
            if os.path.splitext(file)[1] == '.mp4':
                filePath = os.path.join(root, file)
                video = VideoFileClip(filePath)
                L.append(video)
    for vid in L:
        vid.set_fps(24)
    final_clip = concatenate_videoclips(L,method="compose")
    final_clip.write_videofile(path + "/" + name +".mp4", fps=24, remove_temp=True)
    
    # Delete sub videos
    for root, dirs,files in os.walk(path):
        for file in files:
            if os.path.splitext(file)[1] == '.mp4':
                filePath = os.path.join(root, file)
                if filePath[-5].isnumeric() == True:
                    os.remove(filePath)


# function to resize tiktok for youtube
def resize_video(tiktok: VideoFileClip):
    # create mask
    mask = tiktok.resize(1920,1080)




def main():
    # for tag in TAGS:
    #     create_compilation(tag)
    print("main function")
    create_compilation("Hockey")



if __name__ == "__main__":
    main()
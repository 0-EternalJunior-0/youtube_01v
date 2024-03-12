import requests
from typing import List, Dict, Any, AnyStr, Tuple


def search_for_stock_videos(query: str, api_key: str, it: int, time_minimum: int, width_height=[3840, 2160]) \
        -> Dict[Tuple[int, int], List[Dict[str, int]]]:
    # Build headers
    headers = {
        "Authorization": api_key
    }

    video_res = []

    if it > 80:
        response = []
        items_per_page = 80
        for page_number in range(1, int((it // items_per_page) + 2)):
            qurl = f"https://api.pexels.com/videos/search?query={query}&per_page={items_per_page}&page={page_number}"
            r = requests.get(qurl, headers=headers)

            # Перевірте, чи отримали вдалу відповідь перед роботою з нею
            if r.status_code == 200:
                videos_on_page = r.json().get("videos", [])
                response.extend(videos_on_page)  # Розгорнути список "videos" і додати його до response
                print(f"Page {page_number}: {len(videos_on_page)} videos")
            else:
                print(f"Request failed with status code {r.status_code}")

        print(f"Total videos: {len(response)}")

        # Додаткові перевірки на наявність ключів у відповіді
        for video_info in response:
            time = video_info.get("duration", 0)
            if time <= time_minimum:
                continue

            video_files = video_info.get("video_files", [])
            hd_quality_items = [item for item in video_files if item.get("quality") == "hd"]

            if not hd_quality_items:
                continue

            max_resolution_video = next(
                (item for item in hd_quality_items if
                 item.get("width") == width_height[0] and item.get("height") == width_height[1]), None)

            if max_resolution_video:
                max_resolution_video_url = max_resolution_video.get("link", "")

                if max_resolution_video_url:
                    _video_res = {"url": max_resolution_video_url, "time": time, "width": max_resolution_video["width"],
                                  "height": max_resolution_video["height"]}
                    video_res.append(_video_res)

    else:
        qurl = f"https://api.pexels.com/videos/search?query={query}&per_page={it}"
        r = requests.get(qurl, headers=headers)

        # Перевірте, чи отримали вдалу відповідь перед роботою з нею
        if r.status_code == 200:
            response = r.json().get("videos", [])
        else:
            print(f"Request failed with status code {r.status_code}")

        # Додаткові перевірки на наявність ключів у відповіді
        for video_info in response:
            time = video_info.get("duration", 0)
            if time <= time_minimum:
                continue

            video_files = video_info.get("video_files", [])
            hd_quality_items = [item for item in video_files if item.get("quality") == "hd"]

            if not hd_quality_items:
                continue

            max_resolution_video = next(
                (item for item in hd_quality_items if
                 item.get("width") == width_height[0] and item.get("height") == width_height[1]), None)

            if max_resolution_video:
                max_resolution_video_url = max_resolution_video.get("link", "")

                if max_resolution_video_url:
                    _video_res = {"url": max_resolution_video_url, "time": time, "width": max_resolution_video["width"],
                                  "height": max_resolution_video["height"]}
                    video_res.append(_video_res)

    # Розділити відео на кортежі відносно розмірів
    video_tuples = {}
    for video_info in video_res:
        width, height = video_info["width"], video_info["height"]
        video_tuples.setdefault((width, height), []).append(video_info)

    return video_tuples


def main():
    api_key = 'Aj3Eh7hGRp2q8lwI8W5rwvsTZ3mHVGTDG0oZDCsbtBzYqyZJ6cYE3LeC'
    query = 'city above'
    s = search_for_stock_videos(query=query, api_key=api_key, it=1000, time_minimum=30)
    print(s)
    for size, videos in s.items():
        print(f"Size: {size}, Videos: {len(videos)}")


if __name__ == '__main__':
    main()

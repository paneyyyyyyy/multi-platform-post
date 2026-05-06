from uploader import fetch_taobao_info_with_cookie_file

if __name__ == "__main__":
    url = "https://item.taobao.com/item.htm?id=701936194064"
    result = fetch_taobao_info_with_cookie_file(url)
    print(result)

'''
Date: March 3, 2022
Purpose: for downloading pics from website using BeautifulSoup
Author: Jace
'''

import requests
from bs4 import BeautifulSoup
import os
import time

# imitate the browser
header = {
    ''
}

# parent file path to store pictures
path_name = ""

print("*********** This is web content downloading program **********")
print("*********** Downdloading website content from www.example.com ************")

# download with multiple pages, input page numbers
for page in range(int(input("Enter the starting page: ")), int(input("Enter the ending page: "))):
    # get parent url
    par_url = "page url{}/".format(str(page))
    # get parent url
    par_source = requests.get(par_url, headers=header)
    par_source.encoding = "utf-8"
    # find out content tag which is including a tag of each images page
    soup = BeautifulSoup(par_source.text, "html.parser")
    # get the link of image content
    content_link = soup.find("div", class_="posts-wrapper")
    # get all image a link
    image_link = content_link.find_all("div", class_="nv-post-thumbnail-wrap")
    # get all images links
    print("Downloading from page: {}\n url: {}".format(page, par_url)) # display which page we are
    each_image_url_count = len(image_link) # count how many image contents in a page
    print("Total image pages are: {}".format(each_image_url_count))
    for link in image_link:
        # print(link.a)
        imgs_links = link.a
        # print(imgs_links["href"])
        each_page = requests.get(imgs_links["href"], headers=header)
        # using beautifulsoup decoding the url
        soup = BeautifulSoup(each_page.text, "html.parser")
        content_fig = soup.find("figure", class_="wp-block-gallery has-nested-images columns-1") # find figure class
        imges = content_fig.find_all("img") # find images inside figure class
        alter_images = content_fig.find("ul", class_="blocks-gallery-grid")

        # file name/ create file name according to it's heading
        dir_name = soup.find_all("h1", class_="title entry-title")
        for h in dir_name:
            d_name = h.text
            path = os.path.join(path_name, d_name)
            if not os.path.exists(path):
                os.mkdir(path)
            os.chdir(path_name)

        # count content down
        each_image_url_count -= 1
        print("{} image pages are left".format(each_image_url_count))
        # # download images
        downloading_count = len(imges)
        # final target folder
        target_path = path + "/"
        folder_size = os.path.getsize(path)  # returnthe empty folder size which is less than 96
        if folder_size <= 96:  # check whether the file is empty or not
            print("Total images are: {}".format(downloading_count))
            print("Downloading file from page:{}\nTitle: {}\nSource: {}".format(page, d_name, imgs_links["href"]))
            for img in imges:
                time.sleep(1)
                if "webp" in img["src"]:
                    img_src = requests.get(img["src"]).content
                    img_name = img["data-id"]
                    with open(target_path + img_name + ".webp", "wb") as f: # if the folder is is empty then write file
                        f.write(img_src)
                        f.close()
                        downloading_count -= 1
                        print("Now is downloading: {} and {} pictures are left".format(img_name, downloading_count))
            print("Download finished!")
        else:
            print("Requesting file from: {} {} {}".format(d_name, str(page), imgs_links["href"]))
            print("File already existed!")
            continue
print("{} pages are downloaded".format(page))
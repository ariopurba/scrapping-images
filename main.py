# %%
from selenium import webdriver
from selenium.webdriver.common.by import By
import requests
import io
from PIL import Image
import time

# %%
PATH = "C:\\Users\\ariop\\OneDrive - Universitas Sanata Dharma\\Bangkit\\capstone\\KANAPA\\chromedriver.exe"
wd = webdriver.Chrome(PATH)


# %% [markdown]
# ### Satu File Pertama

# %%
img_url = "https://thumb.viva.co.id/media/frontend/thumbs3/2020/10/26/5f966ab70b23a-ikan-laohan-merah-ini-dibeli-seharga-rp-350-juta_1265_711.jpg"


def download_image(download_path, url, file_name):
	try:
		image_content = requests.get(url).content
		image_file = io.BytesIO(image_content)
		image = Image.open(image_file)
		file_path = download_path + file_name

		with open(file_path, "wb") as f:
			image.save(f, "JPEG")

		print("Success")
	except Exception as e:
		print('FAILED -', e)

# %%
# download_image("", img_url, "ikan.jpg")

# %% [markdown]
# ### All Image from google

# %%
def get_images_from_google(wd, delay, max_images):
    def scroll_down(wd):
        wd.execute_script("window.scrollTo(0, document.body.scrollHeight);")
        time.sleep(delay)
        
    url = "https://www.google.com/search?q=fish+neon+tetra&tbm=isch&ved=2ahUKEwjOwOfv4Zz_AhWUi9gFHX9_DFoQ2-cCegQIABAA&oq=fish+neon+tetra&gs_lcp=CgNpbWcQAzIFCAAQgAQyBggAEAcQHjIGCAAQBxAeMgYIABAHEB4yBggAEAcQHjIICAAQBRAHEB4yCAgAEAUQBxAeMggIABAFEAcQHjIICAAQBRAHEB4yBggAEAUQHjoECCMQJzoGCAAQCBAeUJMIWJMIYI4PaABwAHgAgAGWAogB1gOSAQUwLjEuMZgBAKABAaoBC2d3cy13aXotaW1nwAEB&sclient=img&ei=n8Z1ZI71CJSX4t4P__6x0AU&bih=811&biw=1660&rlz=1C1ONGR_enID1029ID1029&hl=en#imgrc=xpwZDPVzeotRaM"
    wd.get(url)
    
    image_urls = set()
    skips = 0       
    
    while len(image_urls) + skips < max_images:
        scroll_down(wd)
        
        thumbnails = wd.find_elements(By.CLASS_NAME, "Q4LuWd")
        
        for img in thumbnails[len(image_urls) + skips:max_images]:
            try:
                img.click()
                time.sleep(delay)
            except:
                continue
            
            images = wd.find_elements(By.CLASS_NAME, "iPVvYb")
            
            for image in images:
                if image.get_attribute('src') in image_urls:
                    max_images += 1
                    skips += 1
                    break
                
                if image.get_attribute('src') and 'http' in image.get_attribute('src'):
                    image_urls.add(image.get_attribute('src'))
                    print(f"found {len(image_urls)} ")
                
    return image_urls

        

# %%
urls = get_images_from_google(wd, 1, 50)
for i, url in enumerate(urls):
	download_image("./dataset/NeonTetra/", url, str(i) + ".jpg")

wd.quit()	

# %%




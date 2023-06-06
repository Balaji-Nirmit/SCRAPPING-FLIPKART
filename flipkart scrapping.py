from bs4 import BeautifulSoup as soup
from urllib.request import urlopen
import csv

search_query="red tshirts with check".replace(" ","+")
flipkart_url=f"https://www.flipkart.com/search?q={search_query}&page=1"
flipkart_http_obj=urlopen(flipkart_url)
flipkart_webdata_total=flipkart_http_obj.read()

flipkart_datafile=open(f"{search_query}.csv","w",newline="")
flipkart_writer=csv.writer(flipkart_datafile)
flipkart_writer.writerow(['Title','new_price','old_price','stars','ratings','off','image_link','product_link'])

def flipkart_details_function(flipkart_product_url):
  flipkart_http_obj_main=urlopen(flipkart_product_url)
  flipkart_webdata_total_main=flipkart_http_obj_main.read()
  flipkart_soupdata_main=soup(flipkart_webdata_total_main,'html.parser')
  # getting title
  title=flipkart_soupdata_main.find('span',{'class':'B_NuCI'})
  title=title.text
  # getting new price
  try:
    new_price=flipkart_soupdata_main.find('div',{'class':'_30jeq3'})
    new_price=new_price.text
  except:
    new_price=None
  # getting old price
  try:
    old_price=flipkart_soupdata_main.find('div',{'class':'_3I9_wc'})
    old_price=old_price.text
  except:
    old_price=None
  # getting off 
  try:
    off=flipkart_soupdata_main.find('div',{'class':'_3Ay6Sb'})
    off=off.text
  except:
    off=None
  # getting stars
  try:
    stars=flipkart_soupdata_main.find('div',{'class':'_3LWZlK'})
    stars=stars.text
  except:
    stars=None
  # getting rating and reviews
  try:
    ratings=flipkart_soupdata_main.find('span',{'class':'_2_R_DZ'})
    ratings=ratings.text
  except:
    ratings=None

  # details
  details_main=[title,new_price,old_price,stars,ratings,off]
  return details_main


# try:
#   for pagenumber in range(2,50):
#     flipkart_url=f"https://www.flipkart.com/search?q={search_query}&page={pagenumber}"
#     flipkart_http_obj=urlopen(flipkart_url)
#     flipkart_webdata=flipkart_http_obj.read()
#     flipkart_webdata_total+=flipkart_webdata
# except:
#   pass
flipkart_soupdata=soup(flipkart_webdata_total,'html.parser')
flipkart_containers=flipkart_soupdata.findAll('div',{'class':'_13oc-S'})
for container in flipkart_containers:
  try:
    flipkart_productlink_data=container.findAll('div',{'class':'_4ddWXP'})
    for i in range(4):
      flipkart_productlink=flipkart_productlink_data[i]
      flipkart_productlink=flipkart_productlink.find('a')['href']
      flipkart_productlink="https://www.flipkart.com"+str(flipkart_productlink)
      try:
        flipkart_image=flipkart_productlink_data[i].find('img')
        flipkart_image=flipkart_image.get('src')
      except:
        flipkart_image=None
      details=flipkart_details_function(flipkart_productlink)
      details.extend([flipkart_image,flipkart_productlink])
      flipkart_writer.writerow(details)
  except:
    try:
      flipkart_productlink_data=container.findAll('div',{'class':'_1xHGtK'})
      for i in range(4):
        flipkart_productlink=flipkart_productlink_data[i]
        flipkart_productlink=flipkart_productlink.find('a')['href']
        flipkart_productlink="https://www.flipkart.com"+str(flipkart_productlink)
        try:
          flipkart_image=flipkart_productlink_data[i].find('img')
          flipkart_image=flipkart_image.get('src')
        except:
          flipkart_image=None
        details=flipkart_details_function(flipkart_productlink)
        details.extend([flipkart_image,flipkart_productlink])
        flipkart_writer.writerow(details)
    except:
        # for 1 row datas like laptops
        flipkart_productlink=container.find('a')['href']
        flipkart_productlink="https://www.flipkart.com"+str(flipkart_productlink)
        try:
          flipkart_image=container.find('img')
          flipkart_image=flipkart_image.get('src')
        except:
          flipkart_image=None
        details=flipkart_details_function(flipkart_productlink)
        details.extend([flipkart_image,flipkart_productlink])
        flipkart_writer.writerow(details)

flipkart_datafile.close()
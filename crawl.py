from bs4 import BeautifulSoup
import requests
import csv
import re
import time
import urllib2

origin_url = 'https://www.booking.com/searchresults.en-gb.html?aid=303948&label=amsterdam-eIvTGYamfLPgBB*zdVZg*QS249036945240%3Apl%3Ata%3Ap11340%3Ap2%3Aac%3Aap1t3%3Aneg%3Afi%3Atikwd-15722330%3Alp9065248%3Ali%3Adec%3Adm&sid=7371de572bb3d285f8e0ca779f5f0f66&checkin_month=8&checkin_monthday=26&checkin_year=2018&checkout_month=8&checkout_monthday=27&checkout_year=2018&city=-2140479&class_interval=1&dest_id=-2140479&dest_type=city&from_sf=1&group_adults=2&group_children=0&label_click=undef&nflt=pri%3D3%3Bclass%3D5%3Bdi%3D145%3B&no_rooms=1&raw_dest_type=city&room1=A%2CA&sb_price_type=total&src=city&ssb=empty&ssne_untouched=Amsterdam&rows={search_num}'
#origin_url = 'https://www.booking.com/searchresults.en-gb.html?aid=304142&label=gen173nr-1DCAEoggJCAlhYSDNYBGipAYgBAZgBLsIBCndpbmRvd3MgMTDIAQzYAQPoAQGSAgF5qAID&sid=7371de572bb3d285f8e0ca779f5f0f66&checkin_month=9&checkin_monthday=21&checkin_year=2018&checkout_month=9&checkout_monthday=22&checkout_year=2018&class_interval=1&dest_id=-2140479&dest_type=city&from_sf=1&group_adults=2&group_children=0&label_click=undef&lsf=pri%7C4%7C107&nflt=pri%3D4%3Bdi%3D145%3B&no_rooms=1&raw_dest_type=city&room1=A%2CA&sb_price_type=total&src=index&ss=Amsterdam&ssb=empty&ssne=Amsterdam&ssne_untouched=Amsterdam&rows=20'
user_agent = 'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/41.0.2272.101 Safari/537.36'
search_num=20

# search_suffix
suffix = '&offset={offset}'
offset = 0

# header variable
headers = { 'User-Agent' : user_agent }


# finished pages
avai_num_hotels = 0
csv_file = open("rent.csv","w") 
csv_writer = csv.writer(csv_file, delimiter=',')#,escapechar=' ',quoting=csv.QUOTE_NONE)

# debug pages
save1_file = open("save.html","w") 

offset = 0

while True:
    if (offset == 0):
        url=origin_url.format(search_num = search_num)
        print("fetch: ", url)
    else:
        url = origin_url.format(search_num = search_num) + suffix.format(offset=offset)
        print("fetch: ", url)
	
    # creating request
    req = urllib2.Request(url, None, headers)
	
    
    # getting html
    html = urllib2.urlopen(req).read()	
    save1_file.write(html)
    response = requests.get(url) 
    html = BeautifulSoup(response.text,"html.parser")
    offset += search_num
    #print html
    #break
    
    house_list_wrapper = html.find("div",{"id" : "hotellist_inner"})
    house_list = html.findAll("h3", {"class" : "sr-hotel__title"})

    #print(house_list)
    print('\n')
    if len(house_list) == 0:
        break
    
    name_list=[]
    address_list=[]
    #extract the info of the hotel
    for house in house_list:
        house_title = house.find_all("span",{"class" : "sr-hotel__name"})[0].contents[0].encode('utf-8')
        name_list.append(house_title)
        #print(house_title)
		
    house_address_list = html.find_all("div",{"class" : "address"})
    for address in house_address_list:
        house_address = address.find_all("a")[0]['data-coords'].encode('utf-8')
        address_list.append(house_address)
        #print(house_address)
		
    for i in range(0,len(name_list)):
        print(name_list[i]+" , "+address_list[i])
        csv_writer.writerow([name_list[i], address_list[i]])
    
csv_file.close()

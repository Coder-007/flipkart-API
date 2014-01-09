import urllib
import requests
import BeautifulSoup

def get_act_url(book_name):
	#returns the most relevant url for the query
    list_url=[]
    url = 'http://www.flipkart.com/books/pr?sid=bks&q='+urllib.quote_plus(book_name)+'&filter=language%3AEnglish'
    r = requests.get(url)
    html = r.text
    soup = BeautifulSoup.BeautifulSoup(html)
    for link in soup.findAll('a',attrs= {'class':'lu-image-link '}):
		list_url.append(link)   
    act_url ='http://www.flipkart.com'+list_url[0]['href']    # most relevant result
    return act_url

def get_details(act_url):
	#outputs various details for the book name queried
    r = requests.get(act_url)
    html = r.text
    soup = BeautifulSoup.BeautifulSoup(html)
    print 'Title:',get_title(soup)
    names_list=[]
    names_list = get_author(soup)  
    if len(names_list)>1:
		print'Authors:',[name.encode('utf-8') for name in names_list]
    else: 
        print 'Author:',names_list[0]
    print 'Price:',get_price(soup),del_price(soup)
    get_info(soup)
    print 'Image Link:',get_image(soup)

def get_price(soup):
	#give price for the book
    price = soup.find('meta',attrs= {'itemprop':'price'})
    curr = soup.find('meta',attrs= {'itemprop':'priceCurrency'})
    return price['content']+" "+curr['content']    
        

def get_title(soup):
	#returns Title of book
    title = soup.h1
    return title.string.strip()

def get_image(soup):
    image_link = soup.find('img',attrs={'onload':'img_onload(this);'})
    try:
        return image_link['src']
    except TypeError:
		return "wasn't able to find image link"

def get_author(soup):
	#author's name
    names=[]
    for name in soup.find('td',attrs={'class':'specs-value fk-data'}):
        if name.string.strip()==',':
            None        
        else:
            names.append(name.string)
    return names

def del_price(soup):
	#give delivery price of book
    price = soup.find('div',attrs={'class':'listing_shipping_charge'})
    if price.string != None: 
        return price.string
    else:
        return "+ delivery charges not known"

def get_info(soup):
	#outputs various other details:publishers,ISBN etc..
    index=[]
    values=[]
    for detail in soup.findAll('td',attrs={'class':'specs-key'}):
        index.append(detail.string)
    for detail in soup.findAll('td',attrs={'class':'specs-value fk-data'}):
        values.append(detail.string)
    for i in range(1,len(index)):
		print index[i],':',values[i]
       
if __name__ == '__main__':
	book = str(raw_input('Book Name:'))
	print '####### FLIPKART BOOK SEARCH RESULT #######'
	link = get_act_url(book)
	get_details(link)

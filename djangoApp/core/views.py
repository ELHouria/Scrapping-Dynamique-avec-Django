from django.shortcuts import render
from django.http import HttpResponse
from bs4 import BeautifulSoup
import requests
# Create your views here.

# go to preject path , run venv\Scripts\activate then go to app path and runserver 





def get_html_content(keyword):
    
           USER_AGENT = "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/44.0.2403.157 Safari/537.36"
           LANGUAGE = "en-US,en;q=0.5"
           session = requests.Session()
           session.headers['User-Agent'] = USER_AGENT
           session.headers['Accept-Language'] = LANGUAGE
           session.headers['Content-Language'] = LANGUAGE
           html_content=session.get(f'https://www.jumia.ma/catalog/?q={keyword}').text
           html_content2=session.get(f'https://www.amazon.com/s?k={keyword}').text
           return html_content,html_content2
    
    
    
#     

# xpath of search bar //*[@id="fi-q"]
def home(request):
    
    
    product_data=None
    product_data2=None
    data=None
    data2=None
    search=''
    length=0
    context=None
    
    
    if 'search' in request.GET:
        # fetch the data
        # we pretend that we are a browser , so that google does not block us
        search=request.GET.get("search")
        
        html_content,html_content2=get_html_content(search)

        # start scraping data 
        product_data={'prod_images':[] ,'prod_prices':[] , 'prod_names':[]}
        product_data2={'prod_images2':[] ,'prod_prices2':[] , 'prod_names2':[]}
        soup = BeautifulSoup(html_content, 'html.parser')
        soup2 = BeautifulSoup(html_content2 , 'html.parser')
        
        #jumia
        products_name=soup.find_all("h3",{'class':'name'})
        products_price=soup.find_all("div",{'class':'prc'})
        products_image=soup.find_all("img",{'class':'img'})
        
        #Amazon
        products_name2=soup2.find_all("span",{'class':'a-size-medium a-color-base a-text-normal'})
        products_price2=soup2.find_all("span",{'class':'a-price-whole'}) # must be converted to dhs
        products_image2=soup2.find_all("img",{'class':'s-image'})
      
      
         #Jumia
        comp=1 
        for prod in products_image:
                product_data['prod_images'].append(prod['data-src'])
                comp+=1
                if(comp==10):
                         break 
        comp=1         
        for prod in products_price:
                
                
                product_data['prod_prices'].append(prod.text)
                comp+=1
                if(comp==10):
                         break 
        comp=1      
        for prod in products_name:
               
               product_data['prod_names'].append(prod.text) 
               comp+=1
               if(comp==10):
                       break 
               
               
        #Amazon
        
        # We need to get only 16 first prod
        comp=1
        for prod in products_image2:
                product_data2['prod_images2'].append(prod['src'])
                comp+=1
                if(comp==10):
                           break 
                
        comp=1 
        for prod in products_price2:
          
                product_data2['prod_prices2'].append(prod.text)
                comp+=1
                if(comp==10):
                         break 
        comp=1
        for prod in products_name2:
         
                product_data2['prod_names2'].append(prod.text) 
                comp+=1
                if(comp==10):
                        break        
               
               
        if(len( product_data['prod_names'])==1):
                 var= product_data2['prod_names2'][0]
                 product_data2['prod_names2']=[]
                 product_data2['prod_names2'].append(var)
                #  product_data2['prod_prices2']= product_data2['prod_prices2'][0]
                #  product_data2['prod_images2']= product_data2['prod_images2'][0]
                #  print(product_data2['prod_names2'])
        for i in range(len(product_data2['prod_prices2']))  :
                prc= product_data2['prod_prices2'][i].replace(".",'')
                prc= prc.replace(",",'')
                prc=round(int(prc)*10.55,2)
                prc= str(prc)+' Dhs'
                product_data2['prod_prices2'][i]=prc
          
          
                   
        data = list(zip(product_data['prod_prices'],  product_data['prod_names'], product_data['prod_images']))
        data2 = list(zip(product_data2['prod_prices2'],  product_data2['prod_names2'], product_data2['prod_images2']))
        length=len(list(data)) 
        length2=len(list(data2)) 

        context={'data':data,'data2':data2, 'query':search , 'length': length ,'length2': length2 ,}
        
        # print(str(length)+"***"+str(length2))
        
            
    return render(request , 'core/home.html' , context)
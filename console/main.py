import requests
import bs4
import json
import demjson
import urllib
import os
import pathlib


def isfloat(value):
  try:
    float(value)
    return True
  except ValueError:
    return False

try:
    path = str(pathlib.Path(__file__).resolve().parent)
except:
    import sys
    path = str(pathlib.Path(sys.argv[0]).resolve().parent)


link = input("Series link: ")


while 'animefox.io/anime/' not in link:
    print('Invalid link, link should look like this:' )
    print('https://animefox.io/anime/name-of-anime')
    link = input("Series link: ")

name = link.split('/')[-1]

while isfloat(name):
    print('Link is probably a link to an episode')
    choice  = input('Do you want to change the link (y) or continue with this one (n): ')
    while choice != 'y' and choice != 'n':
        print('Please choose "y" or "n" and not ' + str(choice))
        choice  = input('Do you want to change the link (y) or continue with this one (n): ')
        print()
    if choice == 'n':
        print('Ok, contineing')
        break
    if choice == 'y':
        link = input("Series link: ")
        name = link.split('/')[-2]
        break


print('Download episodes: ')
start = input('From: ')
end = input('To: ')


while isfloat(start) == False or isfloat(end) == False:
    print('Both choices must be numbers')
    print('Download episodes: ')
    start = input('From: ')
    end = input('To: ')

start = int(start)
end = int(end)

while start>end:
    print('First episode number has to be less or equal to the second one')
    print('Download episodes: ')
    start = input('From: ')
    end = input('To: ')

name = link.split('/')[-1]


video_link = 'https://embed.animefox.io/player/' + name + '/'

n = start
print('Starting download process...')

for i in range(start, end + 1):

    download_link = video_link + str(i)
    response = requests.get(download_link)
    soup = bs4.BeautifulSoup(response.text, features="html.parser")
    links = str(soup.find("script", {"type": "text/javascript"}))
    
    while links.startswith('playlist') == False:
        links = links[1:]    
    links = links[10:]  

    while links.endswith(']') == False:
        links = links[:-1]
    
    json_dumps = json.dumps(links)
    
    json_loads = json.loads(json_dumps)
    
    list = json_loads.strip('][').split(', ')
    
    dict = demjson.decode(list[0])


    for i in dict['sources']:
        if i['label'] == "High Speed":
                final_link = i['file']
                

    if os.path.isdir(path + '/output/' + name) == False:
        os.mkdir(path + '/output/' + name)


    print('Downloading ' + name + '_' + str(n) + '.mp4...')
    urllib.request.urlretrieve(str(final_link), path + '/output/' + name + '/' + name + '_' + str(n) + '.mp4')
    print('Done downloading ' + name + '_' + str(n) + '.mp4')
    
    n += 1


print('Done! Press enter to exit')
input()
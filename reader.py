from bs4 import BeautifulSoup
from bs4.element import Comment
import requests


menu = {}
command = 'm'

def tag_visible(element):
    if element.parent.name in ['style', 'script', 'head', 'title', 'meta', '[document]']:
        return False
    if isinstance(element, Comment):
        return False
    return True

def text_from_html(body):
    soup = BeautifulSoup(body, 'html.parser')
    texts = soup.findAll(text=True)
    visible_texts = filter(tag_visible, texts)
    return u" ".join(t.strip()+'\n\n' for t in visible_texts)

def show_menu():
    r = requests.get("http://lite.cnn.com")

    b = r.text

    soup = BeautifulSoup(b, 'html.parser')

    links = soup.find_all('a')
    
    c = 1
    for link in links:
        menu[c] = link.attrs['href']
        print("{0}: {1}".format(c, link.text))
        c += 1


def load_item(item):
    print("This is article :", item)
    item = int(item)
    r = requests.get("http://lite.cnn.com{0}".format(menu[item]))
    html = r.text.replace("</p>", "\n\n</p>")
    print(text_from_html(html))
    print('-' * 80)
    command = input("(m)enu, (p)rev, (n)ext, number, or exit: ")
    return command


last_item = 0
while command != 'exit':
    if command.lower() == 'm':
        show_menu()
        command = input("Article: ")
    elif command.lower() == 'n':
        command = str(last_item + 1)
    elif command.lower() == 'p':
        command = str(last_item - 1)
    else:
        try:
            option = int(command)
        except:
            break
        last_item = option
        command = load_item(command)

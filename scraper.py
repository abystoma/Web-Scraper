import requests
from bs4 import BeautifulSoup

def retrieve_json(soup: str) -> str:
    json = {}
    title = soup.find('title')
    description = soup.find('meta',attrs={'name':"description"})['content'] #tag, attribute
    json = {"title":title.text, "description":description}
    return json

def main() -> None:
    website = input("Input the URL:")
    r = requests.get(website)
    if r.status_code == 200:
        soup = BeautifulSoup(r.content, 'html.parser')
        check_movie = soup.find('meta', {'property': 'og:type'})
        if check_movie['content']=='image':
            print(retrieve_json(soup))
        else:
            print("Invalid movie page!")
    else:
        print("Invalid movie page!")

main()



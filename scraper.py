import requests

def retrieve_json(link: str) -> str:
    response = link.json()
    try:
        quote = response["content"]
        #dict.get(response, "content")
    except KeyError:
        return "Invalid quote resource!"
    return quote

def main() -> None:
    website = input("Input the URL:")
    r = requests.get(website)
    if r.status_code == 200:
        print(retrieve_json(r))
    else:
        print("Invalid quote resource!")

main()
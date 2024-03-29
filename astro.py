import requests
from bs4 import BeautifulSoup
from time import sleep
import json


def has_tailwind(getStartedLink: str):
    urls = None
    if getStartedLink != "N/A" and "github.com" in getStartedLink:
        url = (
            "https://raw.githubusercontent.com/"
            + getStartedLink.split("github.com/")[-1]
            + "/main/package.json"
        )
        url2 = (
            "https://raw.githubusercontent.com/"
            + getStartedLink.split("github.com/")[-1]
            + "/master/package.json"
        )
        urls = [url, url2]

    if urls is None:
        return False
    # Fetching the contents of package.json
    for url in urls:
        response = requests.get(url)
        if response.status_code == 200:
            package_json = response.json()
            # Check if "tailwindcss" is present in dependencies or devDependencies
            dependencies = package_json.get("dependencies", {})
            dev_dependencies = package_json.get("devDependencies", {})

            if "tailwindcss" in dependencies or "tailwindcss" in dev_dependencies:
                return True
    #     else:
    #         print("tailwindcss is not present in package.json")
    # else:
    #     print("Failed to fetch package.json:", response.status_code)
    return False


def astro_scraper():
    # The base URL for the themes
    base_url = "https://astro.build/themes/"
    hdr = {
        "User-Agent": "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.11 (KHTML, like Gecko) Chrome/23.0.1271.64 Safari/537.11",
        "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8",
        "Accept-Charset": "ISO-8859-1,utf-8;q=0.7,*;q=0.3",
        "Accept-Encoding": "none",
        "Accept-Language": "en-US,en;q=0.8",
        "Connection": "keep-alive",
    }

    r = requests.get(base_url, headers=hdr)
    soup = BeautifulSoup(r.content, "html.parser", from_encoding="iso-8859-1")

    # The number of pages to scrape
    num_pages = str(soup.find("li", class_="sm:hidden").get_text())
    num_pages = str(num_pages).split("of")
    num_pages = int(num_pages[-1])

    # Create a list to store the scraped data
    qlist = []

    # Loop through each page
    for page_num in range(num_pages):
        # Construct the URL for the current page
        url = base_url + str(page_num + 1)
        hdr = {
            "User-Agent": "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.11 (KHTML, like Gecko) Chrome/23.0.1271.64 Safari/537.11",
            "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8",
            "Accept-Charset": "ISO-8859-1,utf-8;q=0.7,*;q=0.3",
            "Accept-Encoding": "none",
            "Accept-Language": "en-US,en;q=0.8",
            "Connection": "keep-alive",
        }

        r = requests.get(url, headers=hdr)
        soup = BeautifulSoup(r.content, "html.parser", from_encoding="iso-8859-1")
        print(url)

        for i in soup.findAll("article"):

            try:
                name = i.find("h3", class_="heading-5 mb-2 text-white")
                name = name.get_text()
                name = str(name)
                name = name.replace("\t", "")
                name = name.replace("\n", "")
                # print(name)

            except:
                name = "N/A"

            try:
                description = i.find("p", class_="line-clamp-3")
                description = description.get_text()
                # print(description)

            except:
                description = "N/A"

            try:
                link = i.find("a", class_="flex h-full flex-col")
                link = link["href"]
                link = "https://astro.build" + str(link)
                # print(link)

            except:
                link = "N/A"

            try:
                imagen = i.find("img", class_="aspect-video w-full object-cover")
                imagen = imagen["src"]
                # imagen = "https://astro.build/" + imagen
                # print(imagen)

            except:
                imagen = "N/A"

            try:
                is_free = i.find(
                    "p",
                    class_="code relative m-px rounded-md px-2 py-1 text-sm text-white secondary z-10",
                )
                if is_free == None or "paid" in is_free.get_text().lower():
                    is_free = "false"
                    # print(is_free)
                else:
                    is_free = "true"
                    # print(is_free)

            except:
                is_free = "false"
                # print(is_free)

            if is_free == "true":
                # Construct the URL for the secundary page
                new_url = link
                new_r = requests.get(new_url, headers=hdr)
                new_soup = BeautifulSoup(
                    new_r.content, "html.parser", from_encoding="iso-8859-1"
                )
                j = new_soup.find(
                    "aside",
                    class_="hidden w-full divide-y divide-astro-gray-500 border-astro-gray-500 md:block md:max-w-md md:border-l",
                )

                try:
                    getStartedLink = j.find("a", class_="button-primary")
                    getStartedLink = getStartedLink["href"]
                    # print(getStartedLink)

                except:
                    getStartedLink = "N/A"

                try:
                    liveDemoLink = j.find("a", class_="button-outline")
                    liveDemoLink = liveDemoLink["href"]
                    # print(liveDemoLink)

                except:
                    liveDemoLink = "N/A"
            else:
                liveDemoLink = "N/A"
                getStartedLink = "N/A"

                # Construct the dictionary.

            item = {
                "name": name,
                "description": description,
                "link": link,
                "image": imagen,
                "free": is_free,
                "getStartedLink": getStartedLink,
                "liveDemoLink": liveDemoLink,
                "deployToVercel": f"https://vercel.com/new/clone?repository-url={getStartedLink}",
            }
            if has_tailwind(getStartedLink):
                qlist.append(item)

    return qlist


result = json.dumps(astro_scraper())
with open("public/result.json", "w") as f:
    f.write(result)

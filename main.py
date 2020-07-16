from bs4 import BeautifulSoup
from requests import get

LIMIT = 10

def search(url: str):
    queue = []
    edges = set()
    discovered = { url }
    queue.append(url) # enqueue
    soup = BeautifulSoup(get(url).text, "html.parser")
    while queue != []:
        try:
            u = queue.pop(0)
            v = BeautifulSoup(get(u).text, "html.parser") # dequeue
        except:
            return edges
        if len(edges) > 10000:
            return edges
        for link in v.findAll('a'):
            if "href" in link.attrs and link["href"] not in discovered:
                href = None     # Now I'm grateful for Haskell
                if any(map(link["href"].startswith, ["http://", "https://", "www."])):
                    href = link["href"]
                elif link["href"].startswith('/') and not link["href"].startswith("//"):
                    href = u + link["href"]
                else:
                    continue
                discovered.add(href)
                queue.append(href)
                edges.add((u, href))
    return edges


def main():
    for src, dest in search("https://gnu.org"):
        print(f"{src}: {dest}")



if __name__ == "__main__":
    main()

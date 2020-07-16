from bs4 import BeautifulSoup
from requests import get
from sys import argv

LIMIT = 1000

def search(url: str) -> set:
    queue = []
    edges = set()
    discovered = { url }
    queue.append(url) # enqueue
    while queue != []:
        try:
            u = queue.pop(0)
            v = BeautifulSoup(get(u).text, "html.parser") # dequeue
        except:
            return edges
        if len(edges) > LIMIT:
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

def dfs_search(url: str) -> set:
    stack = []
    edges = set()
    discovered = { url }
    stack.append(url) # Push
    while stack != []:
        try:
            u = stack.pop()
            v = BeautifulSoup(get(u).text, "html.parser")
        except:
            return edges
        if v not in discovered:
            discovered.add(v)
            for link in v.findAll('a'):
                if "href" in link.attrs and link["href"] not in discovered:
                    href = None
                    if any(map(link["href"].startswith, ["http://", "https://", "www."])):
                        href = link["href"]
                    elif link["href"].startswith('/') and not link["href"].startswith("//"):
                        href = u + link["href"]
                    else:
                        continue
                    discovered.add(href)
                    stack.append(href)
                    edges.add((u, href))

def clean_url(url: str):
    url = url.replace("http://", "").replace("https://", "")
    return '...' + '/'.join(url.split('/')[-2:])

def main():
    print("strict digraph {")
    print("\toverlap = false;")
    print("\tsplines = true;")
    for src, dest in dfs_search(argv[1]):
        print(
            '\t"{}" -> "{}";'.format(
                clean_url(src),
                clean_url(dest)
            )
        )
              
    print("}")


if __name__ == "__main__":
    main()

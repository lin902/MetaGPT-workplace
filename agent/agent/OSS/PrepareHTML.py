from bs4 import BeautifulSoup

with open("github-trending-raw.html") as f:
    html = f.read()

soup = BeautifulSoup(html, "html.parser")
for i in soup.find_all(True):
    for name in list(i.attrs):
        if i[name] and name not in ["class"]:
            del i[name]

for i in soup.find_all(["svg", "img", "video", "audio"]):
    i.decompose()

with open("github-trending-slim.html", "w") as f:
    f.write(str(soup))
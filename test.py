from bs4 import BeautifulSoup
from os import path

management_path = "cbonte.github.io/haproxy-dconv/1.7/configuration.html"

with open(path.join("versions", "1.7.9", management_path)) as f:
  bs = BeautifulSoup(f, "lxml")
  for s in bs.select("h2"):
    if s.get("data-target"):
      title = s.findAll(text=True)[1].strip()
      href = s.select("a")[0].get("href")
      print(title, href)

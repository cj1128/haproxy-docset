#!/usr/bin/env python3
import sys
import fileinput
import sqlite3
from bs4 import BeautifulSoup, NavigableString, Tag
from os import system
from os import path

index_mapping = {
  "1.7.6": "cbonte.github.io/haproxy-dconv/1.7/configuration.html"
}

if len(sys.argv) == 1:
  print("usage: python build.py [version]")
  exit(1)

version = sys.argv[1]

if not version in index_mapping:
  print("no such version, available versions are:", ", ".join(index_mapping.keys()))
  exit(1)

target_docset = f"dist/haproxy-{version}.docset"

system(f"rm -rf {target_docset}")
system(f"cp -r tmpl {target_docset}")

# change version number
index_path = index_mapping[version]
for line in fileinput.input(path.join(target_docset, "Contents", "info.plist"), inplace=True):
  if "__INDEX__" in line:
    print(line.replace("__INDEX__", index_path))
  else:
    print(line)

# copy html to docset
system(f"cp -r versions/{version}/* {target_docset}/Contents/Resources/Documents/")

# generate index
db = sqlite3.connect(path.join(target_docset, "Contents", "Resources", "docSet.dsidx"))
cur = db.cursor()
cur.execute("drop table if exists searchIndex")

cur.execute("create table searchIndex(id interger primary key, name text, type text, path text)")
cur.execute("create unique index anchor on searchIndex (name, type, path)")

CATEGORY = "Category"
SECTION = "Section"
DIRECTIVE = "Directive"

def expand_link(link):
  return path.join(path.dirname(index_path), link)

with open(path.join(target_docset, "Contents", "Resources", "Documents", index_path)) as f:
  bs = BeautifulSoup(f, "lxml")

  # category
  for h in bs.select(".page-header"):
    if len(h.select("a.small")) > 0:
      title = h.select("h1")[0].text.strip()[2:]
      href =  h.select("a.small")[0].get("href")
      cur.execute("insert or ignore into searchIndex(name, type, path) VALUES (?,?,?)", (title, CATEGORY, expand_link(href)))

  # section
  for s in bs.select("h2"):
    if s.get("data-target"):
      title = s.text.strip()[5:]
      href = s.select("a")[0].get("href")
      cur.execute("insert or ignore into searchIndex(name, type, path) VALUES (?,?,?)", (title, SECTION, expand_link(href)))

  # directive
  for d in bs.select("div.keyword"):
    a = d.select("a[href]")[0]
    title = a.text.strip()
    href = a.get("href")
    cur.execute("insert or ignore into searchIndex(name, type, path) VALUES (?,?,?)", (title, DIRECTIVE, expand_link(href)))

db.commit()
db.close()

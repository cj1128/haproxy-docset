#!/usr/bin/env python3
import sys
import fileinput
import sqlite3
from bs4 import BeautifulSoup, NavigableString, Tag
from os import system
from os import path

version = "1.7.9"
content_dir = "cbonte.github.io/haproxy-dconv/1.7"
index_path = path.join(content_dir, "configuration.html")
management_path = path.join(content_dir, "management.html")

target_docset = f"dist/haproxy-{version}.docset"

CATEGORY = "Category"
SECTION = "Section"
DIRECTIVE = "Directive"
ENTRY = "Entry"

def init_db():
  db = sqlite3.connect(path.join(target_docset, "Contents", "Resources", "docSet.dsidx"))
  cur = db.cursor()
  cur.execute("drop table if exists searchIndex")
  cur.execute("create table searchIndex(id interger primary key, name text, type text, path text)")
  cur.execute("create unique index anchor on searchIndex (name, type, path)")
  return db

def expand_link(link):
  return path.join(content_dir, link)

def add_configuration_index(cur):
  with open(path.join(target_docset, "Contents", "Resources", "Documents", index_path)) as f:
    bs = BeautifulSoup(f, "lxml")
    # index
    cur.execute("insert or ignore into searchIndex(name, type, path) VALUES (?,?,?)", ("configuration", ENTRY, expand_link("configuration.html")))
    # category
    for h in bs.select(".page-header"):
      if len(h.select("a.small")) > 0:
        title = h.select("h1")[0].findAll(text=True)[1].strip()
        href =  h.select("a.small")[0].get("href")
        cur.execute("insert or ignore into searchIndex(name, type, path) VALUES (?,?,?)", ("configuration." + title, CATEGORY, expand_link(href)))
    # section
    for s in bs.select("h2"):
      if s.get("data-target"):
        title = s.findAll(text=True)[1].strip()
        href = s.select("a")[0].get("href")
        cur.execute("insert or ignore into searchIndex(name, type, path) VALUES (?,?,?)", ("configuration." + title, SECTION, expand_link(href)))
    # directive
    for d in bs.select("div.keyword"):
      a = d.select("a[href]")[0]
      title = a.text.strip()
      href = a.get("href")
      cur.execute("insert or ignore into searchIndex(name, type, path) VALUES (?,?,?)", ("configuration." + title, DIRECTIVE, expand_link(href)))

def add_management_index(cur):
  with open(path.join(target_docset, "Contents", "Resources", "Documents", management_path)) as f:
    bs = BeautifulSoup(f, "lxml")
    # index
    cur.execute("insert or ignore into searchIndex(name, type, path) VALUES (?,?,?)", ("management", ENTRY, expand_link("management.html")))
    # category
    for h in bs.select(".page-header"):
      if len(h.select("a.small")) > 0:
        title = h.select("h1")[0].findAll(text=True)[1].strip()
        href =  h.select("a.small")[0].get("href")
        cur.execute("insert or ignore into searchIndex(name, type, path) VALUES (?,?,?)", ("management." + title, CATEGORY, expand_link(href)))
    # directive
    for d in bs.select("div.keyword"):
      a = d.select("a[href]")[0]
      title = a.text.strip()
      href = a.get("href")
      cur.execute("insert or ignore into searchIndex(name, type, path) VALUES (?,?,?)", ("management." + title, DIRECTIVE, expand_link(href)))

def run():
  system(f"rm -rf {target_docset}")
  system(f"cp -r tmpl {target_docset}")

  # change version number
  for line in fileinput.input(path.join(target_docset, "Contents", "info.plist"), inplace=True):
    if "__INDEX__" in line:
      print(line.replace("__INDEX__", index_path))
    else:
      print(line)

  # copy html to docset
  system(f"cp -r versions/{version}/* {target_docset}/Contents/Resources/Documents/")

  # generate index
  db = init_db()
  cur = db.cursor()
  add_configuration_index(cur)
  add_management_index(cur)
  db.commit()
  db.close()

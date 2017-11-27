#!/usr/bin/env python3
import os
import sys
import importlib

if len(sys.argv) == 1:
  print("usage: python build.py [version]")
  exit(1)

version = sys.argv[1]
available_versions = os.listdir("versions")

if version not in available_versions:
  print("no such version, available versions are:", ", ".join(available_versions))
  exit(1)

__import__(version.replace(".", "_")).run()

#!/usr/bin/env python3
import os, sys, subprocess, shutil

import argparse
parser = argparse.ArgumentParser()
parser.add_argument(
  "--firefox",
  help="Override the default binary",
  type=str,
)

args = parser.parse_args()
if args.firefox:
  firefox = args.firefox
elif sys.platform == "darwin":
  firefox = "/Applications/Firefox.app/Contents/MacOS/firefox"
elif sys.platform[0:5] == "linux":
  firefox = "/usr/bin/firefox"
else:
  print("Unsupported operating system")
  sys.exit(1)

if not os.path.isdir("./profile"):
  os.mkdir("./profile");

if not os.path.isdir("./xulapp/browser"):
  os.mkdir("./xulapp/browser")
  if sys.platform == "darwin":
    jarfile = "/Applications/Firefox.app/Contents/Resources/browser/omni.ja"
  elif sys.platform[0:5] == "linux":
    jarfile = "/usr/lib64/firefox/browser/omni.ja"
  else:
    print("Unsupported operating system (browser jar)")
    sys.exit(1)

  # extract the jar file
  subprocess.call(
    [
      '/usr/bin/unzip',
      jarfile,

      '-d',
      './xulapp/browser/',
    ]
  )

  # Rewrite xulapp/browser/chrome/chrome.manifest
  manifestFile = open("xulapp/browser/chrome/chrome.manifest", "r")
  manifest = ""
  for line in manifestFile:
    if "branding" in line:
      pass
    elif "override" in line:
      pass
    else:
      manifest += line
  manifestFile.close()

  manifestFile = open("xulapp/browser/chrome/chrome.manifest", "w")
  manifestFile.write(manifest)
  manifestFile.close()

subprocess.call(
  [
    firefox,

    "--app",
    "./xulapp/application.ini",

    "-profile",
    "./profile",

    "--no-remote",
  ]
)
print("\n")

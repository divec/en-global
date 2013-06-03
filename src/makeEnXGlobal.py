#!/usr/bin/env python

import subprocess, shutil, os, re

def getHyphenatedParts(s):
    if "-" not in s: return (s,) 
    return tuple(x for x in s.split("-") if x != "")

def writeDic(name, words):
    with open(name, "w") as f:
        f.writelines((u"\n".join(words).encode("UTF-8"), "\n"))
    subprocess.check_call(["./affixcompress", name]) # make .dic and .aff
    aff = name + ".aff"
    dic = name + ".dic"
    oxtDir = "oxt-" + name
    shutil.copytree("oxt", oxtDir)
    shutil.copy(aff, os.path.join(oxtDir, "dictionaries", aff))
    shutil.copy(dic, os.path.join(oxtDir, "dictionaries", dic))

# Read source files
sets = []
used = []
for code in "au ca gb ie us za".split():
    filename = code + ".txt"
    if not os.path.exists(filename): continue
    used.append(filename)
    with open(filename) as txt:
        sets.append(set(txt.read().strip().decode('UTF-8').split("\n")))

enGlobal = set()
enGlobal.update(*sets)
writeDic("en-x-global", sorted(enGlobal))

os.chdir("oxt-en-x-global")
if os.path.exists("../ooo_global_english_dict.oxt"):
    os.unlink("../ooo_global_english_dict.oxt")
subprocess.check_call(["zip", "-r", "../ooo_global_english_dict.oxt", "META-INF/manifest.xml", "dictionaries.xcu", "license.txt", "description.xml", "dictionaries/en-x-global.aff", "dictionaries/en-x-global.dic"])
print "Used %r" % used

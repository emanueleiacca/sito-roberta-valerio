import os,re,glob
R=os.path.expanduser("~/rv-sito")
n=0
for f in glob.glob(R+"/src/pages/**/*.astro",recursive=True):
    s=open(f,encoding="utf-8").read()
    s2=re.sub(r"import content from '((?:\.\./)+)data/content\.json';",r"import { content } from '\1lib/data.js';",s)
    if s2!=s: open(f,"w",encoding="utf-8").write(s2); n+=1; print("patched",os.path.relpath(f,R))
print(n,"file")

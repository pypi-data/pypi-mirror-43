# nhentai api wrapper

search query (tag, page number)
```
>>> results = [d for d in nhentai.search("yuri", 2)]
>>> results
[doujin:264397, doujin:264394,...]
```

lookup specific doujinshi by /g/number
```
>>> d = nhentai.Doujinshi(264397)
>>> d.name
'(C95) [Gyuunyuuya-san (Gyuunyuu Nomio)]...'
>>> d.pages
22
>>> d.tags
['original',...]
>>> d[5] # (page number)
'https://i.nhentai.net/galleries/1372387/6.png'
```

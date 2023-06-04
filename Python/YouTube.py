import pytube

a = pytube.YouTube("https://youtu.be/qmbdVNuiL4E")
s = a.streams
s.get_by_itag(18).download()

#for i in s:
#	print(i)
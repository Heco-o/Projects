import base64

with open("/storage/emulated/0/Android/data/com.VS.SteelAndFlesh2/files/SB0.xml", "r") as File:
	text = File.read()

code = base64.b64decode(text).decode("utf-8")

with open("/storage/emulated/0/Documents/SB0.xml", "w") as File:
	File.write(code)
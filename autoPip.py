import subprocess
import json
import sys
from pathlib import Path

PROTECTED_FILE = Path("protected_packages.json")
protectedPackages = set()

if PROTECTED_FILE.exists():
	with PROTECTED_FILE.open("r") as file:
		protectedPackages = set(json.load(file))



def saveProtectedPackages():
	with PROTECTED_FILE.open("w") as file:
		json.dump(list(protectedPackages), file)


def getInstalledPackages():
	result = subprocess.run(["pip", "list", "--format=freeze"], capture_output=True, text=True)
	return {pkg.split("==")[0] for pkg in result.stdout.splitlines()}

def installPackage(package):
	result = subprocess.run(["pip", "install", package])
	if result.returncode == 0:
		protectedPackages.add(package)
		saveProtectedPackages()

def uninstallPackage(package):
	if package in protectedPackages:
		response = input(f"{package} -> Deleting protected package. Continue? [y/n] ").lower()
		if response.startswith("n"):
			return
	
	result = subprocess.run(["pipdeptree", "--json-tree"], capture_output=True, text=True)
	try:
		dependencyTree = eval(result.stdout)
	except Exception:
		print("Error: Unable to parse dependency tree. Ensure 'pipdeptree' is installed.")
		return
	
	reverseDependencies = {}
	for pkg in dependencyTree:
		packageName = pkg["key"]
		for dep in pkg.get("dependencies", []):
			reverseDependencies.setdefault(dep["key"], []).append(packageName)
	
	print(reverseDependencies)

while True:
	commands = input("AutoPip[>] ").lower().split()
	if commands[0] == "exit":
		exit()
	elif commands[0] == "install":
		if len(commands) >= 2:
			installPackage(commands[1])
	elif commands[0] == "uninstall":
		if len(commands) >= 2:
			uninstallPackage(commands[1])
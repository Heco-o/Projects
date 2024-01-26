import subprocess
import time

def get_clipboard_content():
	try:
		result = subprocess.check_output(["termux-clipboard-get"], universal_newlines=True)
		return result.strip()
	except subprocess.CalledProcessError:
		return None

def monitor_clipboard():
	previous_clipboard_content = get_clipboard_content()
	text = ""

	while True:
		current_clipboard_content = get_clipboard_content()

		if current_clipboard_content and current_clipboard_content != previous_clipboard_content:
			text += str(current_clipboard_content) + "\n"
			print(f"Clipboard content changed: {text}")

		previous_clipboard_content = current_clipboard_content

		# Adjust the sleep duration based on your needs

if __name__ == "__main__":
	monitor_clipboard()
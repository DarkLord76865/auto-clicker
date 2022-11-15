import os
import sys
import time
from multiprocessing import Process, freeze_support
from tkinter import *

import mouse
import psutil


def resource_path(relative_path):
	""" Get absolute path to resource, works for dev and for PyInstaller """
	try:
		# PyInstaller creates a temp folder and stores path in _MEIPASS
		base_path = sys._MEIPASS
	except AttributeError:
		base_path = os.path.abspath(".")
	return os.path.join(base_path, relative_path)

def clicker(interval):
	while psutil.Process(os.getpid()).parent() is not None:
		mouse.click(button="left")
		time.sleep(interval)

def start():
	global process_clicker
	global ent, status, root

	try:
		alive = process_clicker.is_alive()
	except (NameError, ValueError):
		alive = False

	if not alive:
		ent.config(state="disabled")
		status.config(foreground="green", activeforeground="green", text="Active")
		root.update_idletasks()
		get_txt = ent.get()
		if get_txt == "" or get_txt == ".":
			get_txt = 0
		else:
			get_txt = float(get_txt)
		process_clicker = Process(target=clicker, args=(get_txt, ))
		process_clicker.start()
	else:
		ent.config(state="normal")
		status.config(foreground="red", activeforeground="red", text="Inactive")
		process_clicker.kill()
		process_clicker.join()
		process_clicker.close()

def validate_input(full_text):
	if " " in full_text or "-" in full_text or full_text.count(".") > 1 or len(full_text) > 5:
		return False
	elif full_text == "" or full_text == ".":
		return True
	else:
		try:
			float(full_text)
			return True
		except ValueError:
			return False

def main():
	global process_clicker
	global ent, status, root

	root = Tk()
	root.title("Auto-Clicker")
	root.geometry(f"250x120+{root.winfo_screenwidth() // 2 - 125}+{root.winfo_screenheight() // 2 - 60}")
	root.resizable(False, False)
	root.configure(background="#ffffff")
	root.iconbitmap(resource_path("data/auto-clicker-icon.ico"))

	title = Label(root, background="#ffffff", activebackground="#ffffff", foreground="#000000", activeforeground="#000000", text="Auto-Clicker", font=("Helvetica", 25, "italic", "bold"))
	title.place(x=0, y=0, width=250, height=65)
	creator = Label(root, background="#ffffff", activebackground="#ffffff", text="DarkLord76865", foreground="grey90", activeforeground="#000000", font=("Helvetica", 8, "italic"))
	creator.place(x=170, y=0, width=80, height=10)
	instructions = Label(root, background="#ffffff", activebackground="#ffffff", text="Click middle mouse button to start / stop", foreground="#000000", activeforeground="#000000", font=("Helvetica", 8, "italic"))
	instructions.place(x=0, y=95, width=250, height=25)

	interv_text = Label(root, background="#ffffff", activebackground="#ffffff", text="Interval (seconds): ", foreground="#000000", activeforeground="#000000", font=("Helvetica", 10, "italic"))
	interv_text.place(x=5, y=65, width=115, height=25)
	reg = root.register(validate_input)
	ent = Entry(root, justify=CENTER, validate="key", validatecommand=(reg, "%P"), background="grey90", foreground="#000000", highlightthickness=0, borderwidth=0, font=("Helvetica", 11))
	ent.insert(0, "3")
	ent.place(x=120, y=67, width=55, height=21)
	status = Label(root, background="#ffffff", activebackground="#ffffff", text="Inactive", foreground="red", activeforeground="red", font=("Helvetica", 10, "italic", "bold"))
	status.place(x=175, y=65, width=75, height=25)

	mouse.on_button(start, buttons=(mouse.MIDDLE,), types=(mouse.UP,))
	root.mainloop()
	try:
		process_clicker.kill()
		process_clicker.join()
		process_clicker.close()
	except (NameError, ValueError):
		pass
	psutil.Process(os.getpid()).kill()


if __name__ == "__main__":
	freeze_support()  # for PyInstaller to work with multiprocessing
	main()

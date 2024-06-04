from gui import WebCrawlerApp
import tkinter as tk

if __name__ == "__main__":
    root = tk.Tk()
    root.geometry("800x900")  # Set the initial window size to 1000x800
    app = WebCrawlerApp(root)
    root.mainloop()

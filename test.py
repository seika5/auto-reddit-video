import tkinter as tk
import queue
import threading
import time

class QueueProcessor:
    def __init__(self):
        self.message_queue = queue.Queue()
        self.is_processing = False

    def add_to_queue(self, message):
        self.message_queue.put(message)

    def process_queue(self):
        while True:
            if not self.message_queue.empty():
                message = self.message_queue.get()
                print("Processing:", message)
            time.sleep(2)

def add_to_queue():
    message = entry.get()
    if message:
        processor.add_to_queue(message)
        entry.delete(0, tk.END)

def start_processing():
    if not processor.is_processing:
        processor.is_processing = True
        processing_thread = threading.Thread(target=processor.process_queue)
        processing_thread.daemon = True
        processing_thread.start()
        start_button.config(state=tk.DISABLED)

processor = QueueProcessor()

root = tk.Tk()
root.title("Queue Processor")

frame = tk.Frame(root)
frame.pack(padx=20, pady=20)

entry_label = tk.Label(frame, text="Enter a message:")
entry_label.pack()

entry = tk.Entry(frame)
entry.pack()

add_button = tk.Button(frame, text="Add to Queue", command=add_to_queue)
add_button.pack()

start_button = tk.Button(frame, text="Start Processing", command=start_processing)
start_button.pack()

root.mainloop()
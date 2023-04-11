import os
import subprocess
import tkinter as tk
from tkinter import filedialog
from tkinter import messagebox

class DragDropWindow(tk.Tk):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.title("Cart Magic")
        self.geometry("400x350")

        # Add label for day of the week
        day_options = ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday", "Sunday"]
        day_label = tk.Label(self, text="Select day of the week:", font=("Arial", 12, "bold"))
        day_label.pack()
        self.day_var = tk.StringVar(self)
        self.day_var.set(day_options[0])
        day_menu = tk.OptionMenu(self, self.day_var, *day_options)
        day_menu.pack()

        # Add label for time
        time_options = ["8:00pm", "8:30pm", "9:00pm", "9:30pm", "10:00pm", "10:30pm", "11:00pm"]
        time_label = tk.Label(self, text="Select time:", font=("Arial", 12, "bold"))
        time_label.pack()
        self.time_var = tk.StringVar(self)
        self.time_var.set(time_options[0])
        time_menu = tk.OptionMenu(self, self.time_var, *time_options)
        time_menu.pack()

        # Add label for selected file
        file_label = tk.Label(self, text="Selected file:", font=("Arial", 12, "bold"))
        file_label.pack()

        # Add entry for selected file
        self.file_entry = tk.Entry(self, width=30)
        self.file_entry.pack()

        # Add button to browse files
        browse_button = tk.Button(self, text="Browse", command=self.choose_file)
        browse_button.pack()

        # Add button to run batch file
        run_button = tk.Button(self, text="Run Batch File", command=self.run_batch)
        run_button.pack()

        # Add drag and drop functionality
        self.drop_target = tk.Label(self, text="Drop file here", font=("Arial", 16), width=20, height=10, bg="white", bd=2, relief="groove")
        self.drop_target.pack(pady=20)

        # Bind drag and drop events to label
        self.drop_target.bind("<Enter>", self.handle_drag_enter)
        self.drop_target.bind("<Leave>", self.handle_drag_leave)
        self.drop_target.bind("<<Drop>>", self.handle_drop)

    def handle_drag_enter(self, event):
        """
        Handles drag enter event.
        """
        event.widget.config(bg="light blue")

    def handle_drag_leave(self, event):
        """
        Handles drag leave event.
        """
        event.widget.config(bg="white")

    
    def handle_drop(self, event):
        """
        Handles drop event.
        """
        if event.data:
            file_path = event.data['text']
            if os.path.isfile(file_path):
                self.file_entry.delete(0, tk.END)
                self.file_entry.insert(0, file_path)
                event.widget.config(bg='white')
            else:
                tk.messagebox.showerror("Error", "GUI_01.txtle.")

    def choose_file(self):
        """
        Opens a file dialog to choose a file.
        """
        file_path = filedialog.askopenfilename()
        if file_path:
            self.file_entry.delete(0, tk.END)
            self.file_entry.insert(0, file_path)
    


    def run_batch(self):
        day = self.day_var.get().replace(" ", "_")
        time = self.time_var.get().replace(":", "")
        file_path = self.file_entry.get()

        if not os.path.exists(file_path):
            tk.messagebox.showerror("Error", "Selected file does not exist.")
            return

        file_ext = os.path.splitext(file_path)[1]
        if file_ext.lower() != ".mp4":
            tk.messagebox.showerror("Error", "Selected file is not an MP4 video file.")
            return

        batch_file_name = os.path.join(os.path.dirname(os.path.abspath(__file__)), "batchfile.bat")
        with open(batch_file_name, "w") as f:
            f.write(f'copy "{file_path}" "{day}{time}.mp4"')

        if os.path.exists(batch_file_name):
            subprocess.call([batch_file_name])
            tk.messagebox.showinfo("Success", "Batch file successfully run.")
        else:
            tk.messagebox.showerror("Error", "Failed to create batch file.")
    

if __name__ == "__main__":
        window = DragDropWindow()
        window.mainloop()



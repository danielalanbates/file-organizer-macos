import os
import shutil
import tkinter as tk
from tkinter import filedialog, messagebox

# Mapping of file extensions to project types
PROJECT_TYPES = {
    '.py': 'python',
    '.js': 'javascript',
    '.ts': 'typescript',
    '.tsx': 'typescript',
    '.jsx': 'javascript',
    '.java': 'java',
    '.cpp': 'cpp',
    '.c': 'c',
    '.cs': 'csharp',
    '.php': 'php',
    '.rb': 'ruby',
    '.go': 'go',
    '.rs': 'rust',
    '.html': 'web',
    '.htm': 'web',
    '.css': 'web',
    '.scss': 'web',
    '.sass': 'web',
    '.less': 'web',
    '.json': 'config',
    '.xml': 'config',
    '.yaml': 'config',
    '.yml': 'config',
    '.md': 'docs',
    '.txt': 'docs',
    '.sh': 'scripts',
    '.bat': 'scripts',
    '.ps1': 'scripts',
    # Add more as needed
}

def sort_files(directory):
    """
    Sorts files in the given directory into subfolders based on project type inferred from file extension.
    Files with unknown extensions go into 'other' folder.
    Files without extension go into 'no_extension' folder.
    """
    try:
        files_moved = 0
        for filename in os.listdir(directory):
            filepath = os.path.join(directory, filename)
            if os.path.isfile(filepath) and filename != os.path.basename(__file__):  # Exclude this script
                # Get extension
                _, ext = os.path.splitext(filename)
                ext = ext.lower()
                if ext in PROJECT_TYPES:
                    folder = PROJECT_TYPES[ext]
                elif ext:
                    folder = 'other'
                else:
                    folder = 'no_extension'
                # Create folder if not exists
                folder_path = os.path.join(directory, folder)
                os.makedirs(folder_path, exist_ok=True)
                # Move file
                shutil.move(filepath, os.path.join(folder_path, filename))
                files_moved += 1
        messagebox.showinfo("Success", f"File sorting complete! Moved {files_moved} files.")
    except OSError as e:
        messagebox.showerror("Error", f"An error occurred: {str(e)}")

def select_directory():
    directory = filedialog.askdirectory(title="Select Directory to Sort")
    if directory:
        sort_files(directory)

# GUI
root = tk.Tk()
root.title("File Sorter")
root.geometry("300x100")

label = tk.Label(root, text="Click to select a directory and sort its files:")
label.pack(pady=10)

btn = tk.Button(root, text="Select Directory and Sort", command=select_directory)
btn.pack()

root.mainloop()
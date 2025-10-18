import os
import time
import heapq

# Search my computer for the largest files and sort by size
def find_largest_files(start_path, top_n=10):
    file_sizes = []
    scan_count = 0
    last_dir = start_path
    top_n = max(1, min(top_n, 100)) # Ensure top_n is between 1 and 100
    # Walk the directory tree
    for dirpath, dirnames, filenames in os.walk(start_path):
        last_dir = dirpath
        for filename in filenames:
            filepath = os.path.join(dirpath, filename)
            # Get the file size
            try:
                file_size = os.path.getsize(filepath)
                file_sizes.append((file_size, filepath))
                scan_count += 1
                # Print progress every 100 files
                if scan_count % 100 == 0:
                    print(f" Scanned {scan_count} files... Last directory: {last_dir}", end="\r")
            except (OSError, FileNotFoundError):
                continue

    print(f"Scanned {scan_count} files in {dirpath}")
    largest_files = heapq.nlargest(top_n, file_sizes, key=lambda x: x[0]) # Get the top_n largest files
    print(largest_files)
    return largest_files
    
         


       
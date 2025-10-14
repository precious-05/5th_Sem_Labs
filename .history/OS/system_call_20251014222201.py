# ----------------------------------------------------------
# 📘 Concept: Low-level File Handling (similar to OS System Calls)
# ----------------------------------------------------------
# This Python code replicates the behavior of the C program:
# 1. Opens a file in read-only mode
# 2. Reads its content in small chunks
# 3. Writes each chunk to the terminal (stdout)
# ----------------------------------------------------------

import os    # 'os' module provides access to system calls like open, read, write

# 1️⃣ Open the file using OS-level open (not the built-in open())
# Flags: os.O_RDONLY means "open as read-only"
fd = os.open("/etc/hosts", os.O_RDONLY)

try:
    while True:
        # 2️⃣ Read up to 256 bytes from file descriptor
        data = os.read(fd, 256)

        # If data is empty (EOF), break the loop
        if not data:
            break

        # 3️⃣ Write the data to standard output (same as write(STDOUT_FILENO, ...))
        os.write(1, data)   # 1 = STDOUT file descriptor in Linux

finally:
    # 4️⃣ Close the file descriptor
    os.close(fd)

# ----------------------------------------------------------
# ✅ Output:
# It prints the content of /etc/hosts file on the screen,
# just like the C version.
# ----------------------------------------------------------

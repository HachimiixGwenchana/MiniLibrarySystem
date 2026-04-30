PROJECT_FILE = "project_data.txt"

# ── Helper: show file contents ─────────────────────────────
def show_file():
    print("\nFile contents:")
    print("-" * 35)
    with open(PROJECT_FILE, "r") as f:
        print(f.read())
    print("-" * 35)


# ==============================================================
# MODE "x" — Create ONLY if file does NOT exist
# ==============================================================
print("=" * 35)
print('MODE "x" — Exclusive Creation')
print("=" * 35)

try:
    with open(PROJECT_FILE, "x") as f:    # "x" mode
        f.write("Project: Mini Library System\n")
        f.write("Version: 1.0\n")
        f.write("Status : Active\n")
        f.write("Books  : Harry Potter, The Alchemist, Clean Code\n")

    print("File created successfully!")
    show_file()

except FileExistsError:
    print("FileExistsError: File already exists!")
    print("   'x' mode will NOT overwrite it.")


# ==============================================================
# MODE "w" — Create or OVERWRITE
# ==============================================================
print("\n" + "=" * 35)
print('MODE "w" — Write / Overwrite')
print("=" * 35)

with open(PROJECT_FILE, "w") as f:        # "w" mode
    f.write("Project: Mini Library System\n")
    f.write("Version: 2.0\n")
    f.write("Status : Reset\n")
    f.write("Books  : (empty)\n")

print("File created/overwritten!")
show_file()


# ==============================================================
# MODE "a" — APPEND to end of file
# ==============================================================
print("\n" + "=" * 35)
print('MODE "a" — Append')
print("=" * 35)

with open(PROJECT_FILE, "a") as f:        # "a" mode
    f.write("Book Added: Python Crash Course\n")
    f.write("Book Added: Eloquent JavaScript\n")

print("Books appended successfully!")
show_file()


# ==============================================================
# SUMMARY
# ==============================================================
print('  "x" = Safe create  (fails if file exists)')
print('  "w" = Always write (overwrites if exists)')
print('  "a" = Append      (adds to end of file)')

def student_b_append(book_title):
    # 'a' appends to the end of the file
    with open(PROJECT_FILE, "a") as file:
        file.write(f"Book Added: {book_title}\n")
    print(f"Student B: Appended '{book_title}' to log.")


DATA_FILE = "library_data.txt"


# ==============================================================
# PULL — Read data from .txt file into memory (lists)
# ==============================================================
def pull():
    """
    Reads library_data.txt line by line and loads
    books and members into memory as lists of dicts.
    """
    books   = []
    members = []

    try:
        with open(DATA_FILE, "r") as f:
            section = None

            for line in f:
                line = line.strip()

                if line == "[BOOKS]":
                    section = "books"
                elif line == "[MEMBERS]":
                    section = "members"
                elif line == "" or line.startswith("#"):
                    continue

                elif section == "books":
                    # Format: id|title|author|status
                    parts = line.split("|")
                    if len(parts) == 4:
                        books.append({
                            "id"     : int(parts[0]),
                            "title"  : parts[1],
                            "author" : parts[2],
                            "status" : parts[3]
                        })

                elif section == "members":
                    # Format: id|name|email
                    parts = line.split("|")
                    if len(parts) == 3:
                        members.append({
                            "id"    : int(parts[0]),
                            "name"  : parts[1],
                            "email" : parts[2]
                        })

    except FileNotFoundError:
        # First run — seed default data
        books = [
            {"id": 1, "title": "Harry Potter",  "author": "J.K. Rowling",    "status": "Available"},
            {"id": 2, "title": "The Alchemist", "author": "Paulo Coelho",    "status": "Available"},
            {"id": 3, "title": "Clean Code",    "author": "Robert C. Martin","status": "Available"},
        ]
        members = [
            {"id": 1, "name": "Alice Santos", "email": "alice@email.com"},
            {"id": 2, "name": "Bob Reyes",    "email": "bob@email.com"},
        ]

    return books, members


# ==============================================================
# PUSH — Write memory data back to .txt file
# ==============================================================
def push(books, members):
    """
    Writes all books and members into library_data.txt
    using plain text with | as separator.
    """
    with open(DATA_FILE, "w") as f:
        f.write("# ========================\n")
        f.write("# LIBRARY DATA FILE\n")
        f.write("# Format: id|field1|field2|...\n")
        f.write("# ========================\n\n")

        f.write("[BOOKS]\n")
        for b in books:
            f.write(f"{b['id']}|{b['title']}|{b['author']}|{b['status']}\n")

        f.write("\n[MEMBERS]\n")
        for m in members:
            f.write(f"{m['id']}|{m['name']}|{m['email']}\n")

    print("  💾 Data saved to library_data.txt")


# ==============================================================
# HELPER
# ==============================================================
def divider(title):
    print("\n" + "=" * 50)
    print(f"  {title}")
    print("=" * 50)

def pause():
    input("\n  Press Enter to continue...")

def next_id(lst):
    """Auto-generate next ID from a list of dicts."""
    return max((i["id"] for i in lst), default=0) + 1


# ==============================================================
# BOOKS
# ==============================================================
def view_books(books):
    divider("ALL BOOKS")
    if not books:
        print("  📭 No books yet.")
        return
    print(f"  {'ID':<5} {'Title':<25} {'Author':<22} {'Status'}")
    print("  " + "-" * 65)
    for b in books:
        icon = "✅" if b["status"] == "Available" else "📖"
        print(f"  {b['id']:<5} {b['title']:<25} {b['author']:<22} {icon} {b['status']}")

def add_book(books, members):
    divider("ADD BOOK")
    title  = input("  Title  : ").strip()
    author = input("  Author : ").strip()
    if not title or not author:
        print("  ❌ Title and author cannot be empty.")
        return
    books.append({
        "id"     : next_id(books),
        "title"  : title,
        "author" : author,
        "status" : "Available"
    })
    push(books, members)                    # PUSH after change
    print(f"  ✅ Book '{title}' added!")


# ==============================================================
# MEMBERS — View
# ==============================================================
def view_members(members):
    divider("ALL MEMBERS")
    if not members:
        print("  📭 No members yet.")
        return
    print(f"  {'ID':<5} {'Name':<25} {'Email'}")
    print("  " + "-" * 50)
    for m in members:
        print(f"  {m['id']:<5} {m['name']:<25} {m['email']}")


# ==============================================================
# MEMBERS — Add
# ==============================================================
def add_member(books, members):
    divider("ADD MEMBER")
    name  = input("  Name  : ").strip()
    email = input("  Email : ").strip()
    if not name or not email:
        print("  ❌ Name and email cannot be empty.")
        return
    members.append({
        "id"    : next_id(members),
        "name"  : name,
        "email" : email
    })
    push(books, members)                    # PUSH after change
    print(f"  ✅ Member '{name}' added!")


# ==============================================================
# MEMBERS — Search
# ==============================================================
def search_member(books, members):
    divider("SEARCH MEMBER")

    print("  🔄 Pulling latest data from file...")
    books[:], members[:] = pull()           # PULL latest before search

    keyword = input("  Enter name or email: ").strip().lower()
    results = [
        m for m in members
        if keyword in m["name"].lower() or keyword in m["email"].lower()
    ]

    if not results:
        print(f"  ❌ No member found for '{keyword}'.")
        return

    print(f"\n  Found {len(results)} result(s):\n")
    print(f"  {'ID':<5} {'Name':<25} {'Email'}")
    print("  " + "-" * 50)
    for m in results:
        print(f"  {m['id']:<5} {m['name']:<25} {m['email']}")


# ==============================================================
# MEMBERS — Update (D: pull → edit → push)
# ==============================================================
def update_member(books, members):
    divider("UPDATE MEMBER  (pull → edit → push)")

    print("  🔄 Pulling latest data from file...")
    books[:], members[:] = pull()           # PULL before update

    view_members(members)

    try:
        member_id = int(input("\n  Enter Member ID to update: "))
    except ValueError:
        print("  ❌ Invalid ID.")
        return

    for m in members:
        if m["id"] == member_id:
            print(f"\n  Current Name  : {m['name']}")
            print(f"  Current Email : {m['email']}")
            new_name  = input("\n  New Name  (Enter to keep): ").strip()
            new_email = input("  New Email (Enter to keep): ").strip()

            if new_name:  m["name"]  = new_name
            if new_email: m["email"] = new_email

            push(books, members)            # PUSH after update
            print(f"  ✅ Member updated!")
            return

    print(f"  ❌ Member ID {member_id} not found.")


# ==============================================================
# MEMBERS — Delete (pull → delete → push)
# ==============================================================
def delete_member(books, members):
    divider("DELETE MEMBER  (pull → delete → push)")

    print("  🔄 Pulling latest data from file...")
    books[:], members[:] = pull()           # PULL before delete

    view_members(members)

    try:
        member_id = int(input("\n  Enter Member ID to delete: "))
    except ValueError:
        print("  ❌ Invalid ID.")
        return

    for i, m in enumerate(members):
        if m["id"] == member_id:
            confirm = input(f"  ⚠️  Delete '{m['name']}'? (yes/no): ").strip().lower()
            if confirm == "yes":
                members.pop(i)
                push(books, members)        # PUSH after delete
                print(f"  🗑️  '{m['name']}' deleted.")
            else:
                print("  ❎ Cancelled.")
            return

    print(f"  ❌ Member ID {member_id} not found.")


# ==============================================================
# MEMBERS SUBMENU
# ==============================================================
def members_menu(books, members):
    while True:
        divider("MEMBERS MENU")
        print("  [1] View All Members")
        print("  [2] Add Member")
        print("  [3] Search Member")
        print("  [4] Update Member  (D)")
        print("  [5] Delete Member")
        print("  [0] Back")
        print("=" * 50)

        choice = input("  Choice: ").strip()

        if   choice == "1": view_members(members)
        elif choice == "2": add_member(books, members)
        elif choice == "3": search_member(books, members)
        elif choice == "4": update_member(books, members)
        elif choice == "5": delete_member(books, members)
        elif choice == "0": break
        else: print("  ❌ Invalid choice.")

        pause()


# ==============================================================
# MAIN
# ==============================================================
def main():
    print("  🔄 Pulling data from file...")
    books, members = pull()                 # PULL on startup
    push(books, members)                    # PUSH to create file if new

    while True:
        divider("📚 MINI LIBRARY SYSTEM")
        print(f"  Books: {len(books)}  |  Members: {len(members)}")
        print("=" * 50)
        print("  [1] Books")
        print("  [2] Members")
        print("  [0] Exit")
        print("=" * 50)

        choice = input("  Choice: ").strip()

        if choice == "1":
            while True:
                divider("BOOKS MENU")
                print("  [1] View All Books")
                print("  [2] Add Book")
                print("  [0] Back")
                c = input("  Choice: ").strip()
                if   c == "1": view_books(books)
                elif c == "2": add_book(books, members)
                elif c == "0": break
                else: print("  ❌ Invalid.")
                pause()

        elif choice == "2":
            members_menu(books, members)

        elif choice == "0":
            print("\n  👋 Goodbye! Data saved.\n")
            break
        else:
            print("  ❌ Invalid choice.")

        pause()


if __name__ == "__main__":
    main()
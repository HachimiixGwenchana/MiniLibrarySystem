# ============================================================
# MINI LIBRARY SYSTEM — Updated Version
# Added: D = pull/push (update file content)
#        ALL MEMBERS: Search + Delete
# ============================================================

import json
import os
from datetime import datetime

DATA_FILE = "library_data.txt"


# ==============================================================
# PULL — Load data from file (read)
# ==============================================================
def pull():
    """Pull: reads current data from file into memory."""
    try:
        with open(DATA_FILE, "r") as f:
            return json.load(f)
    except FileNotFoundError:
        # First run — initialize fresh data
        return {
            "next_book_id"   : 4,
            "next_member_id" : 3,
            "books": [
                {"id": 1, "title": "Harry Potter",  "author": "J.K. Rowling",        "status": "Available"},
                {"id": 2, "title": "The Alchemist", "author": "Paulo Coelho",         "status": "Available"},
                {"id": 3, "title": "Clean Code",    "author": "Robert C. Martin",     "status": "Available"},
            ],
            "members": [
                {"id": 1, "name": "Alice Santos", "email": "alice@email.com"},
                {"id": 2, "name": "Bob Reyes",    "email": "bob@email.com"},
            ]
        }
    except json.JSONDecodeError:
        print("⚠️  File corrupted. Starting fresh.")
        return {"next_book_id": 1, "next_member_id": 1, "books": [], "members": []}


# ==============================================================
# PUSH — Save updated data back to file (write)
# ==============================================================
def push(data):
    """Push: writes updated memory data back into the file."""
    with open(DATA_FILE, "w") as f:
        json.dump(data, f, indent=4)
    print("  💾 Data pushed (saved) to file successfully.")


# ==============================================================
# HELPER
# ==============================================================
def divider(title):
    print("\n" + "=" * 50)
    print(f"  {title}")
    print("=" * 50)

def pause():
    input("\n  Press Enter to continue...")


# ==============================================================
# BOOKS MENU
# ==============================================================
def add_book(data):
    divider("ADD BOOK")
    title  = input("  Title  : ").strip()
    author = input("  Author : ").strip()
    if not title or not author:
        print("  ❌ Title and author cannot be empty.")
        return
    data["books"].append({
        "id"     : data["next_book_id"],
        "title"  : title,
        "author" : author,
        "status" : "Available"
    })
    data["next_book_id"] += 1
    push(data)                              # PUSH after update
    print(f"  ✅ Book '{title}' added!")

def view_books(data):
    divider("ALL BOOKS")
    if not data["books"]:
        print("  📭 No books yet.")
        return
    print(f"  {'ID':<5} {'Title':<25} {'Author':<22} {'Status'}")
    print("  " + "-" * 65)
    for b in data["books"]:
        icon = "✅" if b["status"] == "Available" else "📖"
        print(f"  {b['id']:<5} {b['title']:<25} {b['author']:<22} {icon} {b['status']}")


# ==============================================================
# MEMBERS — View All
# ==============================================================
def view_members(data):
    divider("ALL MEMBERS")
    if not data["members"]:
        print("  📭 No members yet.")
        return
    print(f"  {'ID':<5} {'Name':<25} {'Email'}")
    print("  " + "-" * 55)
    for m in data["members"]:
        print(f"  {m['id']:<5} {m['name']:<25} {m['email']}")


# ==============================================================
# MEMBERS — Add
# ==============================================================
def add_member(data):
    divider("ADD MEMBER")
    name  = input("  Name  : ").strip()
    email = input("  Email : ").strip()
    if not name or not email:
        print("  ❌ Name and email cannot be empty.")
        return
    data["members"].append({
        "id"    : data["next_member_id"],
        "name"  : name,
        "email" : email
    })
    data["next_member_id"] += 1
    push(data)                              # PUSH after update
    print(f"  ✅ Member '{name}' added!")


# ==============================================================
# MEMBERS — D: Search (pull latest → search → display)
# ==============================================================
def search_member(data):
    divider("SEARCH MEMBER")

    print("  🔄 Pulling latest data from file...")
    data.update(pull())                     # PULL before search

    keyword = input("  Enter name or email to search: ").strip().lower()
    results = [
        m for m in data["members"]
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
# MEMBERS — D: Delete (pull → delete → push)
# ==============================================================
def delete_member(data):
    divider("DELETE MEMBER")

    print("  🔄 Pulling latest data from file...")
    data.update(pull())                     # PULL before delete

    view_members(data)

    try:
        member_id = int(input("\n  Enter Member ID to delete: "))
    except ValueError:
        print("  ❌ Invalid ID.")
        return

    for i, m in enumerate(data["members"]):
        if m["id"] == member_id:
            confirm = input(f"  ⚠️  Delete '{m['name']}'? (yes/no): ").strip().lower()
            if confirm == "yes":
                data["members"].pop(i)
                push(data)                  # PUSH after delete
                print(f"  🗑️  Member '{m['name']}' deleted.")
            else:
                print("  ❎ Cancelled.")
            return

    print(f"  ❌ Member ID {member_id} not found.")


# ==============================================================
# D — Update content in the file (pull → modify → push)
# ==============================================================
def update_member(data):
    divider("D — UPDATE MEMBER (pull → edit → push)")

    print("  🔄 Pulling latest data from file...")
    data.update(pull())                     # PULL latest content

    view_members(data)

    try:
        member_id = int(input("\n  Enter Member ID to update: "))
    except ValueError:
        print("  ❌ Invalid ID.")
        return

    for m in data["members"]:
        if m["id"] == member_id:
            print(f"\n  Current Name  : {m['name']}")
            print(f"  Current Email : {m['email']}")

            new_name  = input("\n  New Name  (press Enter to keep): ").strip()
            new_email = input("  New Email (press Enter to keep): ").strip()

            if new_name:
                m["name"]  = new_name
            if new_email:
                m["email"] = new_email

            push(data)                      # PUSH updated content
            print(f"  ✅ Member updated successfully!")
            return

    print(f"  ❌ Member ID {member_id} not found.")


# ==============================================================
# MEMBERS SUBMENU
# ==============================================================
def members_menu(data):
    while True:
        divider("MEMBERS MENU")
        print("  [1] View All Members")
        print("  [2] Add Member")
        print("  [3] Search Member")        # NEW
        print("  [4] Update Member  (D)")   # D — pull/push update
        print("  [5] Delete Member")        # NEW
        print("  [0] Back")
        print("=" * 50)

        choice = input("  Choice: ").strip()

        if   choice == "1": view_members(data)
        elif choice == "2": add_member(data)
        elif choice == "3": search_member(data)
        elif choice == "4": update_member(data)
        elif choice == "5": delete_member(data)
        elif choice == "0": break
        else: print("  ❌ Invalid choice.")

        pause()


# ==============================================================
# MAIN MENU
# ==============================================================
def main():
    print("  🔄 Pulling data from file...")
    data = pull()                           # PULL on startup
    push(data)                              # PUSH to create file if new

    while True:
        divider("📚 MINI LIBRARY SYSTEM")
        print(f"  Books  : {len(data['books'])}  |  Members: {len(data['members'])}")
        print("=" * 50)
        print("  [1] Books")
        print("  [2] Members  (Search + Delete + Update)")
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
                if   c == "1": view_books(data)
                elif c == "2": add_book(data)
                elif c == "0": break
                else: print("  ❌ Invalid.")
                pause()

        elif choice == "2":
            members_menu(data)

        elif choice == "0":
            print("\n  👋 Goodbye! Data saved.\n")
            break
        else:
            print("  ❌ Invalid choice.")

        pause()


if __name__ == "__main__":
    main()
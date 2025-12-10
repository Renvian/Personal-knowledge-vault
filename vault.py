NOTES_FILE = "notes.txt"

def save_note(title, body):
    with open(NOTES_FILE, "a", encoding="utf-8") as fp:
        fp.write(f"TITLE:{title}\n")
        fp.write(f"BODY:{body}\n")
        fp.write("---\n")
    print("Note saved successfully!\n")

def load_notes():
    notes = []
    try:
        with open(NOTES_FILE, "r", encoding="utf-8") as f:
            blocks = f.read().strip().split("---\n")
    except FileNotFoundError:
        return notes

    for block in blocks:
        block = block.strip()
        if block == "":
            continue

        note = {"title": "", "body": ""}
        for line in block.split("\n"):
            if line.startswith("TITLE:"):
                note["title"] = line[6:].strip()
            elif line.startswith("BODY:"):
                note["body"] = line[5:].strip()

        notes.append(note)

    return notes


def search_by_keyword(keyword):
    keyword = keyword.lower()
    notes = load_notes()
    results = []

    for note in notes:
        if keyword in note["title"].lower() or keyword in note["body"].lower():
            results.append(note)

    return results


def search_and_select(keyword):
    matches = search_by_keyword(keyword)
    if not matches:
        print("No matching notes found.\n")
        return None

    print("\nMatching Notes:")
    for i, note in enumerate(matches, 1):
        print(f"{i}. {note['title']}")

    try:
        choice = int(input("Select note number: ")) - 1
    except ValueError:
        print("Invalid input.\n")
        return None

    if 0 <= choice < len(matches):
        return matches[choice]
    else:
        print("Invalid selection.\n")
        return None

def edit_note(keyword):
    selected_note = search_and_select(keyword)
    if not selected_note:
        return

    print("\nWhat would you like to edit?")
    print("1. Title only")
    print("2. Body only")
    print("3. Both")
    option = input("Enter option: ")

    original_title = selected_note["title"]
    original_body = selected_note["body"]

    if option == "1":
        selected_note["title"] = input("New title: ")

    elif option == "2":
        selected_note["body"] = input("New body: ")

    elif option == "3":
        selected_note["title"] = input("New title: ")
        selected_note["body"] = input("New body: ")

    all_notes = load_notes()
    for n in all_notes:
        if n["title"] == original_title and n["body"] == original_body:
            n["title"] = selected_note["title"]
            n["body"] = selected_note["body"]

    with open(NOTES_FILE, "w", encoding="utf-8") as f:
        for n in all_notes:
            f.write(f"TITLE:{n['title']}\n")
            f.write(f"BODY:{n['body']}\n")
            f.write("---\n")

    print("Note updated successfully!\n")

def delete_note(keyword):
    selected_note = search_and_select(keyword)
    if not selected_note:
        return

    all_notes = load_notes()
    new_notes = [
        n for n in all_notes
        if not (n["title"] == selected_note["title"] and n["body"] == selected_note["body"])
    ]

    with open(NOTES_FILE, "w", encoding="utf-8") as f:
        for n in new_notes:
            f.write(f"TITLE:{n['title']}\n")
            f.write(f"BODY:{n['body']}\n")
            f.write("---\n")

    print("Note deleted successfully!\n")

def view_notes():
    notes = load_notes()
    if not notes:
        print("No notes found.\n")
        return

    print("\n--- All Notes ---")
    for i, note in enumerate(notes, 1):
        print(f"\n[{i}] {note['title']}")
        print(note["body"])
        print("-" * 30)
    print()

def main():
    while True:
        print("\n--- Personal Knowledge Vault ---")
        print("1. Create Note")
        print("2. View Notes")
        print("3. Search Notes")
        print("4. Edit Note")
        print("5. Delete Note")
        print("0. Exit")

        choice = input("Enter choice: ")

        if choice == "1":
            title = input("Title: ")
            body = input("Body: ")
            save_note(title, body)

        elif choice == "2":
            view_notes()

        elif choice == "3":
            key = input("Enter keyword: ")
            note = search_and_select(key)
            if note:
                print("\n--- Note Details ---")
                print("Title:", note["title"])
                print("Body:", note["body"])
                print("-" * 30)

        elif choice == "4":
            key = input("Enter keyword to edit: ")
            edit_note(key)

        elif choice == "5":
            key = input("Enter keyword to delete: ")
            delete_note(key)

        elif choice == "0":
            print("Goodbye!")
            break

        else:
            print("Invalid choice! Try again.\n")


if __name__ == "__main__":
    main()

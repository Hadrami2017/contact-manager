import os
from typing import List, Optional


# 🧱 Step 1: Contact Class
class Contact:
    """Represents a single contact entry with name and phone."""

    def __init__(self, name: str, phone: str):
        self.name = name.strip()
        self.phone = phone.strip()
        self._validate()

    def _validate(self):
        if not self.name:
            raise ValueError("Contact name cannot be empty.")
        if not self.phone:
            raise ValueError("Contact phone cannot be empty.")
        if not self.phone.replace("-", "").isdigit():
            raise ValueError("Phone number must contain only digits or hyphens.")

    def to_line(self) -> str:
        return f"{self.name} | {self.phone}\n"

    @classmethod
    def from_line(cls, line: str) -> Optional["Contact"]:
        """Factory method to reconstruct a Contact from a text line."""
        if " | " not in line:
            return None
        name, phone = line.strip().split(" | ", 1)
        return cls(name, phone)

    def __repr__(self):
        return f"Contact(name='{self.name}', phone='{self.phone}')"


# 🧱 Step 2: ContactManager Class
class ContactManager:
    """Handles file operations and CRUD for contacts."""

    FILE_NAME = "contacts.txt"

    def __init__(self, file_path: Optional[str] = None):
        self.file_path = file_path or self.FILE_NAME
        os.makedirs(os.path.dirname(self.file_path), exist_ok=True) if os.path.dirname(self.file_path) else None

    def add_contact(self, contact: Contact) -> None:
        contacts = self.get_all_contacts()

        # Prevent duplicate names
        if any(c.name.lower() == contact.name.lower() for c in contacts):
            raise ValueError(f"Contact '{contact.name}' already exists.")

        with open(self.file_path, "a", encoding="utf-8") as file:
            file.write(contact.to_line())

    def get_all_contacts(self) -> List[Contact]:
        if not os.path.exists(self.file_path):
            return []

        with open(self.file_path, "r", encoding="utf-8") as file:
            return [c for line in file if (c := Contact.from_line(line))]

    def delete_contact(self, name: str) -> bool:
        contacts = self.get_all_contacts()
        updated = [c for c in contacts if c.name.lower() != name.lower()]

        if len(updated) == len(contacts):
            return False  # No match found

        with open(self.file_path, "w", encoding="utf-8") as file:
            for contact in updated:
                file.write(contact.to_line())

        return True

    def find_contact(self, name: str) -> Optional[Contact]:
        """Finds a contact by name."""
        for contact in self.get_all_contacts():
            if contact.name.lower() == name.lower():
                return contact
        return None


# 🧱 Step 3: Main Program
def main():
    manager = ContactManager()

    while True:
        print("\n--- 📇 Contact Manager ---")
        print("1. Add Contact")
        print("2. View Contacts")
        print("3. Delete Contact")
        print("4. Search Contact")
        print("5. Exit")

        choice = input("Choose an option: ").strip()

        try:
            if choice == "1":
                name = input("Enter name: ").strip()
                phone = input("Enter phone: ").strip()
                manager.add_contact(Contact(name, phone))
                print("✅ Contact added successfully!")

            elif choice == "2":
                contacts = manager.get_all_contacts()
                if not contacts:
                    print("📭 No contacts found.")
                else:
                    for i, contact in enumerate(contacts, 1):
                        print(f"{i}. {contact.name} — {contact.phone}")

            elif choice == "3":
                name = input("Enter name to delete: ").strip()
                if manager.delete_contact(name):
                    print("🗑️ Contact deleted.")
                else:
                    print("❌ Contact not found.")

            elif choice == "4":
                name = input("Enter name to search: ").strip()
                found = manager.find_contact(name)
                if found:
                    print(f"🔍 Found: {found.name} — {found.phone}")
                else:
                    print("❌ No contact with that name.")

            elif choice == "5":
                print("👋 Goodbye!")
                break

            else:
                print("⚠️ Invalid choice. Try again.")

        except ValueError as e:
            print(f"🚫 Error: {e}")


if __name__ == "__main__":
    main()
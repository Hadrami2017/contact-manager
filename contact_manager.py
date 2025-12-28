import os
from typing import List, Optional


# =======================
# 📇 Contact Model
# =======================
class Contact:
    """Represents a single contact with name and phone number."""

    def __init__(self, name: str, phone: str):
        self.name = name.strip()
        self.phone = phone.strip()
        self._validate()

    def _validate(self) -> None:
        if not self.name:
            raise ValueError("Contact name cannot be empty.")

        if not self.phone:
            raise ValueError("Contact phone cannot be empty.")

        allowed = set("0123456789-+ ()")
        if any(char not in allowed for char in self.phone):
            raise ValueError(
                "Phone number may contain digits, spaces, +, -, or parentheses only."
            )

    def to_line(self) -> str:
        """Serialize contact to file format."""
        return f"{self.name} | {self.phone}\n"

    @classmethod
    def from_line(cls, line: str) -> Optional["Contact"]:
        """Safely create a Contact from a file line."""
        if " | " not in line:
            return None

        name, phone = line.strip().split(" | ", 1)
        try:
            return cls(name, phone)
        except ValueError:
            return None  # Skip malformed lines safely

    def __repr__(self) -> str:
        return f"Contact(name='{self.name}', phone='{self.phone}')"


# =======================
# 📂 Contact Manager
# =======================
class ContactManager:
    """Handles contact storage and CRUD operations."""

    FILE_NAME = "contacts.txt"

    def __init__(self, file_path: Optional[str] = None):
        self.file_path = file_path or self.FILE_NAME

        folder = os.path.dirname(self.file_path)
        if folder:
            os.makedirs(folder, exist_ok=True)

    def get_all_contacts(self) -> List[Contact]:
        """Load all valid contacts from file."""
        if not os.path.exists(self.file_path):
            return []

        contacts: List[Contact] = []
        with open(self.file_path, "r", encoding="utf-8") as file:
            for line in file:
                contact = Contact.from_line(line)
                if contact:
                    contacts.append(contact)

        return contacts

    def add_contact(self, contact: Contact) -> None:
        """Add a new contact if it does not already exist."""
        contacts = self.get_all_contacts()

        if any(c.name.lower() == contact.name.lower() for c in contacts):
            raise ValueError(f"Contact '{contact.name}' already exists.")

        with open(self.file_path, "a", encoding="utf-8") as file:
            file.write(contact.to_line())

    def delete_contact(self, name: str) -> bool:
        """Delete a contact by name."""
        contacts = self.get_all_contacts()
        updated = [c for c in contacts if c.name.lower() != name.lower()]

        if len(updated) == len(contacts):
            return False

        with open(self.file_path, "w", encoding="utf-8") as file:
            for contact in updated:
                file.write(contact.to_line())

        return True

    def find_contact(self, name: str) -> Optional[Contact]:
        """Find a contact by name."""
        for contact in self.get_all_contacts():
            if contact.name.lower() == name.lower():
                return contact
        return None


# =======================
# 🖥️ CLI Application
# =======================
def main() -> None:
    manager = ContactManager()

    while True:
        print("\n📇 --- Contact Manager ---")
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
                print("✅ Contact added successfully.")

            elif choice == "2":
                contacts = sorted(
                    manager.get_all_contacts(),
                    key=lambda c: c.name.lower()
                )
                if not contacts:
                    print("📭 No contacts found.")
                else:
                    for i, contact in enumerate(contacts, 1):
                        print(f"{i}. {contact.name} — {contact.phone}")

            elif choice == "3":
                name = input("Enter name to delete: ").strip()
                if manager.delete_contact(name):
                    print(f"🗑️ Contact '{name}' deleted.")
                else:
                    print("❌ Contact not found.")

            elif choice == "4":
                name = input("Enter name to search: ").strip()
                contact = manager.find_contact(name)
                if contact:
                    print(f"🔍 Found: {contact.name} — {contact.phone}")
                else:
                    print("❌ No contact with that name.")

            elif choice == "5":
                print("👋 Goodbye!")
                break

            else:
                print("⚠️ Invalid option. Please try again.")

        except ValueError as error:
            print(f"🚫 Error: {error}")


if __name__ == "__main__":
    main()

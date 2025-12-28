class Contact:
    def __init__(self, name: str, phone: str):
        self.name = name.strip()
        self.phone = phone.strip()
    

    def to_line(self) -> str:
        return f"{self.name} | {self.phone}\n"
    

class ContactManager:
    FILE_NAME = "contacts.txt"

    def add_contact(self, contact: Contact) -> None:
        if not contact.name or not contact.phone:
            raise ValueError("Name and phone cannot be empty")
        
        with open(self.FILE_NAME, "a") as file:
            file.write(contact.to_line())

    def get_all_contacts(self):
        try:

            with open(self.FILE_NAME, "r") as file:
                return [line.strip() for line in file if " | " in line]
        
        except FileNotFoundError:
            return []

    def delete_contact(self, name: str) -> bool:
        contacts = self.get_all_contacts()
        updated = []
        deleted = False

        for contact in contacts:
            contact_name, phone = contact.split(" | ")  
            if contact_name.lower() != name.lower():
                updated.append(contact)   
            else:
                deleted = True

        if deleted:
            with open(self.FILE_NAME, "w") as file:
                for c in updated:
                    file.write(c + "\n")   

        return deleted    

def main():
    manager = ContactManager()

    while True:
        print("\n--- Contact Manager ---")
        print("1. Add Contact")
        print("2. View Contacts")
        print("3. Delete Contact")
        print("4. Exit")

        choice = input("Choose an option: ")

        try:
            if choice == "1":
                name = input("Enter name: ")
                phone = input("Enter phone: ")
                manager.add_contact(Contact(name, phone))
                print("✅ Contact added")

            elif choice == "2":
                contacts = manager.get_all_contacts()
                if not contacts:
                    print("No contacts found")
                else:
                    for i, c in enumerate(contacts, 1):
                        print(f"{i}. {c}")

            elif choice == "3":
                name = input("Enter name to delete: ")
                if manager.delete_contact(name):
                    print("🗑️ Contact deleted")
                else:
                    print("❌ Contact not found")

            elif choice == "4":
                print("👋 Goodbye!")
                break

            else:
                print("❌ Invalid choice")

        except ValueError as e:
            print(f"Error: {e}")

if __name__ == "__main__":
    main()

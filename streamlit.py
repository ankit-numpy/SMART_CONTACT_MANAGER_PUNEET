# import streamlit as st
# st.title('ABCD')

import streamlit as st
import sqlite3

# Database connection functions
def connect_db():
    conn = sqlite3.connect('contacts.db')
    c = conn.cursor()
    return conn, c

# Initialize the database table if not already created
def init_db():
    conn, c = connect_db()
    c.execute('''CREATE TABLE IF NOT EXISTS contacts (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    name TEXT NOT NULL,
                    phone TEXT NOT NULL,
                    email TEXT)''')
    conn.commit()
    conn.close()

# Function to add a new contact
def add_contact(name, phone, email):
    conn, c = connect_db()
    c.execute("INSERT INTO contacts (name, phone, email) VALUES (?, ?, ?)", (name, phone, email))
    conn.commit()
    conn.close()

# Function to view all contacts
def view_contacts():
    conn, c = connect_db()
    c.execute("SELECT * FROM contacts")
    contacts = c.fetchall()
    conn.close()
    return contacts

# Function to search contacts by name
def search_contact(name):
    conn, c = connect_db()
    c.execute("SELECT * FROM contacts WHERE name LIKE ?", ('%' + name + '%',))
    contacts = c.fetchall()
    conn.close()
    return contacts

# Function to update a contact
def update_contact(contact_id, name, phone, email):
    conn, c = connect_db()
    c.execute("UPDATE contacts SET name = ?, phone = ?, email = ? WHERE id = ?", (name, phone, email, contact_id))
    conn.commit()
    conn.close()

# Function to delete a contact
def delete_contact(contact_id):
    conn, c = connect_db()
    c.execute("DELETE FROM contacts WHERE id = ?", (contact_id,))
    conn.commit()
    conn.close()

# Streamlit UI setup
def app():
    st.title("Contact Management System")

    # Initialize database table
    init_db()

    menu = ["Add Contact", "View Contacts", "Search Contact", "Update Contact", "Delete Contact"]
    choice = st.sidebar.selectbox("Select an option", menu)

    # Add Contact
    if choice == "Add Contact":
        st.subheader("Add New Contact")
        name = st.text_input("Enter Name")
        phone = st.text_input("Enter Phone")
        email = st.text_input("Enter Email")
        
        if st.button("Add Contact"):
            if name and phone:
                add_contact(name, phone, email)
                st.success(f"Contact {name} added successfully.")
            else:
                st.error("Name and Phone are required.")

    # View Contacts
    elif choice == "View Contacts":
        st.subheader("View All Contacts")
        contacts = view_contacts()
        if contacts:
            st.write("Total Contacts:", len(contacts))
            st.table(contacts)
        else:
            st.warning("No contacts found.")

    # Search Contact
    elif choice == "Search Contact":
        st.subheader("Search Contact by Name")
        search_term = st.text_input("Enter Name to Search")
        
        if st.button("Search"):
            contacts = search_contact(search_term)
            if contacts:
                st.table(contacts)
            else:
                st.warning("No contacts found with that name.")

    # Update Contact
    elif choice == "Update Contact":
        st.subheader("Update Contact")
        contact_id = st.number_input("Enter Contact ID", min_value=1)
        name = st.text_input("Enter New Name")
        phone = st.text_input("Enter New Phone")
        email = st.text_input("Enter New Email")

        if st.button("Update Contact"):
            if contact_id and name and phone:
                update_contact(contact_id, name, phone, email)
                st.success(f"Contact ID {contact_id} updated.")
            else:
                st.error("Please fill in all required fields.")

    # Delete Contact
    elif choice == "Delete Contact":
        st.subheader("Delete Contact")
        contact_id = st.number_input("Enter Contact ID to Delete", min_value=1)
        
        if st.button("Delete Contact"):
            if contact_id:
                delete_contact(contact_id)
                st.success(f"Contact ID {contact_id} deleted.")
            else:
                st.error("Please enter a valid contact ID to delete.")

# Run the app
if __name__ == "__main__":
    app()


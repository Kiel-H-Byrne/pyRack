# main.py

import tkinter as tk
from tkinter import ttk
from tkinter import messagebox
from inventory import InventoryManager
from tkinter import simpledialog


# Initialize the main application window
class NetworkInventoryApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Network Rack Inventory Tool")
        self.root.geometry("800x600")  # Set initial window size
        self.root.resizable(True, True)  # Allow resizing

        # Initialize inventory manager before creating menu
        self.inventory_manager = InventoryManager(self)

        # Set up the menu bar after initializing inventory manager
        self.create_menu()

        # Frame for device management and inventory display
        self.main_frame = ttk.Frame(self.root)
        self.main_frame.pack(fill="both", expand=True)

        # Placeholder for Device List and Port Mapping sections
        self.device_list_frame = ttk.Frame(self.main_frame)
        self.device_list_frame.grid(row=0, column=0, sticky="nswe", padx=10, pady=10)
        self.port_mapping_frame = ttk.Frame(self.main_frame)
        self.port_mapping_frame.grid(row=0, column=1, sticky="nswe", padx=10, pady=10)

        # Search bar for filtering devices
        search_label = ttk.Label(self.device_list_frame, text="Search Devices:")
        search_label.pack(pady=5)

        self.search_entry = ttk.Entry(self.device_list_frame, width=30)
        self.search_entry.pack(pady=5)
        self.search_entry.bind("<KeyRelease>", self.filter_devices)

        # Configure row and column weights for resizing
        self.main_frame.columnconfigure(0, weight=1)
        self.main_frame.columnconfigure(1, weight=2)
        self.main_frame.rowconfigure(0, weight=1)

        # Initialize placeholder components
        self.create_device_list()
        self.create_port_mapping()

        # Add buttons for managing devices in the Device List section
        add_device_button = ttk.Button(self.device_list_frame, text="Add Device", command=self.add_device)
        add_device_button.pack(pady=5)
        
        list_device_button = ttk.Button(self.device_list_frame, text="List Devices", command=self.list_devices)
        list_device_button.pack(pady=5)
        
        view_ports_button = ttk.Button(self.device_list_frame, text="View Ports", command=self.view_device_ports)
        view_ports_button.pack(pady=5)


    def create_menu(self):
        menu_bar = tk.Menu(self.root)

        # File menu
        file_menu = tk.Menu(menu_bar, tearoff=0)
        file_menu.add_command(label="New", command=self.new_inventory)
        file_menu.add_command(label="Save", command=self.inventory_manager.save_inventory)
        file_menu.add_command(label="Load", command=self.inventory_manager.load_inventory)
        file_menu.add_command(label="Export to CSV", command=self.inventory_manager.export_to_csv)
        file_menu.add_separator()
        file_menu.add_command(label="Exit", command=self.root.quit)

        menu_bar.add_cascade(label="File", menu=file_menu)

        # Help menu
        help_menu = tk.Menu(menu_bar, tearoff=0)
        help_menu.add_command(label="About", command=self.show_about)
        menu_bar.add_cascade(label="Help", menu=help_menu)

        self.root.config(menu=menu_bar)

    def create_device_list(self):
        # Placeholder Label for Device List section
        device_list_label = ttk.Label(self.device_list_frame, text="Device List")
        device_list_label.pack()

    def add_device(self):
            # Call the add_device method from InventoryManager
            self.inventory_manager.add_device()

    def list_devices(self):
        # Display device list in a message box
        devices = self.inventory_manager.list_devices()
        if not devices:
            messagebox.showinfo("Device List", "No devices added yet.")
        else:
            device_info = "\n".join([f"{name} ({device_type})" for name, device_type in devices])
            messagebox.showinfo("Device List", device_info)

    def create_port_mapping(self):
        # Label for Port Mapping section
        port_mapping_label = ttk.Label(self.port_mapping_frame, text="Port Mapping")
        port_mapping_label.pack()

        # Treeview for port mapping table
        self.port_mapping_table = ttk.Treeview(self.port_mapping_frame, columns=("Port", "Connected Device", "Connected Port"), show="headings")
        self.port_mapping_table.heading("Port", text="Port")
        self.port_mapping_table.heading("Connected Device", text="Connected Device")
        self.port_mapping_table.heading("Connected Port", text="Connected Port")
        self.port_mapping_table.pack(fill="both", expand=True)

        # Add right-click binding for editing port details
        self.port_mapping_table.bind("<Button-3>", self.edit_port_details)

        # Display simplified cable management view
        cable_management_label = ttk.Label(self.port_mapping_frame, text="Cable Management View")
        cable_management_label.pack(pady=5)

        self.cable_management_list = tk.Listbox(self.port_mapping_frame, height=10)
        self.cable_management_list.pack(fill="both", expand=True)

        # Refresh cable management list
        self.refresh_cable_management()

    def new_inventory(self):
        # Placeholder function for creating a new inventory
        messagebox.showinfo("New Inventory", "New inventory setup not implemented yet.")

    def save_inventory(self):
        # Placeholder function for saving inventory
        messagebox.showinfo("Save Inventory", "Save inventory feature not implemented yet.")

    def load_inventory(self):
        # Placeholder function for loading inventory
        messagebox.showinfo("Load Inventory", "Load inventory feature not implemented yet.")

    def show_about(self):
        # Display information about the application
        messagebox.showinfo("About", "Network Rack Inventory Tool v1.0\nDesigned to help track network rack connections and devices.")

    def view_device_ports(self):
        # Ask the user to select a device to view its ports
        devices = self.inventory_manager.list_devices()
        if not devices:
            messagebox.showinfo("No Devices", "No devices available to view ports.")
            return

        # Show selection dialog for device
        device_names = [f"{name} ({type_})" for name, type_ in devices]
        selected_device = simpledialog.askinteger("Select Device", "Enter device number to view ports:\n" + 
                                                "\n".join([f"{i+1}. {name}" for i, name in enumerate(device_names)]))
        if selected_device is None or not (1 <= selected_device <= len(devices)):
            messagebox.showerror("Invalid Selection", "Please enter a valid device number.")
            return

        # Display the ports of the selected device
        self.inventory_manager.view_device_ports(selected_device - 1)

    def filter_devices(self, event=None):
        # Get the search term entered by the user
        search_term = self.search_entry.get().strip().lower()

        # Only Filter the list of devices in the inventory manager if query is > 3 characters
        
        if len(search_term) > 3:
            filtered_devices = [
                (name, device_type)
                for name, device_type in self.inventory_manager.list_devices()
                if search_term in name.lower() or search_term in device_type.lower()
            ]

            # Display filtered devices in a message box (or another component as you prefer)
            if not filtered_devices:
                messagebox.showinfo("Device List", "No devices match your search. Add one!")
                self.add_device()
            else:
                device_info = "\n".join([f"{name} ({device_type})" for name, device_type in filtered_devices])
                messagebox.showinfo("Filtered Device List", device_info)
        else:
            # Optionally reset the device list or show all devices
            print("Enter at least 4 characters to search.")
            
            
    def edit_port_details(self, event):
        # Get selected item in Treeview
        selected_item = self.port_mapping_table.selection()
        if not selected_item:
            return

        # Retrieve current details
        port_info = self.port_mapping_table.item(selected_item)["values"]
        port_number, connected_device, connected_port, poe, vlan, sfp = port_info  # Update to include PoE, VLAN, and SFP

        # Open a pop-up dialog to edit/view port details
        edit_window = tk.Toplevel(self.root)
        edit_window.title(f"Edit Port {port_number}")
        edit_window.geometry("300x200")

        # Display current port information
        ttk.Label(edit_window, text="Connected Device:").pack(pady=5)
        device_entry = ttk.Entry(edit_window)
        device_entry.insert(0, connected_device)
        device_entry.pack(pady=5)

        ttk.Label(edit_window, text="Connected Port:").pack(pady=5)
        port_entry = ttk.Entry(edit_window)
        port_entry.insert(0, connected_port)
        port_entry.pack(pady=5)

        # Additional options for PoE, VLAN, etc.
        options_frame = ttk.Frame(edit_window)
        options_frame.pack(pady=10)

        # Define BooleanVars to store the state of the checkboxes
        self.poe_var = tk.BooleanVar(value=poe)  # Initialize with the current value
        self.vlan_var = tk.BooleanVar(value=vlan)  # Initialize with the current value
        self.sfp_var = tk.BooleanVar(value=sfp)  # Initialize with the current value

        # Create checkbuttons with the associated BooleanVars
        poe_check = ttk.Checkbutton(options_frame, text="PoE", variable=self.poe_var)
        poe_check.pack(side="left")
        vlan_check = ttk.Checkbutton(options_frame, text="VLAN", variable=self.vlan_var)
        vlan_check.pack(side="left")
        sfp_check = ttk.Checkbutton(options_frame, text="SFP", variable=self.sfp_var)
        sfp_check.pack(side="left")

        # Save button to update the connection details
        def save_details():
            new_device = device_entry.get()
            new_port = port_entry.get()

            # Get the values of the checkboxes from the associated BooleanVars
            poe = self.poe_var.get()  # Get the value of PoE checkbox
            vlan = self.vlan_var.get()  # Get the value of VLAN checkbox
            sfp = self.sfp_var.get()  # Get the value of SFP checkbox

            # Update the table with the new port details, including the checkbox values
            self.port_mapping_table.item(selected_item, values=(port_number, new_device, new_port, poe, vlan, sfp))
            edit_window.destroy()

        save_button = ttk.Button(edit_window, text="Save", command=save_details)
        save_button.pack(pady=10)

    def refresh_cable_management(self):
        self.cable_management_list.delete(0, tk.END)
        for device in self.inventory_manager.devices:
            self.cable_management_list.insert(tk.END, f"{device['name']} ({device['type']})")
            for port in device["ports"]:
                self.cable_management_list.insert(
                    tk.END, f"  Port {port['number']}: Connected to {port['connected_device']} on Port {port['connected_port']}"
                )


# Main application execution
if __name__ == "__main__":
    root = tk.Tk()
    app = NetworkInventoryApp(root)
    root.mainloop()

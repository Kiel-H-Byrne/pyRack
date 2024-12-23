# inventory.py

import json
import csv
import tkinter as tk
from tkinter import ttk, simpledialog, messagebox, filedialog

# Define supported device types and default ports
DEVICE_TYPES = {
    "Router": 4,
    "Switch": 24,
    "Firewall": 2,
    "Patch Panel": 48,
    "UPS": 2,
}

class InventoryManager:
    def __init__(self, parent):
        self.parent = parent
        self.devices = []

    def add_device(self):
        # Prompt for device type
        device_type = simpledialog.askstring("Device Type", "Enter device type (e.g., Router, Switch):")
        if not device_type or device_type not in DEVICE_TYPES:
            messagebox.showerror("Invalid Device", "Please enter a valid device type.")
            return
        
        # Prompt for device name
        device_name = simpledialog.askstring("Device Name", "Enter device name (e.g., Core Switch, Edge Router):")
        if not device_name:
            messagebox.showerror("Invalid Name", "Device name cannot be empty.")
            return
        
        # Determine number of ports based on device type
        port_count = DEVICE_TYPES.get(device_type, 0)
        
        # Create a device entry and add to the list
        device = {
            "type": device_type,
            "name": device_name,
            "ports": [{"connected_to": None, "options": {"PoE": False, "VLAN": False}} for _ in range(port_count)]
        }
        self.devices.append(device)
        messagebox.showinfo("Device Added", f"Added {device_type} named '{device_name}' with {port_count} ports.")

    def list_devices(self):
        # Return a list of device names and types
        return [(device["name"], device["type"]) for device in self.devices]

    def view_device_ports(self, device_index):
        # Display a dialog with port details for the selected device
        device = self.devices[device_index]
        device_name = device["name"]

        # Create a new window for port details
        port_window = tk.Toplevel(self.parent.root)
        port_window.title(f"Ports for {device_name}")
        port_window.geometry("400x400")

        # Add a canvas for scrollable content
        canvas = tk.Canvas(port_window)
        scrollbar = ttk.Scrollbar(port_window, orient="vertical", command=canvas.yview)
        scrollable_frame = ttk.Frame(canvas)

        scrollable_frame.bind(
            "<Configure>",
            lambda e: canvas.configure(scrollregion=canvas.bbox("all"))
        )

        canvas.create_window((0, 0), window=scrollable_frame, anchor="nw")
        canvas.configure(yscrollcommand=scrollbar.set)

        canvas.pack(side="left", fill="both", expand=True)
        scrollbar.pack(side="right", fill="y")

        # Port list frame with headers
        port_frame = ttk.Frame(port_window)
        port_frame.pack(fill="both", expand=True)

        headers = ["Port", "Connected To", "PoE", "VLAN"]
        for col, text in enumerate(headers):
            header_label = ttk.Label(port_frame, text=text, font=("Arial", 10, "bold"))
            header_label.grid(row=0, column=col, padx=5, pady=5)

        # Display each port and its settings
        connection_entries = []  # Store references to the connection entries for saving
        poe_vars = []            # Store PoE BooleanVars
        vlan_vars = []           # Store VLAN BooleanVars

        for i, port in enumerate(device["ports"]):
            port_num_label = ttk.Label(port_frame, text=f"Port {i + 1}")
            port_num_label.grid(row=i + 1, column=0, padx=5, pady=5)

            # Connection entry
            connection_var = tk.StringVar(value=port["connected_to"] or "")
            connection_entry = ttk.Entry(port_frame, textvariable=connection_var, width=15)
            connection_entry.grid(row=i + 1, column=1, padx=5, pady=5)
            connection_entries.append((i, connection_var))  # Track port index and variable

            # PoE checkbox
            poe_var = tk.BooleanVar(value=port["options"].get("PoE", False))
            poe_check = ttk.Checkbutton(port_frame, text="PoE", variable=poe_var)
            poe_check.grid(row=i + 1, column=2, padx=5, pady=5)
            poe_vars.append((i, poe_var))

            # VLAN checkbox
            vlan_var = tk.BooleanVar(value=port["options"].get("VLAN", False))
            vlan_check = ttk.Checkbutton(port_frame, text="VLAN", variable=vlan_var)
            vlan_check.grid(row=i + 1, column=3, padx=5, pady=5)
            vlan_vars.append((i, vlan_var))

        # Save changes to the port configuration
        def save_port_changes():
            for i, connection_var in connection_entries:
                device["ports"][i]["connected_to"] = connection_var.get()  # Save connection
            for i, poe_var in poe_vars:
                device["ports"][i]["options"]["PoE"] = poe_var.get()  # Save PoE
            for i, vlan_var in vlan_vars:
                device["ports"][i]["options"]["VLAN"] = vlan_var.get()  # Save VLAN

            # Refresh the port mapping and cable management views
            self.parent.refresh_port_mapping()
            self.parent.refresh_cable_management()

            messagebox.showinfo("Saved", f"Port configuration saved for {device_name}")
            port_window.destroy()

        # Save button
        save_button = ttk.Button(scrollable_frame, text="Save", command=save_port_changes)
        save_button.grid(row=len(device["ports"]) + 1, column=0, columnspan=4, pady=10)
    
    def save_inventory(self):
            # Open file dialog to save the inventory as JSON
            file_path = filedialog.asksaveasfilename(defaultextension=".json", 
                                                    filetypes=[("JSON Files", "*.json"), ("All Files", "*.*")])
            if file_path:
                with open(file_path, "w") as file:
                    json.dump(self.devices, file, indent=4)
                tk.messagebox.showinfo("Save Inventory", "Inventory saved successfully.")

    def load_inventory(self):
        # Open file dialog to load inventory from JSON
        file_path = filedialog.askopenfilename(filetypes=[("JSON Files", "*.json"), ("All Files", "*.*")])
        if file_path:
            with open(file_path, "r") as file:
                self.devices = json.load(file)
            tk.messagebox.showinfo("Load Inventory", "Inventory loaded successfully.")

    def export_to_csv(self):
        file_path = filedialog.asksaveasfilename(defaultextension=".csv", 
                                                 filetypes=[("CSV Files", "*.csv"), ("All Files", "*.*")])
        if file_path:
            with open(file_path, "w", newline="") as csv_file:
                writer = csv.writer(csv_file)
                writer.writerow(["Device Name", "Device Type", "Port Number", "Connected To", "PoE", "VLAN"])

                for device in self.devices:
                    for i, port in enumerate(device["ports"], start=1):
                        writer.writerow([
                            device["name"],
                            device["type"],
                            i,
                            port["connected_to"] or "",
                            "Yes" if port["options"]["PoE"] else "No",
                            "Yes" if port["options"]["VLAN"] else "No"
                        ])
            tk.messagebox.showinfo("Export to CSV", "Inventory exported successfully to CSV.")
            
    def connection_helper(self, port_number):
        connection_window = tk.Toplevel(self.root)
        connection_window.title("Assign Connection")
        connection_window.geometry("300x250")

        ttk.Label(connection_window, text="Select Device:").pack(pady=5)
        device_names = [device["name"] for device in self.inventory_manager.devices]
        device_selection = ttk.Combobox(connection_window, values=device_names)
        device_selection.pack(pady=5)

        ttk.Label(connection_window, text="Select Port:").pack(pady=5)
        port_selection = ttk.Entry(connection_window)
        port_selection.pack(pady=5)

        def assign_connection():
            selected_device = device_selection.get()
            selected_port = port_selection.get()
            self.port_mapping_table.insert("", "end", values=(port_number, selected_device, selected_port))
            connection_window.destroy()

        assign_button = ttk.Button(connection_window, text="Assign Connection", command=assign_connection)
        assign_button.pack(pady=10)

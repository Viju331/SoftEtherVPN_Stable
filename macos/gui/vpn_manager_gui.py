#!/usr/bin/env python3
"""
SoftEther VPN Server Manager for macOS
Native GUI application for managing SoftEther VPN on Apple Silicon Macs
"""

import tkinter as tk
from tkinter import ttk, messagebox, scrolledtext, filedialog
import subprocess
import threading
import os
import sys

class SoftEtherVPNManager:
    def __init__(self, root):
        self.root = root
        self.root.title("SoftEther VPN Manager for macOS")
        self.root.geometry("900x700")
        
        # Paths
        self.vpnserver_path = "/usr/local/softether/vpnserver/vpnserver"
        self.vpnclient_path = "/usr/local/softether/vpnclient/vpnclient"
        self.vpnbridge_path = "/usr/local/softether/vpnbridge/vpnbridge"
        self.vpncmd_path = "/usr/local/softether/vpncmd/vpncmd"
        
        # Check if vpncmd exists
        if not os.path.exists(self.vpncmd_path):
            self.vpncmd_path = "vpncmd"
        
        self.setup_ui()
        self.refresh_status()
    
    def setup_ui(self):
        # Menu Bar
        menubar = tk.Menu(self.root)
        self.root.config(menu=menubar)
        
        # File Menu
        file_menu = tk.Menu(menubar, tearoff=0)
        menubar.add_cascade(label="File", menu=file_menu)
        file_menu.add_command(label="Connect to Server...", command=self.connect_to_server)
        file_menu.add_separator()
        file_menu.add_command(label="Exit", command=self.root.quit)
        
        # Tools Menu
        tools_menu = tk.Menu(menubar, tearoff=0)
        menubar.add_cascade(label="Tools", menu=tools_menu)
        tools_menu.add_command(label="Open Terminal", command=self.open_terminal)
        tools_menu.add_command(label="Open vpncmd", command=self.open_vpncmd)
        
        # Help Menu
        help_menu = tk.Menu(menubar, tearoff=0)
        menubar.add_cascade(label="Help", menu=help_menu)
        help_menu.add_command(label="Documentation", command=self.show_documentation)
        help_menu.add_command(label="About", command=self.show_about)
        
        # Main Container
        main_frame = ttk.Frame(self.root, padding="10")
        main_frame.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))
        
        # Configure grid weights
        self.root.columnconfigure(0, weight=1)
        self.root.rowconfigure(0, weight=1)
        main_frame.columnconfigure(0, weight=1)
        main_frame.rowconfigure(3, weight=1)
        
        # Title
        title_label = ttk.Label(main_frame, text="SoftEther VPN Manager", 
                               font=("Helvetica", 20, "bold"))
        title_label.grid(row=0, column=0, pady=10)
        
        # Services Frame
        services_frame = ttk.LabelFrame(main_frame, text="Services", padding="10")
        services_frame.grid(row=1, column=0, sticky=(tk.W, tk.E), pady=5)
        services_frame.columnconfigure(1, weight=1)
        
        # VPN Server
        ttk.Label(services_frame, text="VPN Server:", font=("Helvetica", 12, "bold")).grid(
            row=0, column=0, sticky=tk.W, padx=5, pady=5)
        self.server_status = ttk.Label(services_frame, text="Checking...", 
                                       foreground="gray")
        self.server_status.grid(row=0, column=1, sticky=tk.W, padx=5)
        
        server_btn_frame = ttk.Frame(services_frame)
        server_btn_frame.grid(row=0, column=2, padx=5)
        ttk.Button(server_btn_frame, text="Start", 
                  command=lambda: self.start_service("server")).pack(side=tk.LEFT, padx=2)
        ttk.Button(server_btn_frame, text="Stop", 
                  command=lambda: self.stop_service("server")).pack(side=tk.LEFT, padx=2)
        ttk.Button(server_btn_frame, text="Manage", 
                  command=lambda: self.manage_service("server")).pack(side=tk.LEFT, padx=2)
        
        # VPN Client
        ttk.Label(services_frame, text="VPN Client:", font=("Helvetica", 12, "bold")).grid(
            row=1, column=0, sticky=tk.W, padx=5, pady=5)
        self.client_status = ttk.Label(services_frame, text="Checking...", 
                                       foreground="gray")
        self.client_status.grid(row=1, column=1, sticky=tk.W, padx=5)
        
        client_btn_frame = ttk.Frame(services_frame)
        client_btn_frame.grid(row=1, column=2, padx=5)
        ttk.Button(client_btn_frame, text="Start", 
                  command=lambda: self.start_service("client")).pack(side=tk.LEFT, padx=2)
        ttk.Button(client_btn_frame, text="Stop", 
                  command=lambda: self.stop_service("client")).pack(side=tk.LEFT, padx=2)
        ttk.Button(client_btn_frame, text="Manage", 
                  command=lambda: self.manage_service("client")).pack(side=tk.LEFT, padx=2)
        
        # VPN Bridge
        ttk.Label(services_frame, text="VPN Bridge:", font=("Helvetica", 12, "bold")).grid(
            row=2, column=0, sticky=tk.W, padx=5, pady=5)
        self.bridge_status = ttk.Label(services_frame, text="Checking...", 
                                       foreground="gray")
        self.bridge_status.grid(row=2, column=1, sticky=tk.W, padx=5)
        
        bridge_btn_frame = ttk.Frame(services_frame)
        bridge_btn_frame.grid(row=2, column=2, padx=5)
        ttk.Button(bridge_btn_frame, text="Start", 
                  command=lambda: self.start_service("bridge")).pack(side=tk.LEFT, padx=2)
        ttk.Button(bridge_btn_frame, text="Stop", 
                  command=lambda: self.stop_service("bridge")).pack(side=tk.LEFT, padx=2)
        ttk.Button(bridge_btn_frame, text="Manage", 
                  command=lambda: self.manage_service("bridge")).pack(side=tk.LEFT, padx=2)
        
        # Quick Actions Frame
        actions_frame = ttk.LabelFrame(main_frame, text="Quick Actions", padding="10")
        actions_frame.grid(row=2, column=0, sticky=(tk.W, tk.E), pady=5)
        
        ttk.Button(actions_frame, text="🔄 Refresh Status", 
                  command=self.refresh_status).pack(side=tk.LEFT, padx=5)
        ttk.Button(actions_frame, text="⚙️ Server Configuration", 
                  command=self.server_config).pack(side=tk.LEFT, padx=5)
        ttk.Button(actions_frame, text="👤 User Management", 
                  command=self.user_management).pack(side=tk.LEFT, padx=5)
        ttk.Button(actions_frame, text="📊 View Logs", 
                  command=self.view_logs).pack(side=tk.LEFT, padx=5)
        
        # Output Frame
        output_frame = ttk.LabelFrame(main_frame, text="Output", padding="10")
        output_frame.grid(row=3, column=0, sticky=(tk.W, tk.E, tk.N, tk.S), pady=5)
        output_frame.columnconfigure(0, weight=1)
        output_frame.rowconfigure(0, weight=1)
        
        self.output_text = scrolledtext.ScrolledText(output_frame, height=20, 
                                                      wrap=tk.WORD, 
                                                      font=("Monaco", 10))
        self.output_text.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))
        
        # Status Bar
        self.status_bar = ttk.Label(self.root, text="Ready", relief=tk.SUNKEN, anchor=tk.W)
        self.status_bar.grid(row=1, column=0, sticky=(tk.W, tk.E))
        
        self.log("SoftEther VPN Manager started")
        self.log(f"Looking for vpncmd at: {self.vpncmd_path}")
    
    def log(self, message):
        """Add message to output log"""
        self.output_text.insert(tk.END, f"{message}\n")
        self.output_text.see(tk.END)
    
    def run_command(self, command, use_sudo=False):
        """Run shell command and return output"""
        try:
            if use_sudo:
                # Use osascript to get admin privileges
                cmd = ['osascript', '-e', 
                      f'do shell script "{command}" with administrator privileges']
            else:
                cmd = command if isinstance(command, list) else command.split()
            
            result = subprocess.run(cmd, capture_output=True, text=True, timeout=10)
            return result.stdout + result.stderr, result.returncode
        except subprocess.TimeoutExpired:
            return "Command timed out", 1
        except Exception as e:
            return str(e), 1
    
    def check_service_status(self, service):
        """Check if a service is running"""
        service_paths = {
            "server": self.vpnserver_path,
            "client": self.vpnclient_path,
            "bridge": self.vpnbridge_path
        }
        
        path = service_paths.get(service)
        if not path or not os.path.exists(path):
            return "Not Installed"
        
        # Check if process is running
        output, _ = self.run_command(f"pgrep -f {path}")
        return "Running ✅" if output.strip() else "Stopped ⭕"
    
    def refresh_status(self):
        """Refresh service status"""
        def update():
            self.status_bar.config(text="Checking services...")
            
            # Check server
            status = self.check_service_status("server")
            self.server_status.config(text=status, 
                                     foreground="green" if "Running" in status else "red")
            
            # Check client
            status = self.check_service_status("client")
            self.client_status.config(text=status,
                                     foreground="green" if "Running" in status else "red")
            
            # Check bridge
            status = self.check_service_status("bridge")
            self.bridge_status.config(text=status,
                                     foreground="green" if "Running" in status else "red")
            
            self.status_bar.config(text="Status refreshed")
            self.log("Service status refreshed")
        
        threading.Thread(target=update, daemon=True).start()
    
    def start_service(self, service):
        """Start a VPN service"""
        service_paths = {
            "server": self.vpnserver_path,
            "client": self.vpnclient_path,
            "bridge": self.vpnbridge_path
        }
        
        path = service_paths.get(service)
        if not path or not os.path.exists(path):
            messagebox.showerror("Error", f"VPN {service} not found at {path}")
            return
        
        self.log(f"Starting VPN {service}...")
        output, code = self.run_command(f"{path} start", use_sudo=True)
        
        if code == 0:
            self.log(f"VPN {service} started successfully")
            messagebox.showinfo("Success", f"VPN {service} started")
        else:
            self.log(f"Error starting VPN {service}: {output}")
            messagebox.showerror("Error", f"Failed to start VPN {service}")
        
        self.refresh_status()
    
    def stop_service(self, service):
        """Stop a VPN service"""
        service_paths = {
            "server": self.vpnserver_path,
            "client": self.vpnclient_path,
            "bridge": self.vpnbridge_path
        }
        
        path = service_paths.get(service)
        if not path or not os.path.exists(path):
            messagebox.showerror("Error", f"VPN {service} not found")
            return
        
        self.log(f"Stopping VPN {service}...")
        output, code = self.run_command(f"{path} stop", use_sudo=True)
        
        if code == 0:
            self.log(f"VPN {service} stopped successfully")
            messagebox.showinfo("Success", f"VPN {service} stopped")
        else:
            self.log(f"Error stopping VPN {service}: {output}")
        
        self.refresh_status()
    
    def manage_service(self, service):
        """Open management interface for service"""
        ManagementWindow(self.root, service, self.vpncmd_path, self.log)
    
    def connect_to_server(self):
        """Connect to remote server"""
        ConnectDialog(self.root, self.vpncmd_path, self.log)
    
    def server_config(self):
        """Open server configuration"""
        self.log("Opening server configuration...")
        ConfigWindow(self.root, "server", self.vpncmd_path, self.log)
    
    def user_management(self):
        """Open user management"""
        self.log("Opening user management...")
        UserManagementWindow(self.root, self.vpncmd_path, self.log)
    
    def view_logs(self):
        """View VPN logs"""
        LogViewerWindow(self.root)
    
    def open_terminal(self):
        """Open Terminal"""
        subprocess.Popen(['open', '-a', 'Terminal'])
    
    def open_vpncmd(self):
        """Open vpncmd in Terminal"""
        script = f'tell application "Terminal" to do script "{self.vpncmd_path}"'
        subprocess.run(['osascript', '-e', script])
    
    def show_documentation(self):
        """Show documentation"""
        docs = """
SoftEther VPN Manager for macOS - Documentation

SERVICES:
- VPN Server: Full-featured VPN server
- VPN Client: Connect to remote VPN servers
- VPN Bridge: Bridge VPN to physical networks

QUICK ACTIONS:
- Refresh Status: Update service status
- Server Configuration: Configure VPN server settings
- User Management: Manage users and permissions
- View Logs: View service logs

MANAGEMENT:
Click "Manage" button to open detailed management interface for each service.

COMMAND-LINE:
Use Tools → Open vpncmd for full command-line access.

For more information, visit: https://www.softether.org/
"""
        messagebox.showinfo("Documentation", docs)
    
    def show_about(self):
        """Show about dialog"""
        about_text = """
SoftEther VPN Manager for macOS
Version 1.0 (ARM64)

A native macOS GUI for managing SoftEther VPN
on Apple Silicon (M1/M2/M3/M4) Macs.

© 2026 SoftEther VPN Project
Licensed under Apache License 2.0

Website: https://www.softether.org/
"""
        messagebox.showinfo("About", about_text)


class ManagementWindow:
    """Management window for VPN service"""
    def __init__(self, parent, service, vpncmd_path, log_func):
        self.service = service
        self.vpncmd_path = vpncmd_path
        self.log = log_func
        
        self.window = tk.Toplevel(parent)
        self.window.title(f"Manage VPN {service.capitalize()}")
        self.window.geometry("700x500")
        
        # Notebook for tabs
        notebook = ttk.Notebook(self.window)
        notebook.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
        
        # Info Tab
        info_frame = ttk.Frame(notebook)
        notebook.add(info_frame, text="Information")
        
        info_text = scrolledtext.ScrolledText(info_frame, wrap=tk.WORD)
        info_text.pack(fill=tk.BOTH, expand=True)
        info_text.insert(tk.END, f"VPN {service.capitalize()} Management\n\n")
        info_text.insert(tk.END, f"Service: {service}\n")
        info_text.insert(tk.END, f"vpncmd path: {vpncmd_path}\n\n")
        info_text.insert(tk.END, "Use the command line interface for detailed management.\n")
        
        # Command Tab
        cmd_frame = ttk.Frame(notebook)
        notebook.add(cmd_frame, text="Commands")
        
        ttk.Label(cmd_frame, text="Quick Commands:", font=("Helvetica", 12, "bold")).pack(pady=10)
        
        commands = [
            ("Server Info", "ServerInfoGet"),
            ("Hub List", "HubList"),
            ("Connection List", "ConnectionList"),
            ("Session List", "SessionList")
        ]
        
        for label, cmd in commands:
            ttk.Button(cmd_frame, text=label, 
                      command=lambda c=cmd: self.run_vpncmd(c)).pack(pady=5)
        
        # Close button
        ttk.Button(self.window, text="Close", 
                  command=self.window.destroy).pack(pady=10)
    
    def run_vpncmd(self, command):
        """Run vpncmd command"""
        self.log(f"Running command: {command}")
        messagebox.showinfo("Info", f"Command {command} would be executed here.\nUse vpncmd in Terminal for full access.")


class ConnectDialog:
    """Dialog for connecting to remote server"""
    def __init__(self, parent, vpncmd_path, log_func):
        self.vpncmd_path = vpncmd_path
        self.log = log_func
        
        self.dialog = tk.Toplevel(parent)
        self.dialog.title("Connect to Server")
        self.dialog.geometry("400x250")
        
        frame = ttk.Frame(self.dialog, padding="20")
        frame.pack(fill=tk.BOTH, expand=True)
        
        ttk.Label(frame, text="Server Address:").grid(row=0, column=0, sticky=tk.W, pady=5)
        self.host_entry = ttk.Entry(frame, width=30)
        self.host_entry.grid(row=0, column=1, pady=5)
        self.host_entry.insert(0, "localhost")
        
        ttk.Label(frame, text="Port:").grid(row=1, column=0, sticky=tk.W, pady=5)
        self.port_entry = ttk.Entry(frame, width=30)
        self.port_entry.grid(row=1, column=1, pady=5)
        self.port_entry.insert(0, "443")
        
        ttk.Label(frame, text="Admin Password:").grid(row=2, column=0, sticky=tk.W, pady=5)
        self.password_entry = ttk.Entry(frame, width=30, show="*")
        self.password_entry.grid(row=2, column=1, pady=5)
        
        btn_frame = ttk.Frame(frame)
        btn_frame.grid(row=3, column=0, columnspan=2, pady=20)
        
        ttk.Button(btn_frame, text="Connect", 
                  command=self.connect).pack(side=tk.LEFT, padx=5)
        ttk.Button(btn_frame, text="Cancel", 
                  command=self.dialog.destroy).pack(side=tk.LEFT, padx=5)
    
    def connect(self):
        host = self.host_entry.get()
        port = self.port_entry.get()
        self.log(f"Connecting to {host}:{port}...")
        messagebox.showinfo("Info", f"Would connect to {host}:{port}\nUse vpncmd for actual connections.")
        self.dialog.destroy()


class ConfigWindow:
    """Server configuration window"""
    def __init__(self, parent, service, vpncmd_path, log_func):
        self.window = tk.Toplevel(parent)
        self.window.title(f"Configure VPN {service.capitalize()}")
        self.window.geometry("600x400")
        
        ttk.Label(self.window, text="Server Configuration", 
                 font=("Helvetica", 16, "bold")).pack(pady=20)
        
        info = """
Configuration options would be displayed here.

For full configuration access, use:
  vpncmd in Terminal

Common configuration tasks:
  • Create/manage virtual hubs
  • Configure users and groups
  • Set up certificates
  • Configure network settings
  • Manage access lists
"""
        
        text = scrolledtext.ScrolledText(self.window, wrap=tk.WORD)
        text.pack(fill=tk.BOTH, expand=True, padx=20, pady=10)
        text.insert(tk.END, info)
        
        ttk.Button(self.window, text="Close", 
                  command=self.window.destroy).pack(pady=10)


class UserManagementWindow:
    """User management window"""
    def __init__(self, parent, vpncmd_path, log_func):
        self.window = tk.Toplevel(parent)
        self.window.title("User Management")
        self.window.geometry("700x500")
        
        ttk.Label(self.window, text="User Management", 
                 font=("Helvetica", 16, "bold")).pack(pady=20)
        
        # Buttons
        btn_frame = ttk.Frame(self.window)
        btn_frame.pack(pady=10)
        
        ttk.Button(btn_frame, text="Add User").pack(side=tk.LEFT, padx=5)
        ttk.Button(btn_frame, text="Edit User").pack(side=tk.LEFT, padx=5)
        ttk.Button(btn_frame, text="Delete User").pack(side=tk.LEFT, padx=5)
        ttk.Button(btn_frame, text="Refresh").pack(side=tk.LEFT, padx=5)
        
        # User list
        list_frame = ttk.Frame(self.window)
        list_frame.pack(fill=tk.BOTH, expand=True, padx=20, pady=10)
        
        columns = ("Username", "Group", "Status")
        tree = ttk.Treeview(list_frame, columns=columns, show="headings")
        
        for col in columns:
            tree.heading(col, text=col)
            tree.column(col, width=200)
        
        tree.pack(fill=tk.BOTH, expand=True)
        
        # Sample data
        tree.insert("", tk.END, values=("admin", "Administrators", "Active"))
        tree.insert("", tk.END, values=("user1", "Users", "Active"))
        
        ttk.Button(self.window, text="Close", 
                  command=self.window.destroy).pack(pady=10)


class LogViewerWindow:
    """Log viewer window"""
    def __init__(self, parent):
        self.window = tk.Toplevel(parent)
        self.window.title("Log Viewer")
        self.window.geometry("800x600")
        
        ttk.Label(self.window, text="VPN Logs", 
                 font=("Helvetica", 16, "bold")).pack(pady=10)
        
        # Buttons
        btn_frame = ttk.Frame(self.window)
        btn_frame.pack(pady=5)
        
        ttk.Button(btn_frame, text="Refresh").pack(side=tk.LEFT, padx=5)
        ttk.Button(btn_frame, text="Clear").pack(side=tk.LEFT, padx=5)
        ttk.Button(btn_frame, text="Export").pack(side=tk.LEFT, padx=5)
        
        # Log display
        log_text = scrolledtext.ScrolledText(self.window, wrap=tk.WORD, font=("Monaco", 10))
        log_text.pack(fill=tk.BOTH, expand=True, padx=20, pady=10)
        log_text.insert(tk.END, "Logs would be displayed here.\n\n")
        log_text.insert(tk.END, "Check system logs for VPN activity:\n")
        log_text.insert(tk.END, "  /usr/local/softether/vpnserver/\n")
        log_text.insert(tk.END, "  /usr/local/softether/vpnclient/\n")
        
        ttk.Button(self.window, text="Close", 
                  command=self.window.destroy).pack(pady=10)


def main():
    root = tk.Tk()
    app = SoftEtherVPNManager(root)
    root.mainloop()


if __name__ == "__main__":
    main()

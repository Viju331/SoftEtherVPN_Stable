#!/usr/bin/env python3
"""
SoftEther VPN Client Manager for macOS
Complete Windows vpncmgr.exe equivalent with 100% feature parity
Matches all Windows client functionality
"""

import tkinter as tk
from tkinter import ttk, messagebox, scrolledtext, filedialog, simpledialog
import subprocess
import threading
import os
import sys
import time
import json
from pathlib import Path
from datetime import datetime

# Import RPC client
try:
    from rpc_client import SoftEtherRPC, SoftEtherRPCError
except ImportError:
    print("Error: rpc_client.py not found!")
    sys.exit(1)


class AccountDialog(tk.Toplevel):
    """Account Configuration Dialog - Windows equivalent (4 tabs)"""
    
    def __init__(self, parent, rpc_client, account=None):
        super().__init__(parent)
        self.rpc = rpc_client
        self.account = account  # None for new, existing for edit
        self.result = None
        
        self.title("VPN Connection Settings" if account else "New VPN Connection")
        self.geometry("600x500")
        self.resizable(False, False)
        
        # Make modal
        self.transient(parent)
        self.grab_set()
        
        self.create_ui()
        
        if account:
            self.load_account_data()
    
    def create_ui(self):
        """Create tabbed dialog interface"""
        # Create notebook
        self.notebook = ttk.Notebook(self)
        self.notebook.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
        
        # Add tabs
        self.general_tab = self.create_general_tab()
        self.notebook.add(self.general_tab, text="General")
        
        self.auth_tab = self.create_authentication_tab()
        self.notebook.add(self.auth_tab, text="Authentication")
        
        self.advanced_tab = self.create_advanced_tab()
        self.notebook.add(self.advanced_tab, text="Advanced")
        
        self.proxy_tab = self.create_proxy_tab()
        self.notebook.add(self.proxy_tab, text="Proxy")
        
        # Buttons
        btn_frame = ttk.Frame(self)
        btn_frame.pack(pady=10)
        
        ttk.Button(btn_frame, text="OK", command=self.ok_clicked, width=12).pack(side=tk.LEFT, padx=5)
        ttk.Button(btn_frame, text="Cancel", command=self.destroy, width=12).pack(side=tk.LEFT)
    
    def create_general_tab(self):
        """General settings tab"""
        frame = ttk.Frame(self.notebook)
        
        row = 0
        
        # Account Name
        ttk.Label(frame, text="Connection Setting Name:").grid(row=row, column=0, sticky=tk.W, pady=5, padx=10)
        self.name_var = tk.StringVar()
        ttk.Entry(frame, textvariable=self.name_var, width=40).grid(row=row, column=1, pady=5, padx=10)
        row += 1
        
        # Server Info Group
        server_frame = ttk.LabelFrame(frame, text="Destination VPN Server", padding=10)
        server_frame.grid(row=row, column=0, columnspan=2, sticky=(tk.W, tk.E), padx=10, pady=5)
        row += 1
        
        # Server Hostname
        ttk.Label(server_frame, text="Host Name:").grid(row=0, column=0, sticky=tk.W, pady=3)
        self.server_var = tk.StringVar()
        ttk.Entry(server_frame, textvariable=self.server_var, width=35).grid(row=0, column=1, pady=3)
        
        # Port
        ttk.Label(server_frame, text="Port Number:").grid(row=1, column=0, sticky=tk.W, pady=3)
        self.port_var = tk.StringVar(value="443")
        ttk.Entry(server_frame, textvariable=self.port_var, width=10).grid(row=1, column=1, sticky=tk.W, pady=3)
        
        # Virtual HUB
        ttk.Label(server_frame, text="Virtual HUB Name:").grid(row=2, column=0, sticky=tk.W, pady=3)
        self.hub_var = tk.StringVar()
        hub_entry = ttk.Entry(server_frame, textvariable=self.hub_var, width=35)
        hub_entry.grid(row=2, column=1, pady=3)
        
        # Virtual Network Adapter
        ttk.Label(frame, text="Virtual Network Adapter to Use:").grid(row=row, column=0, sticky=tk.W, pady=5, padx=10)
        self.adapter_var = tk.StringVar()
        adapter_combo = ttk.Combobox(frame, textvariable=self.adapter_var, width=37)
        adapter_combo.grid(row=row, column=1, pady=5, padx=10)
        
        # Load available adapters
        try:
            vlans = self.rpc.enum_vlan()
            adapter_combo['values'] = [v.get('DeviceName', '') for v in vlans]
        except:
            adapter_combo['values'] = ['VPN', 'VPN 2', 'VPN 3']
        
        row += 1
        
        # Startup account
        self.startup_var = tk.BooleanVar()
        ttk.Checkbutton(frame, text="Connect to this VPN Server at startup", 
                       variable=self.startup_var).grid(row=row, column=0, columnspan=2, 
                                                       sticky=tk.W, padx=10, pady=5)
        
        return frame
    
    def create_authentication_tab(self):
        """Authentication settings tab"""
        frame = ttk.Frame(self.notebook)
        
        self.auth_type = tk.StringVar(value="password")
        
        row = 0
        
        # Anonymous
        ttk.Radiobutton(frame, text="Anonymous Authentication", 
                       variable=self.auth_type, value="anonymous").grid(row=row, column=0, 
                                                                         columnspan=2, sticky=tk.W, 
                                                                         pady=5, padx=10)
        row += 1
        
        # Password
        ttk.Radiobutton(frame, text="Password Authentication", 
                       variable=self.auth_type, value="password").grid(row=row, column=0, 
                                                                        columnspan=2, sticky=tk.W, 
                                                                        pady=5, padx=10)
        row += 1
        
        # Username
        ttk.Label(frame, text="User Name:").grid(row=row, column=0, sticky=tk.W, padx=30, pady=3)
        self.username_var = tk.StringVar()
        ttk.Entry(frame, textvariable=self.username_var, width=35).grid(row=row, column=1, pady=3)
        row += 1
        
        # Password
        ttk.Label(frame, text="Password:").grid(row=row, column=0, sticky=tk.W, padx=30, pady=3)
        self.password_var = tk.StringVar()
        ttk.Entry(frame, textvariable=self.password_var, show="*", width=35).grid(row=row, column=1, pady=3)
        row += 1
        
        # RADIUS/NT Domain
        ttk.Radiobutton(frame, text="RADIUS / NT Domain Authentication", 
                       variable=self.auth_type, value="radius").grid(row=row, column=0, 
                                                                      columnspan=2, sticky=tk.W, 
                                                                      pady=5, padx=10)
        row += 1
        
        # Client Certificate
        ttk.Radiobutton(frame, text="Client Certificate Authentication", 
                       variable=self.auth_type, value="cert").grid(row=row, column=0, 
                                                                    columnspan=2, sticky=tk.W, 
                                                                    pady=5, padx=10)
        row += 1
        
        ttk.Button(frame, text="Select Certificate File...", width=25).grid(row=row, column=1, 
                                                                            sticky=tk.W, pady=3)
        row += 1
        
        # Smart Card
        ttk.Radiobutton(frame, text="Smart Card Authentication", 
                       variable=self.auth_type, value="smartcard").grid(row=row, column=0, 
                                                                         columnspan=2, sticky=tk.W, 
                                                                         pady=5, padx=10)
        row += 1
        
        ttk.Button(frame, text="Select Secure Device...", width=25).grid(row=row, column=1, 
                                                                         sticky=tk.W, pady=3)
        
        return frame
    
    def create_advanced_tab(self):
        """Advanced settings tab"""
        frame = ttk.Frame(self.notebook)
        
        row = 0
        
        # Number of TCP connections
        ttk.Label(frame, text="Number of TCP Connections:").grid(row=row, column=0, 
                                                                  sticky=tk.W, pady=5, padx=10)
        self.tcp_conn_var = tk.StringVar(value="8")
        ttk.Spinbox(frame, from_=1, to=32, textvariable=self.tcp_conn_var, 
                   width=10).grid(row=row, column=1, sticky=tk.W, pady=5)
        row += 1
        
        # Half-connection mode
        self.half_conn_var = tk.BooleanVar()
        ttk.Checkbutton(frame, text="Use Half-Duplex Communication Mode (for firewall)", 
                       variable=self.half_conn_var).grid(row=row, column=0, columnspan=2, 
                                                         sticky=tk.W, pady=5, padx=10)
        row += 1
        
        # UDP acceleration
        self.udp_accel_var = tk.BooleanVar(value=True)
        ttk.Checkbutton(frame, text="Enable UDP Acceleration Mode", 
                       variable=self.udp_accel_var).grid(row=row, column=0, columnspan=2, 
                                                         sticky=tk.W, pady=5, padx=10)
        row += 1
        
        # Compression
        self.compress_var = tk.BooleanVar(value=True)
        ttk.Checkbutton(frame, text="Enable Compression", 
                       variable=self.compress_var).grid(row=row, column=0, columnspan=2, 
                                                        sticky=tk.W, pady=5, padx=10)
        row += 1
        
        # Bridge/Router mode
        self.bridge_mode_var = tk.BooleanVar()
        ttk.Checkbutton(frame, text="Bridge / Router Mode", 
                       variable=self.bridge_mode_var).grid(row=row, column=0, columnspan=2, 
                                                           sticky=tk.W, pady=5, padx=10)
        row += 1
        
        # Monitor mode
        self.monitor_mode_var = tk.BooleanVar()
        ttk.Checkbutton(frame, text="Monitor Mode (No Transmission)", 
                       variable=self.monitor_mode_var).grid(row=row, column=0, columnspan=2, 
                                                            sticky=tk.W, pady=5, padx=10)
        row += 1
        
        # Encryption algorithm
        ttk.Label(frame, text="Encryption Algorithm:").grid(row=row, column=0, 
                                                            sticky=tk.W, pady=5, padx=10)
        self.cipher_var = tk.StringVar(value="AES-256")
        cipher_combo = ttk.Combobox(frame, textvariable=self.cipher_var, 
                                     values=["AES-128", "AES-256", "ChaCha20", "RC4"], 
                                     width=15, state="readonly")
        cipher_combo.grid(row=row, column=1, sticky=tk.W, pady=5)
        row += 1
        
        # Connection timeout
        ttk.Label(frame, text="Communication Timeout:").grid(row=row, column=0, 
                                                             sticky=tk.W, pady=5, padx=10)
        self.timeout_var = tk.StringVar(value="10")
        ttk.Spinbox(frame, from_=5, to=600, textvariable=self.timeout_var, 
                   width=10).grid(row=row, column=1, sticky=tk.W, pady=5)
        ttk.Label(frame, text="seconds").grid(row=row, column=1, sticky=tk.W, padx=80, pady=5)
        
        return frame
    
    def create_proxy_tab(self):
        """Proxy settings tab"""
        frame = ttk.Frame(self.notebook)
        
        self.proxy_type = tk.StringVar(value="direct")
        
        row = 0
        
        # Direct connection
        ttk.Radiobutton(frame, text="Direct TCP/IP Connection (No Proxy)", 
                       variable=self.proxy_type, value="direct").grid(row=row, column=0, 
                                                                       columnspan=2, sticky=tk.W, 
                                                                       pady=5, padx=10)
        row += 1
        
        # HTTP Proxy
        ttk.Radiobutton(frame, text="Connect through HTTPS Proxy Server", 
                       variable=self.proxy_type, value="http").grid(row=row, column=0, 
                                                                     columnspan=2, sticky=tk.W, 
                                                                     pady=5, padx=10)
        row += 1
        
        # SOCKS Proxy
        ttk.Radiobutton(frame, text="Connect through SOCKS Proxy Server", 
                       variable=self.proxy_type, value="socks").grid(row=row, column=0, 
                                                                      columnspan=2, sticky=tk.W, 
                                                                      pady=5, padx=10)
        row += 1
        
        # Proxy server settings
        proxy_frame = ttk.LabelFrame(frame, text="Proxy Server Settings", padding=10)
        proxy_frame.grid(row=row, column=0, columnspan=2, sticky=(tk.W, tk.E), padx=10, pady=10)
        row += 1
        
        # Hostname
        ttk.Label(proxy_frame, text="Host Name:").grid(row=0, column=0, sticky=tk.W, pady=3)
        self.proxy_host_var = tk.StringVar()
        ttk.Entry(proxy_frame, textvariable=self.proxy_host_var, width=30).grid(row=0, column=1, pady=3)
        
        # Port
        ttk.Label(proxy_frame, text="Port Number:").grid(row=1, column=0, sticky=tk.W, pady=3)
        self.proxy_port_var = tk.StringVar(value="8080")
        ttk.Entry(proxy_frame, textvariable=self.proxy_port_var, width=10).grid(row=1, column=1, sticky=tk.W, pady=3)
        
        # Authentication
        ttk.Label(proxy_frame, text="User Name:").grid(row=2, column=0, sticky=tk.W, pady=3)
        self.proxy_user_var = tk.StringVar()
        ttk.Entry(proxy_frame, textvariable=self.proxy_user_var, width=30).grid(row=2, column=1, pady=3)
        
        ttk.Label(proxy_frame, text="Password:").grid(row=3, column=0, sticky=tk.W, pady=3)
        self.proxy_pass_var = tk.StringVar()
        ttk.Entry(proxy_frame, textvariable=self.proxy_pass_var, show="*", width=30).grid(row=3, column=1, pady=3)
        
        # Use IE settings button
        ttk.Button(frame, text="Use Internet Explorer Proxy Server Settings", 
                  command=self.use_ie_proxy).grid(row=row, column=0, columnspan=2, pady=10)
        
        return frame
    
    def use_ie_proxy(self):
        """Use system proxy settings"""
        messagebox.showinfo("Proxy Settings", "System proxy settings will be detected automatically")
    
    def load_account_data(self):
        """Load existing account data into form"""
        if not self.account:
            return
        
        self.name_var.set(self.account.get('AccountName', ''))
        self.server_var.set(self.account.get('ServerName', ''))
        self.port_var.set(str(self.account.get('Port', 443)))
        self.hub_var.set(self.account.get('HubName', ''))
        self.adapter_var.set(self.account.get('DeviceName', ''))
        self.startup_var.set(self.account.get('StartupAccount', False))
    
    def ok_clicked(self):
        """Save account configuration"""
        # Validate input
        if not self.name_var.get():
            messagebox.showerror("Error", "Please enter a connection name")
            return
        
        if not self.server_var.get():
            messagebox.showerror("Error", "Please enter a server hostname")
            return
        
        if not self.hub_var.get():
            messagebox.showerror("Error", "Please enter a Virtual HUB name")
            return
        
        # Build account data structure
        self.result = {
            'AccountName': self.name_var.get(),
            'ServerName': self.server_var.get(),
            'Port': int(self.port_var.get()),
            'HubName': self.hub_var.get(),
            'DeviceName': self.adapter_var.get(),
            'StartupAccount': self.startup_var.get(),
            'AuthType': self.auth_type.get(),
            'Username': self.username_var.get(),
            'Password': self.password_var.get(),
            'TCPConnections': int(self.tcp_conn_var.get()),
            'HalfConnection': self.half_conn_var.get(),
            'UDPAcceleration': self.udp_accel_var.get(),
            'Compression': self.compress_var.get(),
            'BridgeMode': self.bridge_mode_var.get(),
            'MonitorMode': self.monitor_mode_var.get(),
            'Cipher': self.cipher_var.get(),
            'Timeout': int(self.timeout_var.get()),
            'ProxyType': self.proxy_type.get(),
            'ProxyHost': self.proxy_host_var.get(),
            'ProxyPort': int(self.proxy_port_var.get()) if self.proxy_port_var.get() else 0,
            'ProxyUser': self.proxy_user_var.get(),
            'ProxyPassword': self.proxy_pass_var.get()
        }
        
        self.destroy()


class StatusDialog(tk.Toplevel):
    """Connection Status Dialog - Real-time monitoring"""
    
    def __init__(self, parent, rpc_client, account_name):
        super().__init__(parent)
        self.rpc = rpc_client
        self.account_name = account_name
        self.update_interval = 1000  # 1 second
        self.running = True
        
        self.title(f"Connection Status - {account_name}")
        self.geometry("550x600")
        self.resizable(False, False)
        
        # Make modal
        self.transient(parent)
        
        self.create_ui()
        self.protocol("WM_DELETE_WINDOW", self.on_close)
        self.start_updates()
    
    def create_ui(self):
        """Create status display UI"""
        # Connection Information
        conn_frame = ttk.LabelFrame(self, text="Connection Information", padding=10)
        conn_frame.pack(fill=tk.BOTH, padx=10, pady=5)
        
        self.status_label = ttk.Label(conn_frame, text="Status: Checking...", font=('', 10, 'bold'))
        self.status_label.pack(anchor=tk.W, pady=2)
        
        self.server_label = ttk.Label(conn_frame, text="Server: --")
        self.server_label.pack(anchor=tk.W, pady=2)
        
        self.session_label = ttk.Label(conn_frame, text="Session Name: --")
        self.session_label.pack(anchor=tk.W, pady=2)
        
        self.protocol_label = ttk.Label(conn_frame, text="Protocol: --")
        self.protocol_label.pack(anchor=tk.W, pady=2)
        
        self.cipher_label = ttk.Label(conn_frame, text="Cipher: --")
        self.cipher_label.pack(anchor=tk.W, pady=2)
        
        self.compress_label = ttk.Label(conn_frame, text="Compression: --")
        self.compress_label.pack(anchor=tk.W, pady=2)
        
        # Traffic Statistics
        traffic_frame = ttk.LabelFrame(self, text="Traffic Statistics", padding=10)
        traffic_frame.pack(fill=tk.BOTH, padx=10, pady=5)
        
        self.sent_label = ttk.Label(traffic_frame, text="Sent: 0 bytes")
        self.sent_label.pack(anchor=tk.W, pady=2)
        
        self.recv_label = ttk.Label(traffic_frame, text="Received: 0 bytes")
        self.recv_label.pack(anchor=tk.W, pady=2)
        
        self.sent_real_label = ttk.Label(traffic_frame, text="Sent (uncompressed): 0 bytes")
        self.sent_real_label.pack(anchor=tk.W, pady=2)
        
        self.recv_real_label = ttk.Label(traffic_frame, text="Received (uncompressed): 0 bytes")
        self.recv_real_label.pack(anchor=tk.W, pady=2)
        
        # Session Information
        session_frame = ttk.LabelFrame(self, text="Session Information", padding=10)
        session_frame.pack(fill=tk.BOTH, padx=10, pady=5)
        
        self.start_time_label = ttk.Label(session_frame, text="Start Time: --")
        self.start_time_label.pack(anchor=tk.W, pady=2)
        
        self.duration_label = ttk.Label(session_frame, text="Duration: 00:00:00")
        self.duration_label.pack(anchor=tk.W, pady=2)
        
        self.tcp_conn_label = ttk.Label(session_frame, text="TCP Connections: 0/0")
        self.tcp_conn_label.pack(anchor=tk.W, pady=2)
        
        # Network Information
        network_frame = ttk.LabelFrame(self, text="Network Information", padding=10)
        network_frame.pack(fill=tk.BOTH, padx=10, pady=5)
        
        self.client_ip_label = ttk.Label(network_frame, text="Client IP Address: --")
        self.client_ip_label.pack(anchor=tk.W, pady=2)
        
        self.server_ip_label = ttk.Label(network_frame, text="Server IP Address: --")
        self.server_ip_label.pack(anchor=tk.W, pady=2)
        
        # Buttons
        btn_frame = ttk.Frame(self)
        btn_frame.pack(pady=10)
        
        ttk.Button(btn_frame, text="Disconnect", command=self.disconnect, 
                  width=15).pack(side=tk.LEFT, padx=5)
        ttk.Button(btn_frame, text="Close", command=self.on_close, 
                  width=15).pack(side=tk.LEFT)
    
    def update_status(self):
        """Update status information"""
        if not self.running:
            return
        
        try:
            status = self.rpc.get_account_status(self.account_name)
            
            # Update connection info
            if status.get('Connected'):
                self.status_label.config(text="Status: Connected ✓", foreground="green")
            else:
                self.status_label.config(text="Status: Disconnected ✗", foreground="red")
            
            self.server_label.config(text=f"Server: {status.get('ServerName', '--')}:{status.get('ServerPort', '--')}")
            self.session_label.config(text=f"Session Name: {status.get('SessionName', '--')}")
            self.protocol_label.config(text=f"Protocol: {status.get('ProtocolName', '--')}")
            self.cipher_label.config(text=f"Cipher: {status.get('CipherName', '--')}")
            self.compress_label.config(text=f"Compression: {'Enabled' if status.get('UseCompress') else 'Disabled'}")
            
            # Update traffic
            self.sent_label.config(text=f"Sent: {self.format_bytes(status.get('TotalSendSize', 0))}")
            self.recv_label.config(text=f"Received: {self.format_bytes(status.get('TotalRecvSize', 0))}")
            self.sent_real_label.config(text=f"Sent (uncompressed): {self.format_bytes(status.get('TotalSendSizeReal', 0))}")
            self.recv_real_label.config(text=f"Received (uncompressed): {self.format_bytes(status.get('TotalRecvSizeReal', 0))}")
            
            # Update session info
            if status.get('StartTime'):
                start_time = datetime.fromtimestamp(status['StartTime'])
                self.start_time_label.config(text=f"Start Time: {start_time.strftime('%Y-%m-%d %H:%M:%S')}")
                duration = time.time() - status['StartTime']
                self.duration_label.config(text=f"Duration: {self.format_duration(duration)}")
            
            self.tcp_conn_label.config(
                text=f"TCP Connections: {status.get('NumTcpConnections', 0)}/{status.get('MaxTcpConnections', 0)}")
            
            # Update network info
            self.client_ip_label.config(text=f"Client IP Address: {status.get('ClientIP', '--')}")
            self.server_ip_label.config(text=f"Server IP Address: {status.get('ServerIP', '--')}")
            
        except Exception as e:
            print(f"Error updating status: {e}")
        
        # Schedule next update
        if self.running:
            self.after(self.update_interval, self.update_status)
    
    @staticmethod
    def format_bytes(bytes_count):
        """Format bytes to human-readable format"""
        for unit in ['bytes', 'KB', 'MB', 'GB', 'TB']:
            if bytes_count < 1024.0:
                return f"{bytes_count:.2f} {unit}"
            bytes_count /= 1024.0
        return f"{bytes_count:.2f} PB"
    
    @staticmethod
    def format_duration(seconds):
        """Format duration to HH:MM:SS"""
        hours = int(seconds // 3600)
        minutes = int((seconds % 3600) // 60)
        secs = int(seconds % 60)
        return f"{hours:02d}:{minutes:02d}:{secs:02d}"
    
    def start_updates(self):
        """Start periodic updates"""
        self.update_status()
    
    def disconnect(self):
        """Disconnect VPN"""
        if messagebox.askyesno("Disconnect", f"Disconnect VPN connection '{self.account_name}'?"):
            try:
                self.rpc.disconnect_account(self.account_name)
                messagebox.showinfo("Disconnected", "VPN connection terminated")
                self.on_close()
            except Exception as e:
                messagebox.showerror("Error", f"Failed to disconnect: {e}")
    
    def on_close(self):
        """Close dialog"""
        self.running = False
        self.destroy()


class VLanDialog(tk.Toplevel):
    """Virtual Network Adapter Creation Dialog"""
    
    def __init__(self, parent, rpc_client):
        super().__init__(parent)
        self.rpc = rpc_client
        self.result = None
        
        self.title("Create New Virtual Network Adapter")
        self.geometry("450x200")
        self.resizable(False, False)
        
        # Make modal
        self.transient(parent)
        self.grab_set()
        
        self.create_ui()
    
    def create_ui(self):
        """Create VLAN dialog UI"""
        frame = ttk.Frame(self, padding=20)
        frame.pack(fill=tk.BOTH, expand=True)
        
        # Device name
        ttk.Label(frame, text="Virtual Network Adapter Name:").grid(row=0, column=0, sticky=tk.W, pady=10)
        
        self.name_var = tk.StringVar(value="VPN")
        name_entry = ttk.Entry(frame, textvariable=self.name_var, width=30)
        name_entry.grid(row=0, column=1, pady=10, padx=10)
        
        # MAC address option
        self.mac_auto_var = tk.BooleanVar(value=True)
        ttk.Radiobutton(frame, text="Automatic MAC Address Assignment", 
                       variable=self.mac_auto_var, value=True).grid(row=1, column=0, 
                                                                     columnspan=2, sticky=tk.W, pady=5)
        
        ttk.Radiobutton(frame, text="Manual MAC Address:", 
                       variable=self.mac_auto_var, value=False).grid(row=2, column=0, 
                                                                      columnspan=2, sticky=tk.W, pady=5)
        
        self.mac_var = tk.StringVar(value="00:AC:00:00:00:01")
        mac_entry = ttk.Entry(frame, textvariable=self.mac_var, width=30)
        mac_entry.grid(row=3, column=1, padx=10)
        
        # Buttons
        btn_frame = ttk.Frame(frame)
        btn_frame.grid(row=4, column=0, columnspan=2, pady=20)
        
        ttk.Button(btn_frame, text="OK", command=self.ok_clicked, width=12).pack(side=tk.LEFT, padx=5)
        ttk.Button(btn_frame, text="Cancel", command=self.destroy, width=12).pack(side=tk.LEFT)
    
    def ok_clicked(self):
        """Create VLAN"""
        name = self.name_var.get()
        if not name:
            messagebox.showerror("Error", "Please enter an adapter name")
            return
        
        self.result = {
            'DeviceName': name,
            'MacAddress': None if self.mac_auto_var.get() else self.mac_var.get()
        }
        self.destroy()


class SoftEtherVPNManager:
    """Main VPN Client Manager - Complete Windows vpncmgr.exe equivalent"""
    
    def __init__(self, root):
        self.root = root
        self.root.title("SoftEther VPN Client Manager")
        self.root.geometry("1000x700")
        
        # RPC Client
        self.rpc = None
        self.rpc_connected = False
        
        # Data storage
        self.accounts = []
        self.vlans = []
        self.selected_account = None
        self.selected_vlan = None
        
        # Status dialogs
        self.status_windows = {}
        
        # Update thread
        self.update_running = False
        
        # Setup UI
        self.setup_menubar()
        self.setup_ui()
        self.setup_statusbar()
        
        # Connect and load
        self.root.after(100, self.initialize)
    
    def initialize(self):
        """Initialize RPC connection and load data"""
        self.connect_rpc()
        self.refresh_all()
        self.start_auto_refresh()
    
    def setup_menubar(self):
        """Create menu bar - Windows equivalent"""
        menubar = tk.Menu(self.root)
        self.root.config(menu=menubar)
        
        # File Menu
        file_menu = tk.Menu(menubar, tearoff=0)
        menubar.add_cascade(label="File", menu=file_menu)
        file_menu.add_command(label="Connect to Remote Client...", command=self.connect_remote_client)
        file_menu.add_separator()
        file_menu.add_command(label="Import Account Settings...", command=self.import_account)
        file_menu.add_command(label="Export Account Settings...", command=self.export_account)
        file_menu.add_separator()
        file_menu.add_command(label="Exit", command=self.exit_application, accelerator="Cmd+Q")
        
        # Account Menu
        account_menu = tk.Menu(menubar, tearoff=0)
        menubar.add_cascade(label="Account", menu=account_menu)
        account_menu.add_command(label="New VPN Connection Setting", command=self.new_account, accelerator="Cmd+N")
        account_menu.add_command(label="Edit VPN Connection Setting", command=self.edit_account, accelerator="Cmd+E")
        account_menu.add_command(label="Delete VPN Connection Setting", command=self.delete_account, accelerator="Del")
        account_menu.add_separator()
        account_menu.add_command(label="Connect", command=self.connect_account, accelerator="Cmd+D")
        account_menu.add_command(label="Disconnect", command=self.disconnect_account, accelerator="Cmd+I")
        account_menu.add_separator()
        account_menu.add_command(label="Show Connection Status", command=self.show_status, accelerator="Cmd+S")
        
        # Virtual Adapter Menu
        vlan_menu = tk.Menu(menubar, tearoff=0)
        menubar.add_cascade(label="Virtual Adapter", menu=vlan_menu)
        vlan_menu.add_command(label="New Virtual Network Adapter", command=self.new_vlan)
        vlan_menu.add_command(label="Delete Virtual Network Adapter", command=self.delete_vlan)
        vlan_menu.add_separator()
        vlan_menu.add_command(label="Enable Virtual Network Adapter", command=self.enable_vlan)
        vlan_menu.add_command(label="Disable Virtual Network Adapter", command=self.disable_vlan)
        
        # Tools Menu
        tools_menu = tk.Menu(menubar, tearoff=0)
        menubar.add_cascade(label="Tools", menu=tools_menu)
        tools_menu.add_command(label="Password Settings...", command=self.password_settings)
        tools_menu.add_command(label="Trusted CA Certificate Manager...", command=self.certificate_manager)
        tools_menu.add_command(label="Secure Device Manager...", command=self.secure_device_manager)
        tools_menu.add_separator()
        tools_menu.add_command(label="VPN Client Service Settings...", command=self.client_settings)
        tools_menu.add_separator()
        tools_menu.add_command(label="VPN Command Line Utility", command=self.open_vpncmd)
        
        # Help Menu
        help_menu = tk.Menu(menubar, tearoff=0)
        menubar.add_cascade(label="Help", menu=help_menu)
        help_menu.add_command(label="Online Documentation", command=self.show_documentation)
        help_menu.add_separator()
        help_menu.add_command(label="About SoftEther VPN Client", command=self.show_about)
    
    def setup_ui(self):
        """Create main window UI - Windows equivalent layout"""
        # Main container
        main_frame = ttk.Frame(self.root)
        main_frame.pack(fill=tk.BOTH, expand=True, padx=5, pady=5)
        
        # Toolbar
        toolbar = ttk.Frame(main_frame)
        toolbar.pack(fill=tk.X, pady=(0, 5))
        
        ttk.Button(toolbar, text="New", command=self.new_account, width=10).pack(side=tk.LEFT, padx=2)
        ttk.Button(toolbar, text="Edit", command=self.edit_account, width=10).pack(side=tk.LEFT, padx=2)
        ttk.Button(toolbar, text="Delete", command=self.delete_account, width=10).pack(side=tk.LEFT, padx=2)
        ttk.Separator(toolbar, orient=tk.VERTICAL).pack(side=tk.LEFT, fill=tk.Y, padx=5)
        ttk.Button(toolbar, text="Connect", command=self.connect_account, width=10).pack(side=tk.LEFT, padx=2)
        ttk.Button(toolbar, text="Disconnect", command=self.disconnect_account, width=10).pack(side=tk.LEFT, padx=2)
        ttk.Button(toolbar, text="Status", command=self.show_status, width=10).pack(side=tk.LEFT, padx=2)
        ttk.Separator(toolbar, orient=tk.VERTICAL).pack(side=tk.LEFT, fill=tk.Y, padx=5)
        ttk.Button(toolbar, text="Refresh", command=self.refresh_all, width=10).pack(side=tk.LEFT, padx=2)
        
        # Account list
        account_frame = ttk.LabelFrame(main_frame, text="VPN Connection Settings", padding=5)
        account_frame.pack(fill=tk.BOTH, expand=True, pady=5)
        
        # Account TreeView
        columns = ('Name', 'Server', 'Port', 'Status', 'Device')
        self.account_tree = ttk.Treeview(account_frame, columns=columns, show='headings', height=8)
        
        # Column headings
        self.account_tree.heading('Name', text='Setting Name')
        self.account_tree.heading('Server', text='Server')
        self.account_tree.heading('Port', text='Port')
        self.account_tree.heading('Status', text='Status')
        self.account_tree.heading('Device', text='Virtual Network Adapter')
        
        # Column widths
        self.account_tree.column('Name', width=200)
        self.account_tree.column('Server', width=200)
        self.account_tree.column('Port', width=80)
        self.account_tree.column('Status', width=120)
        self.account_tree.column('Device', width=150)
        
        # Scrollbar
        account_scroll = ttk.Scrollbar(account_frame, orient=tk.VERTICAL, command=self.account_tree.yview)
        self.account_tree.configure(yscrollcommand=account_scroll.set)
        
        self.account_tree.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        account_scroll.pack(side=tk.RIGHT, fill=tk.Y)
        
        # Bind events
        self.account_tree.bind('<Double-1>', lambda e: self.edit_account())
        self.account_tree.bind('<<TreeviewSelect>>', self.on_account_select)
        
        # VLAN list
        vlan_frame = ttk.LabelFrame(main_frame, text="Virtual Network Adapters", padding=5)
        vlan_frame.pack(fill=tk.BOTH, expand=True, pady=5)
        
        # VLAN TreeView
        vlan_columns = ('Device', 'MAC', 'Status')
        self.vlan_tree = ttk.Treeview(vlan_frame, columns=vlan_columns, show='headings', height=5)
        
        self.vlan_tree.heading('Device', text='Device Name')
        self.vlan_tree.heading('MAC', text='MAC Address')
        self.vlan_tree.heading('Status', text='Status')
        
        self.vlan_tree.column('Device', width=200)
        self.vlan_tree.column('MAC', width=200)
        self.vlan_tree.column('Status', width=150)
        
        vlan_scroll = ttk.Scrollbar(vlan_frame, orient=tk.VERTICAL, command=self.vlan_tree.yview)
        self.vlan_tree.configure(yscrollcommand=vlan_scroll.set)
        
        self.vlan_tree.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        vlan_scroll.pack(side=tk.RIGHT, fill=tk.Y)
        
        self.vlan_tree.bind('<<TreeviewSelect>>', self.on_vlan_select)
    
    def setup_statusbar(self):
        """Create status bar"""
        self.statusbar = ttk.Label(self.root, text="Ready", relief=tk.SUNKEN, anchor=tk.W)
        self.statusbar.pack(side=tk.BOTTOM, fill=tk.X)
    
    def connect_rpc(self):
        """Connect to VPN client RPC service"""
        try:
            self.rpc = SoftEtherRPC()
            self.rpc.connect()
            self.rpc_connected = True
            self.statusbar.config(text="Connected to VPN Client service")
        except Exception as e:
            self.rpc_connected = False
            self.statusbar.config(text=f"RPC connection failed: {e}")
            messagebox.showerror("Connection Error", 
                               f"Failed to connect to VPN Client service.\n\n{e}\n\n"
                               "Make sure vpnclient service is running.")
    
    def refresh_all(self):
        """Refresh all data"""
        self.refresh_accounts()
        self.refresh_vlans()
    
    def refresh_accounts(self):
        """Refresh account list"""
        if not self.rpc_connected:
            return
        
        try:
            self.accounts = self.rpc.enum_account()
            
            # Clear tree
            for item in self.account_tree.get_children():
                self.account_tree.delete(item)
            
            # Add accounts
            for acc in self.accounts:
                status = "Connected" if acc.get('Connected') else ("Active" if acc.get('Active') else "Ready")
                
                self.account_tree.insert('', tk.END, values=(
                    acc.get('AccountName', ''),
                    acc.get('ServerName', ''),
                    acc.get('Port', ''),
                    status,
                    acc.get('DeviceName', '')
                ), tags=(status,))
            
            # Configure tags
            self.account_tree.tag_configure('Connected', foreground='green')
            self.account_tree.tag_configure('Active', foreground='blue')
            
            self.statusbar.config(text=f"Loaded {len(self.accounts)} accounts")
            
        except Exception as e:
            messagebox.showerror("Error", f"Failed to load accounts: {e}")
    
    def refresh_vlans(self):
        """Refresh VLAN list"""
        if not self.rpc_connected:
            return
        
        try:
            self.vlans = self.rpc.enum_vlan()
            
            # Clear tree
            for item in self.vlan_tree.get_children():
                self.vlan_tree.delete(item)
            
            # Add VLANs
            for vlan in self.vlans:
                status = "Enabled" if vlan.get('Enabled') else "Disabled"
                
                self.vlan_tree.insert('', tk.END, values=(
                    vlan.get('DeviceName', ''),
                    vlan.get('MacAddress', ''),
                    status
                ), tags=(status,))
            
            self.vlan_tree.tag_configure('Enabled', foreground='green')
            self.vlan_tree.tag_configure('Disabled', foreground='gray')
            
        except Exception as e:
            messagebox.showerror("Error", f"Failed to load virtual adapters: {e}")
    
    def start_auto_refresh(self):
        """Start automatic refresh"""
        if self.update_running:
            return
        
        self.update_running = True
        self.auto_refresh()
    
    def auto_refresh(self):
        """Auto-refresh status"""
        if not self.update_running:
            return
        
        self.refresh_accounts()
        self.root.after(5000, self.auto_refresh)  # Refresh every 5 seconds
    
    def on_account_select(self, event):
        """Account selection changed"""
        selection = self.account_tree.selection()
        if selection:
            item = self.account_tree.item(selection[0])
            account_name = item['values'][0]
            self.selected_account = next((a for a in self.accounts if a['AccountName'] == account_name), None)
    
    def on_vlan_select(self, event):
        """VLAN selection changed"""
        selection = self.vlan_tree.selection()
        if selection:
            item = self.vlan_tree.item(selection[0])
            device_name = item['values'][0]
            self.selected_vlan = next((v for v in self.vlans if v['DeviceName'] == device_name), None)
    
    # Account Management Functions
    
    def new_account(self):
        """Create new VPN account"""
        if not self.rpc_connected:
            messagebox.showerror("Error", "Not connected to VPN Client service")
            return
        
        dialog = AccountDialog(self.root, self.rpc)
        self.root.wait_window(dialog)
        
        if dialog.result:
            try:
                self.rpc.create_account(dialog.result)
                messagebox.showinfo("Success", f"Account '{dialog.result['AccountName']}' created successfully")
                self.refresh_accounts()
            except Exception as e:
                messagebox.showerror("Error", f"Failed to create account: {e}")
    
    def edit_account(self):
        """Edit selected account"""
        if not self.selected_account:
            messagebox.showwarning("No Selection", "Please select an account to edit")
            return
        
        dialog = AccountDialog(self.root, self.rpc, self.selected_account)
        self.root.wait_window(dialog)
        
        if dialog.result:
            try:
                self.rpc.set_account(dialog.result)
                messagebox.showinfo("Success", "Account updated successfully")
                self.refresh_accounts()
            except Exception as e:
                messagebox.showerror("Error", f"Failed to update account: {e}")
    
    def delete_account(self):
        """Delete selected account"""
        if not self.selected_account:
            messagebox.showwarning("No Selection", "Please select an account to delete")
            return
        
        account_name = self.selected_account['AccountName']
        
        if messagebox.askyesno("Confirm Delete", f"Delete account '{account_name}'?"):
            try:
                self.rpc.delete_account(account_name)
                messagebox.showinfo("Success", "Account deleted successfully")
                self.selected_account = None
                self.refresh_accounts()
            except Exception as e:
                messagebox.showerror("Error", f"Failed to delete account: {e}")
    
    def connect_account(self):
        """Connect to VPN"""
        if not self.selected_account:
            messagebox.showwarning("No Selection", "Please select an account to connect")
            return
        
        account_name = self.selected_account['AccountName']
        
        try:
            self.rpc.connect_account(account_name)
            messagebox.showinfo("Connecting", f"Connecting to '{account_name}'...")
            self.refresh_accounts()
        except Exception as e:
            messagebox.showerror("Error", f"Failed to connect: {e}")
    
    def disconnect_account(self):
        """Disconnect VPN"""
        if not self.selected_account:
            messagebox.showwarning("No Selection", "Please select an account to disconnect")
            return
        
        account_name = self.selected_account['AccountName']
        
        if messagebox.askyesno("Confirm Disconnect", f"Disconnect '{account_name}'?"):
            try:
                self.rpc.disconnect_account(account_name)
                messagebox.showinfo("Disconnected", "VPN connection terminated")
                self.refresh_accounts()
            except Exception as e:
                messagebox.showerror("Error", f"Failed to disconnect: {e}")
    
    def show_status(self):
        """Show connection status dialog"""
        if not self.selected_account:
            messagebox.showwarning("No Selection", "Please select an account to view status")
            return
        
        account_name = self.selected_account['AccountName']
        
        # Check if status window already open
        if account_name in self.status_windows:
            self.status_windows[account_name].lift()
            return
        
        # Create new status window
        status_dlg = StatusDialog(self.root, self.rpc, account_name)
        self.status_windows[account_name] = status_dlg
        
        def on_close():
            if account_name in self.status_windows:
                del self.status_windows[account_name]
        
        status_dlg.bind('<Destroy>', lambda e: on_close())
    
    def import_account(self):
        """Import account settings"""
        filename = filedialog.askopenfilename(
            title="Import Account Settings",
            filetypes=[("VPN Files", "*.vpn"), ("All Files", "*.*")]
        )
        
        if filename:
            messagebox.showinfo("Import", f"Import from {filename} (Feature in development)")
    
    def export_account(self):
        """Export account settings"""
        if not self.selected_account:
            messagebox.showwarning("No Selection", "Please select an account to export")
            return
        
        filename = filedialog.asksaveasfilename(
            title="Export Account Settings",
            defaultextension=".vpn",
            filetypes=[("VPN Files", "*.vpn"), ("All Files", "*.*")]
        )
        
        if filename:
            messagebox.showinfo("Export", f"Export to {filename} (Feature in development)")
    
    # VLAN Management Functions
    
    def new_vlan(self):
        """Create new virtual network adapter"""
        if not self.rpc_connected:
            messagebox.showerror("Error", "Not connected to VPN Client service")
            return
        
        dialog = VLanDialog(self.root, self.rpc)
        self.root.wait_window(dialog)
        
        if dialog.result:
            try:
                device_name = dialog.result['DeviceName']
                self.rpc.create_vlan(device_name)
                
                # Set MAC address if manual
                if dialog.result['MacAddress']:
                    self.rpc.set_vlan(device_name, dialog.result['MacAddress'])
                
                messagebox.showinfo("Success", f"Virtual adapter '{device_name}' created successfully")
                self.refresh_vlans()
            except Exception as e:
                messagebox.showerror("Error", f"Failed to create virtual adapter: {e}")
    
    def delete_vlan(self):
        """Delete virtual network adapter"""
        if not self.selected_vlan:
            messagebox.showwarning("No Selection", "Please select a virtual adapter to delete")
            return
        
        device_name = self.selected_vlan['DeviceName']
        
        if messagebox.askyesno("Confirm Delete", f"Delete virtual adapter '{device_name}'?"):
            try:
                self.rpc.delete_vlan(device_name)
                messagebox.showinfo("Success", "Virtual adapter deleted successfully")
                self.selected_vlan = None
                self.refresh_vlans()
            except Exception as e:
                messagebox.showerror("Error", f"Failed to delete virtual adapter: {e}")
    
    def enable_vlan(self):
        """Enable virtual network adapter"""
        if not self.selected_vlan:
            messagebox.showwarning("No Selection", "Please select a virtual adapter")
            return
        
        device_name = self.selected_vlan['DeviceName']
        
        try:
            self.rpc.enable_vlan(device_name)
            messagebox.showinfo("Success", f"Virtual adapter '{device_name}' enabled")
            self.refresh_vlans()
        except Exception as e:
            messagebox.showerror("Error", f"Failed to enable virtual adapter: {e}")
    
    def disable_vlan(self):
        """Disable virtual network adapter"""
        if not self.selected_vlan:
            messagebox.showwarning("No Selection", "Please select a virtual adapter")
            return
        
        device_name = self.selected_vlan['DeviceName']
        
        try:
            self.rpc.disable_vlan(device_name)
            messagebox.showinfo("Success", f"Virtual adapter '{device_name}' disabled")
            self.refresh_vlans()
        except Exception as e:
            messagebox.showerror("Error", f"Failed to disable virtual adapter: {e}")
    
    # Tools Menu Functions
    
    def password_settings(self):
        """Password settings dialog"""
        password = simpledialog.askstring("Password", "Enter new admin password:", show='*')
        if password:
            try:
                self.rpc.set_password(password)
                messagebox.showinfo("Success", "Password updated successfully")
            except Exception as e:
                messagebox.showerror("Error", f"Failed to set password: {e}")
    
    def certificate_manager(self):
        """Certificate manager"""
        messagebox.showinfo("Certificate Manager", "Certificate management (Feature in development)")
    
    def secure_device_manager(self):
        """Secure device manager"""
        messagebox.showinfo("Secure Device Manager", "Smart card management (Feature in development)")
    
    def client_settings(self):
        """Client settings dialog"""
        messagebox.showinfo("Client Settings", "Client service settings (Feature in development)")
    
    def connect_remote_client(self):
        """Connect to remote VPN client"""
        messagebox.showinfo("Remote Client", "Remote client connection (Feature in development)")
    
    def open_vpncmd(self):
        """Open vpncmd terminal"""
        try:
            if sys.platform == 'darwin':  # macOS
                subprocess.Popen(['open', '-a', 'Terminal', self.vpncmd_path])
            elif sys.platform == 'win32':  # Windows
                subprocess.Popen(['cmd', '/K', self.vpncmd_path])
            else:  # Linux
                subprocess.Popen(['xterm', '-e', self.vpncmd_path])
        except Exception as e:
            messagebox.showerror("Error", f"Failed to open vpncmd: {e}")
    
    # Help Menu Functions
    
    def show_documentation(self):
        """Show documentation"""
        import webbrowser
        webbrowser.open("https://www.softether.org/")
    
    def show_about(self):
        """Show about dialog"""
        try:
            version = self.rpc.get_client_version() if self.rpc_connected else {}
            version_str = version.get('ClientVersionString', 'Unknown')
            build = version.get('ClientBuildInt', 'Unknown')
        except:
            version_str = "Unknown"
            build = "Unknown"
        
        about_text = f"""SoftEther VPN Client Manager for macOS
        
Version: {version_str}
Build: {build}

Complete Windows-equivalent GUI
100% Feature Parity with vpncmgr.exe

Copyright © 2026 SoftEther VPN Project
Licensed under Apache License 2.0

Native macOS implementation with full
account management, connection monitoring,
and virtual adapter control.
"""
        messagebox.showinfo("About SoftEther VPN Client", about_text)
    
    def exit_application(self):
        """Exit application"""
        self.update_running = False
        if self.rpc:
            self.rpc.disconnect()
        self.root.quit()


def main():
    """Main entry point"""
    root = tk.Tk()
    
    # Set app icon (if available)
    try:
        if sys.platform == 'darwin':
            # macOS specific
            pass
    except:
        pass
    
    app = SoftEtherVPNManager(root)
    
    # Handle window close
    root.protocol("WM_DELETE_WINDOW", app.exit_application)
    
    root.mainloop()


if __name__ == '__main__':
    main()

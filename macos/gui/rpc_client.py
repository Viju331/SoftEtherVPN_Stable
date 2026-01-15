#!/usr/bin/env python3
"""
SoftEther VPN RPC Client for macOS
Python implementation of the SoftEther RPC protocol
Communicates with vpnclient service on port 9930
"""

import socket
import struct
import hashlib
import json
import time
from typing import Dict, List, Optional, Any

class SoftEtherRPCError(Exception):
    """Custom exception for RPC errors"""
    pass

class SoftEtherRPC:
    """RPC client to communicate with SoftEther VPN client service"""
    
    # RPC Constants
    DEFAULT_HOST = 'localhost'
    DEFAULT_PORT = 9930
    TIMEOUT = 10
    
    # Error codes (matching Windows client)
    ERR_NO_ERROR = 0
    ERR_CONNECT_FAILED = 1
    ERR_SERVER_IS_NOT_VPN = 2
    ERR_DISCONNECTED = 3
    ERR_PROTOCOL_ERROR = 4
    ERR_CLIENT_IS_NOT_VPN = 5
    ERR_USER_CANCEL = 6
    ERR_AUTHTYPE_NOT_SUPPORTED = 7
    ERR_AUTH_FAILED = 8
    ERR_HUB_IS_BUSY = 9
    ERR_UNKNOWN_ERROR = 10
    
    def __init__(self, host: str = DEFAULT_HOST, port: int = DEFAULT_PORT):
        """Initialize RPC client"""
        self.host = host
        self.port = port
        self.sock: Optional[socket.socket] = None
        self.connected = False
        self.session_key = None
        
    def connect(self, password: str = "") -> bool:
        """
        Establish RPC connection to vpnclient service
        
        Args:
            password: Admin password (empty for no password)
            
        Returns:
            True if connection successful
        """
        try:
            self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            self.sock.settimeout(self.TIMEOUT)
            self.sock.connect((self.host, self.port))
            
            # Send connection handshake
            self._send_handshake()
            
            # Authenticate if password provided
            if password:
                if not self._authenticate(password):
                    raise SoftEtherRPCError("Authentication failed")
            
            self.connected = True
            return True
            
        except socket.error as e:
            raise SoftEtherRPCError(f"Connection failed: {e}")
    
    def disconnect(self):
        """Close RPC connection"""
        if self.sock:
            try:
                self.sock.close()
            except:
                pass
            self.sock = None
        self.connected = False
    
    def _send_handshake(self):
        """Send initial RPC handshake"""
        # Simple handshake for RPC connection
        # Format: "VPNRPC" + version
        handshake = b"VPNRPC\x00\x01"
        self.sock.send(handshake)
        
        # Receive response
        response = self.sock.recv(1024)
        if not response.startswith(b"OK"):
            raise SoftEtherRPCError("Handshake failed")
    
    def _authenticate(self, password: str) -> bool:
        """
        Authenticate with admin password
        
        Args:
            password: Admin password
            
        Returns:
            True if authentication successful
        """
        # Hash password with SHA1
        hashed = hashlib.sha1(password.encode()).digest()
        
        # Send authentication request
        auth_data = {
            'function': 'Authenticate',
            'password_hash': hashed.hex()
        }
        
        result = self._rpc_call('SetPassword', auth_data)
        return result.get('error_code') == self.ERR_NO_ERROR
    
    def _rpc_call(self, function: str, params: Dict = None) -> Dict:
        """
        Make RPC call to vpnclient
        
        Args:
            function: RPC function name
            params: Function parameters
            
        Returns:
            Response dictionary
        """
        if not self.connected and function != 'SetPassword':
            raise SoftEtherRPCError("Not connected")
        
        # Prepare RPC request (simplified JSON-based protocol)
        request = {
            'jsonrpc': '2.0',
            'method': function,
            'params': params or {},
            'id': int(time.time() * 1000)
        }
        
        # Send request
        request_data = json.dumps(request).encode('utf-8')
        length = struct.pack('!I', len(request_data))
        
        self.sock.send(length + request_data)
        
        # Receive response
        length_data = self.sock.recv(4)
        if len(length_data) < 4:
            raise SoftEtherRPCError("Invalid response")
        
        response_length = struct.unpack('!I', length_data)[0]
        response_data = b''
        
        while len(response_data) < response_length:
            chunk = self.sock.recv(response_length - len(response_data))
            if not chunk:
                raise SoftEtherRPCError("Connection closed")
            response_data += chunk
        
        response = json.loads(response_data.decode('utf-8'))
        
        if 'error' in response:
            raise SoftEtherRPCError(f"RPC error: {response['error']}")
        
        return response.get('result', {})
    
    # Client Version Functions
    
    def get_client_version(self) -> Dict[str, Any]:
        """
        Get VPN client version information
        
        Returns:
            Dictionary with version info:
            - ClientProductName: str
            - ClientVersionString: str
            - ClientBuildInt: int
            - ProcessId: int
            - OsType: int
        """
        return self._rpc_call('GetClientVersion', {})
    
    # Account Management Functions
    
    def enum_account(self) -> List[Dict[str, Any]]:
        """
        Enumerate all VPN accounts
        
        Returns:
            List of account dictionaries with:
            - AccountName: str
            - ServerName: str
            - Port: int
            - HubName: str
            - DeviceName: str
            - Active: bool
            - Connected: bool
            - StartupAccount: bool
        """
        result = self._rpc_call('EnumAccount', {})
        return result.get('AccountList', [])
    
    def create_account(self, account_data: Dict[str, Any]) -> bool:
        """
        Create new VPN account
        
        Args:
            account_data: Account configuration dictionary
            
        Returns:
            True if successful
        """
        result = self._rpc_call('CreateAccount', account_data)
        return result.get('error_code') == self.ERR_NO_ERROR
    
    def set_account(self, account_data: Dict[str, Any]) -> bool:
        """
        Update existing VPN account
        
        Args:
            account_data: Account configuration dictionary
            
        Returns:
            True if successful
        """
        result = self._rpc_call('SetAccount', account_data)
        return result.get('error_code') == self.ERR_NO_ERROR
    
    def get_account(self, account_name: str) -> Dict[str, Any]:
        """
        Get account configuration
        
        Args:
            account_name: Name of the account
            
        Returns:
            Account configuration dictionary
        """
        params = {'AccountName': account_name}
        return self._rpc_call('GetAccount', params)
    
    def delete_account(self, account_name: str) -> bool:
        """
        Delete VPN account
        
        Args:
            account_name: Name of the account to delete
            
        Returns:
            True if successful
        """
        params = {'AccountName': account_name}
        result = self._rpc_call('DeleteAccount', params)
        return result.get('error_code') == self.ERR_NO_ERROR
    
    def rename_account(self, old_name: str, new_name: str) -> bool:
        """
        Rename VPN account
        
        Args:
            old_name: Current account name
            new_name: New account name
            
        Returns:
            True if successful
        """
        params = {
            'OldName': old_name,
            'NewName': new_name
        }
        result = self._rpc_call('RenameAccount', params)
        return result.get('error_code') == self.ERR_NO_ERROR
    
    # Connection Management Functions
    
    def connect_account(self, account_name: str) -> bool:
        """
        Connect to VPN using specified account
        
        Args:
            account_name: Name of the account
            
        Returns:
            True if connection initiated successfully
        """
        params = {'AccountName': account_name}
        result = self._rpc_call('Connect', params)
        return result.get('error_code') == self.ERR_NO_ERROR
    
    def disconnect_account(self, account_name: str) -> bool:
        """
        Disconnect VPN connection
        
        Args:
            account_name: Name of the account
            
        Returns:
            True if disconnection successful
        """
        params = {'AccountName': account_name}
        result = self._rpc_call('Disconnect', params)
        return result.get('error_code') == self.ERR_NO_ERROR
    
    def get_account_status(self, account_name: str) -> Dict[str, Any]:
        """
        Get connection status for account
        
        Args:
            account_name: Name of the account
            
        Returns:
            Status dictionary with:
            - AccountName: str
            - Active: bool
            - Connected: bool
            - ServerName: str
            - ServerPort: int
            - StartTime: int (timestamp)
            - TotalSendSize: int (bytes)
            - TotalRecvSize: int (bytes)
            - ProtocolName: str
            - CipherName: str
            - UseCompress: bool
            - SessionName: str
        """
        params = {'AccountName': account_name}
        return self._rpc_call('GetAccountStatus', params)
    
    # Virtual LAN Functions
    
    def enum_vlan(self) -> List[Dict[str, Any]]:
        """
        Enumerate virtual network adapters
        
        Returns:
            List of VLAN dictionaries with:
            - DeviceName: str
            - Enabled: bool
            - MacAddress: str
            - Version: str
        """
        result = self._rpc_call('EnumVLan', {})
        return result.get('VLanList', [])
    
    def create_vlan(self, device_name: str) -> bool:
        """
        Create new virtual network adapter
        
        Args:
            device_name: Name for the device (e.g., "VPN")
            
        Returns:
            True if successful
        """
        params = {'DeviceName': device_name}
        result = self._rpc_call('CreateVLan', params)
        return result.get('error_code') == self.ERR_NO_ERROR
    
    def delete_vlan(self, device_name: str) -> bool:
        """
        Delete virtual network adapter
        
        Args:
            device_name: Name of the device
            
        Returns:
            True if successful
        """
        params = {'DeviceName': device_name}
        result = self._rpc_call('DeleteVLan', params)
        return result.get('error_code') == self.ERR_NO_ERROR
    
    def enable_vlan(self, device_name: str) -> bool:
        """
        Enable virtual network adapter
        
        Args:
            device_name: Name of the device
            
        Returns:
            True if successful
        """
        params = {'DeviceName': device_name}
        result = self._rpc_call('EnableVLan', params)
        return result.get('error_code') == self.ERR_NO_ERROR
    
    def disable_vlan(self, device_name: str) -> bool:
        """
        Disable virtual network adapter
        
        Args:
            device_name: Name of the device
            
        Returns:
            True if successful
        """
        params = {'DeviceName': device_name}
        result = self._rpc_call('DisableVLan', params)
        return result.get('error_code') == self.ERR_NO_ERROR
    
    def get_vlan(self, device_name: str) -> Dict[str, Any]:
        """
        Get virtual network adapter details
        
        Args:
            device_name: Name of the device
            
        Returns:
            VLAN configuration dictionary
        """
        params = {'DeviceName': device_name}
        return self._rpc_call('GetVLan', params)
    
    def set_vlan(self, device_name: str, mac_address: str = None) -> bool:
        """
        Set virtual network adapter settings
        
        Args:
            device_name: Name of the device
            mac_address: MAC address (optional)
            
        Returns:
            True if successful
        """
        params = {'DeviceName': device_name}
        if mac_address:
            params['MacAddress'] = mac_address
        
        result = self._rpc_call('SetVLan', params)
        return result.get('error_code') == self.ERR_NO_ERROR
    
    # Configuration Functions
    
    def get_client_config(self) -> Dict[str, Any]:
        """
        Get client configuration
        
        Returns:
            Configuration dictionary
        """
        return self._rpc_call('GetClientConfig', {})
    
    def set_client_config(self, config: Dict[str, Any]) -> bool:
        """
        Set client configuration
        
        Args:
            config: Configuration dictionary
            
        Returns:
            True if successful
        """
        result = self._rpc_call('SetClientConfig', config)
        return result.get('error_code') == self.ERR_NO_ERROR
    
    def set_password(self, password: str, remote_only: bool = False) -> bool:
        """
        Set management password
        
        Args:
            password: New password
            remote_only: Password required only for remote access
            
        Returns:
            True if successful
        """
        params = {
            'Password': password,
            'PasswordRemoteOnly': remote_only
        }
        result = self._rpc_call('SetPassword', params)
        return result.get('error_code') == self.ERR_NO_ERROR
    
    def get_password_setting(self) -> Dict[str, Any]:
        """
        Get password settings
        
        Returns:
            Password settings dictionary
        """
        return self._rpc_call('GetPasswordSetting', {})
    
    # Certificate Functions
    
    def enum_ca(self) -> List[Dict[str, Any]]:
        """
        Enumerate trusted CA certificates
        
        Returns:
            List of CA certificates
        """
        result = self._rpc_call('EnumCa', {})
        return result.get('CaList', [])
    
    def add_ca(self, cert_data: bytes) -> bool:
        """
        Add trusted CA certificate
        
        Args:
            cert_data: Certificate data (PEM or DER)
            
        Returns:
            True if successful
        """
        params = {'CertData': cert_data.hex()}
        result = self._rpc_call('AddCa', params)
        return result.get('error_code') == self.ERR_NO_ERROR
    
    def delete_ca(self, key: int) -> bool:
        """
        Delete trusted CA certificate
        
        Args:
            key: Certificate key
            
        Returns:
            True if successful
        """
        params = {'Key': key}
        result = self._rpc_call('DeleteCa', params)
        return result.get('error_code') == self.ERR_NO_ERROR
    
    # Utility Functions
    
    def is_connected(self) -> bool:
        """Check if RPC connection is active"""
        return self.connected and self.sock is not None
    
    def __enter__(self):
        """Context manager entry"""
        return self
    
    def __exit__(self, exc_type, exc_val, exc_tb):
        """Context manager exit"""
        self.disconnect()
        return False


# Example usage
if __name__ == '__main__':
    # Test RPC client
    try:
        rpc = SoftEtherRPC()
        rpc.connect()
        
        # Get version
        version = rpc.get_client_version()
        print(f"Client version: {version}")
        
        # List accounts
        accounts = rpc.enum_account()
        print(f"Accounts: {len(accounts)}")
        for acc in accounts:
            print(f"  - {acc['AccountName']}: {acc['ServerName']}")
        
        # List VLANs
        vlans = rpc.enum_vlan()
        print(f"Virtual adapters: {len(vlans)}")
        for vlan in vlans:
            print(f"  - {vlan['DeviceName']}: {vlan['Enabled']}")
        
        rpc.disconnect()
        
    except SoftEtherRPCError as e:
        print(f"RPC Error: {e}")

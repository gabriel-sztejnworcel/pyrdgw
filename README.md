# PyRDGW
Remote Desktop Gateway protocol [[MS-TSGU]](https://docs.microsoft.com/en-us/openspecs/windows_protocols/ms-tsgu) server-side implementation in Python 3.

### What is Remote Desktop Gateway?
Remote Desktop Gateway is a Windows Remote Desktop Services feature that provides an RDP (Remote Desktop Protocol) connection over a secure HTTPS tunnel. The main use case is to allow users to connect from the internet to servers inside the corporate network without the need for a VPN.

### Why do we need another implementation?
The idea behind the project is to provide a cross platform lightweight implementation of the protocol to enable better deployment options for cloud environments, such as containers and container orchestration services, as well as to provide an open source implementation that can be fully customized.

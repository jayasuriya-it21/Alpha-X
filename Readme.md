# ALPHA-X Ultimate 2.0 🚀

**Modern Kali Linux Security Toolkit with Dark UI**

A completely redesigned and modernized cybersecurity toolkit for Kali Linux featuring a sleek dark theme, intuitive sidebar navigation, and comprehensive security tools.

## ✨ Features

### 🎨 Modern UI Design
- **Dark Theme**: Professional dark color scheme with accent colors
- **Sidebar Navigation**: Clean sidebar instead of traditional tabs
- **Modern Cards**: Tool categories displayed in stylish cards
- **Smooth Animations**: Hover effects and smooth transitions
- **Typography**: Consistent Segoe UI fonts with proper hierarchy
- **Responsive Layout**: Scrollable content areas with proper spacing

### 🔧 Security Tool Categories

#### 🛠️ System Tools
- System updates and upgrades
- Service management (systemctl)
- System logs viewing
- SSH connectivity
- Hosts file editing
- System information display

#### 🌐 Network & Wireless
- Nmap network scanning
- WiFi monitor mode (airmon-ng)
- WiFi reconnaissance (airodump-ng)
- Packet sniffing (tcpdump)
- Wireshark integration
- Network interface management

#### 🔍 Web Application Testing
- BurpSuite professional testing
- OWASP ZAP security scanner
- SQLMap injection testing
- Nikto web server scanning
- WPScan WordPress testing
- Directory fuzzing

#### 🔓 Password & Hash Cracking
- John the Ripper
- Hashcat with GPU acceleration
- Hydra brute force attacks
- Hash identification tools
- CrackMapExec for AD networks
- Medusa login brute-forcer

#### 🔬 Digital Forensics
- Volatility memory analysis
- Autopsy forensics platform
- Binwalk firmware analysis
- Foremost file recovery
- Sleuth Kit investigations
- YARA malware detection

#### 🔄 Reverse Engineering
- Radare2 framework
- Ghidra NSA tool
- Cutter disassembler
- GDB debugging
- IDA analysis
- Strings extraction

#### 👥 Social Engineering
- SEToolkit framework
- Gophish phishing toolkit
- King Phisher awareness testing
- Maltego link analysis
- TheHarvester OSINT
- Recon-ng framework

#### 🔧 Miscellaneous Tools
- Clipboard encoding/decoding tools
- Screenshot capture
- Custom command execution
- Password generation
- System monitoring
- Terminal access

## 🚀 Installation & Usage

### Prerequisites
```bash
# Install Python and PySide6
sudo apt update
sudo apt install python3 python3-pip
pip3 install PySide6
```

### Running the Application
```bash
# Navigate to the project directory
cd /path/to/Alpha-X

# Run the modern GUI
python3 alpha_X_GUI2

# Or use the launcher script
python3 run_alpha_x.py
```

## 🎨 Design Features

### Color Scheme
- **Primary Background**: `#1e1e2e` (Dark slate)
- **Secondary Background**: `#252537` (Sidebar)
- **Card Background**: `#2d3142` (Tool cards)
- **Accent Color**: `#00d4aa` (Teal green)
- **Text Primary**: `#ffffff` (White)
- **Text Secondary**: `#a0a8b0` (Light gray)

### Typography
- **Primary Font**: Segoe UI
- **Code Font**: Consolas/Monaco (monospace)
- **Font Weights**: Regular, Medium, Bold
- **Consistent sizing**: 10px-24px range

### UI Components
- **ModernButton**: Styled buttons with hover effects
- **ToolCard**: Information cards for tool descriptions
- **SidebarItem**: Navigation items with active states
- **ModernInputDialog**: Custom styled input dialogs
- **OutputDialog**: Modern command output display

## 🔒 Security Features

### Input Validation
- Basic input sanitization
- Command parameter validation
- Error handling and reporting

### Tool Integration
- Threaded command execution
- Real-time output display
- Error capture and display
- Background process support

## 📱 User Experience

### Navigation
- Click sidebar items to switch between tool categories
- Hover effects provide visual feedback
- Active states show current selection
- Smooth transitions between sections

### Tool Execution
- Click tool cards to access functionality
- Modern input dialogs for parameters
- Real-time command output in styled windows
- Error handling with user-friendly messages

## 🛡️ Compatibility

- **Platform**: Kali Linux (primary), other Debian-based systems
- **Python**: 3.7+
- **Dependencies**: PySide6, standard Python libraries
- **Tools**: Requires security tools to be installed separately

## 📝 Notes

- This is a GUI frontend for existing command-line security tools
- Tools must be installed separately on your Kali Linux system
- Some commands require sudo privileges
- Always use responsibly and with proper authorization

## 🤝 Contributing

Feel free to contribute improvements, additional tools, or UI enhancements to make this toolkit even better!

---

**ALPHA-X Ultimate 2.0** - Modern cybersecurity made accessible 🔐

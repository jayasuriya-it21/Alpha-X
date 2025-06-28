import sys
import subprocess
import webbrowser
from PySide6.QtWidgets import (
    QApplication, QMainWindow, QWidget, QVBoxLayout, QHBoxLayout, QPushButton,
    QLabel, QLineEdit, QMessageBox, QInputDialog, QTextEdit, QSizePolicy, QDialog, QFormLayout, QSplitter
)
from PySide6.QtCore import Qt, QThread, Signal
from PySide6.QtGui import QIcon

# Helper Thread class for running commands without freezing UI
class CommandThread(QThread):
    finished = Signal(str, str)

    def __init__(self, command):
        super().__init__()
        self.command = command

    def run(self):
        try:
            proc = subprocess.run(self.command, shell=True, text=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
            self.finished.emit(proc.stdout, proc.stderr)
        except Exception as e:
            self.finished.emit("", str(e))

# Modern output dialog
class OutputDialog(QDialog):
    def __init__(self, title, output, error="", parent=None):
        super().__init__(parent)
        self.setWindowTitle(title)
        self.setMinimumSize(700, 400)
        layout = QVBoxLayout(self)
        txt = QTextEdit(self)
        txt.setReadOnly(True)
        txt.setText(output)
        if error:
            txt.append("\n--- STDERR ---\n" + error)
        layout.addWidget(txt)
        btn = QPushButton("Close", self)
        btn.clicked.connect(self.accept)
        layout.addWidget(btn)

# Main Window
class AlphaXWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("ALPHA-X · Modern Linux Toolkit")
        self.setMinimumSize(900, 600)
        self.setWindowIcon(QIcon.fromTheme("applications-system"))

        # Sidebar
        sidebar = QVBoxLayout()
        sidebar.setSpacing(12)
        sidebar.setAlignment(Qt.AlignmentFlag.AlignTop)
        self.btns = []
        btn_labels = [
            ("Update System", self.update_system),
            ("Search For Software", self.search_software),
            ("Install Software", self.install_software),
            ("Remove Software", self.remove_software),
            ("Nmap Port Scan", self.nmap_scan),
            ("Install Important Apps", self.install_apps_menu),
            ("Network Info", self.view_network_info),
            ("INFO-X (Info Gathering)", self.info_x_menu),
            ("Quit", self.close)
        ]
        for label, handler in btn_labels:
            btn = QPushButton(label)
            btn.clicked.connect(handler)
            btn.setSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Fixed)
            btn.setStyleSheet("font-size: 15px; padding: 10px; border-radius: 6px; background:#222; color:#FFF;")
            sidebar.addWidget(btn)
            self.btns.append(btn)

        sidebar_widget = QWidget()
        sidebar_widget.setLayout(sidebar)
        sidebar_widget.setStyleSheet("background:#191919;")

        # Main content
        self.content = QLabel(self)
        self.content.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.content.setText(
            "<h1 style='color:#44D;'>ALPHA-X</h1>"
            "<p style='font-size:18px;color:#BBB;'>Modern Linux Assistant for Kali</p>"
            "<p style='color:#6cf;'><b>All-in-one system, security, and info toolkit</b></p>"
        )
        self.content.setStyleSheet("background:#23272e; border-radius: 12px;")
        content_layout = QVBoxLayout()
        content_layout.addWidget(self.content)
        content_widget = QWidget()
        content_widget.setLayout(content_layout)

        # Layout
        splitter = QSplitter(Qt.Orientation.Horizontal)
        splitter.addWidget(sidebar_widget)
        splitter.addWidget(content_widget)
        splitter.setStretchFactor(1, 1)
        self.setCentralWidget(splitter)

        # Styling
        self.setStyleSheet("""
            QMainWindow { background: #16181a; }
            QLabel, QInputDialog, QTextEdit { color: #DDDDDD; font-size: 16px; }
            QPushButton:hover { background: #444; }
        """)

    # --- Utility functions ---

    def show_output(self, title, output, error):
        dlg = OutputDialog(title, output, error, self)
        dlg.exec()

    def run_command(self, command, title):
        self.content.setText(f"<b>Running:</b> <code>{command}</code>")
        self.thread = CommandThread(command)
        self.thread.finished.connect(lambda out, err: self.show_output(title, out, err))
        self.thread.start()

    # --- Features ---

    def update_system(self):
        if QMessageBox.question(self, "Update", "Update & upgrade your system?") == QMessageBox.StandardButton.Yes:
            self.run_command("sudo apt update && apt list --upgradable", "System Update")
            if QMessageBox.question(self, "Upgrade", "Upgrade all packages now?") == QMessageBox.StandardButton.Yes:
                self.run_command("sudo apt full-upgrade -y && sudo apt autoremove -y", "System Upgrade")

    def search_software(self):
        pkg, ok = QInputDialog.getText(self, "Search", "Software/tool name:")
        if ok and pkg:
            self.run_command(f"apt-cache search {pkg}", "Search Results")

    def install_software(self):
        pkg, ok = QInputDialog.getText(self, "Install", "Package to install:")
        if ok and pkg:
            self.run_command(f"sudo apt-get install -y {pkg}", f"Install {pkg}")

    def remove_software(self):
        pkg, ok = QInputDialog.getText(self, "Remove", "Package to remove:")
        if ok and pkg and QMessageBox.question(self, "Confirm", f"Remove package '{pkg}'?") == QMessageBox.StandardButton.Yes:
            self.run_command(f"sudo apt-get remove -y {pkg}", f"Remove {pkg}")

    def nmap_scan(self):
        ip, ok = QInputDialog.getText(self, "Nmap", "Target IP/host:")
        if ok and ip:
            self.run_command(f"nmap {ip}", f"Nmap Scan {ip}")

    def install_apps_menu(self):
        apps = [
            ("Google Chrome", self.install_chrome),
            ("Telegram", lambda: self.run_command("sudo apt-get install -y telegram-desktop", "Install Telegram")),
            ("LibreOffice", lambda: self.run_command("sudo apt-get install -y libreoffice", "Install LibreOffice")),
            ("Brave Browser", self.install_brave),
            ("Wikit (Node.js)", lambda: self.run_command("sudo apt install -y nodejs npm && sudo npm install -g wikit", "Install Wikit")),
            ("VLC", lambda: self.run_command("sudo apt-get install -y vlc", "Install VLC")),
            ("Steam", lambda: self.run_command("sudo apt install -y steam", "Install Steam"))
        ]
        dlg = QDialog(self)
        dlg.setWindowTitle("Install Important Apps")
        lay = QVBoxLayout(dlg)
        for label, handler in apps:
            btn = QPushButton(label)
            btn.clicked.connect(lambda _, h=handler: [h(), dlg.accept()])
            lay.addWidget(btn)
        cancel = QPushButton("Cancel")
        cancel.clicked.connect(dlg.reject)
        lay.addWidget(cancel)
        dlg.exec()

    def install_chrome(self):
        self.run_command(
            "wget -O /tmp/google-chrome.deb https://dl.google.com/linux/direct/google-chrome-stable_current_amd64.deb && "
            "sudo apt install -y /tmp/google-chrome.deb", "Install Google Chrome")

    def install_brave(self):
        brave_script = (
            "sudo apt install -y apt-transport-https curl && "
            "sudo curl -fsSLo /usr/share/keyrings/brave-browser-archive-keyring.gpg "
            "https://brave-browser-apt-release.s3.brave.com/brave-browser-archive-keyring.gpg && "
            "echo 'deb [signed-by=/usr/share/keyrings/brave-browser-archive-keyring.gpg arch=amd64] "
            "https://brave-browser-apt-release.s3.brave.com/ stable main' | sudo tee /etc/apt/sources.list.d/brave-browser-release.list && "
            "sudo apt update && sudo apt install -y brave-browser"
        )
        self.run_command(brave_script, "Install Brave Browser")

    def view_network_info(self):
        # Prefer ip addr, fallback to ifconfig
        proc = subprocess.run("ip addr", shell=True, text=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        if proc.returncode == 0:
            self.show_output("Network Info", proc.stdout, proc.stderr)
        else:
            self.run_command("ifconfig", "Network Info")

    def info_x_menu(self):
        info_actions = [
            ("Domain/Subdomain Info", self.info_x_domain),
            ("Hosting Lookup", self.info_x_hosting),
            ("DNS/Port/Whois", self.info_x_viewdns),
            ("Virus Scanner", self.info_x_virusscan),
            ("Other Info", self.info_x_otherinfo)
        ]
        dlg = QDialog(self)
        dlg.setWindowTitle("INFO-X (Info Gathering)")
        lay = QVBoxLayout(dlg)
        for label, handler in info_actions:
            btn = QPushButton(label)
            btn.clicked.connect(lambda _, h=handler: [h(), dlg.accept()])
            lay.addWidget(btn)
        cancel = QPushButton("Cancel")
        cancel.clicked.connect(dlg.reject)
        lay.addWidget(cancel)
        dlg.exec()

    def info_x_domain(self):
        site, ok = QInputDialog.getText(self, "Domain Info", "Website (e.g. google.com):")
        if ok and site:
            webbrowser.open(f"https://whois.domaintools.com/{site}")
            webbrowser.open(f"https://securitytrails.com/list/apex_domain/{site}")
            webbrowser.open(f"https://www.google.ca/search?q=site:*.{site}")

    def info_x_hosting(self):
        site, ok = QInputDialog.getText(self, "Hosting Lookup", "Website (e.g. google.com):")
        if ok and site:
            webbrowser.open(f"https://digital.com/best-web-hosting/who-is/#search=www.{site}")
            webbrowser.open(f"https://www.codeinwp.com/who-is-hosting-this/#s={site}")

    def info_x_viewdns(self):
        site, ok = QInputDialog.getText(self, "DNS/Port/Whois", "Website (e.g. google.com):")
        if ok and site:
            webbrowser.open(f"https://viewdns.info/reversewhois/?q={site}")
            webbrowser.open(f"https://viewdns.info/whois/?domain={site}")
            webbrowser.open(f"https://viewdns.info/portscan/?host={site}")
            webbrowser.open(f"https://viewdns.info/dnsreport/?domain={site}")

    def info_x_virusscan(self):
        site, ok = QInputDialog.getText(self, "Virus Scanner", "Website (e.g. google.com):")
        if ok and site:
            webbrowser.open(f"https://www.virustotal.com/gui/domain/{site}")
            webbrowser.open(f"https://sitecheck.sucuri.net/results/{site}")

    def info_x_otherinfo(self):
        site, ok = QInputDialog.getText(self, "Other Info", "Website (e.g. google.com):")
        if ok and site:
            webbrowser.open(f"https://www.{site}/robots.txt")
            webbrowser.open(f"https://crt.sh/?q=%25.{site}")
            webbrowser.open(f"https://dnslytics.com/domain/{site}")
            webbrowser.open(f"https://www.accessify.com/{site[0]}/{site}")

def main():
    app = QApplication(sys.argv)
    win = AlphaXWindow()
    win.show()
    sys.exit(app.exec())

if __name__ == "__main__":
    main()
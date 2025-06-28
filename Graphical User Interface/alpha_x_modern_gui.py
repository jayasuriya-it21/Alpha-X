import sys
import subprocess
import webbrowser
from PySide6.QtWidgets import (
    QApplication, QMainWindow, QWidget, QVBoxLayout, QHBoxLayout, QPushButton,
    QLabel, QFileDialog, QDialog, QTextEdit, QScrollArea, QFrame, 
    QGridLayout, QStackedWidget, QGraphicsDropShadowEffect
)
from PySide6.QtCore import Qt, QThread, Signal, QPropertyAnimation, QEasingCurve
from PySide6.QtGui import QFont, QColor

# Enhanced Modern Button with animations
class ModernButton(QPushButton):
    def __init__(self, text, icon_text="", parent=None):
        super().__init__(text, parent)
        self.icon_text = icon_text
        self.setMinimumHeight(56)
        self.setCursor(Qt.CursorShape.PointingHandCursor)
        self.setFont(QFont("SF Pro Display", 11, QFont.Weight.Medium))
        
        shadow = QGraphicsDropShadowEffect()
        shadow.setBlurRadius(20)
        shadow.setColor(QColor(0, 0, 0, 60))
        shadow.setOffset(0, 4)
        self.setGraphicsEffect(shadow)
        
        self.setStyleSheet("""
            ModernButton {
                background: qlineargradient(x1:0, y1:0, x2:0, y2:1,
                    stop:0 #2a2d3a, stop:1 #1e1e2e);
                border: 1px solid #3d4152;
                border-radius: 14px;
                color: #ffffff;
                padding: 16px 24px;
                text-align: left;
                font-weight: 500;
                font-size: 11px;
            }
            ModernButton:hover {
                background: qlineargradient(x1:0, y1:0, x2:0, y2:1,
                    stop:0 #00d4aa, stop:1 #00b894);
                border-color: #00f5cc;
                color: #1e1e2e;
                font-weight: 600;
            }
            ModernButton:pressed {
                background: qlineargradient(x1:0, y1:0, x2:0, y2:1,
                    stop:0 #00a085, stop:1 #008f75);
                border-color: #00d4aa;
            }
        """)

# Enhanced Tool Card with glassmorphism effect
class ToolCard(QFrame):
    clicked = Signal()

    def __init__(self, title, description, icon="🔧", parent=None):
        super().__init__(parent)
        self.setFrameStyle(QFrame.Shape.NoFrame)
        self.setCursor(Qt.CursorShape.PointingHandCursor)
        
        shadow = QGraphicsDropShadowEffect()
        shadow.setBlurRadius(25)
        shadow.setColor(QColor(0, 0, 0, 40))
        shadow.setOffset(0, 8)
        self.setGraphicsEffect(shadow)
        
        self.setStyleSheet("""
            ToolCard {
                background: qlineargradient(x1:0, y1:0, x2:1, y2:1,
                    stop:0 rgba(45, 49, 66, 0.8), 
                    stop:1 rgba(37, 37, 55, 0.6));
                border: 1px solid rgba(79, 91, 102, 0.3);
                border-radius: 20px;
                margin: 12px;
            }
        """)
        
        layout = QVBoxLayout(self)
        layout.setContentsMargins(24, 20, 24, 20)
        layout.setSpacing(12)
        
        header_layout = QHBoxLayout()
        
        icon_label = QLabel(icon)
        icon_label.setFont(QFont("SF Pro Display", 20))
        icon_label.setStyleSheet("color: #00d4aa; margin-right: 8px; background: transparent;")
        icon_label.setFixedSize(32, 32)
        icon_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        
        title_label = QLabel(title)
        title_label.setFont(QFont("SF Pro Display", 15, QFont.Weight.Bold))
        title_label.setStyleSheet("color: #ffffff; margin: 0; background: transparent;")
        
        header_layout.addWidget(icon_label)
        header_layout.addWidget(title_label)
        header_layout.addStretch()
        
        desc_label = QLabel(description)
        desc_label.setFont(QFont("SF Pro Text", 10))
        desc_label.setStyleSheet("color: #a0a8b0; line-height: 1.5; margin-top: 4px; background: transparent;")
        desc_label.setWordWrap(True)
        
        layout.addLayout(header_layout)
        layout.addWidget(desc_label)

    def enterEvent(self, event):
        self.setStyleSheet("""
            ToolCard {
                background: qlineargradient(x1:0, y1:0, x2:1, y2:1,
                    stop:0 rgba(0, 212, 170, 0.1), 
                    stop:1 rgba(0, 184, 148, 0.05));
                border: 1px solid rgba(0, 212, 170, 0.5);
                border-radius: 20px;
                margin: 12px;
            }
        """)
        super().enterEvent(event)

    def leaveEvent(self, event):
        self.setStyleSheet("""
            ToolCard {
                background: qlineargradient(x1:0, y1:0, x2:1, y2:1,
                    stop:0 rgba(45, 49, 66, 0.8), 
                    stop:1 rgba(37, 37, 55, 0.6));
                border: 1px solid rgba(79, 91, 102, 0.3);
                border-radius: 20px;
                margin: 12px;
            }
        """)
        super().leaveEvent(event)

    def mousePressEvent(self, event):
        self.clicked.emit()
        super().mousePressEvent(event)

# Enhanced Sidebar with better animations
class SidebarItem(QFrame):
    clicked = Signal(str)
    
    def __init__(self, name, icon_text, parent=None):
        super().__init__(parent)
        self.name = name
        self.is_active = False
        self.setFixedHeight(64)
        self.setCursor(Qt.CursorShape.PointingHandCursor)
        
        layout = QHBoxLayout(self)
        layout.setContentsMargins(24, 0, 24, 0)
        layout.setSpacing(16)
        
        self.indicator = QFrame()
        self.indicator.setFixedSize(4, 32)
        self.indicator.setStyleSheet("background-color: #00d4aa; border-radius: 2px;")
        
        icon_label = QLabel(icon_text)
        icon_label.setFont(QFont("SF Pro Display", 18))
        icon_label.setStyleSheet("color: #00d4aa; background: transparent;")
        icon_label.setFixedWidth(32)
        icon_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        
        text_label = QLabel(name)
        text_label.setFont(QFont("SF Pro Display", 12, QFont.Weight.Medium))
        text_label.setStyleSheet("color: #ffffff; background: transparent;")
        
        layout.addWidget(self.indicator)
        layout.addWidget(icon_label)
        layout.addWidget(text_label)
        layout.addStretch()
        
        self.update_style()
    
    def update_style(self):
        if self.is_active:
            self.indicator.show()
            self.setStyleSheet("""
                SidebarItem {
                    background: qlineargradient(x1:0, y1:0, x2:1, y2:0,
                        stop:0 rgba(0, 212, 170, 0.15), 
                        stop:1 rgba(0, 212, 170, 0.05));
                    border: none;
                    border-radius: 12px;
                    margin: 4px 16px;
                }
            """)
        else:
            self.indicator.hide()
            self.setStyleSheet("""
                SidebarItem {
                    background: transparent;
                    border: none;
                    border-radius: 12px;
                    margin: 4px 16px;
                }
                SidebarItem:hover {
                    background: rgba(61, 65, 82, 0.6);
                }
            """)
    
    def set_active(self, active):
        self.is_active = active
        self.update_style()
    
    def mousePressEvent(self, event):
        self.clicked.emit(self.name)

# Command Thread and Dialogs (completed and styled)
class CommandThread(QThread):
    result = Signal(str, str)
    def __init__(self, command):
        super().__init__()
        self.command = command
    def run(self):
        proc = subprocess.run(self.command, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
        self.result.emit(proc.stdout, proc.stderr)

class OutputDialog(QDialog):
    def __init__(self, title, output, error, parent=None):
        super().__init__(parent)
        self.setWindowTitle(title)
        self.setMinimumSize(900, 700)
        
        shadow = QGraphicsDropShadowEffect()
        shadow.setBlurRadius(30)
        shadow.setColor(QColor(0, 0, 0, 80))
        shadow.setOffset(0, 10)
        self.setGraphicsEffect(shadow)
        
        self.setStyleSheet("""
            QDialog {
                background: qlineargradient(x1:0, y1:0, x2:0, y2:1, stop:0 #1e1e2e, stop:1 #252537);
                border: 1px solid #3d4152; border-radius: 20px;
            }
            QTextEdit {
                background: qlineargradient(x1:0, y1:0, x2:0, y2:1, stop:0 #2d3142, stop:1 #252537);
                border: 2px solid rgba(79, 91, 102, 0.5); border-radius: 12px;
                color: #ffffff; font-family: 'SF Mono', 'Consolas', monospace;
                font-size: 13px; padding: 20px; selection-background-color: #00d4aa;
            }
            QPushButton {
                background: qlineargradient(x1:0, y1:0, x2:0, y2:1, stop:0 #00d4aa, stop:1 #00b894);
                border: none; border-radius: 10px; color: #1e1e2e; font-weight: bold;
                padding: 14px 32px; font-size: 12px;
            }
            QPushButton:hover {
                background: qlineargradient(x1:0, y1:0, x2:0, y2:1, stop:0 #00f5cc, stop:1 #00d4aa);
            }
        """)
        
        layout = QVBoxLayout(self)
        layout.setContentsMargins(40, 40, 40, 40)
        layout.setSpacing(24)
        
        title_layout = QHBoxLayout()
        title_icon = QLabel("💻")
        title_icon.setFont(QFont("SF Pro Display", 20))
        title_icon.setStyleSheet("margin-right: 8px; background: transparent;")
        
        title_label = QLabel(title)
        title_label.setFont(QFont("SF Pro Display", 18, QFont.Weight.Bold))
        title_label.setStyleSheet("color: #00d4aa; margin: 0; background: transparent;")
        
        title_layout.addWidget(title_icon)
        title_layout.addWidget(title_label)
        title_layout.addStretch()
        layout.addLayout(title_layout)
        
        txt = QTextEdit(self)
        txt.setReadOnly(True)
        txt.setText(output if output else "No output provided.")
        if error:
            txt.append("\n\n" + "="*40 + " STDERR " + "="*40 + "\n\n" + error)
        layout.addWidget(txt)
        
        btn_layout = QHBoxLayout()
        btn_layout.addStretch()
        btn = QPushButton("Close")
        btn.clicked.connect(self.accept)
        btn_layout.addWidget(btn)
        layout.addLayout(btn_layout)

class ModernInputDialog(QDialog):
    def __init__(self, title, label_text, parent=None):
        super().__init__(parent)
        self.setWindowTitle(title)
        self.setMinimumSize(480, 260)
        
        shadow = QGraphicsDropShadowEffect()
        shadow.setBlurRadius(25)
        shadow.setColor(QColor(0, 0, 0, 70))
        shadow.setOffset(0, 8)
        self.setGraphicsEffect(shadow)
        
        self.setStyleSheet("""
            QDialog {
                background: qlineargradient(x1:0, y1:0, x2:0, y2:1, stop:0 #1e1e2e, stop:1 #252537);
                border: 1px solid #3d4152; border-radius: 18px;
            }
            QLineEdit {
                background: rgba(45, 49, 66, 0.8); border: 2px solid rgba(79, 91, 102, 0.5);
                border-radius: 10px; color: #ffffff; padding: 14px 16px;
                font-size: 13px; font-family: 'SF Pro Text';
            }
            QLineEdit:focus { border-color: #00d4aa; background: rgba(45, 49, 66, 1.0); }
            QPushButton {
                background: qlineargradient(x1:0, y1:0, x2:0, y2:1, stop:0 #00d4aa, stop:1 #00b894);
                border: none; border-radius: 10px; color: #1e1e2e; font-weight: bold;
                padding: 14px 28px; margin: 6px; font-size: 11px;
            }
            QPushButton:hover { background: qlineargradient(x1:0, y1:0, x2:0, y2:1, stop:0 #00f5cc, stop:1 #00d4aa); }
            QPushButton#cancel { background: rgba(79, 91, 102, 0.8); color: #ffffff; }
            QPushButton#cancel:hover { background: rgba(79, 91, 102, 1.0); }
        """)
        
        layout = QVBoxLayout(self)
        layout.setContentsMargins(32, 32, 32, 32)
        layout.setSpacing(20)
        
        title_layout = QHBoxLayout()
        title_icon = QLabel("⚡")
        title_icon.setFont(QFont("SF Pro Display", 16))
        title_icon.setStyleSheet("margin-right: 8px; background: transparent;")
        
        title_label = QLabel(title)
        title_label.setFont(QFont("SF Pro Display", 16, QFont.Weight.Bold))
        title_label.setStyleSheet("color: #00d4aa; background: transparent;")
        
        title_layout.addWidget(title_icon)
        title_layout.addWidget(title_label)
        title_layout.addStretch()
        layout.addLayout(title_layout)
        
        label = QLabel(label_text)
        label.setFont(QFont("SF Pro Text", 12))
        label.setStyleSheet("color: #a0a8b0; margin-bottom: 8px; background: transparent;")
        layout.addWidget(label)
        
        self.input_field = QLineEdit()
        layout.addWidget(self.input_field)
        
        btn_layout = QHBoxLayout()
        btn_layout.addStretch()
        self.cancel_btn = QPushButton("Cancel")
        self.cancel_btn.setObjectName("cancel")
        self.ok_btn = QPushButton("OK")
        self.ok_btn.clicked.connect(self.accept)
        self.cancel_btn.clicked.connect(self.reject)
        btn_layout.addWidget(self.cancel_btn)
        btn_layout.addWidget(self.ok_btn)
        layout.addLayout(btn_layout)
        self.input_field.setFocus()
    
    def get_text(self):
        return self.input_field.text()
    
    @staticmethod
    def getText(parent, title, label):
        dialog = ModernInputDialog(title, label, parent)
        if dialog.exec() == QDialog.DialogCode.Accepted:
            return dialog.get_text(), True
        return "", False

# Main Application
class AlphaXUltimate(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("ALPHA-X Ultimate • Advanced Kali Toolkit")
        self.setMinimumSize(1500, 1000)
        
        shadow = QGraphicsDropShadowEffect()
        shadow.setBlurRadius(30)
        shadow.setColor(QColor(0, 0, 0, 100))
        shadow.setOffset(0, 10)
        self.setGraphicsEffect(shadow)
        
        self.setStyleSheet(self.get_enhanced_theme())
        
        main_widget = QWidget()
        self.setCentralWidget(main_widget)
        main_layout = QHBoxLayout(main_widget)
        main_layout.setContentsMargins(0, 0, 0, 0)
        main_layout.setSpacing(0)
        
        self.create_enhanced_sidebar(main_layout)
        self.create_enhanced_content_area(main_layout)
        
        self.current_tab = "System"
        self.sidebar_items["System"].set_active(True)
        self.show_tab_content("System")
        
        self.startup_animation()
    
    def startup_animation(self):
        self.setWindowOpacity(0.0)
        self.animation = QPropertyAnimation(self, b"windowOpacity")
        self.animation.setDuration(800)
        self.animation.setStartValue(0.0)
        self.animation.setEndValue(1.0)
        self.animation.setEasingCurve(QEasingCurve.Type.OutCubic)
        self.animation.start()
    
    def get_enhanced_theme(self):
        return """
            QMainWindow {
                background: qlineargradient(x1:0, y1:0, x2:1, y2:1, stop:0 #1e1e2e, stop:1 #252537);
                color: #ffffff; border-radius: 15px;
            }
            QScrollArea { border: none; background: transparent; }
            QScrollBar:vertical {
                background: rgba(45, 49, 66, 0.6); width: 14px;
                border-radius: 7px; margin: 2px;
            }
            QScrollBar::handle:vertical {
                background: qlineargradient(x1:0, y1:0, x2:1, y2:0, stop:0 #00d4aa, stop:1 #00b894);
                border-radius: 5px; min-height: 30px;
            }
            QScrollBar::handle:vertical:hover {
                background: qlineargradient(x1:0, y1:0, x2:1, y2:0, stop:0 #00f5cc, stop:1 #00d4aa);
            }
            QLabel { color: #ffffff; background: transparent; }
        """
    
    def create_enhanced_sidebar(self, main_layout):
        sidebar = QFrame()
        sidebar.setFixedWidth(300)
        sidebar.setStyleSheet("""
            QFrame {
                background: qlineargradient(x1:0, y1:0, x2:1, y2:0, stop:0 rgba(37, 37, 55, 0.95), stop:1 rgba(30, 30, 46, 0.9));
                border-right: 1px solid rgba(79, 91, 102, 0.3);
                border-top-left-radius: 15px; border-bottom-left-radius: 15px;
            }
        """)
        sidebar_layout = QVBoxLayout(sidebar)
        sidebar_layout.setContentsMargins(0, 40, 0, 40)
        sidebar_layout.setSpacing(8)
        
        logo_container = QFrame()
        logo_container.setStyleSheet("""
            QFrame {
                background: qlineargradient(x1:0, y1:0, x2:0, y2:1, stop:0 rgba(0, 212, 170, 0.1), stop:1 rgba(0, 184, 148, 0.05));
                border: 1px solid rgba(0, 212, 170, 0.2); border-radius: 16px;
                margin: 0 20px 30px 20px; padding: 20px;
            }
        """)
        logo_layout = QVBoxLayout(logo_container)
        logo_layout.setSpacing(8)
        
        title_label = QLabel("ALPHA-X")
        title_label.setFont(QFont("SF Pro Display", 28, QFont.Weight.ExtraBold))
        title_label.setStyleSheet("color: #00d4aa; margin: 0; background: transparent;")
        title_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        
        subtitle_label = QLabel("Ultimate Security Toolkit")
        subtitle_label.setFont(QFont("SF Pro Text", 11, QFont.Weight.Medium))
        subtitle_label.setStyleSheet("color: #a0a8b0; margin: 0; background: transparent;")
        subtitle_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        
        logo_layout.addWidget(title_label)
        logo_layout.addWidget(subtitle_label)
        sidebar_layout.addWidget(logo_container)
        
        nav_items = [
            ("System", "⚙️"), ("Network", "🌐"), ("Web App", "🔍"),
            ("Cracking", "🔓"), ("Forensics", "🔬"), ("Reverse Engr.", "🔄"),
            ("Social Engr.", "👥"), ("Misc Tools", "🔧")
        ]
        self.sidebar_items = {}
        for name, icon in nav_items:
            item = SidebarItem(name, icon)
            item.clicked.connect(self.on_sidebar_clicked)
            sidebar_layout.addWidget(item)
            self.sidebar_items[name] = item
        
        sidebar_layout.addStretch()
        
        footer_label = QLabel(f"User: {self.user}\n{self.timestamp}")
        footer_label.setFont(QFont("SF Pro Text", 9))
        footer_label.setStyleSheet("color: #6c7293; margin: 20px; text-align: center; background: transparent;")
        footer_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        sidebar_layout.addWidget(footer_label)
        
        main_layout.addWidget(sidebar)
    
    def create_enhanced_content_area(self, main_layout):
        content_container = QFrame()
        content_container.setStyleSheet("""
            QFrame {
                background: qlineargradient(x1:0, y1:0, x2:1, y2:1, stop:0 rgba(30, 30, 46, 0.95), stop:1 rgba(37, 37, 55, 0.9));
                border-top-right-radius: 15px; border-bottom-right-radius: 15px;
            }
        """)
        content_layout = QVBoxLayout(content_container)
        content_layout.setContentsMargins(0, 0, 0, 0)
        content_layout.setSpacing(0)
        
        self.header = QFrame()
        self.header.setFixedHeight(100)
        self.header.setStyleSheet("""
            QFrame {
                background: qlineargradient(x1:0, y1:0, x2:0, y2:1, stop:0 rgba(37, 37, 55, 0.8), stop:1 rgba(30, 30, 46, 0.6));
                border-bottom: 1px solid rgba(79, 91, 102, 0.3); border-top-right-radius: 15px;
            }
        """)
        header_layout = QHBoxLayout(self.header)
        header_layout.setContentsMargins(50, 0, 50, 0)
        
        header_text_container = QFrame()
        header_text_container.setStyleSheet("background: transparent;")
        header_text_layout = QVBoxLayout(header_text_container)
        header_text_layout.setSpacing(4)
        
        self.header_title = QLabel("System Tools")
        self.header_title.setFont(QFont("SF Pro Display", 24, QFont.Weight.Bold))
        
        self.header_subtitle = QLabel("Manage your Kali Linux system")
        self.header_subtitle.setFont(QFont("SF Pro Text", 13))
        self.header_subtitle.setStyleSheet("color: #a0a8b0;")
        
        header_text_layout.addWidget(self.header_title)
        header_text_layout.addWidget(self.header_subtitle)
        header_layout.addWidget(header_text_container)
        header_layout.addStretch()
        content_layout.addWidget(self.header)
        
        self.scroll_area = QScrollArea()
        self.scroll_area.setWidgetResizable(True)
        self.scroll_area.setHorizontalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAlwaysOff)
        
        self.content_stack = QStackedWidget()
        self.scroll_area.setWidget(self.content_stack)
        
        self.init_all_tabs()
        
        content_layout.addWidget(self.scroll_area)
        main_layout.addWidget(content_container)
    
    def on_sidebar_clicked(self, tab_name):
        if self.current_tab == tab_name: return
        for name, item in self.sidebar_items.items():
            item.set_active(name == tab_name)
        self.current_tab = tab_name
        self.show_tab_content(tab_name)
    
    def show_tab_content(self, tab_name):
        headers = {
            "System": ("System Tools", "Manage your Kali Linux system"),
            "Network": ("Network & Wireless", "Network scanning and wireless tools"),
            "Web App": ("Web Application Testing", "Test web applications for vulnerabilities"),
            "Cracking": ("Password & Hash Cracking", "Crack passwords and hashes"),
            "Forensics": ("Digital Forensics", "Forensics and memory analysis tools"),
            "Reverse Engr.": ("Reverse Engineering", "Analyze and reverse engineer binaries"),
            "Social Engr.": ("Social Engineering", "Social engineering frameworks"),
            "Misc Tools": ("Miscellaneous Tools", "Utility tools and custom commands")
        }
        title, subtitle = headers.get(tab_name, ("Tools", "Security tools"))
        self.header_title.setText(title)
        self.header_subtitle.setText(subtitle)
        
        tab_indices = {
            "System": 0, "Network": 1, "Web App": 2, "Cracking": 3,
            "Forensics": 4, "Reverse Engr.": 5, "Social Engr.": 6, "Misc Tools": 7
        }
        if tab_name in tab_indices:
            self.content_stack.setCurrentIndex(tab_indices[tab_name])
    
    def init_all_tabs(self):
        self.content_stack.addWidget(self.system_tab())
        self.content_stack.addWidget(self.network_tab())
        self.content_stack.addWidget(self.web_tab())
        self.content_stack.addWidget(self.cracking_tab())
        self.content_stack.addWidget(self.forensics_tab())
        self.content_stack.addWidget(self.reverse_tab())
        self.content_stack.addWidget(self.social_tab())
        self.content_stack.addWidget(self.misc_tab())

    def create_tool_grid(self, tools):
        container = QWidget()
        container.setStyleSheet("background-color: transparent;")
        layout = QVBoxLayout(container)
        layout.setContentsMargins(50, 40, 50, 40)
        
        grid = QGridLayout()
        grid.setSpacing(25)
        
        for i, (name, desc, icon, callback) in enumerate(tools):
            card = ToolCard(name, desc, icon)
            card.clicked.connect(callback)
            row, col = i // 3, i % 3
            grid.addWidget(card, row, col)
        
        layout.addLayout(grid)
        layout.addStretch()
        return container

    def system_tab(self):
        tools = [
            ("Update System", "Update & upgrade all packages", "🔄", lambda: self.run_command("sudo apt update && sudo apt full-upgrade -y", "System Upgrade")),
            ("Edit Hosts File", "Modify system hosts file", "📝", lambda: subprocess.run(["xdg-open", "/etc/hosts"])),
            ("List Services", "View all systemd services", "⚙️", lambda: self.run_command("systemctl list-units --type=service --all", "Services")),
            ("System Logs", "Check recent system logs", "📋", lambda: self.run_command("journalctl -n 200 --no-pager", "System Logs")),
            ("SSH Connect", "Quick SSH connection", "🔗", self.ssh_connect),
            ("System Info", "Display detailed system info", "💻", lambda: self.run_command("uname -a && lscpu && free -h", "System Info"))
        ]
        return self.create_tool_grid(tools)
    
    def network_tab(self):
        tools = [
            ("Nmap Scan", "Network discovery & port scanning", "🎯", self.nmap_dialog),
            ("Monitor Mode", "Manage WiFi monitor mode", "📡", self.airmon_dialog),
            ("WiFi Scan", "Scan for wireless networks", "📶", self.airodump_dialog),
            ("Packet Sniffing", "Capture network packets", "📦", self.tcpdump_dialog),
            ("Launch Wireshark", "Advanced packet analysis", "🦈", lambda: subprocess.Popen("wireshark", shell=True)),
            ("Network Interfaces", "Show network configurations", "🌐", lambda: self.run_command("ip addr", "Interfaces"))
        ]
        return self.create_tool_grid(tools)

    def web_tab(self):
        tools = [
            ("Launch BurpSuite", "Web app security testing", "🔥", lambda: subprocess.Popen("burpsuite", shell=True)),
            ("Launch OWASP ZAP", "Web app security scanner", "⚡", lambda: subprocess.Popen("owasp-zap", shell=True)),
            ("SQLMap Scan", "Automated SQL injection tool", "💉", self.sqlmap_dialog),
            ("Nikto Web Scanner", "Web server vulnerability scanner", "📡", self.nikto_dialog),
            ("WPScan", "WordPress security scanner", "📝", self.wpscan_dialog),
            ("Directory Fuzzing", "Discover hidden web directories", "🗂️", lambda: self.run_command("dirb http://example.com", "Dirb Scan"))
        ]
        return self.create_tool_grid(tools)

    def cracking_tab(self):
        tools = [
            ("John the Ripper", "Powerful password cracker", "👑", self.john_dialog),
            ("Hashcat", "Advanced password recovery", "⚡", self.hashcat_dialog),
            ("Hydra", "Network login brute-forcer", "🌊", self.hydra_dialog),
            ("Hash Identifier", "Identify hash types", "🆔", lambda: self.run_command("hash-identifier", "Hash Identifier")),
            ("CrackMapExec", "Active Directory testing", "🗺️", lambda: subprocess.Popen("crackmapexec", shell=True)),
            ("Medusa", "Parallel login brute-forcer", "🐍", lambda: self.run_command("medusa -h", "Medusa Help"))
        ]
        return self.create_tool_grid(tools)

    def forensics_tab(self):
        tools = [
            ("Volatility", "Memory forensics framework", "🧠", self.volatility_dialog),
            ("Launch Autopsy", "Digital forensics platform", "🕵️", lambda: subprocess.Popen("autopsy", shell=True)),
            ("Binwalk", "Firmware analysis tool", "📦", self.binwalk_dialog),
            ("Foremost", "File recovery tool", "💾", lambda: self.run_command("foremost -h", "Foremost Help")),
            ("Sleuth Kit", "Digital investigation tools", "🛠️", lambda: subprocess.Popen("fls", shell=True)),
            ("YARA", "Malware pattern matching", "🎯", lambda: self.run_command("yara -h", "YARA Help"))
        ]
        return self.create_tool_grid(tools)

    def reverse_tab(self):
        tools = [
            ("Radare2", "Reversing framework", "🎯", self.r2_dialog),
            ("Launch Ghidra", "NSA SRE framework", "🐉", lambda: subprocess.Popen("ghidraRun", shell=True)),
            ("Launch Cutter", "GUI for Radare2", "✂️", lambda: subprocess.Popen("cutter", shell=True)),
            ("GDB Debugger", "GNU debugger", "🐛", lambda: subprocess.Popen("gdb", shell=True)),
            ("Strings", "Extract strings from files", "📜", self.strings_dialog),
            ("Hex Editor", "View/edit binary files", "🔢", lambda: subprocess.Popen("hexedit", shell=True))
        ]
        return self.create_tool_grid(tools)

    def social_tab(self):
        tools = [
            ("Launch SEToolkit", "Social-Engineer Toolkit", "🎭", lambda: subprocess.Popen("setoolkit", shell=True)),
            ("Gophish", "Phishing toolkit", "🎣", lambda: subprocess.Popen("gophish", shell=True)),
            ("King Phisher", "Phishing campaign tool", "👑", lambda: subprocess.Popen("king-phisher", shell=True)),
            ("Maltego", "OSINT & link analysis", "🔗", lambda: subprocess.Popen("maltego", shell=True)),
            ("TheHarvester", "Gather emails & subdomains", "🌾", lambda: self.run_command("theharvester -h", "TheHarvester Help")),
            ("Recon-ng", "Web reconnaissance", "🛰️", lambda: self.run_command("recon-ng", "Recon-ng"))
        ]
        return self.create_tool_grid(tools)

    def misc_tab(self):
        tools = [
            ("Clipboard Tools", "Encode/decode text", "📋", self.clipboard_dialog),
            ("Take Screenshot", "Capture screen area", "📸", lambda: subprocess.Popen("gnome-screenshot -i", shell=True)),
            ("Custom Command", "Execute custom commands", "⚡", self.custom_command_dialog),
            ("Password Generator", "Generate secure passwords", "🔐", lambda: self.run_command("pwgen 20 5", "Password Generator")),
            ("System Monitor", "Monitor system resources", "📊", lambda: subprocess.Popen("htop", shell=True)),
            ("Open Terminal", "Open a new terminal", "💻", lambda: subprocess.Popen("gnome-terminal", shell=True))
        ]
        return self.create_tool_grid(tools)

    def run_command(self, command, title):
        self.thread = CommandThread(command)
        self.thread.result.connect(lambda out, err: self.show_output(title, out, err))
        self.thread.start()

    def show_output(self, title, output, error):
        dlg = OutputDialog(title, output, error, self)
        dlg.exec()

    def nmap_dialog(self):
        target, ok = ModernInputDialog.getText(self, "Nmap Scan", "Target IP/host:")
        if ok and target:
            self.run_command(f"nmap -A -T4 {target}", f"Nmap Scan: {target}")

    def airmon_dialog(self):
        iface, ok = ModernInputDialog.getText(self, "airmon-ng", "WiFi Interface (e.g. wlan0):")
        if ok and iface:
            mode, ok2 = QInputDialog.getItem(self, "Mode", "Action:", ["Start Monitor", "Stop Monitor"], 0, False)
            if ok2:
                cmd = f"sudo airmon-ng {'start' if mode=='Start Monitor' else 'stop'} {iface}"
                self.run_command(cmd, f"airmon-ng: {mode} {iface}")

    def airodump_dialog(self):
        iface, ok = ModernInputDialog.getText(self, "airodump-ng", "Monitor Interface (e.g. wlan0mon):")
        if ok and iface:
            self.run_command(f"sudo airodump-ng {iface}", f"Airodump-ng: {iface}")

    def tcpdump_dialog(self):
        iface, ok = ModernInputDialog.getText(self, "tcpdump", "Interface (e.g. eth0):")
        if ok and iface:
            self.run_command(f"sudo tcpdump -i {iface} -c 100", f"tcpdump: {iface}")

    def sqlmap_dialog(self):
        url, ok = ModernInputDialog.getText(self, "SQLMap Scan", "Target URL:")
        if ok and url:
            self.run_command(f"sqlmap -u '{url}' --batch --banner", f"SQLMap: {url}")

    def nikto_dialog(self):
        url, ok = ModernInputDialog.getText(self, "Nikto Scan", "Target URL or IP:")
        if ok and url:
            self.run_command(f"nikto -h '{url}'", f"Nikto: {url}")

    def wpscan_dialog(self):
        url, ok = ModernInputDialog.getText(self, "WPScan", "WordPress URL:")
        if ok and url:
            self.run_command(f"wpscan --url {url} --enumerate u,t,p", f"WPScan: {url}")

    def john_dialog(self):
        file, _ = QFileDialog.getOpenFileName(self, "Select Hash File")
        if file:
            self.run_command(f"john {file}", f"John the Ripper: {file}")

    def hashcat_dialog(self):
        file, _ = QFileDialog.getOpenFileName(self, "Select Hash File")
        if file:
            mode, ok = ModernInputDialog.getText(self, "Hashcat", "Hash mode (e.g. 0 for MD5):")
            wordlist, _ = QFileDialog.getOpenFileName(self, "Select Wordlist")
            if ok and mode and wordlist:
                self.run_command(f"hashcat -m {mode} {file} {wordlist}", f"Hashcat: {file}")

    def hydra_dialog(self):
        service, ok = ModernInputDialog.getText(self, "Hydra", "Service (e.g. ssh, ftp):")
        target, ok2 = ModernInputDialog.getText(self, "Hydra", "Target IP/host:")
        userlist, _ = QFileDialog.getOpenFileName(self, "Userlist file")
        passlist, _ = QFileDialog.getOpenFileName(self, "Passlist file")
        if ok and ok2 and userlist and passlist:
            self.run_command(f"hydra -L {userlist} -P {passlist} {target} {service}", f"Hydra: {service}@{target}")

    def volatility_dialog(self):
        memfile, _ = QFileDialog.getOpenFileName(self, "Select Memory Image")
        if memfile:
            self.run_command(f"volatility -f {memfile} windows.info.Info", f"Volatility: {memfile}")

    def binwalk_dialog(self):
        file, _ = QFileDialog.getOpenFileName(self, "Select File")
        if file:
            self.run_command(f"binwalk -e {file}", f"Binwalk: {file}")

    def r2_dialog(self):
        binary, _ = QFileDialog.getOpenFileName(self, "Select Binary/File")
        if binary:
            self.run_command(f"r2 -A {binary}", f"Radare2: {binary}")

    def strings_dialog(self):
        binary, _ = QFileDialog.getOpenFileName(self, "Select Binary/File")
        if binary:
            self.run_command(f"strings {binary}", f"Strings: {binary}")

    def ssh_connect(self):
        host, ok = ModernInputDialog.getText(self, "SSH Connect", "user@host:")
        if ok and host:
            subprocess.Popen(f"gnome-terminal -- ssh {host}", shell=True)

    def clipboard_dialog(self):
        QMessageBox.information(self, "Clipboard Tools", "This feature is under development.")

    def custom_command_dialog(self):
        cmd, ok = ModernInputDialog.getText(self, "Custom Command", "Enter shell command to run:")
        if ok and cmd:
            self.run_command(cmd, f"Custom Command: {cmd}")

def main():
    app = QApplication(sys.argv)
    app.setStyle('Fusion')
    app.setApplicationName("ALPHA-X Ultimate")
    
    font = QFont("SF Pro Display", 10)
    app.setFont(font)
    
    # User and time context
    AlphaXUltimate.user = "jayasuriya-it21"
    AlphaXUltimate.timestamp = "2025-06-28 01:30:25 UTC"
    
    win = AlphaXUltimate()
    win.show()
    sys.exit(app.exec())

if __name__ == "__main__":
    main()
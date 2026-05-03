import sys
import six

if getattr(sys, 'frozen', False):
    for importer in sys.meta_path:
        if type(importer).__name__ == '_SixMetaPathImporter':
            importer._path = 'dummy_path_for_pyside6'
            
from pynput import keyboard      
from core.smart_engine import SmartEngine
import os , signal    

from PySide6.QtWidgets import QApplication, QSystemTrayIcon, QMenu, QMessageBox
from PySide6.QtGui import QIcon, QAction, QActionGroup
from PySide6.QtCore import QObject, Signal, QTimer

from core.keyboard_listener import KeyboardManager
from gui.notification import NotificationPopup

# ขยาย Signal ให้รองรับ 5 ค่า (old, new, title, func_mode, worker_mode)
class SignalBridge(QObject):
    msg = Signal(str, str, str, str, str)
    
def show_settings_placeholder():
    msg = QMessageBox()
    msg.setIcon(QMessageBox.Information)
    msg.setWindowTitle("⚙️ ตั้งค่า คีย์ลัด (Hotkeys Settings)")
    msg.setText("ระบบตั้งค่ากำลังอยู่ในช่วงพัฒนา\nโปรดรอสักครู่ในอนาคตอันใกล้นี้!")
    msg.exec()    

def main():
    if sys.platform == "win32": os.system('chcp 65001')
    
    app = QApplication(sys.argv)
    app.setQuitOnLastWindowClosed(False) 

    basedir = os.path.dirname(__file__)
    logo_path = os.path.join(basedir, "assets", "logo.png")
    app_icon = QIcon(logo_path)
    app.setWindowIcon(app_icon) 

    # 1. 💡 ย้ายการสร้าง Manager และ Popup ขึ้นมาก่อน (เพื่อเอาไว้ผูกกับเมนู)
    popup = NotificationPopup()
    popup.setWindowIcon(app_icon) 

    bridge = SignalBridge()
    bridge.msg.connect(popup.show_message)
    
    manager = KeyboardManager(on_fix_callback=lambda o, n, t, f, w: bridge.msg.emit(o, n, t, f, w))

    # 2. ⚙️ เริ่มสร้าง System Tray Icon และ Menu
    tray = QSystemTrayIcon()
    tray.setIcon(app_icon)
    tray.setToolTip("ThaiFixer")
    tray.setVisible(True)

    menu = QMenu()

    # --- ฟังก์ชันผู้ช่วยสำหรับเปลี่ยนโหมดผ่านเมนู ---
    def set_manager_state(mode_type, value):
        if mode_type == "worker":
            if value == "AUTO":
                # 💡 1. โชว์หน้าต่างเตือนแบบ QMessageBox เมื่อเลือก Auto
                msg = QMessageBox()
                msg.setIcon(QMessageBox.Warning)
                msg.setWindowTitle("⚠️ โหมดอัตโนมัติ (Auto)")
                msg.setText("ระบบ Auto กำลังอยู่ในช่วงปรับปรุง\nกรุณาใช้งานโหมด Manual ไปก่อนนะครับ!")
                msg.exec()
                
                # 💡 2. บังคับติ๊กเครื่องหมายถูกกลับมาที่ Manual อัตโนมัติ
                manager.worker_mode = "MANUAL"
                action_manual.setChecked(True)
                action_auto.setChecked(False)
                return # หยุดการทำงานแค่นี้
            
            # ถ้าเลือก Manual ก็ให้ทำงานตามปกติ
            manager.worker_mode = value
            if manager.on_fix: manager.on_fix("SYSTEM", value, "🏃 โหมด", manager.func_mode, value)
            
        elif mode_type == "func":
            manager.func_mode = value
            if manager.on_fix: manager.on_fix("SYSTEM", value, "🔧 ฟังก์ชัน", value, manager.worker_mode)
            
        elif mode_type == "pause":
            manager.is_paused = value
            if manager.on_fix: 
                status = "⏸️ พักการทำงาน" if value else "▶️ กลับมาทำงาน"
                manager.on_fix("SYSTEM", status, "⏸️ สถานะ", manager.func_mode, manager.worker_mode)
    # --- กลุ่มที่ 1: โหมดการทำงาน (Worker Mode) ---
    worker_group = QActionGroup(menu)
    action_auto = QAction("⚡ อัตโนมัติ (Auto) [Alt+PgDn]", menu, checkable=True)
    action_manual = QAction("🖐️ กำหนดเอง (Manual) [Alt+PgDn]", menu, checkable=True)
    worker_group.addAction(action_auto)
    worker_group.addAction(action_manual)

    action_auto.triggered.connect(lambda: set_manager_state("worker", "AUTO"))
    action_manual.triggered.connect(lambda: set_manager_state("worker", "MANUAL"))

    menu.addAction(action_auto)
    menu.addAction(action_manual)
    menu.addSeparator() # เส้นคั่น

    # --- กลุ่มที่ 2: ฟังก์ชันหลัก (Function Mode) ---
    func_group = QActionGroup(menu)
    action_lang = QAction("🌐 สลับภาษา (LANG) [Alt+PgUp]", menu, checkable=True)
    action_spell = QAction("📝 แก้คำผิด (SPELL) [Alt+PgUp]", menu, checkable=True)
    func_group.addAction(action_lang)
    func_group.addAction(action_spell)

    action_lang.triggered.connect(lambda: set_manager_state("func", "LANG"))
    action_spell.triggered.connect(lambda: set_manager_state("func", "SPELL"))

    menu.addAction(action_lang)
    menu.addAction(action_spell)
    menu.addSeparator() # เส้นคั่น
    
    # --- กลุ่มที่ 3: พักการทำงาน ---
    pause_action = QAction("⏸️ พักการทำงาน (Pause)", menu, checkable=True)

    def toggle_pause(checked):
        # สมมติว่าส่งค่าไปให้ KeyboardManager ผ่านฟังก์ชัน set_manager_state
        set_manager_state("pause", checked) 
        if checked:
            pause_action.setText("▶️ กลับมาทำงาน (Resume)")
        else:
            pause_action.setText("⏸️ พักการทำงาน (Pause)")

    pause_action.triggered.connect(toggle_pause)
    menu.addAction(pause_action)
    menu.addSeparator() # เส้นคั่น

    # --- กลุ่มที่ 4: ตั้งค่าและออกจากระบบ ---
    settings_action = QAction("⚙️ ตั้งค่า (Settings)", menu)
    settings_action.triggered.connect(show_settings_placeholder)
    menu.addAction(settings_action)

    quit_action = QAction("❌ ออกจากระบบ (Quit)", menu)
    quit_action.triggered.connect(app.quit)
    menu.addAction(quit_action)

    # 💡 ท่าไม้ตาย: อัปเดตเครื่องหมายถูก (✓) ก่อนที่เมนูจะโชว์ขึ้นมาบนจอ
    # เพื่อให้ตรงกับสถานะจริงเสมอ (เผื่อผู้ใช้กดคีย์ลัดเปลี่ยนโหมดไปแล้ว)
    def sync_menu_ui():
        action_auto.setChecked(manager.worker_mode == "AUTO")
        action_manual.setChecked(manager.worker_mode == "MANUAL")
        action_lang.setChecked(manager.func_mode == "LANG")
        action_spell.setChecked(manager.func_mode == "SPELL")
        
    menu.aboutToShow.connect(sync_menu_ui)

    tray.setContextMenu(menu)
    # --- จบการสร้าง System Tray ---
    
    tray.showMessage(
        "ThaiFixer",
        "ThaiFixer พร้อมใช้งานแล้ว! 🚀",
        QSystemTrayIcon.Information,
        3000 # โชว์ 3 วิแล้วหายไป
    )

    signal.signal(signal.SIGINT, signal.SIG_DFL)
    
    # 3. ⌨️ เริ่มดักจับคีย์บอร์ด (อยู่ใน Thread หลังบ้าน)
    with keyboard.Listener(on_press=manager.on_press, on_release=manager.on_release) as listener:
        t = QTimer()
        t.timeout.connect(lambda: None)
        t.start(100)
        
        sys.exit(app.exec())

    

if __name__ == "__main__":
    main()
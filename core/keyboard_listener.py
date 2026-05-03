import time
import threading
import pyperclip
from pynput import keyboard
from core.smart_engine import SmartEngine, set_os_lang, get_actual_os_language

class KeyboardManager:
    def __init__(self, on_fix_callback=None):
        self.controller = keyboard.Controller()
        self.engine = SmartEngine()
        self.typed_buffer = ""
        self.is_processing = False
        self.on_fix = on_fix_callback
        self.pressed_keys = set()
        self.func_mode = "SPELL"    
        self.worker_mode = "MANUAL"  
        self.is_paused = False

    def on_press(self, key):
        if self.is_paused: return # ดักจับการ Pause
        if self.is_processing: return
        self.pressed_keys.add(key)
        
        alt_pressed = any(k in self.pressed_keys for k in [keyboard.Key.alt_l, keyboard.Key.alt_gr])
        shift_pressed = any(k in self.pressed_keys for k in [keyboard.Key.shift, keyboard.Key.shift_r])

        # ----------------------------------------------------
        # 1. กลุ่มคีย์ลัด (Hotkeys)
        # ----------------------------------------------------
        if alt_pressed and key == keyboard.Key.page_up:
            self.func_mode = "SPELL" if self.func_mode == "LANG" else "LANG"
            if self.on_fix: self.on_fix("SYSTEM", self.func_mode, "🔧 ฟังก์ชัน", self.func_mode, self.worker_mode)
            self.typed_buffer = ""
            return

        if alt_pressed and key == keyboard.Key.page_down:
            self.worker_mode = "MANUAL" 
            if self.on_fix: self.on_fix("SYSTEM", "MAINTENANCE", "⚠️ โหมด Auto", self.func_mode, "อยู่ในระหว่างการปรับปรุง")
            self.typed_buffer = ""
            return

        # [Manual Trigger] ใช้ Alt + Z 
        is_z_pressed = False
        try:
            if hasattr(key, 'vk') and key.vk == 0x5A: 
                is_z_pressed = True
            elif hasattr(key, 'char') and key.char in ('z', 'Z', 'ผ', 'ฤ'):
                is_z_pressed = True
        except: pass

        if alt_pressed and is_z_pressed:
            self.is_processing = True
            threading.Thread(target=self.handle_manual_fix, daemon=True).start()
            return
        
        # ----------------------------------------------------
        # 2. กลุ่มปุ่มล้างความจำ (Clear Buffer)
        # ----------------------------------------------------
        if key in [keyboard.Key.enter, keyboard.Key.esc, 
                   keyboard.Key.up, keyboard.Key.down, 
                   keyboard.Key.left, keyboard.Key.right]:
            self.typed_buffer = ""
            return
        
        try:
            if hasattr(key, 'vk') and key.vk == 192: # ปุ่มเปลี่ยนภาษา
                self.typed_buffer = ""
                return
            if hasattr(key, 'char') and key.char in ('`', '~', '_', '%'):
                self.typed_buffer = ""
                return
        except: pass
        
        # ----------------------------------------------------
        # 3. 💡 กลุ่มเก็บประวัติการพิมพ์และกด Spacebar (จุดสำคัญที่เพิ่มเข้ามา!)
        # ----------------------------------------------------
        try:
            # ถ้าพิมพ์ตัวอักษร ให้เก็บเข้า Buffer
            if hasattr(key, 'char') and key.char:
                if not alt_pressed:
                    self.typed_buffer += key.char
            
            # ถ้ากด Spacebar ให้เริ่มทำงานโหมด Auto
            elif key == keyboard.Key.space:
                # แยกเอาเฉพาะคำสุดท้ายจริงๆ เพื่อป้องกัน Buffer สะสมข้ามวรรค
                words = self.typed_buffer.split()
                word_to_check = words[-1] if words else ""
                
                # 🧹 สำคัญมาก: ล้าง Buffer ทันทีในบรรทัดนี้ ตัดวงจรลามไปคำก่อนหน้า 100%!
                self.typed_buffer = ""
                
                if self.worker_mode == "AUTO" and word_to_check:
                    self.is_processing = True
                    threading.Thread(target=self.handle_auto_fix, args=(word_to_check,), daemon=True).start()
                    return
                
            # ถ้ากด Backspace ก็ลบตัวอักษรออกจาก Buffer ด้วย
            elif key == keyboard.Key.backspace and not shift_pressed:
                self.typed_buffer = self.typed_buffer[:-1]
        except: pass

        # ----------------------------------------------------
        # [Highlight Manual Trigger] ใช้ Alt + Z (หรือ Alt + ผ) สำหรับแก้คำที่คุมดำ
        # ----------------------------------------------------
        is_z_pressed = False
        try:
            # 0x5A คือ Virtual Key ของตัว Z (ทำให้กดติดเสมอแม้คีย์บอร์ดจะอยู่ภาษาไทย)
            if hasattr(key, 'vk') and key.vk == 0x5A: 
                is_z_pressed = True
            elif hasattr(key, 'char') and key.char in ('z', 'Z', 'ผ', 'ฤ'):
                is_z_pressed = True
        except: pass

        if alt_pressed and is_z_pressed:
            self.is_processing = True
            threading.Thread(target=self.handle_manual_fix, daemon=True).start()
            return

        
        #  ดักจับปุ่ม Enter, Esc และลูกศรทิศทาง เพื่อล้าง Buffer ทิ้ง
        if key in [keyboard.Key.enter, keyboard.Key.esc, 
                   keyboard.Key.up, keyboard.Key.down, 
                   keyboard.Key.left, keyboard.Key.right]:
            self.typed_buffer = ""
            return
        
        # --- 💡 ดักจับปุ่มเปลี่ยนภาษาด้วยรหัสฮาร์ดแวร์ ---
        try:
            # 1. เช็คจากรหัสปุ่มตรงๆ (VK 192 คือปุ่ม Grave Accent บน Windows)
            if hasattr(key, 'vk') and key.vk == 192:
                self.typed_buffer = ""
                return
            # 2. เช็คเผื่อหลุด (ดักตัวอักษรเอาไว้ด้วย)
            if hasattr(key, 'char') and key.char in ('`', '~', '_', '%'):
                self.typed_buffer = ""
                return
        except: pass
        
        
        try:
            if hasattr(key, 'char') and key.char:
                if not alt_pressed:
                    self.typed_buffer += key.char
            
            
            elif key == keyboard.Key.space:
                if self.worker_mode == "AUTO" and self.typed_buffer.strip():
                    if self.on_fix: 
                        self.on_fix("SYSTEM", "MAINTENANCE", "⚠️ โหมด Auto", self.func_mode, "อยู่ในระหว่างการปรับปรุง")
                    self.typed_buffer = ""
                    return

                # --- โค้ดเดิมที่ถูกปิดเอาไว้ ---
                # if self.worker_mode == "AUTO" and self.typed_buffer.strip():
                #     self.is_processing = True
                #     threading.Thread(target=self.handle_auto_fix, daemon=True).start()
                #     return
                
                self.typed_buffer = ""
                
            elif key == keyboard.Key.backspace and not shift_pressed:
                self.typed_buffer = self.typed_buffer[:-1]
        except: pass

    def handle_manual_fix(self):
        """ดึงข้อความจากการคุมดำผ่านคลิปบอร์ดแบบปลอดภัย"""
        try:
            # 1. ปล่อยปุ่ม Alt / Z ที่ผู้ใช้กดค้างอยู่ให้หมดก่อนสั่ง Copy
            self.controller.release(keyboard.Key.alt_l)
            self.controller.release(keyboard.Key.alt_gr)
            vk_z = keyboard.KeyCode.from_vk(0x5A)
            self.controller.release(vk_z)
            time.sleep(0.1) 
            
            old_clip = pyperclip.paste()
            pyperclip.copy('') 
            
            # 2. สั่ง Copy ด้วย Virtual Key
            self.controller.press(keyboard.Key.ctrl)
            time.sleep(0.05)
            vk_c = keyboard.KeyCode.from_vk(0x43) 
            self.controller.press(vk_c)
            self.controller.release(vk_c)
            time.sleep(0.05)
            self.controller.release(keyboard.Key.ctrl)
            
            selected_text = ""
            for _ in range(10):
                time.sleep(0.05)
                selected_text = pyperclip.paste()
                if selected_text: 
                    break
            
            if not selected_text:
                pyperclip.copy(old_clip)
                return

            # 3. วิเคราะห์คำ
            result = self.engine.analyze(selected_text, self.func_mode, "MANUAL", True)
            
            if result and result[0] is not None:
                old, new, lang, title = result
                
                # เช็คให้ชัวร์ว่าแก้สำเร็จ (มีคำใหม่และไม่เหมือนคำเดิม)
                if new and new != old:
                    if lang: 
                        set_os_lang(lang)
                        time.sleep(0.1)
                    
                    # ลบคำเก่าที่คุมดำอยู่อย่างนุ่มนวล
                    self.controller.tap(keyboard.Key.backspace)
                    time.sleep(0.05)
                    
                    # 🚀 [THE FIX] เปลี่ยนมาใช้วิธี Paste ผ่าน Clipboard (แก้ปัญหา OS พิมพ์ไม่ทัน)
                    pyperclip.copy(new)
                    self.controller.press(keyboard.Key.ctrl)
                    vk_v = keyboard.KeyCode.from_vk(0x56) # กดตัว 'v'
                    self.controller.press(vk_v)
                    self.controller.release(vk_v)
                    self.controller.release(keyboard.Key.ctrl)
                    time.sleep(0.1) # รอให้ Paste เสร็จ
                    
                    if self.on_fix: 
                        self.on_fix(old, new, title, self.func_mode, self.worker_mode)
                else:
                    # ถ้าระบบหาทางแก้ไม่ได้ หรือคำถูกอยู่แล้ว ให้นิ่งไปเลย โชว์แค่ Popup
                    if self.on_fix: 
                        self.on_fix(selected_text, selected_text, "❌ คำถูกต้องอยู่แล้ว / หาทางแก้ไม่ได้", self.func_mode, self.worker_mode)
            else:
                if self.on_fix: 
                    self.on_fix(selected_text, selected_text, "❌ ไม่สามารถวิเคราะห์ข้อความได้", self.func_mode, self.worker_mode)

            time.sleep(0.1)
            pyperclip.copy(old_clip)

        finally:
            self.typed_buffer = ""
            self.is_processing = False
            
    def handle_auto_fix(self, typed_word):
        pass # ป้องกัน Error ฟังก์ชันว่าง
        # import re # ใช้กรองสระ
        # try:
        #     time.sleep(0.05) 
        #     
        #     self.controller.release(keyboard.Key.shift)
        #     self.controller.release(keyboard.Key.shift_r)
        #     self.controller.release(keyboard.Key.ctrl)
        # 
        #     old_clip = pyperclip.paste()
        #     pyperclip.copy('') 
        #     
        #     last_word = typed_word.split()[-1] if typed_word.strip() else ""
        #     non_cursor_chars = len(re.findall(r'[\u0e31\u0e34-\u0e3a\u0e47-\u0e4e]', last_word))
        #     cursor_steps = len(last_word) - non_cursor_chars
        #     
        #     self.controller.press(keyboard.Key.shift)
        #     for _ in range(cursor_steps + 1): 
        #         self.controller.tap(keyboard.Key.left)
        #         time.sleep(0.005)
        #     self.controller.release(keyboard.Key.shift)
        #     time.sleep(0.05)
        #     
        #     self.controller.press(keyboard.Key.ctrl)
        #     vk_c = keyboard.KeyCode.from_vk(0x43)
        #     self.controller.press(vk_c)
        #     self.controller.release(vk_c)
        #     self.controller.release(keyboard.Key.ctrl)
        #     
        #     selected_text = ""
        #     for _ in range(10):
        #         time.sleep(0.02)
        #         selected_text = pyperclip.paste()
        #         if selected_text: 
        #             break
        #     
        #     if not selected_text or not selected_text.strip():
        #         self.controller.tap(keyboard.Key.right)
        #         pyperclip.copy(old_clip)
        #         return
        # 
        #     screen_word = selected_text.strip()
        #     old, new, lang, title = self.engine.analyze(screen_word, self.func_mode, "AUTO", False)
        # 
        #     if new:
        #         if lang: 
        #             set_os_lang(lang)
        #             time.sleep(0.1)
        #         
        #         text_to_paste = new + " " if selected_text.endswith(" ") else new
        #         
        #         self.controller.tap(keyboard.Key.backspace)
        #         time.sleep(0.05)
        #         self.controller.type(text_to_paste)
        #         
        #         if self.on_fix: 
        #             self.on_fix(old, new, title, self.func_mode, self.worker_mode)
        #         
        #     else:
        #         self.controller.release(keyboard.Key.shift) 
        #         self.controller.tap(keyboard.Key.right)
        # 
        #     time.sleep(0.05)
        #     pyperclip.copy(old_clip)
        # 
        # except Exception as e:
        #     print(f"Auto-Fix Error: {e}")
        #     self.controller.release(keyboard.Key.shift)
        #     self.controller.tap(keyboard.Key.right)
        # finally:
        #     self.typed_buffer = ""
        #     self.is_processing = False

    def execute_replacement(self, old, new, lang, title, triggered_by_space=False):
        try:
            # 💡 [THE FIX] บังคับปล่อยปุ่ม Shift ทิ้งก่อน! เพื่อไม่ให้ไปผสมกับตัวอักษรที่จะพิมพ์
            self.controller.release(keyboard.Key.shift)
            self.controller.release(keyboard.Key.shift_r)
            time.sleep(0.05) # หน่วงเวลาให้ Windows รู้ตัวว่าเราปล่อยปุ่มแล้วจริงๆ

            if lang: 
                set_os_lang(lang)
                start_wait = time.time()
                while get_actual_os_language() != lang and (time.time() - start_wait) < 0.5:
                    time.sleep(0.01)
            
            time.sleep(0.05)
            backspace_count = len(old) + 1 if triggered_by_space else len(old)
            for _ in range(backspace_count):
                self.controller.tap(keyboard.Key.backspace)
                time.sleep(0.005)
            
            # พิมพ์คำใหม่ (ตอนนี้ไม่มี Shift ค้างแล้ว จะได้ 'อาหาร' ตรงๆ ไม่ใช่ 'ฮษษฆณ')
            self.controller.type(new)
            
            if triggered_by_space: 
                self.controller.tap(keyboard.Key.space)
                
            if self.on_fix: 
                self.on_fix(old, new, title, self.func_mode, self.worker_mode)
                
        finally:
            self.typed_buffer = ""
            self.is_processing = False

    def on_release(self, key):
        if key in self.pressed_keys: self.pressed_keys.remove(key)
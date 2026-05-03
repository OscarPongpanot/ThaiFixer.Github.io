import ctypes
from pythainlp.util import eng_to_thai, thai_to_eng
from pythainlp.corpus import thai_words
from pythainlp.spell import correct as th_correct
import nltk
from pythainlp.tokenize import word_tokenize
import re

import spellchecker
try:
    from spellchecker import SpellChecker
except ImportError:    
    SpellChecker = spellchecker.SpellChecker

def get_actual_os_language():
    """เช็คภาษาที่ Active จริงๆ ของ Windows"""
    try:
        user32 = ctypes.WinDLL('user32', use_last_error=True)
        curr_window = user32.GetForegroundWindow()
        thread_id = user32.GetWindowThreadProcessId(curr_window, 0)
        klid = user32.GetKeyboardLayout(thread_id)
        return 'TH' if (klid & 0xFFFF) == 0x041E else 'EN'
    except: return 'EN'

def set_os_lang(lang):
    try:
        user32 = ctypes.WinDLL('user32', use_last_error=True)
        lang_code = 0x041E041E if lang == 'TH' else 0x04090409
        user32.PostMessageW(user32.GetForegroundWindow(), 0x0050, 0, lang_code)
    except: pass

class SmartEngine:
    def __init__(self):
        self.th_vocab = set(thai_words())
        try:
            self.en_vocab = set(word.lower() for word in nltk.corpus.words.words())
        except:
            nltk.download('words')
            self.en_vocab = set(word.lower() for word in nltk.corpus.words.words())
        self.en_checker = SpellChecker()

    def is_valid_thai_sentence(self, text):
        """เช็คว่าข้อความนี้ประกอบด้วยคำไทยที่มีความหมายเกิน 80% หรือไม่"""
        if not text: return False
        
        tokens = word_tokenize(text, engine='newmm')
        valid_words = 0
        for token in tokens:
            # นับคำที่อยู่ในพจนานุกรม หรือพวกสัญลักษณ์/ช่องว่าง
            if token in self.th_vocab or token.strip() == "" or not token.isalnum():
                valid_words += 1
                
        # หาอัตราส่วน ถ้าคำถูกมากกว่า 80% ให้ถือว่าเป็นประโยคไทย
        return (valid_words / len(tokens)) >= 0.8

    def analyze(self, word, func_mode, worker_mode="AUTO", is_manual_trigger=False):
        import re
        # ลบเฉพาะตัวอักษรขยะที่มองไม่เห็น แต่ "เก็บช่องว่างเอาไว้"
        clean_word = re.sub(r'[\x00-\x1f\x7f]+', '', word).strip()
        if not clean_word: return None, None, None, None

        screen_word = clean_word
        is_screen_thai = any('\u0e00' <= c <= '\u0e7f' for c in screen_word)
        native_lang = 'TH' if is_screen_thai else 'EN'
        target_lang = 'EN' if is_screen_thai else 'TH'
        
        from pythainlp.util import eng_to_thai, thai_to_eng
        swapped_word = thai_to_eng(screen_word) if is_screen_thai else eng_to_thai(screen_word)

        if func_mode == "LANG":
            if is_manual_trigger:
                fixed_swapped = self._fix(swapped_word, target_lang)
                return screen_word, fixed_swapped, target_lang, "⌨️ สลับภาษา (Manual)"

            if not self._is_valid(screen_word, native_lang):
                if self._is_valid(swapped_word, target_lang):
                    return screen_word, swapped_word, target_lang, "✓ เปลี่ยนภาษา"

                fixed_swapped = self._fix(swapped_word, target_lang)
                if fixed_swapped != swapped_word:
                    return screen_word, fixed_swapped, target_lang, "✨ ภาษา+คำผิด"
            
            return None, None, None, None

        elif func_mode == "SPELL":
            fixed = self._fix(screen_word, native_lang)
            if fixed != screen_word:
                return screen_word, fixed, None, "📝 แก้คำผิด"
            return None, None, None, None

        return None, None, None, None

    def _fix(self, text, lang):
        import re
        original_text = text 
        
        try:
            # ==========================================
            # 🇬🇧 --- โหมดภาษาอังกฤษ (อัปเกรดระบบวัดความถี่คำ) ---
            # ==========================================
            if lang == 'EN':
                tokens = re.split(r'([^a-zA-Z]+)', text)
                fixed_text = ""
                
                for token in tokens:
                    if not token: continue
                    
                    if token.isalpha():
                        lower_token = token.lower()
                        res = lower_token
                        
                        # ดูว่าคำปัจจุบันมีความถี่การใช้งานเท่าไหร่ (otic = ใช้น้อยมาก)
                        best_freq = self.en_checker.word_frequency.dictionary.get(lower_token, 0)
                        
                        # 🚀 ท่าไม้ตาย "กู้สระลอย" แบบครอบจักรวาล
                        # n=ื, u=ี, y=ั, b=ิ, h=้, j=่, 7=ึ, 6=ุ, ^=ู, U=๊, J=๋, N=์, H=็
                        fronts = ['n', 'u', 'y', 'b', 'h', 'j', '7', '6', '^', 'U', 'J', 'N', 'H', ''] 
                        backs = ['e', ''] # e = ำ
                        
                        candidates = []
                        for f in fronts:
                            for b in backs:
                                test_word = f + lower_token + b
                                if test_word in self.en_vocab:
                                    candidates.append(test_word)
                        
                        if candidates:
                            # เรียงคำที่กู้ได้ตามความถี่ที่คนใช้ (notice > otic)
                            candidates.sort(key=lambda w: self.en_checker.word_frequency.dictionary.get(w, 0), reverse=True)
                            best_candidate = candidates[0]
                            cand_freq = self.en_checker.word_frequency.dictionary.get(best_candidate, 0)
                            
                            # ถ้าคำที่กู้มาได้ เป็นคำที่คนใช้บ่อยกว่าคำเดิม ให้เปลี่ยนทันที!
                            if cand_freq > best_freq:
                                res = best_candidate
                                best_freq = cand_freq
                        
                        # ถ้ากู้ไม่ได้ และคำเดิมก็ผิดชัวร์ๆ ให้ Spell Checker แก้ปกติ
                        if res == lower_token and best_freq == 0:
                            suggested = self.en_checker.correction(lower_token)
                            if suggested: res = suggested
                        
                        if token.istitle(): res = res.capitalize() 
                        elif token.isupper(): res = res.upper()    
                        
                        fixed_text += res
                    else:
                        fixed_text += token 
                        
                return fixed_text
            
            # ==========================================
            # 🇹🇭 --- โหมดภาษาไทย (แก้แบบประโยค 100%) ---
            # ==========================================
            from pythainlp.tokenize import word_tokenize
            from pythainlp.spell import correct as th_correct
            
            # หั่นเป็นคำๆ ก่อนแก้ ป้องกันปัญหา "รอยาการข้าสา"
            tokens = word_tokenize(text, engine='newmm', keep_whitespace=True)
            fixed_tokens = []
            
            i = 0
            while i < len(tokens):
                token = tokens[i]
                if not token.strip() or not bool(re.search(r'[\u0E00-\u0E7F]', token)):
                    fixed_tokens.append(token)
                    i += 1
                    continue
                
                # ลองรวบ 3 คำที่ติดกันเผื่อเป็นคำเดียวที่พิมพ์ผิด
                if i <= len(tokens) - 3:
                    comb3 = tokens[i] + tokens[i+1] + tokens[i+2]
                    sug3 = th_correct(comb3)
                    if sug3 != comb3 and sug3 in self.th_vocab:
                        fixed_tokens.append(sug3)
                        i += 3
                        continue
                
                # ลองรวบ 2 คำ
                if i <= len(tokens) - 2:
                    comb2 = tokens[i] + tokens[i+1]
                    sug2 = th_correct(comb2)
                    if sug2 != comb2 and sug2 in self.th_vocab:
                        fixed_tokens.append(sug2)
                        i += 2
                        continue
                
                # แก้ทีละคำ
                if token not in self.th_vocab:
                    sug1 = th_correct(token)
                    fixed_tokens.append(sug1 if sug1 else token)
                else:
                    fixed_tokens.append(token)
                i += 1
            
            res = "".join(fixed_tokens)
            return res
            
        except Exception: 
            return original_text
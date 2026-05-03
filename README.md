# 🚀 ThaiFixer: Intelligent Thai-English Spell & Language Corrector

> **ThaiFixer** คือโปรแกรมอรรถประโยชน์ (Utility Tool) ที่ออกแบบมาเพื่อแก้ปัญหาการพิมพ์ที่พบบ่อยในชีวิตประจำวัน โดยใช้เทคนิค **Natural Language Processing (NLP)** เข้ามาช่วยวิเคราะห์และแก้ไขข้อความโดยอัตโนมัติ ไม่ว่าจะเป็นการลืมสลับภาษา (Keyboard Layout Trap) หรือการสะกดผิดตามเสียงอ่าน (Phonetic Typo)[cite: 4]

---

## 📋 Table of Contents

1. [Pain Points: ปัญหา "พิมพ์ผิดชีวิตเปลี่ยน"](#pain-points)
2. [วัตถุประสงค์และประโยชน์ที่คาดว่าจะได้รับ](#objectives)
3. [เครื่องมือและเทคโนโลยี (Development Stack)](#tech-stack)
4. [คุณสมบัติเด่นของโปรแกรม (Core Features)](#core-features)
5. [โครงสร้างซอฟต์แวร์ (Software Architecture)](#architecture)
6. [Comparison: ThaiFixer vs RightLang](#comparison)
7. [ปัญหาและข้อจำกัดในปัจจุบัน (Known Issues)](#limitations)
8. [สิ่งที่ต้องการนำไปต่อยอด (Future Works)](#future-works)

---

## 🚩 Pain Points: ปัญหา "พิมพ์ผิดชีวิตเปลี่ยน" <a name="pain-points"></a>

*   **ภาษาต่างดาว (The Alien Language):** การพิมพ์ข้อความยาวๆ โดยลืมสลับภาษา (เช่น พิมพ์ `l;ylfu` แทน `สวัสดี`) ทำให้ต้องลบและพิมพ์ใหม่ซ้ำๆ เสียเวลาและจังหวะการทำงาน[cite: 4]
*   **พิมพ์ตามเสียงสะกด (Phonetic Shift):** ผู้ใช้มักพิมพ์คำผิดตามความคุ้นเคยของเสียงอ่าน (เช่น `รำคาน`) ซึ่งระบบตรวจคำผิดมาตรฐานมักจะตรวจไม่พบ หรือไม่สามารถเสนอคำแก้ที่ถูกต้องได้[cite: 4]
*   **ข้อจำกัดของระบบมาตรฐาน:** Spellchecker ทั่วไปมัก "ยอมแพ้" เมื่อเจอความกำกวมของมาตราตัวสะกดในภาษาไทย[cite: 4]

---

## 🎯 วัตถุประสงค์และประโยชน์ที่คาดว่าจะได้รับ <a name="objectives"></a>

### วัตถุประสงค์
1. เพื่อเพิ่มประสิทธิภาพการตรวจจับและแก้ไขคำสะกดผิด (**Smart Spell Correction**)[cite: 4]
2. เพื่อประยุกต์ใช้การวิเคราะห์บริบททางภาษา (**Contextual Analysis**) มาช่วยในการตัดสินใจเลือกคำ[cite: 4]
3. เพื่อสร้างประสบการณ์การพิมพ์ที่ราบลื่น (**Seamless Typing Experience**) โดยไม่ต้องละมือจากคีย์บอร์ด[cite: 4]

### ประโยชน์ที่คาดว่าจะได้รับ
*   **ด้านประสิทธิภาพการสื่อสาร:** ลดเวลาและขั้นตอนในการแก้ไขข้อความ ลดความขัดแย้งในการสื่อสาร[cite: 4]
*   **ด้านความถูกต้องแม่นยำ:** ข้อมูลที่พิมพ์มีความถูกต้องแม่นยำตามหลักภาษาศาสตร์และมาตรฐาน[cite: 4]
*   **ด้านการประหยัดทรัพยากรผู้ใช้:** ลดภาระทางสมอง (Cognitive Load) ของผู้ใช้ในการกังวลเรื่องการพิมพ์ผิด[cite: 4]

---

## 🛠️ เครื่องมือและเทคโนโลยี (Development Stack) <a name="tech-stack"></a>

*   **Language:** Python 3.x[cite: 4]
*   **IDE:** Visual Studio Code (VS Code)[cite: 4]
*   **NLP Libraries:**
    *   **PyThaiNLP:** เครื่องมือหลักในการจัดการภาษาไทย (Tokenization, Spell Check)[cite: 1, 4]
    *   **NLTK:** สำหรับจัดการคลังคำศัพท์ภาษาอังกฤษ[cite: 1, 4]
    *   **Pyspellchecker:** วิเคราะห์ความถี่และแก้ไขคำสะกดภาษาอังกฤษ[cite: 1, 4]
*   **System Integration:**
    *   **ctypes:** เชื่อมต่อ Windows API (`user32.dll`) เพื่อตรวจสอบและสลับ Keyboard Layout[cite: 4]
    *   **PySide6:** สำหรับสร้างระบบ UI และ Notification Popup[cite: 4]

---

## ✨ คุณสมบัติเด่นของโปรแกรม (Core Features) <a name="core-features"></a>

*   **Lexical Transformation:** แปลง Unicode Sequence ระหว่างไทย-อังกฤษได้อย่างแม่นยำ (Keyboard Layout Mapping)[cite: 1, 4]
*   **Sliding Window Word Tokenization:** ใช้วิธี "รวบกลุ่มคำ" (Chunking) เพื่อประเมินความถูกต้องจากบริบท ป้องกันปัญหาการตัดคำผิดพลาด[cite: 1, 4]
*   **Dual-Language Validation:** ระบบวิเคราะห์ความถูกต้องของประโยค (Threshold 80%) เพื่อตัดสินใจสลับภาษาอัตโนมัติ[cite: 4]
*   **Interactive Notification:** ระบบ Popup แจ้งเตือนผลการแก้ไขแบบ Real-time โดยไม่รบกวนการทำงาน[cite: 4]

---

## 🏗️ โครงสร้างซอฟต์แวร์ (Software Architecture) <a name="architecture"></a>

โปรแกรมประกอบด้วย 4 ส่วนสำคัญที่ทำงานประสานกัน:

1.  **`smart_engine.py` (The Brain):** วิเคราะห์ข้อความ ตรวจสอบภาษา และแก้ไขคำผิดโดยใช้กฎทางสถิติและพจนานุกรม[cite: 4]
2.  **`keyboard_listener.py` (The Senses):** ดักจับเหตุการณ์การพิมพ์ (Keyboard Hooking) และจัดการหน่วยความจำชั่วคราว (Typed Buffer)[cite: 4]
3.  **`notification.py` (The Feedback):** แสดงหน้าต่างแจ้งเตือนการแก้ไขข้อความผ่านระบบ Popup โปร่งแสง[cite: 4]
4.  **`ThaiFixer.py` (The Controller):** จุดเริ่มต้นของโปรแกรม จัดการโหมดการทำงานและ UI ผ่าน System Tray[cite: 4]

---

## ⚖️ Comparison: ThaiFixer vs RightLang <a name="comparison"></a>

เพื่อให้เห็นภาพความแตกต่างของระบบแก้ไขภาษาในปัจจุบัน นี่คือการเปรียบเทียบระหว่าง ThaiFixer และ RightLang (โปรแกรมสลับภาษาดั้งเดิม):

| หัวข้อเปรียบเทียบ | RightLang (Standard) | ThaiFixer (NLP Enhanced) |
| :--- | :--- | :--- |
| **กลไกการตัดสินใจ** | ใช้ Dictionary Matching แบบคำต่อคำ | ใช้ **Sliding Window Chunking** วิเคราะห์กลุ่มคำร่วมกับพจนานุกรม[cite: 4] |
| **การจัดการภาษาอังกฤษ** | สลับเลเยอร์คีย์บอร์ดตามปกติ | มี **Heuristic-based String Correction** เพื่อกู้คืนสระลอย (Floating Vowels)[cite: 4] |
| **การแก้ไขคำสะกดผิด** | เน้นการสลับภาษาเป็นหลัก | มีฟังก์ชัน **SPELL Mode** สำหรับแก้คำสะกดผิดโดยเฉพาะ[cite: 4] |
| **ความยืดหยุ่นของข้อมูล** | ยึดตามลำดับอักขระที่พิมพ์ | มีระบบ **Language Detection & Scoring (Threshold 80%)** เพื่อลดการสลับภาษาผิดพลาด[cite: 4] |
| **การประมวลผลคำไทย** | ตัดคำตามช่องว่างหรือ Dictionary ทั่วไป | ใช้ **PyThaiNLP (newmm engine)** ที่มีความแม่นยำสูงในการตัดคำไทย[cite: 1, 4] |

---

## ⚠️ ปัญหาและข้อจำกัดในปัจจุบัน (Known Issues) <a name="limitations"></a>

*   **Lack of Contextual Semantics:** บางครั้งโปรแกรมปล่อยผ่านคำที่สะกดถูกแต่ผิดบริบทของประโยค[cite: 4]
*   **Greedy Matching Failures:** ปัญหาความกำกวมของโครงสร้างคำที่อาจทำให้ระบบรวมกลุ่มพยัญชนะผิดพลาด[cite: 4]
*   **Out-of-Vocabulary (OOV):** คำศัพท์สแลงหรือคำเกิดใหม่ที่ยังไม่มีในพจนานุกรมหลัก[cite: 4]
*   **OS & Hardware Race Conditions:** ปัญหาคอขวดเมื่อระบบมีการประมวลผลหนัก หรือการแย่งใช้งาน Clipboard[cite: 4]

---

## 🔮 สิ่งที่ต้องการนำไปต่อยอด (Future Works) <a name="future-works"></a>

*   **Full Auto Mode:** พัฒนาให้ระบบแก้ไขคำผิดได้ทันทีโดยไม่ต้องใช้ Manual Trigger[cite: 4]
*   **Syllable-Level Processing:** พัฒนาการประมวลผลระดับ "พยางค์" เพื่อจัดการโครงสร้างภาษาไทยที่ลึกขึ้น[cite: 1, 4]
*   **Hybrid Functionality:** พัฒนาให้ฟังก์ชันสลับภาษาและแก้คำผิดทำงานร่วมกันได้อย่างไร้รอยต่อ[cite: 4]
*   **Suggest Percentage (Confidence Scoring System):**
    *   พัฒนาระบบคำนวณค่าความเชื่อมั่น (Confidence Score) ของคำที่ระบบเสนอแก้ไข โดยแสดงผลเป็นเปอร์เซ็นต์ความน่าจะเป็น[cite: 1]
    *   ใช้หลักการ **Goodness-of-Exemplar** จาก **Prototype Theory** เพื่อวัดความคล้ายคลึงระหว่างคำที่พิมพ์ผิดกับคำต้นแบบในคลังข้อมูล[cite: 1]
    *   ช่วยให้ผู้ใช้ตัดสินใจได้ง่ายขึ้นในกรณีที่คำผิดนั้นสามารถแก้ไขได้หลายรูปแบบ (Ambiguity)[cite: 1]
*   **Code Switching Support (Multi-language Processing):**
    *   พัฒนาอัลกอริทึมให้รองรับการพิมพ์สลับภาษาระหว่างประโยค (เช่น "ไปกินข้าวที่ Siam Paragon") โดยที่ระบบไม่สลับภาษาผิดพลาดเมื่อเจอคำทับศัพท์[cite: 1]
    *   ใช้การวิเคราะห์ **Language Identification** ในระดับหน่วยคำ (Token Level) เพื่อให้ระบบจัดการกับประโยคที่มีความผสมผสานทางภาษาได้อย่างแม่นยำ[cite: 1]

---

> **Summary:** ThaiFixer ไม่ใช่แค่โปรแกรม Utility ทั่วไป แต่เป็นการนำทฤษฎี NLP มาเปลี่ยนเป็นเครื่องมือที่ใช้แก้ปัญหาจริง (Real-world Problem) เพื่อให้การสื่อสารราบลื่นที่สุด[cite: 4]

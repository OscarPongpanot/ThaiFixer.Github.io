# 🚀 ThaiFixer: Intelligent Thai-English Spell & Language Corrector

> **ThaiFixer** คือโปรแกรมอรรถประโยชน์ (Utility Tool) ที่ออกแบบมาเพื่อแก้ปัญหาการพิมพ์ที่พบบ่อยในชีวิตประจำวัน โดยใช้เทคนิค **Natural Language Processing (NLP)** เข้ามาช่วยวิเคราะห์และแก้ไขข้อความโดยอัตโนมัติ ไม่ว่าจะเป็นการลืมสลับภาษา (Keyboard Layout Trap) หรือการสะกดผิดตามเสียงอ่าน (Phonetic Typo)

---

## 📋 Table of Contents

1. [Pain Points: ปัญหา "พิมพ์ผิดชีวิตเปลี่ยน"](#pain-points)
2. [วัตถุประสงค์และประโยชน์ที่คาดว่าจะได้รับ](#objectives)
3. [เครื่องมือและเทคโนโลยี (Development Stack)](#tech-stack)
4. [โครงสร้างและสถาปัตยกรรมซอฟต์แวร์ (Software Architecture)](#architecture)
5. [คุณสมบัติเด่นของโปรแกรม (Core Features)](#core-features)
6. [โครงสร้างซอฟต์แวร์ (Software Architecture)](#architecture)
7. [Comparison: ThaiFixer vs RightLang](#comparison)
8. [ปัญหาและข้อจำกัดในปัจจุบัน (Known Issues)](#limitations)
9. [สิ่งที่ต้องการนำไปต่อยอด (Future Works)](#future-works)

---

## 🚩 Pain Points: ปัญหา "พิมพ์ผิดชีวิตเปลี่ยน" <a name="pain-points"></a>

*   **ภาษาต่างดาว (The Alien Language):** การพิมพ์ข้อความยาวๆ โดยลืมสลับภาษา (เช่น พิมพ์ `l;ylfu` แทน `สวัสดี`) ทำให้ต้องลบและพิมพ์ใหม่ซ้ำๆ เสียเวลาและจังหวะการทำงาน
*   **พิมพ์ตามเสียงสะกด (Phonetic Shift):** ผู้ใช้มักพิมพ์คำผิดตามความคุ้นเคยของเสียงอ่าน (เช่น `รำคาน`) ซึ่งระบบตรวจคำผิดมาตรฐานมักจะตรวจไม่พบ หรือไม่สามารถเสนอคำแก้ที่ถูกต้องได้
*   **ข้อจำกัดของระบบมาตรฐาน:** Spellchecker ทั่วไปมัก "ยอมแพ้" เมื่อเจอความกำกวมของมาตราตัวสะกดในภาษาไทย

---

## 🎯 วัตถุประสงค์และประโยชน์ที่คาดว่าจะได้รับ <a name="objectives"></a>

### วัตถุประสงค์
1. เพื่อเพิ่มประสิทธิภาพการตรวจจับและแก้ไขคำสะกดผิด (**Smart Spell Correction**)
2. เพื่อประยุกต์ใช้การวิเคราะห์บริบททางภาษา (**Contextual Analysis**) มาช่วยในการตัดสินใจเลือกคำ
3. เพื่อสร้างประสบการณ์การพิมพ์ที่ราบลื่น (**Seamless Typing Experience**) โดยไม่ต้องละมือจากคีย์บอร์ด

### ประโยชน์ที่คาดว่าจะได้รับ
*   **ด้านประสิทธิภาพการสื่อสาร:** ลดเวลาและขั้นตอนในการแก้ไขข้อความ ลดความขัดแย้งในการสื่อสาร
*   **ด้านความถูกต้องแม่นยำ:** ข้อมูลที่พิมพ์มีความถูกต้องแม่นยำตามหลักภาษาศาสตร์และมาตรฐาน
*   **ด้านการประหยัดทรัพยากรผู้ใช้:** ลดภาระทางสมอง (Cognitive Load) ของผู้ใช้ในการกังวลเรื่องการพิมพ์ผิด

---

## 🛠️ เครื่องมือและเทคโนโลยี (Development Stack) <a name="tech-stack"></a>

*   **Language:** Python 3.x
*   **IDE:** Visual Studio Code (VS Code)
*   **NLP Libraries:**
    *   **PyThaiNLP:** เครื่องมือหลักในการจัดการภาษาไทย (Tokenization, Spell Check)
    *   **NLTK:** สำหรับจัดการคลังคำศัพท์ภาษาอังกฤษ
    *   **Pyspellchecker:** วิเคราะห์ความถี่และแก้ไขคำสะกดภาษาอังกฤษ
*   **System Integration:**
    *   **ctypes:** เชื่อมต่อ Windows API (`user32.dll`) เพื่อตรวจสอบและสลับ Keyboard Layout
    *   **PySide6:** สำหรับสร้างระบบ UI และ Notification Popup

---

## 🏗️ โครงสร้างและสถาปัตยกรรมซอฟต์แวร์ (Software Architecture) <a name="architecture"></a>

สถาปัตยกรรมของโปรเจกต์ถูกออกแบบในลักษณะ **Modular Architecture** โดยแบ่งออกเป็น 4 ส่วนประกอบหลักที่ทำงานประสานกันเปรียบเสมือนการทำงานของระบบร่างกาย:

| ส่วนประกอบ (Module) | บทบาทหน้าที่ (Core Responsibility) | รายละเอียดการทำงาน (Implementation Details) |
| :--- | :--- | :--- |
| **1. `smart_engine.py`**<br>(The Brain) | **สมองส่วนกลาง** | • เป็นส่วนประมวลผลหลัก (Core Logic) ที่ใช้เทคนิค Lexical Analysis และ Statistical NLP<br>• วิเคราะห์ข้อความ ตรวจสอบภาษา กู้คืนข้อความต่างดาว และแก้ไขคำผิดผ่านพจนานุกรมและความถี่คำ |
| **2. `keyboard_listener.py`**<br>(The Senses) | **ประสาทสัมผัส** | • ทำหน้าที่เป็น Input & Event Listener คอยเฝ้าสังเกตการณ์การพิมพ์ (Keyboard Hooking)<br>• ดักจับคีย์ลัด ควบคุมโหมดการทำงาน จำลองการสั่งงานคีย์บอร์ด และจัดการหน่วยความจำชั่วคราว (Typed Buffer) |
| **3. `notification.py`**<br>(The Feedback) | **การสื่อสาร** | • ส่วนติดต่อผู้ใช้เชิงโต้ตอบ (Interactive UI) ในรูปแบบหน้าต่าง Popup โปร่งแสง (Translucent Overlay)<br>• รายงานผลและยืนยันการแก้ไขข้อความให้ผู้ใช้ทราบทันที พร้อมระบบซ่อนอัตโนมัติ (Auto-Hide Mechanism) |
| **4. `ThaiFixer.py`**<br>(The Controller) | **ศูนย์กลางควบคุม** | • จุดเริ่มต้นโปรแกรม (Application Entry Point) รวบรวมการทำงานของ Engine, Listener และ UI<br>• จัดการโหมดผ่าน System Tray และควบคุมการสื่อสารระหว่างโมดูลด้วยสถาปัตยกรรม Event-Driven |

---

## ✨ คุณสมบัติเด่นของโปรแกรม (Core Features) <a name="core-features"></a>

*   **Lexical Transformation:** แปลง Unicode Sequence ระหว่างไทย-อังกฤษได้อย่างแม่นยำ (Keyboard Layout Mapping)
*   **Sliding Window Word Tokenization:** ใช้วิธี "รวบกลุ่มคำ" (Chunking) เพื่อประเมินความถูกต้องจากบริบท ป้องกันปัญหาการตัดคำผิดพลาด
*   **Dual-Language Validation:** ระบบวิเคราะห์ความถูกต้องของประโยค (Threshold 80%) เพื่อตัดสินใจสลับภาษาอัตโนมัติ
*   **Interactive Notification:** ระบบ Popup แจ้งเตือนผลการแก้ไขแบบ Real-time โดยไม่รบกวนการทำงาน

---

## ⚖️ Comparison: ThaiFixer vs RightLang <a name="comparison"></a>

เพื่อให้เห็นภาพความแตกต่างของระบบแก้ไขภาษาในปัจจุบัน นี่คือการเปรียบเทียบระหว่าง ThaiFixer และ RightLang (โปรแกรมสลับภาษาดั้งเดิม):

| หัวข้อเปรียบเทียบ | RightLang (Standard) | ThaiFixer (NLP Enhanced) |
| :--- | :--- | :--- |
| **กลไกการตัดสินใจ** | ใช้ Dictionary Matching แบบคำต่อคำ | ใช้ **Sliding Window Chunking** วิเคราะห์กลุ่มคำร่วมกับพจนานุกรม |
| **การจัดการภาษาอังกฤษ** | สลับเลเยอร์คีย์บอร์ดตามปกติ | มี **Heuristic-based String Correction** เพื่อกู้คืนสระลอย (Floating Vowels) |
| **การแก้ไขคำสะกดผิด** | เน้นการสลับภาษาเป็นหลัก | มีฟังก์ชัน **SPELL Mode** สำหรับแก้คำสะกดผิดโดยเฉพาะ |
| **ความยืดหยุ่นของข้อมูล** | ยึดตามลำดับอักขระที่พิมพ์ | มีระบบ **Language Detection & Scoring (Threshold 80%)** เพื่อลดการสลับภาษาผิดพลาด |
| **การประมวลผลคำไทย** | ตัดคำตามช่องว่างหรือ Dictionary ทั่วไป | ใช้ **PyThaiNLP (newmm engine)** ที่มีความแม่นยำสูงในการตัดคำไทย |

---

## ⚠️ ปัญหาและข้อจำกัดในปัจจุบัน (Known Issues) <a name="limitations"></a>

*   **Lack of Contextual Semantics:** บางครั้งโปรแกรมปล่อยผ่านคำที่สะกดถูกแต่ผิดบริบทของประโยค
*   **Greedy Matching Failures:** ปัญหาความกำกวมของโครงสร้างคำที่อาจทำให้ระบบรวมกลุ่มพยัญชนะผิดพลาด
*   **Out-of-Vocabulary (OOV):** คำศัพท์สแลงหรือคำเกิดใหม่ที่ยังไม่มีในพจนานุกรมหลัก
*   **OS & Hardware Race Conditions:** ปัญหาคอขวดเมื่อระบบมีการประมวลผลหนัก หรือการแย่งใช้งาน Clipboard

---

## 🔮 สิ่งที่ต้องการนำไปต่อยอด (Future Works) <a name="future-works"></a>

*   **Full Auto Mode:** พัฒนาให้ระบบแก้ไขคำผิดได้ทันทีโดยไม่ต้องใช้ Manual Trigger
*   **Syllable-Level Processing:** พัฒนาการประมวลผลระดับ "พยางค์" เพื่อจัดการโครงสร้างภาษาไทยที่ลึกขึ้น
*   **Hybrid Functionality:** พัฒนาให้ฟังก์ชันสลับภาษาและแก้คำผิดทำงานร่วมกันได้อย่างไร้รอยต่อ
*   **Suggest Percentage (Confidence Scoring System):**
    *   พัฒนาระบบคำนวณค่าความเชื่อมั่น (Confidence Score) ของคำที่ระบบเสนอแก้ไข โดยแสดงผลเป็นเปอร์เซ็นต์ความน่าจะเป็น
    *   ใช้หลักการ **Goodness-of-Exemplar** จาก **Prototype Theory** เพื่อวัดความคล้ายคลึงระหว่างคำที่พิมพ์ผิดกับคำต้นแบบในคลังข้อมูล
    *   ช่วยให้ผู้ใช้ตัดสินใจได้ง่ายขึ้นในกรณีที่คำผิดนั้นสามารถแก้ไขได้หลายรูปแบบ (Ambiguity)
*   **Code Switching Support (Multi-language Processing):**
    *   พัฒนาอัลกอริทึมให้รองรับการพิมพ์สลับภาษาระหว่างประโยค (เช่น "ไปกินข้าวที่ Siam Paragon") โดยที่ระบบไม่สลับภาษาผิดพลาดเมื่อเจอคำทับศัพท์
    *   ใช้การวิเคราะห์ **Language Identification** ในระดับหน่วยคำ (Token Level) เพื่อให้ระบบจัดการกับประโยคที่มีความผสมผสานทางภาษาได้อย่างแม่นยำ

---

> **Summary:** ThaiFixer ไม่ใช่แค่โปรแกรม Utility ทั่วไป แต่เป็นการนำทฤษฎี NLP มาเปลี่ยนเป็นเครื่องมือที่ใช้แก้ปัญหาจริง (Real-world Problem) เพื่อให้การสื่อสารราบลื่นที่สุด

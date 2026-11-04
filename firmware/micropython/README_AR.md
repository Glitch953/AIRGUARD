# AIRGUARD — MicroPython Firmware Rev 1

## مهم
اللوحة ESP32-S3 لا تشغّل ملف Python العادي مباشرة. المطلوب تثبيت **MicroPython firmware** على ESP32-S3 أولاً، ثم نسخ `main.py` و`ssd1306.py` إلى ذاكرة الجهاز. هذا المشروع يستخدم MicroPython، وليس CPython على الكمبيوتر.

## وظائف النسخة
- مسح شبكات Wi-Fi القريبة بشكل سلبي فقط.
- عرض اسم الشبكة (SSID)، القناة، قوة الإشارة RSSI، ونوع الحماية على OLED.
- أزرار للتنقل وعرض التفاصيل وإعادة المسح.
- لا يتصل بأي شبكة، ولا يحاول معرفة كلمات المرور، ولا يرسل deauthentication أو تشويشاً.
- الجرس معطّل في هذه النسخة؛ لا تركّب U3.

## Pin map المستخرج من لوحة AIRGUARD
| الوظيفة | GPIO | ملاحظة |
|---|---:|---|
| OLED SDA | 6 | من U1 pad 6 / net SDA |
| OLED SCL | 7 | من U1 pad 7 / net SCL |
| SW1 Up | 1 | active-low إلى GND |
| SW2 Down | 2 | active-low إلى GND |
| SW3 Select | 3 | active-low؛ لا تضغطه أثناء إعادة التشغيل/الإقلاع |
| SW4 Back | 4 | active-low إلى GND |
| SW5 Scan | 5 | active-low إلى GND |
| SW6 Reset | EN | إعادة تشغيل عتادية |
| Buzzer | GPIO10 / BUZZER_DRV | معطّل، لا تركّب الجرس في هذه النسخة |

ملاحظة: تعيين SDA/SCL إلى GPIO6/GPIO7 مبني على أرقام أرجل U1 في المخطط والـPCB وعلى pinout وحدة ESP32-S3-WROOM-1. إذا كانت نسخة الموديول/اللوحة مختلفة، قِس أو راجع الـdatasheet قبل التشغيل.

## توصيل OLED
J2:
1. GND
2. 3V3
3. SDA
4. SCL

الكود يحاول العنوان 0x3C ثم 0x3D. شاشة 128×64 متوقعة.

## تثبيت MicroPython وتشغيل الكود
1. نزّل إصدار MicroPython الرسمي المناسب لـ ESP32-S3 من صفحة تنزيل MicroPython.
2. استخدم Thonny أو esptool لكتابة firmware على اللوحة. تأكد من اختيار ملف ESP32-S3 الصحيح.
3. في Thonny اختر Interpreter: MicroPython (ESP32).
4. اتصل عبر USB. إذا لم يظهر المنفذ، جرّب كابل USB بيانات واضغط BOOT أثناء توصيل USB ثم اتركه.
5. انسخ `ssd1306.py` و`main.py` إلى جهاز ESP32 (Save as: MicroPython device).
6. أعد التشغيل. تظهر واجهة AIRGUARD على OLED.

## التحكم
- SW1: تحريك للأعلى
- SW2: تحريك للأسفل
- SW3: عرض تفاصيل الشبكة المحددة
- SW4: رجوع
- SW5: إعادة مسح الشبكات

## تنبيه GPIO3
GPIO3 في ESP32-S3 له وظيفة strapping. لا تترك SW3 مضغوطاً عند الضغط على Reset أو أثناء تشغيل اللوحة لأول مرة. إذا ظهرت مشكلة إقلاع، اترك الأزرار كلها غير مضغوطة ثم أعد التشغيل.

## إذا لم تعمل الشاشة
افتح REPL في Thonny وشغّل:
```python
from machine import Pin, SoftI2C
i2c = SoftI2C(scl=Pin(7), sda=Pin(6), freq=100000)
print(i2c.scan())
```
المتوقع ظهور `[60]` للعنوان 0x3C أو `[61]` للعنوان 0x3D.

## الاختبار الأول
- تحقق من أن R7 وU3 غير مركّبتين (DNP).
- شغّل الجهاز بمصدر 5V محدود التيار.
- تحقق من 3V3 قبل الاستخدام.
- تحقق من ظهور OLED.
- جرّب الأزرار الخمسة.
- اضغط Scan وانتظر النتائج.
- لا تعتبر اللوحة مثبتة النجاح قبل اختبار USB وWi-Fi وOLED على العتاد الحقيقي.

## حدود النسخة
هذا Firmware أولي. مسح Wi-Fi يعتمد على دعم MicroPython المدمج في إصدار ESP32-S3. قد تختلف أسماء auth modes حسب نسخة MicroPython. لا يتضمن تسجيل بيانات، اتصالاً بالشبكات، أو ميزات هجومية.

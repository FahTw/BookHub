# การสร้าง Order หลายรายการจาก Cart

## การเปลี่ยนแปลงหลัก

### 1. PaymentView.post() - สร้าง Order แยกตามแต่ละ Cart Item
- **เดิม**: สร้าง 1 Order จาก Cart Item แรกเท่านั้น
- **ใหม่**: สร้าง Order แยกสำหรับแต่ละ Cart Item
- ใช้ `transaction.atomic()` เพื่อความปลอดภัยของข้อมูล
- สร้าง Payment แยกสำหรับแต่ละ Order
- จัดการ payment slip และ method ที่แตกต่างกัน

### 2. เพิ่ม Views ใหม่

#### AddToCartView
- เพิ่มหนังสือลงตะกร้าได้ทีละเล่ม
- ตรวจสอบว่ามีสินค้าในตะกร้าแล้วหรือไม่
- เพิ่มจำนวนถ้ามีอยู่แล้ว หรือสร้างใหม่

#### CreateSampleCartView
- สร้างข้อมูลตัวอย่าง 3 รายการในตะกร้า
- แต่ละรายการมีจำนวนต่างกัน (1, 2, 3)
- ใช้สำหรับทดสอบการสร้าง Order หลายรายการ

### 3. ปรับปรุง OrderHistoryView
- จัดกลุ่ม Order ตามวันที่และเวลา
- แสดงจำนวน Order ทั้งหมด
- เปลี่ยน template path เป็น "home/orderhistory.html"

### 4. เพิ่ม URL Patterns
```python
path('add_to_cart/<int:user_id>/<int:book_id>/', views.AddToCartView.as_view(), name='add_to_cart'),
path('create_sample_cart/<int:user_id>/', views.CreateSampleCartView.as_view(), name='create_sample_cart'),
```

### 5. ปรับปรุง book_list.html
- เพิ่มปุ่ม "เพิ่มลงตะกร้า" สำหรับแต่ละหนังสือ
- เพิ่มปุ่ม "สร้างตะกร้าตัวอย่าง" สำหรับทดสอบ
- เพิ่มปุ่ม "ดูตะกร้าสินค้า"

## วิธีการทดสอบ

1. **สร้างข้อมูลตัวอย่าง**:
   - ไปที่หน้า Book List
   - คลิก "สร้างตะกร้าตัวอย่าง (3 รายการ)"

2. **ตรวจสอบตะกร้า**:
   - คลิก "ดูตะกร้าสินค้า"
   - จะเห็น 3 รายการ ปริมาณ 1, 2, 3 ตามลำดับ

3. **ทำการชำระเงิน**:
   - คลิก "ดำเนินการชำระเงิน"
   - เลือกวิธีการชำระเงิน
   - อัปโหลดสลิป (ถ้าไม่ใช่เก็บเงินปลายทาง)
   - คลิก "ยืนยันการชำระเงิน"

4. **ตรวจสอบผลลัพธ์**:
   - ระบบจะสร้าง 3 Orders แยกกัน
   - แต่ละ Order จะมี Payment แยกกัน
   - Cart items จะเปลี่ยน status เป็น 'notin_cart'

## ผลลัพธ์

- **Order 1**: หนังสือเล่มที่ 1, จำนวน 1, ราคาตาม book.price × 1
- **Order 2**: หนังสือเล่มที่ 2, จำนวน 2, ราคาตาม book.price × 2  
- **Order 3**: หนังสือเล่มที่ 3, จำนวน 3, ราคาตาม book.price × 3

แต่ละ Order จะมี Payment record แยกต่างหาก พร้อมกับ payment slip (ถ้ามี)

## Error Handling

- ใช้ `transaction.atomic()` เพื่อ rollback ทั้งหมดถ้าเกิด error
- ลบ Orders ที่สร้างไปแล้วถ้าเกิดปัญหา
- แสดงข้อความ error ให้ผู้ใช้ทราบ
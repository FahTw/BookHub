-- BookHub Sample Data for Models Migration
-- This file contains sample data that matches the models.py structure

-- Insert CustomUsers - password: 123456789@za
INSERT INTO book_customuser (id, username, first_name, last_name, email, is_staff, is_active, is_superuser, date_joined, password, phone, address, province, postal_code) VALUES
(10, 'admin', 'Admin', 'System', 'admin@bookhub.com', true, true, true, '2025-01-01 00:00:00', 'pbkdf2_sha256$1000000$2Ke79T51Wwh3p492ZJ3AaI$sML7HagBRHvVOhYFA4UIJmnBpNFiLQeVP/OOxJ+otQM=', '02-123-4567', '456 ถนนสีลม', 'กรุงเทพมหานคร', '10500'),
(11, 'somchai', 'สมชาย', 'ใจดี', 'somchai@email.com', false, true, false, '2025-01-01 00:00:00', 'pbkdf2_sha256$1000000$2Ke79T51Wwh3p492ZJ3AaI$sML7HagBRHvVOhYFA4UIJmnBpNFiLQeVP/OOxJ+otQM=', '081-234-5678', '123 ถนนพระราม 4 แขวงสีลม เขตบางรัก', 'กรุงเทพมหานคร', '10500'),
(12, 'suda', 'สุดา', 'สวยงาม', 'suda@email.com', false, true, false, '2025-01-01 00:00:00', 'pbkdf2_sha256$1000000$2Ke79T51Wwh3p492ZJ3AaI$sML7HagBRHvVOhYFA4UIJmnBpNFiLQeVP/OOxJ+otQM=', '081-345-6789', '789 ถนนสุขุมวิท แขวงคลองตัน เขตคลองตัน', 'กรุงเทพมหานคร', '10110'),
(13, 'niran', 'นิรันดร์', 'รักเรียน', 'niran@email.com', false, true, false, '2025-01-01 00:00:00', 'pbkdf2_sha256$1000000$2Ke79T51Wwh3p492ZJ3AaI$sML7HagBRHvVOhYFA4UIJmnBpNFiLQeVP/OOxJ+otQM=', '081-456-7890', '321 ถนนลาดพร้าว แขวงจอมพล เขตจตุจักร', 'กรุงเทพมหานคร', '10900'),
(14, 'mana', 'มานะ', 'ขยันหมั่นเพียร', 'mana@email.com', true, true, false, '2025-01-01 00:00:00', 'pbkdf2_sha256$1000000$2Ke79T51Wwh3p492ZJ3AaI$sML7HagBRHvVOhYFA4UIJmnBpNFiLQeVP/OOxJ+otQM=', '081-567-8901', '654 ถนนเพชรบุรี แขวงมักกะสัน เขตราชเทวี', 'กรุงเทพมหานคร', '10400');

-- Insert Books
INSERT INTO book_book (id, title, image, author, publisher, publication_date, pages, language, detail, price, stock, sold, rating_average, rating_count) VALUES
(10, 'พอใจ', 'book/pojai.jpg', 'นิตยา เทวดา', 'นานมีบุ๊คส์', '2023-06-15', 320, 'ไทย', 'นวนิยายเรื่องราวความรักและความฝันของสาวน้อยในชนบท ที่เดินทางมาสู่กรุงเทพฯ เพื่อค้นหาความหมายของชีวิต', 350.00, 15, 25, 4.2, 18),
(11, 'จิตวิทยาสายดาร์ก', 'book/dark_psychology.jpg', 'ดร.สมศักดิ์ จิตเข้มแข็ง', 'สำนักพิมพ์จิตวิทยา', '2023-08-20', 280, 'ไทย', 'เข้าใจจิตใจมนุษย์ในแง่มุมที่ซ่อนเร้น การอ่านใจคน และเทคนิคการปกป้องตนเองจากการถูกใช้ประโยชน์', 420.00, 8, 32, 4.5, 27),
(12, 'Python Programming Complete', 'book/python_programming.jpg', 'John Smith', 'TechBooks Publishing', '2023-09-10', 450, 'English', 'Complete guide to Python programming from basics to advanced topics including web development, data science, and machine learning', 890.00, 12, 18, 4.7, 15),
(13, 'ธุรกิจยุคดิจิทัล', 'book/digital_business.jpg', 'ผศ.ดร.วิทยา ธุรกิจดี', 'สำนักพิมพ์ธุรกิจ', '2023-07-25', 380, 'ไทย', 'กลยุทธ์และแนวทางการทำธุรกิจในยุคดิจิทัล การตลาดออนไลน์ และการพัฒนาช่องทางการขาย', 520.00, 20, 14, 4.3, 12),
(14, 'สุขภาพดีด้วยโยคะ', 'book/yoga_health.jpg', 'อาจารย์สุขใจ แข็งแรง', 'สุขภาพดีพับลิชชิ่ง', '2023-05-30', 250, 'ไทย', 'คู่มือการฝึกโยคะเบื้องต้นสำหรับมื้อใหม่ ท่าโยคะเพื่อสุขภาพ และการผ่อนคลาย', 380.00, 25, 8, 4.1, 6),
(15, 'การศึกษาในศตวรรษที่ 21', 'book/education_21st.jpg', 'ศ.ดร.การศึกษา เรียนรู้', 'สำนักพิมพ์การศึกษา', '2023-04-18', 320, 'ไทย', 'แนวโน้มและการเปลี่ยนแปลงของการศึกษาในยุคใหม่ เทคโนโลยีเพื่อการศึกษา และการเรียนรู้ตลอดชีวิต', 450.00, 18, 5, 4.0, 4);

-- Insert Book Categories
INSERT INTO book_bookcategory (id, category_name, description) VALUES
(10, 'นวนิยาย', 'หนังสือนวนิยายแนวต่างๆ ทั้งไทยและแปล'),
(11, 'การพัฒนาตนเอง', 'หนังสือเพื่อการพัฒนาและเสริมสร้างตัวเอง'),
(12, 'เทคโนโลยี', 'หนังสือเกี่ยวกับเทคโนโลยีและการเขียนโปรแกรม'),
(13, 'ธุรกิจ', 'หนังสือเกี่ยวกับการทำธุรกิจและการลงทุน'),
(14, 'สุขภาพ', 'หนังสือเกี่ยวกับการดูแลสุขภาพและการออกกำลังกาย'),
(15, 'การศึกษา', 'หนังสือสำหรับการศึกษาและการเรียนรู้');

-- Insert Book Categories Relationships (Many-to-Many)
INSERT INTO book_book_categories (id, book_id, bookcategory_id) VALUES
(10, 10, 10), -- พอใจ -> นวนิยาย
(11, 11, 11), -- จิตวิทยาสายดาร์ก -> การพัฒนาตนเอง
(12, 12, 12), -- Python Programming -> เทคโนโลยี
(13, 13, 13), -- ธุรกิจยุคดิจิทัล -> ธุรกิจ
(14, 13, 12), -- ธุรกิจยุคดิจิทัล -> เทคโนโลยี
(15, 14, 14), -- สุขภาพดีด้วยโยคะ -> สุขภาพ
(16, 15, 15); -- การศึกษาในศตวรรษที่ 21 -> การศึกษา

-- Insert Carts
INSERT INTO book_cart (id, user_id, book_id, quantity, price, total_price, status) VALUES
(10, 12, 13, 1, 520.00, 520.00, 'in_cart'), -- สุดา กำลังเลือกซื้อ ธุรกิจยุคดิจิทัล
(11, 12, 14, 2, 380.00, 760.00, 'in_cart'), -- สุดา กำลังเลือกซื้อ สุขภาพดีด้วยโยคะ x2
(12, 13, 15, 1, 450.00, 450.00, 'in_cart'), -- นิรันดร์ กำลังเลือกซื้อ การศึกษาในศตวรรษที่ 21
(13, 11, 10, 2, 350.00, 700.00, 'notin_cart'), -- สมชาย ซื้อ พอใจ x2 แล้ว
(14, 12, 11, 1, 420.00, 420.00, 'notin_cart'); -- สุดา ซื้อ จิตวิทยาสายดาร์ก แล้ว

-- Insert Orders
INSERT INTO book_order (id, user_id, cart_id, order_date, total_amount, status) VALUES
(10, 11, 13, '2025-01-15 10:30:00', 700.00, 'delivered'), -- สมชาย สั่งซื้อ พอใจ x2
(11, 12, 14, '2025-01-14 14:20:00', 420.00, 'shipped'), -- สุดา สั่งซื้อ จิตวิทยาสายดาร์ก
(12, 13, 12, '2025-01-13 09:15:00', 450.00, 'processing'), -- นิรันดร์ สั่งซื้อ การศึกษาในศตวรรษที่ 21
(13, 14, 10, '2025-01-12 16:45:00', 520.00, 'paid'), -- มานะ สั่งซื้อ ธุรกิจยุคดิจิทัล
(14, 11, 11, '2025-01-11 11:30:00', 760.00, 'cancelled'); -- สมชาย สั่งซื้อ สุขภาพดีด้วยโยคะ x2

-- Insert Payments
INSERT INTO book_payment (id, order_id, payment_slip, payment_date, method, amount, status, verified_date) VALUES
(10, 10, 'payment/slip_001.jpg', '2025-01-15 10:35:00', 'promptpay', 700.00, 'approved', '2025-01-15 11:00:00'),
(11, 11, 'payment/slip_002.jpg', '2025-01-14 14:25:00', 'bank', 420.00, 'approved', '2025-01-14 15:00:00'),
(12, 12, 'payment/slip_003.jpg', '2025-01-13 09:20:00', 'promptpay', 450.00, 'approved', '2025-01-13 10:00:00'),
(13, 13, 'payment/slip_004.jpg', '2025-01-12 16:50:00', 'bank', 520.00, 'pending', NULL),
(14, 14, NULL, '2025-01-11 11:30:00', 'cash', 760.00, 'pending', NULL);

-- Insert Reviews (updated for new Review model structure)
INSERT INTO book_review (id, user_id, book_id, rating, comment, created_date) VALUES
(10, 11, 10, 4, 'หนังสือดีมาก เนื้อเรื่องน่าติดตาม อ่านแล้วซาบซึ้งใจ', '2025-01-16 08:00:00'),
(11, 12, 11, 5, 'เนื้อหาลึกซึ้งมาก ได้ความรู้เยอะ แนะนำให้คนที่สนใจจิตวิทยา', '2025-01-15 18:30:00'),
(12, 13, 12, 5, 'Perfect book for Python beginners and advanced users. Very comprehensive!', '2025-01-14 20:15:00'),
(13, 11, 11, 4, 'อ่านเพิ่มเติมนอกเหนือจากที่สั่งซื้อ เนื้อหาดีจริง', '2025-01-10 14:20:00'),
(14, 14, 13, 5, 'หนังสือธุรกิจที่ดีมาก เข้าใจง่าย มีประโยชน์สำหรับผู้ประกอบการ', '2025-01-09 16:45:00');

-- BookHub Sample Data for Models Migration
-- This file contains sample data that matches the models.py structure

-- Insert Book Categories
INSERT INTO book_bookcategory (id, category_name, description) VALUES
(1, 'นวนิยาย', 'หนังสือนวนิยายแนวต่างๆ ทั้งไทยและแปล'),
(2, 'การพัฒนาตนเอง', 'หนังสือเพื่อการพัฒนาและเสริมสร้างตัวเอง'),
(3, 'เทคโนโลยี', 'หนังสือเกี่ยวกับเทคโนโลยีและการเขียนโปรแกรม'),
(4, 'ธุรกิจ', 'หนังสือเกี่ยวกับการทำธุรกิจและการลงทุน'),
(5, 'สุขภาพ', 'หนังสือเกี่ยวกับการดูแลสุขภาพและการออกกำลังกาย'),
(6, 'การศึกษา', 'หนังสือสำหรับการศึกษาและการเรียนรู้');

-- Insert Users
INSERT INTO book_user (id, first_name, last_name, email, phone, password, role, address, province, postal_code) VALUES
(1, 'Admin', 'System', 'admin@bookhub.com', '02-123-4567', 'hashed_password_admin', 'admin', '456 ถนนสีลม', 'กรุงเทพมหานคร', '10500'),
(2, 'สมชาย', 'ใจดี', 'somchai@email.com', '081-234-5678', 'hashed_password_1', 'user', '123 ถนนพระราม 4 แขวงสีลม เขตบางรัก', 'กรุงเทพมหานคร', '10500'),
(3, 'สุดา', 'สวยงาม', 'suda@email.com', '081-345-6789', 'hashed_password_2', 'user', '789 ถนนสุขุมวิท แขวงคลองตัน เขตคลองตัน', 'กรุงเทพมหานคร', '10110'),
(4, 'นิรันดร์', 'รักเรียน', 'niran@email.com', '081-456-7890', 'hashed_password_3', 'user', '321 ถนนลาดพร้าว แขวงจอมพล เขตจตุจักร', 'กรุงเทพมหานคร', '10900'),
(5, 'มานะ', 'ขยันหมั่นเพียร', 'mana@email.com', '081-567-8901', 'hashed_password_4', 'user', '654 ถนนเพชรบุรี แขวงมักกะสัน เขตราชเทวี', 'กรุงเทพมหานคร', '10400');

-- Insert Books
INSERT INTO book_book (id, title, image, author, publisher, publication_date, pages, language, detail, price, stock, sold_count, rating_average, rating_count) VALUES
(1, 'พอใจ', 'book/pojai.jpg', 'นิตยา เทวดา', 'นานมีบุ๊คส์', '2023-06-15', 320, 'ไทย', 'นวนิยายเรื่องราวความรักและความฝันของสาวน้อยในชนบท ที่เดินทางมาสู่กรุงเทพฯ เพื่อค้นหาความหมายของชีวิต', 350.00, 15, 25, 4.2, 18),
(2, 'จิตวิทยาสายดาร์ก', 'book/dark_psychology.jpg', 'ดร.สมศักดิ์ จิตเข้มแข็ง', 'สำนักพิมพ์จิตวิทยา', '2023-08-20', 280, 'ไทย', 'เข้าใจจิตใจมนุษย์ในแง่มุมที่ซ่อนเร้น การอ่านใจคน และเทคนิคการปกป้องตนเองจากการถูกใช้ประโยชน์', 420.00, 8, 32, 4.5, 27),
(3, 'Python Programming Complete', 'book/python_programming.jpg', 'John Smith', 'TechBooks Publishing', '2023-09-10', 450, 'English', 'Complete guide to Python programming from basics to advanced topics including web development, data science, and machine learning', 890.00, 12, 18, 4.7, 15),
(4, 'ธุรกิจยุคดิจิทัล', 'book/digital_business.jpg', 'ผศ.ดร.วิทยา ธุรกิจดี', 'สำนักพิมพ์ธุรกิจ', '2023-07-25', 380, 'ไทย', 'กลยุทธ์และแนวทางการทำธุรกิจในยุคดิจิทัล การตลาดออนไลน์ และการพัฒนาช่องทางการขาย', 520.00, 20, 14, 4.3, 12),
(5, 'สุขภาพดีด้วยโยคะ', 'book/yoga_health.jpg', 'อาจารย์สุขใจ แข็งแรง', 'สุขภาพดีพับลิชชิ่ง', '2023-05-30', 250, 'ไทย', 'คู่มือการฝึกโยคะเบื้องต้นสำหรับมื้อใหม่ ท่าโยคะเพื่อสุขภาพ และการผ่อนคลาย', 380.00, 25, 8, 4.1, 6),
(6, 'การศึกษาในศตวรรษที่ 21', 'book/education_21st.jpg', 'ศ.ดร.การศึกษา เรียนรู้', 'สำนักพิมพ์การศึกษา', '2023-04-18', 320, 'ไทย', 'แนวโน้มและการเปลี่ยนแปลงของการศึกษาในยุคใหม่ เทคโนโลยีเพื่อการศึกษา และการเรียนรู้ตลอดชีวิต', 450.00, 18, 5, 4.0, 4);

-- Insert Book Categories Relationships (Many-to-Many)
INSERT INTO book_book_categories (id, book_id, bookcategory_id) VALUES
(1, 1, 1), -- พอใจ -> นวนิยาย
(2, 2, 2), -- จิตวิทยาสายดาร์ก -> การพัฒนาตนเอง
(3, 3, 3), -- Python Programming -> เทคโนโลยี
(4, 4, 4), -- ธุรกิจยุคดิจิทัล -> ธุรกิจ
(5, 4, 3), -- ธุรกิจยุคดิจิทัล -> เทคโนโลยี
(6, 5, 5), -- สุขภาพดีด้วยโยคะ -> สุขภาพ
(7, 6, 6); -- การศึกษาในศตวรรษที่ 21 -> การศึกษา

-- Insert Orders
INSERT INTO book_order (id, user_id, order_date, total_amount, shipping_cost, discount_amount, final_amount, status) VALUES
(1, 2, '2025-01-15 10:30:00', 700.00, 50.00, 0.00, 750.00, 'delivered'),
(2, 3, '2025-01-14 14:20:00', 420.00, 50.00, 30.00, 440.00, 'shipped'),
(3, 4, '2025-01-13 09:15:00', 890.00, 50.00, 0.00, 940.00, 'processing'),
(4, 5, '2025-01-12 16:45:00', 520.00, 50.00, 20.00, 550.00, 'paid'),
(5, 2, '2025-01-11 11:30:00', 380.00, 50.00, 0.00, 430.00, 'pending');

-- Insert Order Details
INSERT INTO book_orderdetail (id, order_id, book_id, quantity, price) VALUES
(1, 1, 1, 2, 350.00), -- Order 1: พอใจ x2
(2, 2, 2, 1, 420.00), -- Order 2: จิตวิทยาสายดาร์ก x1
(3, 3, 3, 1, 890.00), -- Order 3: Python Programming x1
(4, 4, 4, 1, 520.00), -- Order 4: ธุรกิจยุคดิจิทัล x1
(5, 5, 5, 1, 380.00); -- Order 5: สุขภาพดีด้วยโยคะ x1

-- Insert Payments
INSERT INTO book_payment (id, order_id, payment_slip, payment_date, method, amount, status, verified_date) VALUES
(1, 1, 'payment/slip_001.jpg', '2025-01-15 10:35:00', 'promptpay', 750.00, 'approved', '2025-01-15 11:00:00'),
(2, 2, 'payment/slip_002.jpg', '2025-01-14 14:25:00', 'bank_transfer', 440.00, 'approved', '2025-01-14 15:00:00'),
(3, 3, 'payment/slip_003.jpg', '2025-01-13 09:20:00', 'promptpay', 940.00, 'approved', '2025-01-13 10:00:00'),
(4, 4, 'payment/slip_004.jpg', '2025-01-12 16:50:00', 'bank_transfer', 550.00, 'pending', NULL),
(5, 5, NULL, '2025-01-11 11:30:00', 'cash_on_delivery', 430.00, 'pending', NULL);

-- Insert Reviews
INSERT INTO book_review (id, user_id, book_id, order_id, rating, comment, created_date, updated_date) VALUES
(1, 2, 1, 1, 4, 'หนังสือดีมาก เนื้อเรื่องน่าติดตาม อ่านแล้วซาบซึ้งใจ', '2025-01-16 08:00:00', '2025-01-16 08:00:00'),
(2, 3, 2, 2, 5, 'เนื้อหาลึกซึ้งมาก ได้ความรู้เยอะ แนะนำให้คนที่สนใจจิตวิทยา', '2025-01-15 18:30:00', '2025-01-15 18:30:00'),
(3, 4, 3, 3, 5, 'Perfect book for Python beginners and advanced users. Very comprehensive!', '2025-01-14 20:15:00', '2025-01-14 20:15:00'),
(4, 2, 2, NULL, 4, 'อ่านเพิ่มเติมนอกเหนือจากที่สั่งซื้อ เนื้อหาดีจริง', '2025-01-10 14:20:00', '2025-01-10 14:20:00');

-- Insert Carts (for active shopping carts)
INSERT INTO book_cart (id, user_id, created_date, updated_date) VALUES
(1, 3, '2025-01-16 10:00:00', '2025-01-16 10:30:00'),
(2, 4, '2025-01-16 12:00:00', '2025-01-16 12:15:00');

-- Insert Cart Details
INSERT INTO book_cartdetail (id, cart_id, book_id, quantity, price) VALUES
(1, 1, 4, 1, 520.00), -- สุดา กำลังเลือกซื้อ ธุรกิจยุคดิจิทัล
(2, 1, 5, 2, 380.00), -- สุดา กำลังเลือกซื้อ สุขภาพดีด้วยโยคะ x2
(3, 2, 6, 1, 450.00); -- นิรันดร์ กำลังเลือกซื้อ การศึกษาในศตวรรษที่ 21

-- Reset sequences (for PostgreSQL)
-- SELECT setval('book_bookcategory_id_seq', (SELECT MAX(id) FROM book_bookcategory));
-- SELECT setval('book_user_id_seq', (SELECT MAX(id) FROM book_user));
-- SELECT setval('book_book_id_seq', (SELECT MAX(id) FROM book_book));
-- SELECT setval('book_order_id_seq', (SELECT MAX(id) FROM book_order));
-- SELECT setval('book_orderdetail_id_seq', (SELECT MAX(id) FROM book_orderdetail));
-- SELECT setval('book_payment_id_seq', (SELECT MAX(id) FROM book_payment));
-- SELECT setval('book_review_id_seq', (SELECT MAX(id) FROM book_review));
-- SELECT setval('book_cart_id_seq', (SELECT MAX(id) FROM book_cart));
-- SELECT setval('book_cartdetail_id_seq', (SELECT MAX(id) FROM book_cartdetail));
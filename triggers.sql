use bookwallah;
-- A trigger that updates the stock count in the bookstore_inventory table after a new order is placed in the order_details table.
delimiter 
CREATE TRIGGER update_stock_after_order
AFTER INSERT ON order_details
FOR EACH ROW
BEGIN
    UPDATE bookstore_inventory
    SET book_count = book_count - 1
    WHERE book_ref_id = NEW.book_ref_id;
END;
delimiter;

-- A trigger that checks the stock count in the bookstore_inventory table before a new order is placed in the order_details table.
delimiter 
CREATE TRIGGER check_stock_before_order
BEFORE INSERT ON order_details
FOR EACH ROW
BEGIN
    DECLARE book_count INT;
    SELECT book_count INTO @book_count FROM bookstore_inventory WHERE book_ref_id = NEW.book_ref_id;
    IF @book_count <= 0 THEN
        SIGNAL SQLSTATE '45000' SET MESSAGE_TEXT = 'This book is out of stock.';
    END IF;
END;
delimiter;

-- A trigger that updates the payment status in the orders table after a payment is made.
delimiter 
CREATE TRIGGER update_payment_status_after_payment
AFTER UPDATE ON orders
FOR EACH ROW
BEGIN
    IF NEW.amount > 0 THEN
        UPDATE orders SET payment_status = 'Paid' WHERE order_id = NEW.order_id;
    END IF;
END;
delimiter;

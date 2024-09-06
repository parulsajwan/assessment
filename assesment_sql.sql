CREATE TABLE Products (
    product_id INT PRIMARY KEY,
    product_name VARCHAR(255) NOT NULL,
    category VARCHAR(255) NOT NULL
);

CREATE TABLE Customers (
    customer_id INT PRIMARY KEY,
    customer_name VARCHAR(255) NOT NULL,
    email VARCHAR(255) NOT NULL,
    signup_date DATE NOT NULL
);

CREATE TABLE Orders (
    order_id INT PRIMARY KEY,
    customer_id INT,
    order_date DATE NOT NULL,
    total_amount DECIMAL(10, 2) NOT NULL,
    FOREIGN KEY (customer_id) REFERENCES Customers(customer_id)
);

CREATE TABLE Order_Items (
    order_item_id INT PRIMARY KEY,
    order_id INT,
    product_id INT,
    quantity INT NOT NULL,
    price_per_unit DECIMAL(10, 2) NOT NULL,
    FOREIGN KEY (order_id) REFERENCES Orders(order_id),
    FOREIGN KEY (product_id) REFERENCES Products(product_id)
);

INSERT INTO
    Customers (customer_id, customer_name, email, signup_date)
VALUES
    (1, 'User1', 'user.1@gmail.com', '2024-01-01'),
    (2, 'User2', 'user.2@gmail.com', '2023-01-02'),
    (3, 'User3', 'user.3@gmail.com', '2024-04-03'),
    (4, 'User4', 'user.4@gmail.com', '2024-06-04'),
    (5, 'User5', 'user.5@gmail.com', '2023-12-05'),
    (6, 'User6', 'user.6@gmail.com', '2024-02-06');

INSERT INTO
    Products (product_id, product_name, category)
VALUES
    (1, 'P1', 'Electronics'),
    (2, 'P2', 'Electronics'),
    (3, 'P3', 'Books'),
    (4, 'P4', 'Books'),
    (5, 'P5', 'Clothes'),
    (6, 'P6', 'Clothes');

INSERT INTO
    Orders (order_id, customer_id, order_date, total_amount)
VALUES
    (1, 1, '2024-01-02', 1543.00),
    (2, 2, '2023-01-03', 500.00),
    (3, 3, '2022-11-04', 210.00),
    (4, 4, '2024-03-05', 320.00),
    (5, 5, '2024-04-06', 1500.00),
    (6, 6, '2024-07-07', 710.00);

INSERT INTO
    Order_Items (
        order_item_id,
        order_id,
        product_id,
        quantity,
        price_per_unit
    )
VALUES
    (1, 1, 1, 1, 1000.00),
    (2, 2, 2, 12, 500.00),
    (3, 3, 3, 6, 100.00),
    (4, 4, 4, 4, 100.00),
    (5, 5, 5, 9, 1500.00),
    (6, 6, 6, 2, 350.00);

SELECT
    c.customer_id,
    c.customer_name,
    c.email,
    SUM(oi.quantity * oi.price_per_unit) AS total_spent,
    (
        SELECT
            p.category
        FROM
            Order_Items oi2
            JOIN Products p ON oi2.product_id = p.product_id
        WHERE
            oi2.order_id IN (
                SELECT
                    o2.order_id
                FROM
                    Orders o2
                WHERE
                    o2.customer_id = c.customer_id
            )
        GROUP BY
            p.category
        ORDER BY
            SUM(oi2.quantity * oi2.price_per_unit) DESC
        FETCH FIRST
            1 ROW ONLY
    ) AS most_purchased_category
FROM
    Orders o
    JOIN Order_Items oi ON o.order_id = oi.order_id
    JOIN Customers c ON o.customer_id = c.customer_id
WHERE
    o.order_date >= CURRENT_DATE - INTERVAL '1 year'
GROUP BY
    c.customer_id,
    c.customer_name,
    c.email
ORDER BY
    total_spent DESC
FETCH FIRST
    5 ROWS ONLY;
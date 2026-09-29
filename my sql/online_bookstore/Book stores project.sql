create database onlinebookstore;
use onlinebookstore;
select * from orders;
select * from customer;


-- 1 Retrieve all books in the "Fiction" genre:
 select * from  book
 where genre ='Fiction';
 
 -- 2 List all customers from the pune:
 select * from customer
 where city ="pune";
 
 -- 3 show orders placed in november 2026
select * from orders
where order_date  between'02-01-2026' and '22-01-2026'; 

-- 3 Retrive the total stock_quantity of books available:
select sum(stock_quantity)  as total_stock_qunatity
From book;

-- 4 find the details of the most expensive book:
select * from book order by price desc limit 1 ;

-- 5 show all the customer who order more then 1 quantity of a book:
select * from orders
where Quantity>1;

-- 6 Retrive all orders where the total amount exceeds size:
select * from orders
where Total_Amount>500;

-- 7 List all genre available in the books table:
select distinct genre from book;

-- 8 find the book the lowest stock:
select * from book order by stock_quantity asc;

-- 9 calculate the total revenue generated from all orders:
select * from orders;
select sum(Total_Amount) as revenue
from orders;

-- 10 Retrive the total number of books sold each genre:
select * from orders;

select b.genre, sum(o.Quantity) as total_book_sold
from orders o 
join book b on o.book_id = b.book_id
group by b.genre;

-- 11 find the average price of books in the  "Fantasy" genre:
select avg(price) as average_price
from book 
where genre = 'Fantasy';

-- 12 list customer who have placed at least 2 orders:
select Customer_ID, count(Order_ID) as order_count
from orders
group by Customer_ID
having count(Order_ID) >= 2;

-- 13 find the most frequantly ordered book:
select Book_ID, count(Order_ID) as order_count
from orders 
group by Book_ID
order  by order_count desc;

-- 14 show the top 3 most expensive books os "Fantasy" genre
select * from book
where genre = 'Fantasy'
order by price desc limit 3;

-- 15 Retrive the total quantity of books sold by each author
select b.author, sum(o.quantity) as Total_book_sold
from orders o
join book b on o.Book_ID=b.Book_ID
group by b.author;

-- 15 list the cities where customer spent over 530 are located:
select distinct c.city,total_amount
from orders o
join customer c on o.Customer_ID=c.Customer_ID
where o.total_amount > 30;

-- 16 find the customer who spent the most on orders:
select c.Customer_ID, c.name,sum(o.Total_amount) as total_spent
from orders o
join customer c on o.Customer_ID=c.Customer_Id
group by c.Customer_ID,c.name
order by total_spent desc; 


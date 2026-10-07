use northwind;
show tables;
select * from customer;
select contactname from customer;
select companyname from customer;
select cantacttitale from customer;
select address from customer;
select city from customer;
select region from customer;
select postalcode from customer;
select country from customer;
select email from customer;
select phone from customer;
select mobile from customer;
select fax from customer;
select distinct city from customer;
select count(distinct city) from customer;
select distinct companyName from customer;
select * from customer where country="Mexico";
select * from customer where contactTitle="Owner";
select * from employee;
select lastname from employee;
select title from employee;
select count(distinct title) from employee;
select distinct city from employee;

select * from customer;
select companyName,city,country from customer;

select * from product;
select productName,unitPrice from product;
select * from employee;
select companyName from customer where country ="Germany";
select companyName from customer where country ="USA";
select companyName from customer where country ="London";
select unitPrice from product where unitPrice>50;
select unitPrice from product where unitprice<20;
select unitPrice from product where unitPrice=18;
select unitPrice from product where unitprice>=30;
select unitPrice from product where unitPrice<=20;
select lastname from employee where city="Seattle";

select * from employee order by city;
select * from employee where country="UK" AND city="London";
select * from employee where title="CEO" AND city="Seattle";
select * from employee where city="Redmond" AND city="Berlin";
select * from employee where city="Redmond" OR city="Berlin";

select * from employee where country="USA" AND(city="Berlin" OR city="Seattle");
select * from employee where NOT country="Germany";
select * from employee where NOT country="USA";

select * from customer where country="Germany" And not country="USA";
select * from employee where firstname NOT like "A%";
select * from employee where employeeId NOT between 1 AND 6;

select * from employee where city not in("London","Seattle");
select * from employee where city not in("London","Paris"); 

select * from employee where Not employeeId>5;
select * from employee where Not employeeId<5;

select * from employee order by hireDate;
select contactTitle,companyName from customer order by companyName desc;

select * from orderdetail;
select * from customer where country="Germany" and postalCode=12209;
select * from product where unitPrice>20 and unitsInStock>50;
select * from customer where contactTitle="Sales Repredentative" and custId>2;
select contactName from customer where city="Berlin" and country="Germany";
select firstName from employee  where hireDate>1993-01-01 and city="London";
select productName from product where categoryId=1 and unitPrice<50;
select * from customer where country="Brazil"and city="Sao Paulo";
show tables;
select * from salesorder;
select * from salesorder where shipCountr="France";

select * from salesorder where freight between 20 and 50 and shipCountry="France";
select * from salesorder where shipCountry ="Japan" and shipPostalCode='1%';
select * from salesorder;
select * from customer where country="Germany" or country="France";

show tables;
select * from supplier;
select * from product;
select companyName from supplier where country="Japan" or country="UK";
select productName from product where categoryId=1 or categoryId=2;
select * from shipper;
select shipName from salesorder where shipCountry="Brazil" or shipCountry="Mexico";
select * from employee;
select firstname from employee where city="London" or city="Seattle";
select productName,unitPrice from product where unitPrice<20 or unitPrice>100;

select *
from customer
where region is NULL;

select min(unitPrice) from product;
select min(unitPrice)as cheaper from product;
select max(unitPrice) from product;
select max(unitPrice) as expensive from product;
select count(*) from product;

select count(productID)
from product;
select count(distinct unitPrice)
from product;

select count(productID)
from product
where unitPrice > 20;

select sum(unitPrice)
from product;

select Avg(unitPrice)
from product;

select Avg(unitPrice)
from product where categoryId=1;

select * from product
where unitPrice >(select avg(unitPrice)from product);

select * from customer
where city like '%B%n';

select * from customer where region is null;
select * from customer where region is not null;
select * from customer where region  is null;
select * from employee;
select * from employee where mgrId is null;
select * from supplier;
select * from supplier where region is null;
select * from supplier where fax is null;

select count(*) from customer;
select count(*) from product;
select count(*)from supplier;
select count(*) from salesorder;
select count(*) from employee;

select sum(unitsInStock) from product;
select sum(freight) from salesorder;
select * from salesorder;

select avg(freight) from salesorder;
select avg(unitPrice) from product;

select max(unitPrice) from product;
select max(freight) from salesorder;
select max(unitsInStock) from product;

select min(unitPrice) from product;
select min(freight) from salesorder;
select min(unitsInStock) from product;

select * from employee where birthDate between '1968-01-09 00:00:00' and '1970-05-29 00:00:00';
select * from salesorder;
select * from salesorder where freight between 50 and 148;
select freight as f from salesorder where freight  between 50 and 148;

select sum(productId),avg(unitPrice) from product;
select sum(unitsInStock),max(unitsInStock),min(unitsInStock) from product;
select * from supplier;
select * from employee;
select sum(unitsInstock),max(unitsInstock),min(unitsInstock) from product;
select * from customer;
select * from supplier;

select count(productId)
from product
where unitPrice > 20;

select avg(unitprice) from product where categoryId=1;
select sum(freight) from salesorder where shipCountry="Germany";

select max(unitPrice) from product where categoryId=2;
 

select  productName from product where categoryId between 1 and 3 and unitPrice between 20 and 50; 
select * from salesorder where shipCountry in ('Germany',' France') and freight between 20 and 100;
select * from customer;
select companyName as c ,country  as coun from customer where country in ("Germany","France","Brazill");

select productName as Item_Name,
unitPrice As price
from product
where unitPrice Between 10 and 40;
select * from employee;
select firstname as s ,lastname as l from employee where hireDate between '2002-05-01 00:00:00' and '2004-11-15 00:00:00';

select * from customer where country in("Germany","France","Brazil");
select * from customer where country in("USA","UK","Japan");
select * from product  where categoryId in(1,2,3);
select * from salesorder where shipCountry in ("Germany","France","Mexico");
select * from employee where city in("London","Seattle");
select * from customer where postalCode in(12209,05023);
select * from supplier where city in("Osaka","Tokyo","London");
select * from product where categoryId in(4,5,6);

select unitPrice from product where unitPrice between 20 and 50;
select unitsInStock from product where unitsInStock between 10 and 50;
select freight from salesorder where freight between 20 and 50;
select * from employee where hireDate between 1992-02-01 and 1994-12-31;
select unitsInstock from product where unitsInStock between 1 and 20;
select * from orderdetail;

select companyName as Company from Customer;
select firstname as Frist_Name from employee;
select productname as Product_Name,unitPrice as Price from product;


-- Database: adventure_works_oltp

---------------------------
--		DML QUERIES 	-- 
---------------------------

-- 1) list of subcategories
select sc.productsubcategoryid, sc.productcategoryid, sc.name
from "production".productsubcategory as sc;

-- 2) list of products
select pr.productid, pr.name, pr.listprice
from "production".product as pr
where pr.listprice > 200
order by pr.listprice asc;

-- 3) list of purchase order heads
select ord.purchaseorderid, ord.vendorid, ord.employeeid, ord.subtotal
from "purchasing".purchaseorderheader ord


-- 4) list of purchase order details
select pod.purchaseorderid, pod.purchaseorderdetailid, pod.productid, pod.orderqty, pod.unitprice 
from "purchasing".purchaseorderdetail as pod;

-- 5) list with join of tables: order details, product and subcategory
select sc.name as subcategory, pr.name as product, pod.orderqty, pod.unitprice
from "purchasing".purchaseorderdetail as pod
inner join "production".product as pr
on pod.productid = pr.productid 
inner join "production".productsubcategory as sc
on pr.productsubcategoryid = sc.productsubcategoryid;

-- 6) group of number of products by subcategory
select sc.name, count(pr.productid)
from "production".productsubcategory as sc
inner join "production".product as pr
on sc.productsubcategoryid = pr.productsubcategoryid
group by sc.name;

-- 7) group of total amount of purchases by product filtering total < 5000
select pr.name, sum(pod.orderqty * pod.unitprice)
from "purchasing".purchaseorderdetail as pod
inner join "production".product as pr
on pod.productid = pr.productid
group by pr.name
having sum(pod.orderqty * pod.unitprice) < 5000;

-- 8) total of products
select count(pr.productid) 
from "production".product as pr;

-- 9) total amount of purchases
select sum(pod.subtotal)
from "purchasing".purchaseorderheader as pod;


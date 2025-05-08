
-- 1st query
select salesorderid, productid, unitprice 
from "sales".salesorderdetail
where orderqty = 5

-- 2nd query

-- query for salesoderdetail
select salesorderid, productid, orderqty, unitprice 
from "sales".salesorderdetail;

-- query for product
select productid, name, safetystocklevel
from "production".product;

-- inner join
select od.salesorderid, pr.name, pr.safetystocklevel, od.orderqty, od.unitprice
from "sales".salesorderdetail as od
inner join "production".product as pr
on od.productid = pr.productid
where od.orderqty > 10










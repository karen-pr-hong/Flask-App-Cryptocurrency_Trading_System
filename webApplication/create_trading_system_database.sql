/*drop database test;*/
create database test;
use test;
show tables;
/*SELECT SYSDATE();*/
/*drop table profit_and_loss;*/
create table profit_and_loss(p_n_l_pk int not null auto_increment primary key,
							 crypto_img varchar(255),
							 crypto_currency_symbol varchar(10),
							 crypto_currency_name varchar(100),
							 ask_price decimal(30,6),
							 bid_price decimal(30,6),
                             total_quantity decimal(30,6),
							 unrealized_pl decimal(30,6),
							 realized_pl decimal(30,6),
                             vwap decimal(30,6)
							);

insert into profit_and_loss(crypto_img,
							crypto_currency_symbol,
							 crypto_currency_name,
							 ask_price,
							 bid_price,
                             total_quantity,
							 unrealized_pl,
							 realized_pl,
                             vwap)
values("bitcoin.png",'BTC-USD','Bitcoin', 100.25,100,0,0,0,0),
	  ("ethereum.png",'ETH-USD','Ethereum', 90.25,90,0,0,0,0),
      ("litecoin.png",'LTC-USD','Litecoin', 70.25,70,0,0,0,0);
      
select * from profit_and_loss;



use test;




/*drop table blotter;*/
create table blotter(trade_pk int not null auto_increment,
					 crypto_currency_fk int,
                     side varchar(10),
                     trade_timestamp timestamp,
                     trade_count int,
                     price decimal(30,6),
                     trade_quantity decimal(30,6),
                     primary key (trade_pk),
                     foreign key (crypto_currency_fk) references profit_and_loss(p_n_l_pk)
                     );

/*insert into blotter(crypto_currency_fk,
	side,
    trade_timestamp,
    trade_count,
    price,
    trade_quantity) 
values(1, 'Buy', sysdate(), 1, 1000.002344, 200);*/					
select * from blotter;
use test;


/*drop table cash*/
create table cash(id int not null auto_increment primary key,
				  cash_amount decimal(30,6));
insert into cash (cash_amount)
values (1000000);

select * from cash;
select cash_amount from cash where id = 1






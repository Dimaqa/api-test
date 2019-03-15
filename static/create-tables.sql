create Table companies(
	id serial primary key,
	name varchar(64) not null unique,
	phone varchar(64)
);
create Table workers(
	id serial primary key,
	name varchar(64) not null unique,
    company varchar(64),
	phone varchar(64),
    foreign key (company) References companies(name)
);
create table products(
	id serial primary key,
	name varchar(64) NOT Null unique
);
create Table connection(
	worker_id serial Not null,
	product_id serial Not null,
	primary key(worker_id, product_id),
	foreign key(worker_id) References workers(id),
	foreign key(product_id) References products(id)
);
insert into wokers(name) values('Oleg');
insert into products(name) values('Sheep');
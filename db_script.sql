CREATE TABLE users(
    id SERIAL PRIMARY KEY not null,
    login varchar(30) not null,
    email varchar(50) unique not null,
    password varchar(20) not null,
    admin_role bool default false
);

CREATE TABLE products(
    id SERIAL PRIMARY KEY not null,
    title text not null,
    annotation text not null,
    tags varchar(20)[],
    banner_link text not null,
    price bigint not null
);

CREATE TABLE carts(
    id SERIAL PRIMARY KEY not null,
    user_id int,
    FOREIGN KEY (user_id)  REFERENCES users(id),
    product_id int,
    FOREIGN KEY (product_id)  REFERENCES products(id)
);

CREATE TABLE favorites(
    id SERIAL PRIMARY KEY not null,
    user_id int,
    FOREIGN KEY (user_id)  REFERENCES users(id),
    product_id int,
    FOREIGN KEY (product_id)  REFERENCES products(id)
);

CREATE TABLE orders(
    id SERIAL PRIMARY KEY not null,
    user_id int,
    FOREIGN KEY (user_id)  REFERENCES users(id)
);

CREATE TABLE orders_products(
    id SERIAL PRIMARY KEY not null,
    order_id int,
    FOREIGN KEY (order_id)  REFERENCES orders(id),
    product_id int,
    FOREIGN KEY (product_id)  REFERENCES products(id)
);
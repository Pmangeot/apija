-- Create the "app_user" table
CREATE TABLE app_user (
    id SERIAL PRIMARY KEY,
    firstname VARCHAR(128) NOT NULL UNIQUE,
    lastname VARCHAR(128) NOT NULL,
    email VARCHAR(128) DEFAULT FALSE,
    password VARCHAR(128) DEFAULT FALSE,
    admin BOOLEAN DEFAULT FALSE
);

-- Create the "type" table
CREATE TABLE type (
    id SERIAL PRIMARY KEY,
    name VARCHAR(128) NOT NULL,
    description TEXT NOT NULL
);

-- Create the "state" table
CREATE TABLE state (
    id SERIAL PRIMARY KEY,
    name VARCHAR(128) NOT NULL
);

-- Create the "season" table
CREATE TABLE season (
    id SERIAL PRIMARY KEY,
    name VARCHAR(128) NOT NULL,
    active BOOLEAN DEFAULT FALSE
);

-- Create the "reservation" table
CREATE TABLE reservation (
    id SERIAL PRIMARY KEY,
    date DATE NOT NULL,
    articles_total INTEGER NOT NULL,
    user_id INTEGER NOT NULL,
    state_id INTEGER NOT NULL,
    season_id INTEGER NOT NULL,
    FOREIGN KEY (user_id) REFERENCES app_user (id),
    FOREIGN KEY (state_id) REFERENCES state (id),
    FOREIGN KEY (season_id) REFERENCES season (id)
);

-- Create the "article" table
CREATE TABLE article (
    id SERIAL PRIMARY KEY,
    name VARCHAR(128) NOT NULL,
    type_id INTEGER,
    description TEXT NOT NULL,
    total_stock INTEGER NOT NULL,
    remaining_quantity INTEGER NOT NULL,
    season_id INTEGER,
    FOREIGN KEY (type_id) REFERENCES type (id),
    FOREIGN KEY (season_id) REFERENCES season (id)
);

-- Create the "reservation_article" table
CREATE TABLE reservation_article (
    id SERIAL PRIMARY KEY,
    reservation_id INTEGER NOT NULL,
    article_id INTEGER NOT NULL,
    quantity INTEGER NOT NULL,
    FOREIGN KEY (reservation_id) REFERENCES reservation (id),
    FOREIGN KEY (article_id) REFERENCES article (id)
);

INSERT INTO type (name, description) VALUES ('Tomates', 'Plants de tomates à planter directement en terre');
INSERT INTO type (name, description) VALUES ('Cucurbitacés', 'Plants de cucurbitacés à planter directement en terre');
INSERT INTO type (name, description) VALUES ('Aromatiques', 'Plantes aromatiques à planter directement en terre');

INSERT INTO state (name) VALUES ('En attente');
INSERT INTO state (name) VALUES ('Validée');

INSERT INTO season (name, active) VALUES ('2023', FALSE);
INSERT INTO season (name, active) VALUES ('2024', TRUE);

INSERT INTO app_user (firstname, lastname, email, password, admin) VALUES ('admin_f_n', 'admin_l_n', 'admin@admin.com', 'admin', TRUE);
INSERT INTO app_user (firstname, lastname, email, password, admin) VALUES ('user_f_n', 'user_l_n', 'user@user.com', 'user', FALSE);
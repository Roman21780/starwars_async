CREATE TABLE characters (
    id SERIAL PRIMARY KEY,
    birth_year VARCHAR(10),
    eye_color VARCHAR(20),
    films TEXT,
    gender VARCHAR(10),
    hair_color VARCHAR(20),
    height VARCHAR(10),
    homeworld VARCHAR(255),
    mass VARCHAR(10),
    name VARCHAR(100),
    skin_color VARCHAR(20),
    species TEXT,
    starships TEXT,
    vehicles TEXT
);
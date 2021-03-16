
CREATE TABLE  client (
   	client_id VARCHAR PRIMARY KEY,
	first_name VARCHAR ( 50 ) UNIQUE NOT NULL,
	last_name VARCHAR ( 50 ) NOT NULL,
	user_type VARCHAR (50) NOT NULL,
	email VARCHAR ( 255 ) UNIQUE NOT NULL,
	user_name VARCHAR ( 50 ) UNIQUE NOT NULL,
	password BYTEA NOT NULL
);


CREATE TABLE  databaseinfo (
   	id serial PRIMARY KEY,
	database_user_name VARCHAR ( 50 ) ,
	database_host VARCHAR(50)   NOT NULL ,
	database_port INTEGER  NOT NULL  ,
	database_password VARCHAR ( 50 ),
	client_id VARCHAR NOT NULL,
	FOREIGN KEY (client_id) REFERENCES client(client_id)  
);
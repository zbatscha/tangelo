DROP TABLE IF EXISTS widgets;

CREATE TABLE widgets (id int, title CHAR, description CHAR);

INSERT INTO widgets (id, title, description)
  VALUES (1,'Clock','Check the time!');
INSERT INTO widgets (id, title, description)
  VALUES (2,'Weather','Check the weather!');
INSERT INTO widgets (id, title, description)
  VALUES (3,'Calendar','Whats happening at Princeton?');

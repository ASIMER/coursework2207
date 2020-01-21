INSERT INTO "user" (login, password, role) VALUES
    ('asimer', 'asimer', 'admin'),
    ('kelioris', 'kelioris', 'user'),
    ('nikita', '123456', 'user');


INSERT INTO site (site_address, login, site_name, create_date) VALUES
	('site1', 'asimer', 'site1', '2018-02-10'),
	('site2', 'asimer', 'site2', '2019-02-10'),
	('site3', 'kelioris', 'site3', '2019-06-10');


INSERT INTO page (site_address, path, title) VALUES
	('site1', 'main', 'main'),
	('site1', 'info', 'info'),
	('site2', 'main', 'main');


INSERT INTO theme (theme_name, theme_popularity, code) VALUES
	('bold', 564, 'bold'),
	('italic', 448, 'italic'),
	('margin', 874, 'margin=1');


INSERT INTO block (site_address, path, "position", theme_name, block_type, content, focus_time) VALUES
    ('site1', 'main', '100:100:100', 'bold', 'div', 'test 1 1 1', '0:0:22.369432'),
    ('site1', 'main', '120:100:100', 'bold', 'div', 'test this kourse woork', '0:0:12.369432'),
    ('site1', 'info', '460:100:100', 'italic', 'div', 'test 1 1 1', '0:0:55.369432'),
    ('site2', 'main', '120:100:100', 'italic', 'div', 'test 213123', '0:0:21.369432'),
    ('site2', 'main', '180:100:100', 'margin', 'div', 'test 512515', '0:0:12.369432'),
    ('site2', 'main', '173:100:100', 'margin', 'div', 'test 222222', '0:0:53.369432');
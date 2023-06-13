import sqlite3

# membuat koneksi ke database
conn = sqlite3.connect('scheduling.db')

# membuat cursor
c = conn.cursor()

# membuat tabel
c.execute(''' CREATE TABLE IF NOT EXISTS tb_guru
    (id INTEGER PRIMARY KEY, nama, mapel)''')

# memasukkan data ke tabel
c.execute("INSERT INTO tb_guru VALUES (1, 'Dra. Toiriyah', 2)")
c.execute("INSERT INTO tb_guru VALUES (2, 'Drs. Kusdaryanto', 15)")
c.execute("INSERT INTO tb_guru VALUES (3, 'Drs. Mursid', 17)")
c.execute("INSERT INTO tb_guru VALUES (4, 'Irma Umi T., S.Pd.', 3)")
c.execute("INSERT INTO tb_guru VALUES (5, 'Anna Dimah, S.Pd.', 3)")
c.execute("INSERT INTO tb_guru VALUES (6, 'R. Umar Fadil, S.Ag.', 1)")
c.execute("INSERT INTO tb_guru VALUES (7, 'Yuni Lestari, S.Pd.', 5)")
c.execute("INSERT INTO tb_guru VALUES (8, 'Tri Karyanto, S.Pd.', 17)")
c.execute("INSERT INTO tb_guru VALUES (9, 'A. Rafik, S.Pd.', 4)")
c.execute("INSERT INTO tb_guru VALUES (10, 'Abd. Manaf Bakri, S.Pd.', 12)")
c.execute("INSERT INTO tb_guru VALUES (11, 'Halimatus Ainis, S.Pd.', 21)")
c.execute("INSERT INTO tb_guru VALUES (12, 'Pinik Retnowati, S.Pd.', 16)")
c.execute("INSERT INTO tb_guru VALUES (13, 'Setiawan, S.Pd.', 8)")
c.execute("INSERT INTO tb_guru VALUES (14, 'M. Tofan Hanib, M.Pd.', 10)")
c.execute("INSERT INTO tb_guru VALUES (15, 'Akh. Taufiq, S.Pd.', 13)")
c.execute("INSERT INTO tb_guru VALUES (16, 'Drs. Syaiful Muluk', 7)")
c.execute("INSERT INTO tb_guru VALUES (17, 'Dra. Sujiati', 16)")
c.execute("INSERT INTO tb_guru VALUES (18, 'Rifatun, S.Pd.', 11)")
c.execute("INSERT INTO tb_guru VALUES (19, 'Jumaidah, S.Pd.', 11)")
c.execute("INSERT INTO tb_guru VALUES (20, 'Widyawati SHF, S.Pd.', 10)")
c.execute("INSERT INTO tb_guru VALUES (21, 'Moh. Kusnarto, S.Pd.', 15)")
c.execute("INSERT INTO tb_guru VALUES (22, 'Marfuatun, S.Pd.', 10)")
c.execute("INSERT INTO tb_guru VALUES (23, 'Abd. Mannan, S.Pd.', 12)")
c.execute("INSERT INTO tb_guru VALUES (24, 'Endang Wasiati N, S.Pd.', 16)")
c.execute("INSERT INTO tb_guru VALUES (25, 'Uswatul Hasanah, S.Pd.', 4)")
c.execute("INSERT INTO tb_guru VALUES (26, 'Nia Hotimah, M.Pd.Si.', 12)")
c.execute("INSERT INTO tb_guru VALUES (27, 'Risnani, S.Pd.', 13)")
c.execute("INSERT INTO tb_guru VALUES (28, 'Ika Pujiyanti, S.Or.', 8)")
c.execute("INSERT INTO tb_guru VALUES (29, 'Deky Andy C., S.Si.', 23)")
c.execute("INSERT INTO tb_guru VALUES (30, 'Fadlun Duifa, S.Pd.', 14)")
c.execute("INSERT INTO tb_guru VALUES (31, 'Syarifah Ulfiati, S.Pd.', 5)")
c.execute("INSERT INTO tb_guru VALUES (32, 'Lailatul Hotilah, S.Pd.', 9)")
c.execute("INSERT INTO tb_guru VALUES (33, 'Nurul Farida, S.Pd.', 3)")
c.execute("INSERT INTO tb_guru VALUES (34, 'Rima Nirmalasari, S.Pd.', 12)")
c.execute("INSERT INTO tb_guru VALUES (35, 'Eka Sulistiawati, S.Pd.', 21)")
c.execute("INSERT INTO tb_guru VALUES (36, 'Sinarsih, S.Pd.', 3)")
c.execute("INSERT INTO tb_guru VALUES (37, 'Pamungkas Detri Nugroho,, S.Pd.', 14)")
c.execute("INSERT INTO tb_guru VALUES (38, 'Agus Mujib, S.Pd.', 14)")
c.execute("INSERT INTO tb_guru VALUES (39, 'Arif setiawan, S.Pd.', 1)")
c.execute("INSERT INTO tb_guru VALUES (40, 'Miswaroh, S.Pd.', 9)")
c.execute("INSERT INTO tb_guru VALUES (41, 'Lailatul Hidayah, S.S.', 9)")
c.execute("INSERT INTO tb_guru VALUES (42, 'Rummah, S.Pd.', 22)")
c.execute("INSERT INTO tb_guru VALUES (43, 'Siti Fatihah, S.Hi.', 22)")
c.execute("INSERT INTO tb_guru VALUES (44, 'Abd. Latif S.MZ, S.Pd.', 22)")
c.execute("INSERT INTO tb_guru VALUES (45, 'Happy Dwi Saktia S, S.Pd.', 8)")
c.execute("INSERT INTO tb_guru VALUES (46, 'Haris Maulidi, S.Pd.', 4)")
c.execute("INSERT INTO tb_guru VALUES (47, 'Dian Nur Faradita, S.Pd.', 7)")
c.execute("INSERT INTO tb_guru VALUES (48, 'Aniessa Yulia Fajrin, S.Pd.', 21)")
c.execute("INSERT INTO tb_guru VALUES (49, 'Ali Fahmi, S.Or.', 8)")
c.execute("INSERT INTO tb_guru VALUES (50, 'Yeshinta Brendha Sugiyanto, S.Pd.', 7)")
c.execute("INSERT INTO tb_guru VALUES (51, 'Islamiyah, S.Pd.', 2)")
c.execute("INSERT INTO tb_guru VALUES (52, 'Atiris Atifah, S.Pd.', 2)")

# menampilkan semua tabel dalam database
c.execute("SELECT name FROM sqlite_master WHERE type='table'")
tables = c.fetchall()

# menampilkan seluruh tabel
for tabel in tables:
    print(tabel[0])

# menyimpan perubahan
conn.commit()

# menutup koneksi
conn.close()

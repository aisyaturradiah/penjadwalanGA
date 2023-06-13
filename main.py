# ---------------------------------------------------------------------------------------------------------------------------------------
# KUMPULAN LIBRARY
# ---------------------------------------------------------------------------------------------------------------------------------------

import sqlite3 # library untuk database
import pandas as pd # library untuk dataframe
import random # untuk generate angka random
import time # untuk mengambil current time

import streamlit as st # untuk front end sistem
from streamlit_option_menu import option_menu

# ---------------------------------------------------------------------------------------------------------------------------------------
# CONFIG DATABASE
# ---------------------------------------------------------------------------------------------------------------------------------------

# membuat koneksi ke database
conn = sqlite3.connect('scheduling.db')

c = conn.cursor() # membuat cursor

def buka_koneksi():
    # membuat koneksi ke database
    conn = sqlite3.connect('scheduling.db')
    # membuat cursor
    c = conn.cursor()
    
    return conn, c

# ---------------------------------------------------------------------------------------------------------------------------------------
# FUNCTION TO GENERATE DATA FROM DATABASE
# ---------------------------------------------------------------------------------------------------------------------------------------

def load_guru(): # get data guru
    conn, c = buka_koneksi()
    c.execute("SELECT nama from tb_guru ORDER BY id")
    rows = c.fetchall()
    conn.close()
    
    return pd.DataFrame(rows, columns=['Nama Guru'])

def load_mapel(): # get data mapel
    conn, c = buka_koneksi()
    c.execute("SELECT nama_mapel from tb_mapel ORDER BY id")
    rows = c.fetchall()
    conn.close()
    
    return pd.DataFrame(rows, columns=['Mata Pelajaran'])

def load_kelas(): # get data kelas
    conn, c = buka_koneksi()
    c.execute("SELECT nama_kelas from tb_kelas ORDER BY id")
    rows = c.fetchall()
    conn.close()
    
    return pd.DataFrame(rows, columns=['Kelas'])

def load_hari(): # get data hari
    conn, c = buka_koneksi()
    c.execute("SELECT hari from tb_hari ORDER BY id")
    rows = c.fetchall()
    conn.close()
    
    return pd.DataFrame(rows, columns=['Hari'])

def load_jam(): # get data jam
    conn, c = buka_koneksi()
    c.execute("SELECT waktu from tb_jam ORDER BY id")
    rows = c.fetchall()
    conn.close()
    
    return pd.DataFrame(rows, columns=['Waktu'])

# ---------------------------------------------------------------------------------------------------------------------------------------
# GET DATA FROM DB / INISIALISASI VARIABEL YANG DIBUTUHKAN
# ---------------------------------------------------------------------------------------------------------------------------------------

data_guru = load_guru()
data_mapel = load_mapel()
data_kelas = load_kelas()
data_hari = load_hari()
data_jam = load_jam()
# load data dari db -> pandas dataframe

# convert df to list
data_guru = data_guru['Nama Guru'].tolist()
data_mapel = data_mapel['Mata Pelajaran'].tolist()
data_kelas = data_kelas['Kelas'].tolist()
data_hari = data_hari['Hari'].tolist()
data_jam = data_jam['Waktu'].tolist()

n_IPA = 14 # jumlah kelas IPA
n_IPS = 10 # jumlah kelas IPS
n_kelas = n_IPA + n_IPS # jumlah kelas
n_sesi = (10*4) + 7 # senin-kamis = 10 sesi dan jumat 7 sesi
hard_bc = 0.0350

# rule mapel

# mapel untuk ipa ips
mapel_ipa = [0,1,2,3,4,6,7,8,9,10,11,13,16,17,18,20,21,22] # kelas ipa
mapel_ips = [0,1,2,4,5,6,7,8,12,13,14,15,16,19,20,21,22,23] # kelas ips

# waktu sesi setiap kelas
waktu_sesi_ipa = [
    [3, 2, 4, 3, 2, 0, 2, 3, 2, 3, 3, 3, 0, 2, 0, 0, 0, 3, 3, 0, 4, 2, 2, 0], # X IPA
    [3, 2, 4, 4, 2, 0, 2, 3, 2, 4, 4, 4, 0, 2, 0, 0, 4, 0, 0, 0, 4, 2, 0, 0], # XI IPA
    [3, 2, 4, 4, 2, 0, 2, 3, 2, 4, 4, 4, 0, 2, 0, 0, 4, 0, 0, 0, 4, 2, 0, 0] # XII IPA
# id 0  1  2  3  4  5  6  7  8  9  10 11 12 13 14 15 16 17 18 19 20 21 22 23
]

waktu_sesi_ips = [
    [3, 2, 4, 0, 2, 3, 2, 3, 2, 0, 0, 0, 3, 2, 3, 3, 0, 0, 0, 3, 4, 2, 2, 3], # X IPS
    [3, 2, 4, 0, 2, 0, 2, 3, 2, 0, 0, 0, 4, 2, 4, 4, 4, 0, 0, 0, 4, 2, 0, 4], # XI IPS
    [3, 2, 4, 0, 2, 0, 2, 3, 2, 0, 0, 0, 4, 2, 4, 4, 4, 0, 0, 0, 4, 2, 0, 4] # XII IPS
# id 0  1  2  3  4  5  6  7  8  9  10 11 12 13 14 15 16 17 18 19 20 21 22 23
]

guru_pengampu = [
    [5, 38], # Pendidikan Agama dan Budi Pekerti (PAI)
    [0, 50, 51], # PPKN
    [3, 4, 32, 35], # Bahasa Indonesia
    [8, 24, 45], # Matematika
    [6, 30], # Bahasa Inggris
    [19], # Biologi Lintas Minat
    [15, 46, 49], # Seni Budaya
    [12, 27, 44, 48, 52], # Penjaskes
    [31, 39, 40], # Prakarya
    [13, 21], # Biologi
    [17, 18], # Kimia
    [9, 25, 33], # Fisika
    [14, 26], # Geografi
    [29, 37], # Sejarah Indonesia
    [1], # Sosiologi
    [11, 23], # Ekonomi
    [2, 7], # Bahasa dan Sastra Inggris
    [16], # Ekonomi Lintas Minat
    [20], # Sosiologi Lintas Minat
    [22], # Fisika Lintas Minat
    [10, 34, 47], # Matematika Umum
    [41, 42, 43], # Bahasa Madura
    [28], # TIK
    [36], # Sejarah Peminatan
]

# ---------------------------------------------------------------------------------------------------------------------------------------
# SETTING UTILITIES
# ---------------------------------------------------------------------------------------------------------------------------------------

# # global set untuk tampilan halaman web
# st.set_page_config(
#     page_title='Tugas Akhir`s',
#     layout='wide',
#     page_icon='random',
# )

# membuka file style.css untuk listing tampilan
with open("style.css") as f:
    st.markdown('<style>{}</style>'.format(f.read()), unsafe_allow_html=True)

# modifikasi utilitas halaman streamlit
# digunakan untuk mematikan menu streamlit dan padding atas halaman
hide_streamlit_style = """
    <style>
        #MainMenu {visibility: hidden; }
        .css-z5fcl4 {padding-top: 1rem;}
    </style>
"""
st.markdown(hide_streamlit_style, unsafe_allow_html=True)

# memanggil file bootstrap untuk css pada navigation
st.markdown('<link rel="stylesheet" href="https://maxcdn.bootstrapcdn.com/bootstrap/4.0.0/css/bootstrap.min.css" integrity="sha384-Gn5384xqQ1aoWXA+058RXPxPg6fy4IWvTNh0E263XmFcJlSAwiGgFAW/dAiS6JXm" crossorigin="anonymous">', unsafe_allow_html=True)

# ---------------------------------------------------------------------------------------------------------------------------------------
# KUMPULAN FUNCTION
# ---------------------------------------------------------------------------------------------------------------------------------------

# fungsi untuk menampilkan teks
def printing_text(teks_1, teks_2):
    col1, col2 = st.columns([1,3])
    with col1:
        st.markdown(teks_1)
    with col2:
        st.markdown(f'`{teks_2}`')

# fungsi untuk menampilkan teks menggunakan streamlit.info
def printing_info(teks_1, teks_2):
    col1, col2, col3 = st.columns([0.5,3,0.5])
    with col1:
        st.markdown(teks_1)
    with col2:
        st.info(teks_2)
    with col3:
        st.markdown(teks_1)

# fungsi untuk memberikan space kosong antar section
def spaces():
    st.markdown('##### spaces')

# function untuk membuat kromosom
def make_kromosom():
    kromosom = list()
    for i in range(n_kelas):
        # identifikasi kelas, x ipa 4, x ips 3, xi ipa 5, xi ips 3, xii ipa 5, xii ips 4
        kelas = 0 if i < 4 else 1 if i < 9 else 2 if i < 14 else 0 if i < 17 else 1 if i < 20 else 2
        gen = [[] for i in range(n_sesi)] # membuat sesi dari list kosong sebanyak panjang sesi (47)
        gen[0] = ['Upacara',''] # untuk mapel pertama selalu upacara

        if i < n_IPA: # untuk ke 14 kelas ipa
            daftar_mapel = mapel_ipa.copy() # membuat tampungan daftar mapel ipa
            random.shuffle(daftar_mapel) # list tampungan yg dibuat di acak agar saat diambil tetap bersifat random
            increment = 1 # untuk cursor pengisian di setiap sesi

            for mapel in daftar_mapel: # list tampungan yg di acak, digunakan sebagai refrensi pengambilan mapel
                if waktu_sesi_ipa[kelas][mapel] > 0: # cek rule sesi dari mapel yg diambil (panjang sesi)
                    id_guru = random.choice(guru_pengampu[mapel]) # untuk mapel yg diambil, ambil guru pengampu secara random
                    # perulangan untuk memasukan mapel ke dalam kromosom / jadwal yg akan dibuat
                    for sesi_mapel in range(waktu_sesi_ipa[kelas][mapel]):
                        
                        # mulai pengisian mapel ke dalam sesi jadwal setiap kelas
                        if increment <= len(gen):
                            if gen[increment] == []:
                                gen[increment] = [data_mapel[mapel], id_guru]
                            else:
                                gen[increment + 1] = [data_mapel[mapel], id_guru]
                        increment += 1 # jangan lupa incrementnya
                        
        else: # disini untuk kelas ips yg jumlah nya 10 kelas kalo ga salah
            daftar_mapel = mapel_ips.copy() # membuat tampungan daftar mapel ips
            random.shuffle(daftar_mapel) # list tampungan yg dibuat di acak agar saat diambil tetap bersifat random
            increment = 1 # untuk cursor pengisian di setiap sesi

            for mapel in daftar_mapel: # list tampungan yg di acak, digunakan sebagai refrensi pengambilan mapel
                if waktu_sesi_ips[kelas][mapel] > 0: # cek rule sesi dari mapel yg diambil (panjang sesi)
                    id_guru = random.choice(guru_pengampu[mapel]) # untuk mapel yg diambil, ambil guru pengampu secara random
                    # perulangan untuk memasukan mapel ke dalam kromosom / jadwal yg akan dibuat
                    for sesi_mapel in range(waktu_sesi_ips[kelas][mapel]):
                        
                        # mulai pengisian mapel ke dalam sesi jadwal setiap kelas
                        if increment <= len(gen):
                            if gen[increment] == []:
                                gen[increment] = [data_mapel[mapel], id_guru]
                            else:
                                gen[increment + 1] = [data_mapel[mapel], id_guru]
                        increment += 1 # jangan lupa incrementnya

        indices_to_move = []
        for i, item in enumerate(gen):
            if item[0] == 'Penjaskes':
                indices_to_move.append(i)

        if indices_to_move[0] == 1 or indices_to_move[0] == 10 or indices_to_move[0] == 20 or indices_to_move[0] == 30 or indices_to_move[0] == 40:
            pass
        else:
            sesi_penjas = [1, 10, 20, 30, 40]
            rand_sesi = random.choice(sesi_penjas)
            # Pindahkan sesi mata pelajaran 'Penjaskes' ke indeks sebelumnya
            gen[indices_to_move[0]], gen[rand_sesi] = gen[rand_sesi], gen[indices_to_move[0]]
            gen[indices_to_move[1]], gen[rand_sesi + 1] = gen[rand_sesi + 1], gen[indices_to_move[1]]
            gen[indices_to_move[2]], gen[rand_sesi + 2] = gen[rand_sesi + 2], gen[indices_to_move[2]]

        # setiap perulangan, baik itu untuk jadwal ipa ataupun ips
        # jangan lupa disimpan kedalam list tampungan yg namanya kromosom
        kromosom.append(gen)
    return kromosom # kalo sudah, di return yaak

# function untuk mutasi
def mutasi(i, mapel_ipa, mapel_ips, waktu_sesi_ipa, waktu_sesi_ips, data_mapel, guru_pengampu):
    # identifikasi kelas, x ipa 4, x ips 3, xi ipa 5, xi ips 3, xii ipa 5, xii ips 4
    kelas = 0 if i < 4 else 1 if i < 9 else 2 if i < 14 else 0 if i < 17 else 1 if i < 20 else 2

    if i < n_IPA: # untuk ke 14 kelas ipa
        gen = [[] for i in range(n_sesi)] # membuat sesi dari list kosong sebanyak panjang sesi (47)
        gen[0] = ['Upacara',''] # untuk mapel pertama selalu upacara
        
        daftar_mapel = mapel_ipa.copy() # membuat tampungan daftar mapel ipa
        random.shuffle(daftar_mapel) # list tampungan yg dibuat di acak agar saat diambil tetap bersifat random
        increment = 1 # untuk cursor pengisian di setiap sesi

        for mapel in daftar_mapel: # list tampungan yg di acak, digunakan sebagai refrensi pengambilan mapel
            if waktu_sesi_ipa[kelas][mapel] > 0: # cek rule sesi dari mapel yg diambil (panjang sesi)
                id_guru = random.choice(guru_pengampu[mapel]) # untuk mapel yg diambil, ambil guru pengampu secara random
                # perulangan untuk memasukan mapel ke dalam kromosom / jadwal yg akan dibuat
                for sesi_mapel in range(waktu_sesi_ipa[kelas][mapel]):
                    
                    # mulai pengisian mapel ke dalam sesi jadwal setiap kelas
                    if increment <= len(gen):
                        if gen[increment] == []:
                            gen[increment] = [data_mapel[mapel], id_guru]
                        else:
                            gen[increment + 1] = [data_mapel[mapel], id_guru]
                    increment += 1 # jangan lupa incrementnya
                                        
    else: # disini untuk kelas ips yg jumlah nya 10 kelas kalo ga salah
        gen = [[] for i in range(n_sesi)] # membuat sesi dari list kosong sebanyak panjang sesi (47)
        gen[0] = ['Upacara',''] # untuk mapel pertama selalu upacara
        
        daftar_mapel = mapel_ips.copy() # membuat tampungan daftar mapel ips
        random.shuffle(daftar_mapel) # list tampungan yg dibuat di acak agar saat diambil tetap bersifat random
        increment = 1 # untuk cursor pengisian di setiap sesi

        for mapel in daftar_mapel: # list tampungan yg di acak, digunakan sebagai refrensi pengambilan mapel
            if waktu_sesi_ips[kelas][mapel] > 0: # cek rule sesi dari mapel yg diambil (panjang sesi)
                id_guru = random.choice(guru_pengampu[mapel]) # untuk mapel yg diambil, ambil guru pengampu secara random
                # perulangan untuk memasukan mapel ke dalam kromosom / jadwal yg akan dibuat
                for sesi_mapel in range(waktu_sesi_ips[kelas][mapel]):
                    
                    # mulai pengisian mapel ke dalam sesi jadwal setiap kelas
                    if increment <= len(gen):
                        if gen[increment] == []:
                            gen[increment] = [data_mapel[mapel], id_guru]
                        else:
                            gen[increment + 1] = [data_mapel[mapel], id_guru]
                    increment += 1 # jangan lupa incrementnya

    indices_to_move = []
    for i, item in enumerate(gen):
        if item[0] == 'Penjaskes':
            indices_to_move.append(i)

    if indices_to_move[0] == 1 or indices_to_move[0] == 10 or indices_to_move[0] == 20 or indices_to_move[0] == 30 or indices_to_move[0] == 40:
        pass
    else:
        sesi_penjas = [1, 10, 20, 30, 40]
        rand_sesi = random.choice(sesi_penjas)
        # Pindahkan sesi mata pelajaran 'Penjaskes' ke indeks sebelumnya
        gen[indices_to_move[0]], gen[rand_sesi] = gen[rand_sesi], gen[indices_to_move[0]]
        gen[indices_to_move[1]], gen[rand_sesi + 1] = gen[rand_sesi + 1], gen[indices_to_move[1]]
        gen[indices_to_move[2]], gen[rand_sesi + 2] = gen[rand_sesi + 2], gen[indices_to_move[2]]

    return gen # kalo sudah, di return yaak

# rule constrain
# dalam 1 waktu yg sama guru tidak boleh mengajar lebih dari 1 sesi mata pelajaran
def rule1(kromosom):
    temp = list() # buat list untuk tampungan
    for i in range(len(kromosom[0])): # terus cek banyak nya kelas
        res = list() # buat list lagi untuk tampungan
        for j in range(len(kromosom)): # perulangan untuk setiap kromosom (sebanyak popsize harusnya bakal ada 10)
            # mengambil anggota terakhir (indeks -1) dari list yang berada pada indeks ke-0
            # gampangannya, disini kita ingin mengambil id si guru
            res.append(kromosom[j][i][-1])
        temp.append(res) # kalo udah dapet tuh list guru-gurunya, masukin deh ke temp
        # kenapa kok dimasukin ke temp? karna gini, kan total ada 24 kelas
        # nah si res hanya menampung total 47 sesi tadi untuk 1 kelas saja
        # karna kita ingin tau keseluruhan guru yg mengajar di 24 kelas tadi
        # maka setiap res akan di tampung dulu di temp, nah skrng isi dari temp adalah id guru sebanyak 47 sesi dalam 24 kelas

    hasil = int() # buat 0 dulu yaa
    for i in range(len(temp)): # cek panjang list temp, harusnya bakal ada 24 (mewakili total kelas kita)
        # disini branching untuk menghindari index ke 0, karna index 0 sudah pasti ga ada gurunya
        # kan ada upacara, jadi tiap senin mereka upacara gitu tuh
        if i != 0:
            id_guru = list() # buat list yaa untuk menampung id setiap guru nantinya
            for ind in temp[i]: # sekarang cek untuk setiap sesi di seluruh kelas
                # nah kalo ga ditemukan id guru dalam list yg udah dibuat tampungan id guru tadi
                if ind not in id_guru:
                    id_guru.append(ind) # masukin tuh id guru nya ke list tampungan tadi
            for j in id_guru: # disini perulangan untuk ngecek id guru yaa
                # terus cek, kalo seumpama dalam satu sesi yg sama (meski beda kelas)
                # kalo id guru itu tadi muncul lebih dari 1, berarti kan maruk tuh gurunya
                if temp[i].count(j) > 1:
                    hasil += hard_bc # nah kalo udah maruk, kasih SP deh, berupa penambahan bobot constrainnya 0.001

    return hasil # jangan lupa di return nilai constrainnya

# rule constrain
# setiap guru mengajar maksimal 36 jam
def rule2(kromosom):
    temp = list() # buat list untuk tampungan
    for i in range(len(kromosom[0])): # terus cek banyak nya kelas
        res = list() # buat list lagi untuk tampungan
        for j in range(len(kromosom)): # perulangan untuk setiap kromosom (sebanyak popsize harusnya bakal ada 10)
            # mengambil anggota terakhir (indeks -1) dari list yang berada pada indeks ke-0
            # gampangannya, disini kita ingin mengambil id si guru
            res.append(kromosom[j][i][-1])
        temp.append(res) # kalo udah dapet tuh list guru-gurunya, masukin deh ke temp
        # kenapa kok dimasukin ke temp? karna gini, kan total ada 24 kelas
        # nah si res hanya menampung total 47 sesi tadi untuk 1 kelas saja
        # karna kita ingin tau keseluruhan guru yg mengajar di 24 kelas tadi
        # maka setiap res akan di tampung dulu di temp, nah skrng isi dari temp adalah id guru sebanyak 47 sesi dalam 24 kelas

    hasil = int() # buat 0 dulu yaa
    for i in range(len(temp)): # cek panjang list temp, harusnya bakal ada 24 (mewakili total kelas kita)
        # disini branching untuk menghindari index ke 0, karna index 0 sudah pasti ga ada gurunya
        # kan ada upacara, jadi tiap senin mereka upacara gitu tuh
        res = int()
        for j in range(len(kromosom)):
            res += (kromosom[j].count(i))
        if res > 36:
            hasil += hard_bc

    return hasil # jangan lupa di return nilai constrainnya

# function untuk menghitung nilai fitness
def func_fitness(populasi):
    fitness = list() # buat list untuk menampung nilai fitness dari semua gen (10 gen sesuai popsize)
    for i in range(len(populasi)): # perulangan untuk setiap gen
        nilai_fitness = 1/(1 + rule1(populasi[i]) + rule2(populasi[i])) # hitung nilai fitness setiap gen pake fungsi rule tadi
        fitness.append(nilai_fitness) # masukin nilai fitness yg udah di hitung ke list tampungan tadi
    return fitness # terus di return lah

# nah di sini main sistem nya
# jadi ku buat func untuk memudahkan proses running program
# juga biar gampang aja ngecek waktu komputasi nya

def penjadwalan(cr, mr, popsize, max_iter):
    populasi_awal = list() # buat list kosong buat nampung populasi awal
    for i in range(popsize): # buat kromosom sebanya gen / nilai popsize
        populasi_awal.append(make_kromosom()) # setiap gen nya masukin ke populasi awal
    populasi = populasi_awal.copy() # terus populasi awal tadi di gandakan dulu ya, nanti soalnya dibutuhkan

    generasi = 1 # disini log generasi biar kita tahu berapa generasi yg udah di buat
    best = int() # terus ini variabel buat ngecek fitness disetiap generasi
    best_fitness = int() # nah ini untuk nyimpen nilai fitness dari generasi terbaik
    total_fitness = 0

    while best != 1 and generasi <= max_iter: # oke skrang jalankan GA sebanyak max_iter yang diinginkan

        temp = func_fitness(populasi) # nah disini kita hitung dulu nilai fitness dari populasi awal tadi
        sorting = temp.copy() # terus di copy dulu
        sorting.sort() # kalo udah urutkan nilai fitness duplikat dari populasi awal tadi

        # di sini kita hitung, kita mau buat anak berapa
        # eh maaf salah, maksutnya kita hitung, berapa banyak ortu yg boleh mantab mantab
        offspringcross = int(popsize * cr) # 4
        cross = list() # buat list kosong dulu yaa

        for i in sorting[offspringcross:]: # terus ambil ortu ortu terpilih tadi
            cross.append(populasi[temp.index(i)].copy()) # nah ortu nya masukin ke list
            # jadi disini kita isolasi mereka biar nyaman pas mantab mantab

        ortu = list() # buat list kosong lagi
        for i in cross:
            res = random.randrange(0, len(populasi_awal[0])) # ambil ortu dari populasi awal secara random
            ortu.append(res) # masukin ke dalam ortu

        anak = list() # sekarng buat list untuk nampung hasil perbuatan si ortu
        for i in range(len(cross)): # perulangan sebanyak ortu terpilih
            cross_ = cross.copy() # di duplikat dulu list yg isinya ortu terpilih
            born = cross_[i].copy() # terus untuk setiap gen dari ortu tampung dalam born

            # di sini kita lakukan proses crossover antar 2 ortu dengan urutan index pertama
            # sampai di crossover kembali ke index pertama
            if i != len(ortu) - 1:
                idx = i + 1
                ortu_ = cross_[i + 1].copy()
            else:
                idx = 0
                ortu_ = cross_[0].copy()
            born_ = ortu_[ortu[i]].copy()
            born[ortu[i]] = born_ # hasil dari proses crossover ini akan menghasilkan anak yg baru lahir
            # kita kasih nama born aja yaa

        # kita lakukan mutasi dengan tujuan untk mengembalikan kerusakan materi gen selama proses crossover tadi
        for i in range(len(born)):
            # disini, peluang untuk mutasi di notasikan dengan angka random dari 0-10 | 9/10 = 0.9 < 0.8
            # angka random tadi harus di bagi 10 dan dibandingkan dengan nilai mr
            # kalo lebih besar mr maka mutasi boleh dilakukan, kalo sebliknya yaa jangan harap mutasi lahh
            if random.randrange(0, 11)/10 < mr: # mr = mutasi rate
                # panggil func mutasi
                born[i] = mutasi(i, mapel_ipa, mapel_ips, waktu_sesi_ipa, waktu_sesi_ips, data_mapel, guru_pengampu).copy()
                break
        anak.append(born) # nah hasil akhir dari crossover dan mutasi, masukin ke list anak
        # karna udah gede dan yaa berhak untuk dianggap sbg suatu individu dalam populasi

        for i in range(len(anak)): # untuk setiap anak
            # cek nilai fitnessnya, apakah lebih besar dari populasi ortnya
            if func_fitness([populasi[sorting.index(sorting[i])]])[0] <= func_fitness([anak[i]])[0]:
                # kalau ternyata lebih bagus si anak
                # berarti ortu ketinggalan zaman dan kita gantikan dengan si anak
                populasi[temp.index(sorting[i])] = anak[i].copy()

        # disini kita ambil nilai fitness nya si anak
        best = func_fitness([populasi[i]])[0]
        print('Generasi %d' % generasi) # print info generasi
        print('Fitness =',best) # print info generasi
        total_fitness += best

        if best_fitness < best: # disini branching buat kita simpen individu terbaik
            best_fitness = best # ambil nilai fitnessnya
            generasi_ke = generasi # cari tahu dia generasi ke berapa
            populasi_final = populasi # trus comot juga individu tadi

        generasi += 1 # increment info generasi
        
    return total_fitness, best_fitness, generasi_ke, populasi_final # return info info tadi

def buat_jadwal(jadwal, kelas):
    jadwal_kelas = []
    for jam in range(len(jadwal[kelas])):
        if jadwal[kelas][jam][1] == '':
            value_sesi = f'{jadwal[kelas][jam][0]}'
        else:
            value_sesi = f'{jadwal[kelas][jam][0]} - {data_guru[jadwal[kelas][jam][1]]}'
        jadwal_kelas.append(value_sesi)
        
    return jadwal_kelas

# ---------------------------------------------------------------------------------------------------------------------------------------
# LOGIKA DAN TAMPILAN SISTEM
# ---------------------------------------------------------------------------------------------------------------------------------------

# NAVIGATION SECTION
# ---------------------------------------------------------------------------------------------------------------------------------------

# st.markdown("""
# <nav class="navbar fixed-top navbar-expand-lg navbar-dark" style="background-color: #392B58;">
#   <button class="navbar-toggler" type="button" data-toggle="collapse" data-target="#navbarNav" aria-controls="navbarNav" aria-expanded="false" aria-label="Toggle navigation">
#     <span class="navbar-toggler-icon"></span>
#   </button>
#   <div class="collapse navbar-collapse" id="navbarNav">
#     <ul class="navbar-nav">
#       <li class="nav-item active">
#         <a class="nav-link disabled" href="#home">Home <span class="sr-only">(current)</span></a>
#       </li>
#       <li class="nav-item">
#         <a class="nav-link" href="#data">Data</a>
#       </li>
#       <li class="nav-item">
#         <a class="nav-link" href="#penjadwalan">Penjadwalan Mata Pelajaran</a>
#       </li>
#     </ul>
#   </div>
# </nav>
# """, unsafe_allow_html=True)
st.set_page_config(
    page_title="Anemia Classification",
    page_icon='blood.png',
    layout='centered',
    initial_sidebar_state="expanded",
    menu_items={
        'Get Help': 'https://www.extremelycoolapp.com/help',
        'Report a bug': "https://www.extremelycoolapp.com/bug",
        'About': "# This is a header. This is an *extremely* cool app!"
    }
)
st.write("""<h1>Aplikasi Klasifikasi Penderita Anemia</h1>""",unsafe_allow_html=True)

# HOME / HEADER SECTION
# ---------------------------------------------------------------------------------------------------------------------------------------

# navigation point untuk home section
st.markdown('''
##### Home
''')

# tampilkan judul sistem
st.write('''
# Optimasi Penjadwalan Mata Pelajaran
### *--*
''')

# inisialisasi informasi penelitian
info = '''
- Penerapan yang dilakukan menggunakan metode **Genetic Algorithm (GA)**
- Penelitian dilakukan dengan studi kasus di **SMA Negeri 1 Torjun, Sampang**
'''

# tampilkan informasi yg dibuat ke dalam sistem
printing_info('',info)

# DATA SECTION
# ---------------------------------------------------------------------------------------------------------------------------------------

st.markdown('''
##### data
''')

# navigation point untuk dataset section
st.markdown('''
## **Data**
''')

try:
    # layouting kolom untuk data section
    col_data = st.columns([0.8,0.1,2])

    with col_data[0]: # layout bagian kiri
        # selecbox untuk memilih data yg ditampilkan
        pilih_data = st.selectbox('Lihat Data', ['Guru', 'Mata Pelajaran', 'Kelas'], index= 0)

    with col_data[2]: # layout bagian kanan
        if pilih_data == 'Guru':
            # membuat daftar mapel yg di ampu oleh setiap guru
            pengampu = ['' for i in range(len(data_guru))]
            for indices, data in enumerate (guru_pengampu):
                for guru in data:
                    pengampu[guru] = data_mapel[indices]

            # membuat dataframe untuk data guru
            df_guru = pd.DataFrame(
                {
                    'Nama Guru' : data_guru,
                    'Bidang Studi' : pengampu
                }
            )
            # tampilkan dataframe
            st.dataframe(
                df_guru,
                use_container_width=True,
                hide_index=True
            )

        elif pilih_data == 'Mata Pelajaran':
            # buat dataframe untuk data mapel
            no_mapel = [i+1 for i in range(len(data_mapel))]
            df_mapel = pd.DataFrame(
                {
                    'No' : no_mapel,
                    'Nama Mata Pelajaran' : data_mapel
                }
            )
            # tampilkan dataframe
            st.dataframe(
                df_mapel,
                use_container_width=True,
                hide_index=True
            )
        elif pilih_data == 'Kelas':
            # buat dataframe untuk data kelas
            no_kelas = [i+1 for i in range(len(data_kelas))]
            df_kelas = pd.DataFrame(
                {
                    'No' : no_kelas,
                    'Kelas' : data_kelas
                }
            )
            # tampilkan dataframe
            st.dataframe(
                df_kelas,
                use_container_width=True,
                hide_index=True
            )
except Exception as e:
    st.error('Terjadi masalah! Data tidak ditemukan')
    #st.exception(e)
spaces() # memberikan space kosong

# Penjadwalan Mata Pelajaran
# ---------------------------------------------------------------------------------------------------------------------------------------

st.markdown('''
##### penjadwalan
''')

# navigation point untuk dataset section
st.markdown('''
## **Penjadwalan Mata Pelajaran**
''')

try:
    # layouting kolom untuk data section
    col_jadwal = st.columns([0.4,0.1,2])

    with col_jadwal[0]: # layout bagian kiri
        # input number widget untuk nilai cr
        value_cr = st.number_input('**cr** value', min_value= 0.1, max_value= 0.9, value= 0.2, step= 0.1, key= 'cr value')

        # input number widget untuk nilai mr
        value_mr = st.number_input('**mr** value', min_value= 0.1, max_value= 0.9, value= 0.8, step= 0.1, key= 'mr value')

        # input number widget untuk nilai popsize
        value_pop = st.number_input('**popsize** value', min_value= 10, max_value= 90, value= 10, step= 10, key= 'pop value')

        # input number widget untuk nilai n_generasi
        value_gen = st.number_input('**jumlah generasi** value', min_value= 1000, max_value= 9000, value= 1000, step= 1000, key= 'generasi value')

        spaces() # memberikan space kosong
        # button train model
        button_apply = st.button('Apply', use_container_width = True)

    with col_jadwal[2]: # layout bagian kanan
        if button_apply:
            # Waktu mulai
            start_time = time.time()

            with st.spinner('Wait for it...'):
                # penjadwalan GA
                total_fitness, best_fitness, generasi_ke, populasi_final = penjadwalan(value_cr, value_mr, value_pop, value_gen)

            # Waktu selesai
            end_time = time.time()

            tr_duration = end_time - start_time
            hours = tr_duration // 3600
            minutes = (tr_duration - (hours * 3600)) // 60
            seconds = tr_duration - ((hours * 3600) + (minutes * 60))


            for i, fitness in enumerate(func_fitness(populasi_final)):
                if best_fitness == fitness:
                    jadwal_GA = populasi_final[i]

            # jadwal
            sesi = [i % 10 + 1 for i in range(n_sesi)]
            sesi[40:] = [i % 7 + 1 for i in range(7)]

            jadwal = jadwal_GA.copy()

            for kelas in range(len(jadwal)):
                if kelas == 0:
                    x_ipa_1 = buat_jadwal(jadwal, kelas)
                elif kelas == 1:
                    x_ipa_2 = buat_jadwal(jadwal, kelas)
                elif kelas == 2:
                    x_ipa_3 = buat_jadwal(jadwal, kelas)
                elif kelas == 3:
                    x_ipa_4 = buat_jadwal(jadwal, kelas)
                elif kelas == 4:
                    xi_ipa_1 = buat_jadwal(jadwal, kelas)
                elif kelas == 5:
                    xi_ipa_2 = buat_jadwal(jadwal, kelas)
                elif kelas == 6:
                    xi_ipa_3 = buat_jadwal(jadwal, kelas)
                elif kelas == 7:
                    xi_ipa_4 = buat_jadwal(jadwal, kelas)
                elif kelas == 8:
                    xi_ipa_5 = buat_jadwal(jadwal, kelas)
                elif kelas == 9:
                    xii_ipa_1 = buat_jadwal(jadwal, kelas)
                elif kelas == 10:
                    xii_ipa_2 = buat_jadwal(jadwal, kelas)
                elif kelas == 11:
                    xii_ipa_3 = buat_jadwal(jadwal, kelas)
                elif kelas == 12:
                    xii_ipa_4 = buat_jadwal(jadwal, kelas)
                elif kelas == 13:
                    xii_ipa_5 = buat_jadwal(jadwal, kelas)
                elif kelas == 14:
                    x_ips_5 = buat_jadwal(jadwal, kelas)
                elif kelas == 15:
                    x_ips_6 = buat_jadwal(jadwal, kelas)
                elif kelas == 16:
                    x_ips_7 = buat_jadwal(jadwal, kelas)
                elif kelas == 17:
                    xi_ips_6 = buat_jadwal(jadwal, kelas)
                elif kelas == 18:
                    xi_ips_7 = buat_jadwal(jadwal, kelas)
                elif kelas == 19:
                    xi_ips_8 = buat_jadwal(jadwal, kelas)
                elif kelas == 20:
                    xii_ips_6 = buat_jadwal(jadwal, kelas)
                elif kelas == 21:
                    xii_ips_7 = buat_jadwal(jadwal, kelas)
                elif kelas == 22:
                    xii_ips_8 = buat_jadwal(jadwal, kelas)
                elif kelas == 23:
                    xii_ips_9 = buat_jadwal(jadwal, kelas)
            
            dict_jadwal = {
                'Hari' : '',
                'Sesi' : sesi,
                'X IPA 1' : x_ipa_1,
                'X IPA 2' : x_ipa_2,
                'X IPA 3' : x_ipa_3,
                'X IPA 4' : x_ipa_4,
                'XI IPA 1' : xi_ipa_1,
                'XI IPA 2' : xi_ipa_2,
                'XI IPA 3' : xi_ipa_3,
                'XI IPA 4' : xi_ipa_4,
                'XI IPA 5' : xi_ipa_5,
                'XII IPA 1' : xii_ipa_1,
                'XII IPA 2' : xii_ipa_2,
                'XII IPA 3' : xii_ipa_3,
                'XII IPA 4' : xii_ipa_4,
                'XII IPA 5' : xii_ipa_5,
                'X IPS 5' : x_ips_5,
                'X IPS 6' : x_ips_6,
                'X IPS 7' : x_ips_7,
                'XI IPS 6' : xi_ips_6,
                'XI IPS 7' : xi_ips_7,
                'XI IPS 8' : xi_ips_8,
                'XII IPS 6' : xii_ips_6,
                'XII IPS 7' : xii_ips_7,
                'XII IPS 8' : xii_ips_8,
                'XII IPS 9' : xii_ips_9,
            }

            df_jadwal = pd.DataFrame(dict_jadwal)
            
            temp = 0
            for indices, jam in enumerate (sesi):
                if jam == 1:
                    df_jadwal['Hari'][indices] = data_hari[temp]
                    temp += 1
                else:
                    df_jadwal['Hari'][indices] = ' '
            st.dataframe(df_jadwal, use_container_width=True, hide_index=True)
            df_jadwal.to_csv('Penjadwalan GA.csv', index=False)

            printing_text('CR', '%.1f' % value_cr)
            printing_text('MR', '%.1f' % value_mr)
            printing_text('Nilai Rata-rata Fitness', '%.3f' % (total_fitness/value_gen))
            printing_text('Nilai Fitness terbaik', '%.3f' % best_fitness)
            printing_text('Generasi terbaik', '%d' % generasi_ke)
            msg = f'{str(hours)} jam, {minutes:4.1f} menit, {seconds:4.2f} detik'
            printing_text('Waktu komputasi', msg)
        if not button_apply:
            try:
                read = pd.read_csv('Penjadwalan GA.csv')
                st.dataframe(read, use_container_width=True, hide_index=True)
            except:
                pass

except Exception as e:
    st.error('Terjadi masalah! Data tidak ditemukan')
    #st.exception(e)
spaces() # memberikan space kosong

# ---------------------------------------------------------------------------------------------------------------------------------------
# FOOTER SECTION
# ---------------------------------------------------------------------------------------------------------------------------------------

# modifikasi bagian footer menggunakan css
footer="""
    <style>
        footer{
            visibility: visible;
        }
        footer:before{
            content: 'Copyright © 2023, Nailatur Rohmah';
            display: block;
        }
        .css-17es36v {
            color: rgba(209, 209, 209, 1);
        }
    </style>
"""
# tampilkan hasil modifikasi pada footer
st.markdown(footer, unsafe_allow_html=True)
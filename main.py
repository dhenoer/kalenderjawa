import datetime as dt
import os, sys

# daftar nama-nama bulan
BULAN = {
        # key: nama bulan, banyaknya hari, makna
        1: ['Sura', 30, 'Rijal'],
        2: ['Sapar', 29, 'Wiwit'],
        3: ['Mulud', 30, 'Kanda'],
        4: ['Bakda Mulud', 29, 'Ambuka'],
        5: ['Jumadil Awal', 30, 'Wiwara'],
        6: ['Jumadil Akhir', 29, 'Rahsa'],
        7: ['Rejeb', 30, 'Purwa'],
        8: ['Ruwah', 29, 'Dumadi'],
        9: ['Puwasa', 30, 'Madya'],
        10: ['Sawal', 29, 'Wujud'],
        11: ['Sela', 30, 'Wusana'],
        12: ['Besar', 29, 'Kosong']} # 29 atau 30 tergantung tahun

'''
bulanAlternatif = {
        1: ['Kasa', (23,6), (2,8)], # 23 Jun - 2 Ags
        2: ['Karo', (3,8), (25,8)], # 3 Ags - 25 Ags
        3: ['Katelu', (26,8), (18,9)], # 26 Ags - 18 Sep
        4: ['Kapat', (19,9), (13,10)], # 19 Sep - 13 Okt
        5: ['Kalima', (14,10), (9,11)], # 14 Okt - 9 Nov
        6: ['Kanem', (10,11), (22,12)], # 10 Nov - 22 Des
        7: ['Kapitu', (23,12), (3,2)], # 23 Des - 3 Feb
        8: ['Kawolu', (4,2), (1,3)], # 4 Feb, 1 Mar
        9: ['Kasanga', (2,3), (23,3)], # 2 Mar - 23 Mar
        10: ['Kadasa', (27,3), (19,4)], # 27 Mar - 19 Apr
        11: ['Dhesta', (20,4), (12,5)], # 20 Apr - 12 Mei
        12: ['Sadha', (13,5), (22,6)], # 13 Mei - 22 Juni
        }
'''

# daftar nama tahun dalam siklus 1 windu
WINDU_TAHUN = {
        # key: nama tahun, hari pasaran, banyaknya hari
        1: ['Alip', ('Selasa','Pon'), 354], 
        2: ['Ehe', ('Sabtu','Pahing'), 355], 
        3: ['Jimawal', ('Kamis','Pahing'), 354], 
        4: ['Je', ('Senin','Legi'), 354], 
        5: ['Dal', ('Jumat','Kliwon'), 355], 
        6: ['Be', ('Rabu','Kliwon'), 354], 
        7: ['Wawu', ('Ahad','Wage'), 354], 
        8: ['Jimakir', ('Kamis','Pon'), 355], 
        }

#1 'Purwana, Alip, artinya ada-ada (mulai berniat)'],
#2 'Karyana, Ehe, artinya tumandang (imelakukan)'],
#3 'Anama, Jemawal, artinya gawe (pekerjaan)'],
#4 'Lalana, Je, artinya lelakon (proses, nasib)'],
#5 'Ngawana, Dal, artinya urip (hidup)'],
#6 'Pawaka, Be, artinya bola-balik (selalu kembali)'],
#7 'Wasana, Wawu, artinya marang (kearah)'],
#8 'Swasana, Jimakir, artinya suwung (kosong)']

# daftar nama hari dan neptu-nya
HARI5  = ['Pon', 'Wage', 'Kliwon', 'Legi', 'Pahing']
NEPTU5 = [7, 4, 8, 5, 9]
HARI7  = ['Senin', 'Selasa', 'Rabu', 'Kamis', 'Jumat', 'Sabtu', 'Minggu']
NEPTU7 = [4, 3, 7, 8, 6, 9, 5]

# Pon = Petak, melambangkan sare (tidur)
# Wage = Cemeng, melambangkan lenggah (duduk)
# Kliwon = Asih, melambangkan jumeneng (berdiri)
# Legi = Manis, melambangkan mungkur (berbalik arah kebelakang)
# Pahing = Pahit, melambangkan madep (menghadap)

# Weton dipakai untuk menghitung jodoh
WETON = {
        1: ['Wasesa segara', 'Sabar, pemaaf, berbudi luhur, berwibawa'],
        2: ['Tunggak semi', 'Memiliki rezeki yang lancar'],
        3: ['Satria wibawa', 'Memperoleh kemuliaan dan keluhuran'],
        4: ['Sumur seneba', 'Banyak yang berguru'],
        5: ['Satria wirang', 'Banyak mengalami duka cita'],
        6: ['Bumi kepethak', 'Tabah, banyak kesedihan, pekerja keras'],
        7: ['Lebu katiyup angin', 'Tidak pernah mencapai cita-cita, mengalami duka nestapa']
        }

# Banyaknya hari dalam 1 kurup dan 1 windu
MASA_WINDU = 2835
MASA_KURUP = MASA_WINDU * 15 - 1

# Patokan awal Kurup 24 Maret 1936 = Selasa Pon Alip 1867  
# cek 10/08/2021 M = 1 Sura 1955 J, Alip Selasa Pon, Awal Windu

ORD_AWAL_KURUP_1867 = dt.date(1936, 3, 24).toordinal()
TAHUN_PATOKAN = 1867

# Debugging
DEBUG = False


def convertMasehi2Jawa(tgl, outputCalendar=True):

    def hitung(ordTanggal, ordPatokan):
        ordHari    = ordTanggal - ordPatokan
        pasaran    = HARI5[abs(ordHari) % 5]
        tglMasehi  = dt.date.fromordinal(ordTanggal)
        hariMasehi = HARI7[tglMasehi.weekday()]

        neptu5 = NEPTU5[abs(ordHari) % 5]
        neptu7 = NEPTU7[tglMasehi.weekday()]
        neptu = neptu5 + neptu7

        return [pasaran, hariMasehi, tglMasehi, neptu]

    # tanggal sekarang!
    ordTanggal = tgl.toordinal()

    # proses mendapatkan awal kurup, awal windu 
    jarakAwalKurup1867 = ordTanggal - ORD_AWAL_KURUP_1867
    jarakAwalKurup  = jarakAwalKurup1867 % MASA_KURUP
    deltaKurup      = jarakAwalKurup1867 // MASA_KURUP
    jarakAwalWindu  = jarakAwalKurup % MASA_WINDU
    deltaWindu      = jarakAwalKurup // MASA_WINDU
    ordAwalWindu    = ordTanggal - jarakAwalWindu

    # proses mendapatkan awal tahun 
    # iterasi tahun
    ordHari = ordAwalWindu
    for k, tahun in WINDU_TAHUN.items():

        # akumulasi hari
        if ordHari + tahun[2] < ordTanggal:
            ordHari += tahun[2]

        # ketemu tahunnya
        else:
            # proses mendapatkan awal bulan
            # iterasi bulan
            for q, bulan in BULAN.items():

                # set banyaknya hari
                # untuk bulan besar (akhir tahun),
                # disesuaikan dg banyaknya hari dlm satu tahun
                nhari = bulan[1]
                if q == 12 and tahun[2] == 355:
                    nhari = 30

                # akumulasi haru
                if ordHari + nhari < ordTanggal:
                    ordHari += bulan[1] 
            
                # ketemu bulannya
                else:

                    # cetak kalendar
                    if outputCalendar:

                        tahunJawa = TAHUN_PATOKAN + \
                            deltaKurup * 120 + \
                            deltaWindu * 8 + k - 1

                        print()
                        print('Kalender Jawa')
                        print('`````````````')
                        print(f'Bulan {q}.{bulan[0]}')
                        print(f'Tahun {tahun[0]} {tahunJawa}')

                        print()
                        print('Tgl Pasaran  Hari/Tgl Masehi   Neptu')
                        print('--- -------- ----------------- -----')

                        for tgl in range(1, nhari+1):

                            if tgl > 1 and (tgl-1) % 10 == 0:
                                pause()
                            ord = ordHari + tgl -1
                            hasil = hitung(ord, ORD_AWAL_KURUP_1867)

                            pasaran    = hasil[0]
                            hariMasehi = hasil[1]
                            tglMasehi  = hasil[2]
                            neptu      = hasil[3]

                            print(f'{tgl:>2d}  ', end='')
                            print(f'{pasaran:8s} ', end='')
                            print(f'{hariMasehi:6s}', tglMasehi.strftime('%d/%m/%Y'), end='')
                            print(f'{neptu:>4d}', end='')

                            #print(ord, ordTanggal, end='')
                            if ord == ordTanggal:
                                print(' <--')
                            else:
                                print()

                    # hanya konversi
                    else:
                        ord   = ordTanggal
                        hasil = hitung(ord, ORD_AWAL_KURUP_1867)
                        return hasil

                    break
            break
    pause()

def pause():
    input('-- Enter untuk lanjut..')

def menuKalenderJawa():
    print('\nMenu Kalender Jawa')
    print('* Masukan tanggal Masehi')
    print('* Input dalam format dd/mm/yyyy')
    print('* Blank untuk input tgl hari ini')
    tglInput = input('> Input tanggal: ')

    if tglInput == '':
        tglSkr = dt.date.today()
        tglIso = tglSkr.isoformat()

    else:
        tsplit = tglInput.split('/')
        try:
            assert len(tsplit) == 3
            tsplit = list(map(int, tsplit))
            tglIso = f'{tsplit[2]:02d}-{tsplit[1]:02d}-{tsplit[0]:02d}'
            dt.date.fromisoformat(tglIso)
        except Exception as e:
            if e: print('--', e)
            print('-- Error format tanggal')
            pause()
            return
    # tglIso ready to convert
    convertMasehi2Jawa(dt.date.fromisoformat(tglIso))


def hitungWetonJodoh(n1, n2):
    weton = (n1 + n2) % 7
    if weton == 0: weton = 7

    print('\nHasil penghitungan Weton pasangan:')
    print(f'{weton} : {WETON[weton][0]}')
    print(f'"{WETON[weton][1]}"')
    pause()

def menuWetonJodoh():
    print('\nMenu Weton Jodoh')
    print('* Neptu dapat dilihat pada kalender')
    print('* Input neptu masing2 pasangan')
    print('* Input dpisah dengan spasi')
    print('* Contoh: 13 9')
    neptuInput = input('> Input pasangan neptu : ')
    pasangan = neptuInput.split()
    try:
        assert len(pasangan) == 2
        n1 = int(pasangan[0])
        n2 = int(pasangan[1])
        assert 7 <= n1 <= 18
        assert 7 <= n2 <= 18
        hitungWetonJodoh(n1, n2)

    except Exception as e:
        if e: print('--', e)
        print('-- Error, format/range neptu tidak valid')
        pause()



# ------------------MAIN PROGRAM ------------------

while True:

    if sys.platform in ['linux', 'darwin']: os.system('clear')
    else: os.system('cls')

    print('KALENDER JAWA DAN WETON JODOH')
    print('`````````````````````````````')
    print('Menu:')
    print('1. Kalender Jawa')
    print('2. Weton Jodoh')
    print('X. Keluar')

    opsi = input('> Pilihan: ')

    if opsi == '1':
        menuKalenderJawa()
    elif opsi == '2':
        menuWetonJodoh()
    elif opsi and opsi in 'xX':
        break
    else:
        print('-- Error tidak ada pilihan')
        pause()

import datetime as dt
import os, sys


BULAN = {
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

WINDU = {
        1: ['Alip', ('Selasa','Pon'), 354], 
            #'Purwana, Alip, artinya ada-ada (mulai berniat)'],
        2: ['Ehe', ('Sabtu','Pahing'), 355], 
            #'Karyana, Ehe, artinya tumandang (imelakukan)'],
        3: ['Jimawal', ('Kamis','Pahing'), 354], 
            #'Anama, Jemawal, artinya gawe (pekerjaan)'],
        4: ['Je', ('Senin','Legi'), 354], 
            #'Lalana, Je, artinya lelakon (proses, nasib)'],
        5: ['Dal', ('Jumat','Kliwon'), 355], 
            #'Ngawana, Dal, artinya urip (hidup)'],
        6: ['Be', ('Rabu','Kliwon'), 354], 
            #'Pawaka, Be, artinya bola-balik (selalu kembali)'],
        7: ['Wawu', ('Ahad','Wage'), 354], 
            #'Wasana, Wawu, artinya marang (kearah)'],
        8: ['Jimakir', ('Kamis','Pon'), 355], 
            #'Swasana, Jimakir, artinya suwung (kosong)']
        }

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
        0: ['Lebu katiyup angin', 'Tidak pernah mencapai cita-cita, mengalami duka nestapa']
        }

# Banyaknya hari dalam 1 windu
WINDUHARI = 2835 

# Patokan tahun jawa dan awal windu 1955
# Patokan konversi : 1 Sura 1955 = 10 Agustus 2021 = Selasa Pon = Alip
TAHUNPATOKAN = 1955
ORDTGLPATOKAN = dt.date(2021, 8, 10).toordinal()

# Debugging
DEBUG = False


def convertMasehi2Jawa(tgl, outputCalendar=True):

    def hitung(ordAwalWindu, hariWindu, hariTahun, tgl):
        ordHari    = ordAwalWindu + hariWindu + hariTahun + tgl - 1
        pasaran    = HARI5[abs(ordHari - ordAwalWindu) % 5]
        tglMasehi  = dt.date.fromordinal(ordHari)
        hariMasehi = HARI7[tglMasehi.weekday()]

        neptu5 = NEPTU5[abs(ordHari - ordAwalWindu) % 5]
        neptu7 = NEPTU7[tglMasehi.weekday()]
        neptu = neptu5 + neptu7

        return [ordHari, pasaran, hariMasehi, tglMasehi, neptu]


    ordTanggal = tgl.toordinal()
    ordPatokan = ORDTGLPATOKAN

    jarakHari      = ordTanggal - ordPatokan
    jarakWindu     = jarakHari // WINDUHARI
    jarakHariWindu = jarakHari % WINDUHARI
    ordAwalWindu   = ordPatokan + jarakWindu * WINDUHARI

    if DEBUG:
        print('ordTanggal', ordTanggal)
        print('ordPtokan', ordPatokan)
        print('jarakHari', jarakHari)
        print('jarakWindu', jarakWindu)
        print('jarakHariWindu', jarakHariWindu)
        print('ordAwalWindu', ordAwalWindu)

    hariWindu = 0
    for k,w in WINDU.items():

        if hariWindu + w[2] > jarakHariWindu:

            tahunWindu = k
            hariTahun  = 0

            for q,b in BULAN.items():

                maxHariBulan = (w[2] - hariTahun) if q==12 else b[1]
                
                if hariWindu + hariTahun + maxHariBulan >= jarakHariWindu:

                    bulanTahun = q
                    tahunJawa = TAHUNPATOKAN + jarakWindu*8 + tahunWindu - 1 

                    if outputCalendar:

                        print()
                        print('Kalender Jawa')
                        print('`````````````')
                        print('Bulan {}.{} (Tahun {} {})'.format(q, 
                            b[0], w[0], tahunJawa))

                        if DEBUG:
                            print('hariWindu', hariWindu)
                            print('hariTahun', hariTahun)
                            print('maxHariBulan', maxHariBulan)

                        print()
                        print('Tanggal Pasaran  Hari/Tanggal Masehi Neptu')
                        print('------- -------- ------------------- -----')

                        for tgl in range(1, maxHariBulan+1):

                            if tgl == 16:
                                input('> Enter untuk lanjut..')

                            hasil = hitung(ordAwalWindu, hariWindu, hariTahun, tgl)

                            ordHari    = hasil[0]
                            pasaran    = hasil[1]
                            hariMasehi = hasil[2]
                            tglMasehi  = hasil[3]
                            neptu      = hasil[4]

                            print(f'{tgl:>5d}   ', end='')
                            print(f'{pasaran:8s} ', end='')
                            print(f'{hariMasehi:6s}', tglMasehi.strftime('%d/%m/%Y'), end='')
                            print(f'{neptu:>6d}', end='')

                            if ordHari == ordTanggal:
                                print(' <---')
                            else:
                                print()


                    else:

                        hasil = hitung(ordAwalWindu, hariWindu, hariTahun, 1)
                        ordHasil = hasil[0]
                        deltaHari = ordTanggal - ordHasil +1
                        hasil = hitung(ordAwalWindu, hariWindu, hariTahun, deltaHari)
                        return hasil

                    break
                else:
                    hariTahun += b[1]
            break

        else:
            hariWindu += w[2]

    input('> Enter untuk lanjut..')


def menuKalenderJawa():
    print('\nMenu Kalender Jawa')
    tglInput = input('> Input tanggal dalam format dd/mm/yyyy: ')
    tsplit = tglInput.split('/')
    try:
        assert len(tsplit) == 3
        newtgl = f'{tsplit[2]}-{tsplit[1]}-{tsplit[0]}'
        dt.date.fromisoformat(newtgl)
        if newtgl:
            convertMasehi2Jawa(dt.date.fromisoformat(newtgl))
    except Exception as e:
        print('--', e)
        input('-- Error format tanggal, Enter untuk lanjut..')


def hitungWetonJodoh(n1, n2):
    weton = (n1 + n2) % 7
    print('\nHasil penghitungan Weton pasangan:')
    print(f'"{WETON[weton][0]}"')
    print(WETON[weton][1])

    input('\n> Enter untuk lanjut..')


def menuWetonJodoh():
    print('\nMenu Weton Jodoh')
    print('Neptu dapat dilihat pada kalender')
    print('Masukan pasangan masing-masing Neptu dipisah spasi')
    neptuInput = input('> Input pasangan Neptu (misal 14 8): ')
    pasangan = neptuInput.split()
    try:
        assert len(pasangan) == 2
        n1 = int(pasangan[0])
        n2 = int(pasangan[1])
        assert 7 <= n1 <= 18
        assert 7 <= n2 <= 18
        hitungWetonJodoh(n1, n2)

    except Exception as e:
        print('--', e)
        input('-- Error, format/range neptu tidak valid. Enter untuk lanjut..')



# ------------------MAIN PROGRAM ------------------

while True:

    if sys.platform in ['linux', 'darwin']: os.system('clear')
    else: os.system('cls')

    print('KALENDER JAWA DAN WETON JODOH')
    print('`````````````````````````````')
    print('Menu:')
    print('1. Kalender Jawa')
    print('2. Weton Jodoh')
    print('x. Keluar')

    opsi = input('> Pilihan: ')

    if opsi == '1':
        menuKalenderJawa()
    elif opsi == '2':
        menuWetonJodoh()
    elif opsi and opsi in 'xX':
        break
    else:
        input('-- Error tidak ada pilihan. Enter untuk lanjut..')



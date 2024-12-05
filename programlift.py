# Simulasi Sistem Lift
# Program ini mensimulasikan operasi beberapa lift di sebuah gedung.
# Pengguna memberikan input untuk jumlah lift, jumlah lantai,
# dan kapasitas muatan tiap lift, dan sistem mensimulasikan bagaimana lift
# bergerak berdasarkan permintaan penumpang.

# Kamus:
#   - Titlecard (str): Judul besar program
#   - lifts (list): Daftar yang berisi objek lift. Setiap objek lift berisi:
#       - floor (int): Posisi lantai lift saat ini.
#       - load (int): Jumlah orang yang ada di dalam lift saat ini.
#       - target (int): Lantai target yang ingin dituju lift.
#       - is_used (bool): Flag yang menandakan apakah lift sedang digunakan.
#       - queue (list): Daftar lantai yang harus dikunjungi lift untuk perjalanan tambahan.
#   - lift_amount (int): Jumlah lift yang ada di gedung.
#   - lift_loadlimit (int): Batas maksimum muatan (jumlah orang) yang bisa ditampung oleh lift.
#   - floor_amount (int): Jumlah lantai yang ada di gedung./
#   - time_spent (list): Daftar yang berisi perhitungan waktu untuk setiap lift, dengan:
#       - time_spent[x][0] (int): Waktu yang dibutuhkan lift untuk memenuhi permintaan.
#       - time_spent[x][1] (int): Jenis pergerakan (0: arah yang sama, 1: arah yang sama dalam jarak tertentu, 2: arah berbeda).
#   - temp_floor (int): Variabel sementara untuk menyimpan lantai lift saat inisialisasi.
#   - temp_load (int): Variabel sementara untuk menyimpan jumlah muatan lift saat inisialisasi.
#   - temp_target (int): Variabel sementara untuk menyimpan lantai target lift saat inisialisasi.
#   - cur_floor (int): Lantai saat ini dari pengguna yang meminta lift.
#   - cur_people (int): Jumlah orang yang terdeteksi oleh sistem di lantai saat ini.
#   - cur_target (int): Lantai target dari pengguna yang meminta lift.
#   - available (bool): Flag yang menandakan apakah ada lift yang tersedia.
#   - fastest (int): Indeks lift tercepat yang akan memenuhi permintaan saat ini.

# Fungsi:
#   - lift.returnmove(): Menentukan pergerakan lift: diam (s), naik (u), atau turun (d).
#   - lift.move(): Memindahkan lift menuju lantai target.
#   - visualize_lifts(lifts, floor_amount): Memvisualisasikan posisi dan status setiap lift.
#   - main loop: Menangani input pengguna dan mengendalikan permintaan serta pergerakan lift.

titlecard = """
=============================================================================
     .-') _    ('-.             .-. .-')             _ (`-. .-. .-')
    ( OO ) )  ( OO ).-.         \  ( OO )           ( (OO  )\  ( OO )
,--./ ,--,'   / . --. /  ,-.-') ,--. ,--.  ,-.-')  _.`     \,--. ,--.
|   \ |  |\   | \-.  \   |  |OO)|  .'   /  |  |OO)(__...--''|  .'   /
|    \|  | ).-'-'  |  |  |  |  \|      /,  |  |  \ |  /  | ||      /,
|  .     |/  \| |_.'  |  |  |(_/|     ' _) |  |(_/ |  |_.' ||     ' _)
|  |\    |    |  .-.  | ,|  |_.'|  .   \  ,|  |_.' |  .___.'|  .   \\
|  | \   |    |  | |  |(_|  |   |  |\   \(_|  |    |  |     |  |\   \\
`--'  `--'    `--' `--'  `--'   `--' '--'  `--'    `--'     `--' '--'

                    v 1.4
                    Jangan liftnya doang yang naik bre...
=============================================================================
"""
print(titlecard)

class lift:
    def __init__(self, floor, load, target):
        # Inisialisasi objek lift
        self.floor = floor  # Lokasi lift sekarang
        self.load = load  # Beban di lift sekarang
        self.target = target  # Tujuan lift sekarang
        self.is_used = False  # Indikator apakah lift sedang digunakan untuk beberapa trip
        self.queue = []  # Barisan beberapa trip lift

    def returnmove(self):
        # Menentukan pergerakan lift, s = stationary, u = up, d = down
        if self.target == self.floor:
            self.load = 0
            return 's'
        return 'd' if self.target - self.floor < 0 else 'u'

    def move(self):
        # Mengerakkan lift menuju targetnya
        if self.returnmove() == 'd':
            self.floor -= 1  # Ke atas
        elif self.returnmove() == 'u':
            self.floor += 1  # Ke bawah
        else:
            # Ketika berhenti, mengecek jika misalkan ada target lainnya di barisan queue
            if self.is_used:
                if not self.queue:  # Kalau kosong, bearti lift sudah siap digunakan untuk beberapa trip
                    self.is_used = False
                else:
                    # Mengubah target berdasarkan queue
                    self.target = self.queue.pop(0)
                    # Mulai menggerakkan lift kembali
                    if self.returnmove() == 'd':
                        self.floor -= 1
                    elif self.returnmove() == 'u':
                        self.floor += 1

def visualize_lifts(lifts, floor_amount):
    # Visualisasi posisi lift di setiap lantai
    lift_positions = [[" " for _ in range(len(lifts))] for _ in range(floor_amount)]
    for i, lift in enumerate(lifts):
        lift_positions[floor_amount - lift.floor][i] = "L"  # Penandaan posisi lift
    print("\nLift Visualization:")
    for i in range(floor_amount):
        # Penampilan lantai
        floor_number = f"Floor {floor_amount - i}".ljust(8)
        floor_representation = "|" + "|".join(lift_positions[i]) + "|"
        print(f"{floor_number} {floor_representation}")
    # Penampilan status setiap lift
    print(" " * 8 + " " + "   ".join([f"Lift-{i + 1}" for i in range(len(lifts))]))
    for i in range(lift_amount):
        status = "(NOT AVAILABLE)" if lifts[i].is_used else "AVAILABLE"
        print(f"Lift-{i + 1}. Floor: {lifts[i].floor} | Target: {lifts[i].target} | Load: {lifts[i].load} | Status: {status}")

# Variabel input pengguna terkait kondisi awal
temp_floor = 0
temp_load = 0
temp_target = 0
cur_floor = 0
cur_people = 0
cur_target = 0
lifts = []
lift_amount = int(input("How many lifts are there? "))  # Jumlah lift
lift_loadlimit = int(input("How many people can one lift hold? "))  # Batasan spesifikasi lift
floor_amount = int(input("How many floors are there? "))  # Jumlah lantai
time_spent = [[0, 0] for i in range(lift_amount)]  # Pengecek waktu yang dibutuhkan setiap lift

#time_spent[[x,y]], x menandakan waktu yang dibutuhkan untuk memenuhi permintaan, sementara y menandakan jenis gerak yang dilalui (lebih rinci dibawah)

# Inisialisasi objek lift
for i in range(lift_amount):
    print(f"For lift {i + 1}:")
    temp_floor = int(input("Floor: "))
    temp_target = int(input("Heading to floor: "))
    temp_load = int(input("Load: "))
    lifts.append(lift(temp_floor, temp_load, temp_target))

# Main loop
while True:
    visualize_lifts(lifts, floor_amount)
    print("-- Insert Data --")
    cur_floor = input("(input xxx to stop |Enter to continue) Current floor: ")
    if cur_floor == 'xxx':  # kondisi terminasi
        break
    elif cur_floor == '':
        # Menggerakkan semua lift (ibarat 1 satuan waktu berlewat dan tidak ada yang memencet)
        for i in range(lift_amount):
            lifts[i].move()
    else:
        # Menerima input
        cur_floor = int(cur_floor)
        cur_people = int(input("Amount of people detected: "))
        cur_direction = input("Up or Down? (u/d) ")
        cur_target = int(input("Heading to floor: "))
        for i in range(lift_amount):
            # Kalkulasi waktu yang dibutuhkan setiap lift untuk memenuhi request
            if cur_direction == lifts[i].returnmove():
                # Ketika lift bergerak searah
                if (lifts[i].returnmove() == 'u' and cur_floor < lifts[i].floor) or (lifts[i].returnmove() == 'd' and cur_floor > lifts[i].floor):
                    # Ketika penumpang berada di luar jangkauan gerak lift (Jarak lift ke penumpang)
                    time_spent[i][0] = abs(lifts[i].target - lifts[i].floor) + abs(lifts[i].target - cur_floor)
                    time_spent[i][1] = 0
                else:
                    # Ketika penumpang berada di dalam jangkauan gerak lift (Jarak lift ke penumpang)
                    time_spent[i][0] = abs(cur_floor - lifts[i].floor)
                    time_spent[i][1] = 1
            else:
                # Ketika lift bergerak beda arah (Lift ke target dulu, baru dari target ke penumpang)
                time_spent[i][0] = abs(lifts[i].target - lifts[i].floor) + abs(lifts[i].target - cur_floor)
                time_spent[i][1] = 2
            # time_spent[x][1] menandakan jenis gerak, 0 = searah, di luar jangkauan, 1 = searah, di dalam jangkauan, 2 = berbeda arah

            # Mengecek kondisi overload
            if lifts[i].load + cur_people > lift_loadlimit:
                # Menambah waktu sesuai dengan berapa trip yang dibutuhkan
                time_spent[i][0] += ((lifts[i].load + cur_people) // lift_loadlimit) * 2 * max(abs(cur_floor - cur_target), abs(cur_floor - lifts[i].target))
        print(time_spent)
        available = True
        # Mengecek ketersediaan lift
        for i in range(len(time_spent)):
            if not lifts[i].is_used:
                fastest = i
                break
            if i == len(time_spent) - 1:
                print("NO LIFTS ARE AVAILABLE AT THE MOMENT, PLEASE WAIT")
                available = False
        # Menentukan lift yang tercepat
        if available:
            for i in range(len(time_spent)):
                if time_spent[i][0] < time_spent[fastest][0] and not lifts[i].is_used:
                    fastest = i

            # Mengubah target sesuai dengan jenis gerak
            if time_spent[fastest][1] == 0:
                lifts[fastest].queue.append(cur_floor)
                lifts[fastest].queue.append(cur_target)
                lifts.is_used = True
            elif time_spent[fastest][1] == 1:
                if abs(lifts[fastest].target-cur_floor) < abs(cur_target-cur_floor):
                    lifts[fastest].target = cur_target
            elif time_spent[fastest][1] == 2:
                lifts[fastest].queue.append(cur_floor)
                lifts[fastest].queue.append(cur_target)
                lifts[fastest].is_used = True
            # Menambahkan ke queue untuk kasus overload
            if lifts[fastest].load + cur_people > lift_loadlimit:
                trips = (lifts[fastest].load + cur_people) // lift_loadlimit
                for i in range(trips):
                    lifts[fastest].queue.append(cur_floor)
                    lifts[fastest].queue.append(lifts[fastest].target)
                    lifts[fastest].is_used=True
            lifts[fastest].load = min(20, lifts[fastest].load + cur_people)

        # Menggerakkan semua lift
        for i in range(lift_amount):
            lifts[i].move()
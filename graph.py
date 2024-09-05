import pandas as pd
import matplotlib.pyplot as plt
from matplotlib.widgets import Slider
import os

# CSV verilerini pandas DataFrame'e yükle
def load_sensor_data(file_path):
    data = pd.read_csv(file_path)
    return data

# Bireysel grafikleri ayrı pencerelerde çizme fonksiyonu
def plot_individual_graph(times, y_data, title, ylabel, window_size):
    total_points = len(times)

    # Her grafik için ayrı bir figür oluştur
    fig, ax = plt.subplots(figsize=(10, 6))  # Grafik için yeni bir figür oluştur
    fig.canvas.manager.window.showMaximized()  # Tam ekran görünüm için pencereyi maksimize et

    ax.set_title(title)
    ax.set_xlabel("Zaman (saniye)")
    ax.set_ylabel(ylabel)
    ax.set_xlim(times[0], times[window_size - 1])  # Başlangıçta x ekseni sınırları
    ax.set_ylim(min(y_data) * 10, max(y_data) * 10)  # 10x y sınırları

    # İlk verilerle çizgiyi başlat
    line, = ax.plot(times[:window_size], y_data[:window_size], 'r-')

    # Kaydırıcı hareket ettirildikçe grafiği güncelleyen fonksiyon
    def update(val):
        idx = int(val)  # Kaydırıcı değerini tam sayı olarak al
        start = idx
        end = idx + window_size

        # Tüm eksenler için x ekseni sınırlarını güncelle
        ax.set_xlim(times[start], times[end - 1])

        # Tüm çizgiler için y verilerini güncelle
        line.set_data(times[start:end], y_data[start:end])

        fig.canvas.draw_idle()  # Kanvasa yeniden çizim yaptır

    # Grafiğin altına bir kaydırıcı ekle
    ax_slider = plt.axes([0.2, 0.05, 0.65, 0.03], facecolor='lightgoldenrodyellow')
    slider = Slider(ax_slider, 'Kaydır', 0, total_points - window_size, valinit=0, valstep=1)

    # Kaydırıcı değiştirildiğinde update fonksiyonunu çağır
    slider.on_changed(update)

    # Grafiği ayrı bir pencerede göster
    plt.show()

# Tüm grafikleri içeren 7. grafiği çizme fonksiyonu
def plot_combined_graph(times, data_map, titles, window_size):
    total_points = len(times)

    # 7. grafik için figür ve eksen oluştur
    fig, ax = plt.subplots(figsize=(10, 6))  # Yeni figür oluştur
    fig.canvas.manager.window.showMaximized()  # Pencereyi tam ekran yap

    ax.set_title("Tüm Grafikler")
    ax.set_xlabel("Zaman (saniye)")
    ax.set_ylabel("Değer")
    ax.set_xlim(times[0], times[window_size - 1])  # Başlangıç x ekseni sınırları

    # Tüm veriler için çizgiler oluştur
    lines = []
    colors = ['r-', 'g-', 'b-', 'c-', 'm-', 'y-']  # Her grafik için renkler
    for i in range(6):
        line, = ax.plot(times[:window_size], data_map[i][:window_size], colors[i], label=titles[i])
        lines.append(line)

    ax.legend()  # Efsane ekle

    # Kaydırıcı hareket ettikçe tüm çizgileri güncelleyen fonksiyon
    def update(val):
        idx = int(val)  # Kaydırıcı değerini tam sayı olarak al
        start = idx
        end = idx + window_size

        # X ekseni sınırlarını güncelle
        ax.set_xlim(times[start], times[end - 1])

        # Her çizgi için y verilerini güncelle
        for i, line in enumerate(lines):
            line.set_data(times[start:end], data_map[i][start:end])

        fig.canvas.draw_idle()  # Kanvasa yeniden çizim yaptır

    # Kaydırıcı ekle
    ax_slider = plt.axes([0.2, 0.05, 0.65, 0.03], facecolor='lightgoldenrodyellow')
    slider = Slider(ax_slider, 'Kaydır', 0, total_points - window_size, valinit=0, valstep=1)

    # Kaydırıcı değiştirildiğinde update fonksiyonunu çağır
    slider.on_changed(update)

    # Grafiği göster
    plt.show()

# Ana fonksiyon
def plot_scrollable_graph(file_path):
    # CSV verilerini yükle
    data = load_sensor_data(file_path)

    # Veri sütunlarını çıkar
    times = data["Zaman"]
    accel_x = data["İvme X"]
    accel_y = data["İvme Y"]
    accel_z = data["İvme Z"]
    gyro_x = data["Jiroskop X"]
    gyro_y = data["Jiroskop Y"]
    gyro_z = data["Jiroskop Z"]

    # Pencere boyutu
    window_size = 250  # Aynı anda gösterilecek nokta sayısı (ayarlanabilir)

    # Her grafik için başlıklar ve etiketler
    titles = ["İvmeölçer X", "İvmeölçer Y", "İvmeölçer Z",
              "Jiroskop X", "Jiroskop Y", "Jiroskop Z"]
    ylabels = ["İvme (g)", "İvme (g)", "İvme (g)",
               "Dönme Hızı (deg/s)", "Dönme Hızı (deg/s)", "Dönme Hızı (deg/s)"]

    # Verileri her grafikle eşleştir
    data_map = [accel_x, accel_y, accel_z, gyro_x, gyro_y, gyro_z]

    # Her grafiği ayrı bir pencerede çiz
    for i in range(6):
        plot_individual_graph(times, data_map[i], titles[i], ylabels[i], window_size)

    # 7. grafiği çiz (tüm grafikleri içeren)
    plot_combined_graph(times, data_map, titles, window_size)

# Dosya kimliğini (son 4 basamak) sor
file_id = input("Veri dosyasının son 4 basamağını girin: ")
file_path = f'sensor_data_{file_id}.csv'

# Dosyanın var olup olmadığını kontrol et
if os.path.exists(file_path):
    plot_scrollable_graph(file_path)
else:
    print(f"'sensor_data_{file_id}.csv' dosyası bulunamadı.")

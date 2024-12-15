import cv2
import numpy as np
import time

# Kamera bağlantısını başlatıyoruz
camera = cv2.VideoCapture(0)

if not camera.isOpened():
    print("Kamera açılmadı.")
    exit()

# Kamera ayarlarını yapalım
camera.set(3, 640)  # Genişlik
camera.set(4, 480)  # Yükseklik

# Engel ve yol tespiti için fonksiyon
def detect_obstacles(frame):
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    blurred = cv2.GaussianBlur(gray, (5, 5), 0)
    edges = cv2.Canny(blurred, 50, 150)
    return edges

def detect_lanes(frame):
    # Yol çizgilerini tespit etme
    hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)
    
    # Mavi zemini tespit etme (yolun altı)
    lower_blue = np.array([100, 50, 50])
    upper_blue = np.array([140, 255, 255])
    
    # Siyah yolu tespit etme
    lower_black = np.array([0, 0, 0])
    upper_black = np.array([180, 255, 50])
    
    # Beyaz çizgileri tespit etme (yolun kenarları)
    lower_white = np.array([0, 0, 200])
    upper_white = np.array([180, 30, 255])
    
    # Turuncu çizgileri tespit etme (yol çizgileri)
    lower_orange = np.array([5, 150, 150])
    upper_orange = np.array([15, 255, 255])
    
    # Beyaz başlangıç çizgisi
    lower_white_start = np.array([0, 0, 255])
    upper_white_start = np.array([180, 30, 255])

    # Mavi zemini maskeleyelim
    mask_blue = cv2.inRange(hsv, lower_blue, upper_blue)
    
    # Siyah yolu maskeleyelim
    mask_black = cv2.inRange(hsv, lower_black, upper_black)
    
    # Beyaz çizgileri maskeleyelim
    mask_white = cv2.inRange(hsv, lower_white, upper_white)
    
    # Turuncu çizgileri maskeleyelim
    mask_orange = cv2.inRange(hsv, lower_orange, upper_orange)
    
    # Beyaz başlangıç çizgisi maskelemesi
    mask_white_start = cv2.inRange(hsv, lower_white_start, upper_white_start)
    
    # Maskeleri birleştiriyoruz
    mask = cv2.bitwise_or(mask_blue, mask_black)
    mask = cv2.bitwise_or(mask, mask_white)
    mask = cv2.bitwise_or(mask, mask_orange)
    mask = cv2.bitwise_or(mask, mask_white_start)
    
    # Maskeyi uygulayıp çizgileri tespit edelim
    masked_frame = cv2.bitwise_and(frame, frame, mask=mask)
    
    return masked_frame

# Ana döngü
while True:
    # Kamera görüntüsünü al
    ret, frame = camera.read()

    if not ret:
        print("Kamera görüntüsü alınamadı.")
        break

    # Engel tespiti
    edges = detect_obstacles(frame)
    
    # Yol çizgilerini tespit etme
    lane_frame = detect_lanes(frame)
    
    # Engelleri tespit edilen siyah beyaz görüntü
    edges_colored = cv2.cvtColor(edges, cv2.COLOR_GRAY2BGR)  # Siyah beyazı renkliye çevir
    
    # Yol tespiti üzerine çizgileri ekleyelim
    result = cv2.addWeighted(frame, 0.8, lane_frame, 1.0, 0)  # Yol çizgileriyle harmanla
    
    # Engelleri de gösterelim
    final_result = cv2.addWeighted(result, 1.0, edges_colored, 0.5, 0)  # Engellerle harmanla
    
    # Sonuçları gösterelim
    cv2.imshow('Combined View', final_result)

    # Klavye girişlerini bekle
    key = cv2.waitKey(1) & 0xFF

    # 'q' tuşuna basılırsa çıkış yap
    if key == ord('q'):
        print("Çıkılıyor...")
        break

    # 'c' tuşuna basılırsa fotoğraf çek ve kaydet
    if key == ord('c'):
        timestamp = time.strftime("%Y%m%d-%H%M%S")
        cv2.imwrite(f"photo_{timestamp}.jpg", frame)
        print(f"Fotoğraf kaydedildi: photo_{timestamp}.jpg")
        time.sleep(1)  # Fotoğraf çekildikten sonra 1 saniye bekle

# Kamera ve pencereleri serbest bırak
camera.release()
cv2.destroyAllWindows()

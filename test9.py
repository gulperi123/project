import Jetson.GPIO as GPIO
import time
import keyboard

# GPIO Pinlerinin tanımlanması
servo_pin = 33
dc_motor_pwm_pin = 32
dc_motor_dir_pin1 = 29  # Motor yönü için 1. pin (ön motor)
dc_motor_dir_pin2 = 31  # Motor yönü için 2. pin (ön motor)

# GPIO modunu ayarlayın
GPIO.setmode(GPIO.BOARD)  # GPIO.BOARD veya GPIO.BCM kullanabilirsiniz

# Pinleri çıkış olarak ayarlayın
GPIO.setup(servo_pin, GPIO.OUT)
GPIO.setup(dc_motor_pwm_pin, GPIO.OUT)
GPIO.setup(dc_motor_dir_pin1, GPIO.OUT)
GPIO.setup(dc_motor_dir_pin2, GPIO.OUT)

# PWM nesneleri oluşturuluyor
servo = GPIO.PWM(servo_pin, 50)  # Servo için 50 Hz
dc_motor_pwm = GPIO.PWM(dc_motor_pwm_pin, 1000)  # DC motor için 1000 Hz

# PWM başlatılıyor
servo.start(0)  # Servo başlat (başlangıçta 0 derece)
dc_motor_pwm.start(0)  # DC motor başlat (başlangıçta duruyor)

# Servo motorunun açısını ayarlayan fonksiyon
def set_servo_angle(angle):
    duty_cycle = 2 + (angle / 18)  # Servo için duty cycle hesaplama
    servo.ChangeDutyCycle(duty_cycle)
    time.sleep(0.1)
    servo.ChangeDutyCycle(0)

# DC motorunun yönünü ve hızını ayarlayan fonksiyon
def set_dc_motor(speed, direction):
    # Motor yönünü ayarlama
    if direction == "forward":
        GPIO.output(dc_motor_dir_pin1, GPIO.HIGH)
        GPIO.output(dc_motor_dir_pin2, GPIO.LOW)
    elif direction == "backward":
        GPIO.output(dc_motor_dir_pin1, GPIO.LOW)
        GPIO.output(dc_motor_dir_pin2, GPIO.HIGH)
    
    # DC motor hızını ayarlama
    dc_motor_pwm.ChangeDutyCycle(speed)

# Ana program döngüsü
try:
    current_servo_angle = 90  # Servo başlangıç açısı
    print("W: DC Motor Forward, S: DC Motor Backward, A: Servo Left, D: Servo Right, Q: Quit")

    while True:
        # 'W' tuşu ile DC motoru ileri hareket ettir
        if keyboard.is_pressed('w'):
            print("W tuşuna basıldı: DC Motor İleri")
            set_dc_motor(75, "forward")  # DC motoru %75 hızında ileri hareket ettir
        
        # 'S' tuşu ile DC motoru geri hareket ettir
        elif keyboard.is_pressed('s'):
            print("S tuşuna basıldı: DC Motor Geri")
            set_dc_motor(75, "backward")  # DC motoru %75 hızında geri hareket ettir
        
        # 'A' tuşu ile servo motorunu sola hareket ettir
        elif keyboard.is_pressed('a'):
            print("A tuşuna basıldı: Servo Sol")
            current_servo_angle = max(0, current_servo_angle - 10)
            set_servo_angle(current_servo_angle)
        
        # 'D' tuşu ile servo motorunu sağa hareket ettir
        elif keyboard.is_pressed('d'):
            print("D tuşuna basıldı: Servo Sağ")
            current_servo_angle = min(180, current_servo_angle + 10)
            set_servo_angle(current_servo_angle)
        
        # 'Q' tuşuna basıldığında çıkış yap
        elif keyboard.is_pressed('q'):
            print("Çıkılıyor...")
            break
        
        else:
            set_dc_motor(0, "forward")  # Eğer başka bir tuşa basılmamışsa motoru durdur

        time.sleep(0.1)  # Küçük bir bekleme süresi

finally:
    # Program sonlandığında PWM'leri durdurun ve GPIO'yu temizleyin
    servo.stop()
    dc_motor_pwm.stop()
    GPIO.cleanup()
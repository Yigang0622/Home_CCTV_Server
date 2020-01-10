import RPi.GPIO as GPIO
import time

# PWM 
# 2.5 -> 0 degree
# 7.5 -> 90
# 12.5 -> 180

GPIO.setwarnings(False)

class MyServo(object):
	"""docstring for MyServo"""
	def __init__(self, pin, default_postion=0):

		self.b = 2.5
		self.a = 10

		self.pin = pin
		self.frequency  = 50
		self.default_postion = default_postion

		GPIO.setmode(GPIO.BCM)
		GPIO.setup(pin, GPIO.OUT)
		self.pwm = GPIO.PWM(pin, self.frequency)

		self.pwm.start(2.5)
		print("伺服电机PIN", self.pin, '初始化')
		print("PWM频率", self.frequency)
		self.reset()



	def reposition(self,angle):
		if angle < 0 or angle > 180:
			print("Invalid position angle,", angle)
			return
		duty_cycle = self.b + self.a*(angle/180)
		self.pwm.ChangeDutyCycle(duty_cycle)

	def reset(self):
		print("电机PIN",self.pin,"复位")
		self.reposition(self.default_postion)

	def release(self):
		print("伺服电机",self.pin,"释放")
		self.pwm.stop()




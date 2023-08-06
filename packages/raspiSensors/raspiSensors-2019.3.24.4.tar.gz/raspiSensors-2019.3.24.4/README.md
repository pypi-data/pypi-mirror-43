# Raspberry Pi Sensors

This is a Python 3 package that enables Raspberry Pi to read various sensors .It has been tested on Python 3.5/Raspbian (stretch).
Supported devices include:

* HCSR04 ultrasonic sensor
* PCA9685 Adafruit 16-channel 12 Bit PWM Driver
* BMP280 Barometer
* Triple Axis Magnetometer QMC5883L 


### REQUIREMENTS


1. adafruit-circuitpython-servokit

### Installation

1. From source  (incl. examples, fritzing and ebooks)
   
 ```sh

       git clone https://github.com/hanshof/rpiSensors.git
       cd rpiSensors
       python install setup.py
 ```
       
2. PIP

 ```sh

     pip install raspiSensors
     
 ```






### HCSR04 ultrasonic sensor



> This is the HC-SR04 ultrasonic distance sensor. 
> This economical sensor provides 2cm to 400cm 
> of non-contact measurement functionality with a ranging accuracy 
> that can reach up to 3mm. 
> Each HC-SR04 module includes an ultrasonic transmitter
>, a receiver and a control circuit.

> There are only four pins that you need to worry about on the HC-SR04: 
> VCC (Power), Trig (Trigger), Echo (Receive), and GND (Ground). 
> You will find this sensor very easy to set up and use for your next range-finding project!

Example:

  ```python

    from raspiSensors import hcsr04 as HCSR04
    ultrasonic = HCSR04(trigger_pin = 21, echo_pin = 20)
    print(ultrasonic.distance())

    returns distance in cm
    
  ```
    
### PCA9685 Adafruit 16-channel 12 Bit PWM Driver


> Using only two pins, control 16 free-running PWM outputs! 
> You can even chain up 62 breakouts to control up to 992 PWM outputs (which we would really like to see since it would be glorious)
> It's an i2c-controlled PWM driver with a built in clock. That means that, unlike the TLC5940 family, you do not need to continuously send it signal tying up your microcontroller, its completely free running!
> It is 5V compliant, which means you can control it from a 3.3V microcontroller and still safely drive up to 6V outputs (this is good for when you want to control white or blue LEDs with 3.4+ forward voltages)
> 6 address select pins so you can wire up to 62 of these on a single i2c bus, a total of 992 outputs - that's a lot of servos or LEDs
> Adjustable frequency PWM up to about 1.6 KHz
> 12-bit resolution for each output - for servos, that means about 4us resolution at 60Hz update rate
> Configurable push-pull or open-drain output
> Output enable pin to quickly disable all the outputs

Example:

  ```python
  
      from raspiSensors import pca9685 as PCA9685
      servos = PCA9685(channels=16)
      
      servos.kit.servo[0].angle = 90
  ```
      
      
      
### BMP280 Barometer

  
> This is a Barometer Pressure Sensor module
> It could measure the pressure and temperature.
> This program depend on BMP280.py writted by Adafruit. 

   ```python
    
    from raspiSensors import bmp280 as BMP280
    sensor = BMP280.BMP280()
    elev = 240 # altitude of your location in meters
    print('Temp = {0:0.1f} *C'.format(sensor.read_temperature()))
    print('Pressure = {0:0.1f} hPa'.format(sensor.read_pressure()/10**2))
    print('Sealevel Pressure = {0:0.1f} hPa'.format(sensor.read_sealevel_pressure(elev)/10**2)) # altitude of your location in meters
   ```


### Triple Axis Magnetometer QMC5883L 


> Magnetometer QMC5883L is used for measuring the direction and magnitude of the Earth’s magnetic field. It is used for low cost compassing and magnetometry.
> It measures the Earth’s magnetic field value along the X, Y and Z axes from milli-gauss to 8 gauss.
> It can be used to find the direction of heading of the device.
> It uses I2C protocol for communication with microcontroller.

  ```python

      from raspiSensors import qmc5883l as QMC5883L
      from time import sleep

      sensor = QMC5883L()
      sensor.set_declination(8.0)

      while True:

         # Read Accelerometer raw value

         m = sensor.get_magnet()
         heading = sensor.get_bearing()

         print("Heading Angle = %d°" % heading)
         print("Magnet = {}".format(sensor.get_magnet()))

         sleep(1)
  ```

    

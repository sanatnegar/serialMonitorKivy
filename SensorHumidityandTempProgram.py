
import kivy
from kivy.app import App
from kivy.uix.relativelayout import RelativeLayout
from kivy.uix.floatlayout import FloatLayout
from kivy.graphics import *
from kivy.core.window import Window #setting the window size in kivy 
from kivy.uix.label import Label
from kivy.uix.button import Button
from kivy.uix.textinput import TextInput
import serial 
import schedule
import time 
from datetime import datetime


class HumidityandTempSerial(RelativeLayout):
    def __init__(self,**kwargs):#creating the constructor 
        super(HumidityandTempSerial, self).__init__(**kwargs)
        layoutHome = FloatLayout()
        Window.clearcolor=(0.157,0.157,0.157,1)
        
        lblInstructions = Label(text="Press Button To Start Recording Temperature and Humidity Data",size_hint=(0.3,0.1), pos_hint={'x':0.362, 'y':0.88},color=(.9,.9,.9,1))
        layoutHome.add_widget(lblInstructions)
        
        def recording(self):
            print("RECORDING DATA")
            #Main Code
            rawValues = [] #creating values in a list format 
            floatValues = []
            now = datetime.now() #variable to hold the current date and time 
            dateTimeString = now.strftime("%m/%d/%Y %H:%M:%S") #converting the date and time to a string 
                
            arduino = serial.Serial('com3', 9600) #specify serial port and baud rate 
            print("Serial communication Established")
            arduinoData = arduino.readline() #gets the serial data 
                
            serialToString = str(arduinoData[0:len(arduinoData)].decode("utf-8")) #decodes serial data into a string 
            rawValues = serialToString.split('x') #Splits the readings 
                
            for item in rawValues: #changes data into a floating point number 
                floatValues.append(float(item))
                    
            print(f'Collected readings from Arduino: {floatValues}') #prints the temp and humidity reading 
            print(f'Humidity: {floatValues[0]}',"%") #prints the first item in the list
            print(f'Temperature(F): {floatValues[1]}') #prints the second item in the list 
                
            #writing the data to a txt file 
            sensorRecording = open("sensorData.txt", "a")#opening with a instead of w writes to the next empty line 
            sensorRecording.writelines(f'{dateTimeString}\n')
            sensorRecording.writelines(f'Humidity: {floatValues[0]}  ')
            sensorRecording.writelines(f'Temperature(F):  {floatValues[1]}\n')
            sensorRecording.writelines("--------------------------------------\n")
            sensorRecording.close() #closing the file 
            
            entrData.text = f'{dateTimeString}\n Humidity: {floatValues[0]} Temperature(F):  {floatValues[1]}\n --------------------------------------\n'
            #entrData.text = sensorRecording    
            #clearing the variables 
            arduinoData = 0 
            floatValues.clear()
            rawValues.clear()
            arduino.close()
            print("-----CONNTECTION CLOSED-------")

                
        def stopRecording(self):
            print("STOPPED RECORDING DATA")
            recording(self).exit() 
        
        btnStartRecording = Button(text="Record Data", size_hint=(0.3,0.1), pos_hint={'x':0.390, 'y':0.80}, on_press = recording)
        layoutHome.add_widget(btnStartRecording)
        
        entrData = TextInput(size_hint=(0.7,0.258), pos_hint={'x':0.18, 'y':0.53}, multiline=True)
        layoutHome.add_widget(entrData)
        
        lblTextfile = Label(text="*All recording are saved in sensorData.txt file", size_hint=(0.3,0.1), pos_hint={'x':0.22,'y':0.45})
        layoutHome.add_widget(lblTextfile)

        
        self.add_widget(layoutHome)#adding the innerlayout to the root

class sensorProgram(App):
    def build(self):
        return HumidityandTempSerial()  
     
if __name__ == "__main__":
    sensorProgram().run()

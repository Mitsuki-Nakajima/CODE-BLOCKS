"""
IMPORT/SETUP BLOCK
Essential imports and module variale setups are made here.
"""
    
if __name__ == "__main__":
    from RPLCD.i2c import CharLCD
    lcd = CharLCD(i2c_expander = 'PCF8574',address = 0x27,port = 1,cols=16,rows=2,dotsize=8)
    lcd.clear()
    lcd.write_string("Initializing...")
    import csv
    from cv2 import imread, imshow, cvtColor, COLOR_BGR2RGB, rotate, ROTATE_180, ROTATE_90_CLOCKWISE, ROTATE_90_COUNTERCLOCKWISE
    import numpy as np
    from qreader import QReader
    from picamera2 import Picamera2, Preview
    import RPi.GPIO as GPIO
    
    from time import sleep
    
    import os
    import gspread

# Initializes modules that need initializing
    
    '''
    picam = Picamera2()
   
    camera_config = picam.create_still_configuration(main={"size": (4608,2592)})
    mode=picam.sensor_modes[1]
    config = picam.create_still_configuration(sensor={'output_size': mode['size'], 'bit_depth':mode['bit_depth']})
    picam.configure("still")
    print(picam.camera_config)
    '''
    qreader = QReader()
    goober = open("programtobeexecuted","r+",encoding="utf-8")

"""
FUNCTION BLOCK
This section holds the functions
necessary for the program to run.
"""

# Converts the inputs in the QR list to an actual list
def list_converter(dictionary,list):
    ret_list = []
    end_counter = 0
    for item in list:
        try:
            ret_list.append(dictionary[item])
        except KeyError:
            ret_list.append(item)

    # This is used to end an indent
    end_counter += ret_list.count("$$$ENDENDENDENDEND$$$")

    while "$$$ENDENDENDENDEND$$$" in ret_list:
        ret_list.remove("$$$ENDENDENDENDEND$$$")
    return ret_list, end_counter

# Assembles a loop line
def linemaker_loop(list):
    assembly = f"{list[0]} {' '.join(list[1:])}:"
    return assembly

# Assembles a default line with no spaces between characters
def linemaker_default(list):
    assembly = f"{list[0]}{''.join(list[1:])}"
    return assembly

# Assembles a function line
def linemaker_function(list):
    assembly = f"{list[0]}({','.join(list[1:])})"
    return assembly

# Assembles a special line, which is a default line but with spaces between the characters
def linemaker_special(list):
    assembly = f"{list[0]} {' '.join(list[1:])}"
    return assembly

# Arranges the QR Codes into ordered rows
def image_arranger(decoded_text):

    processed_2d = [(decoded_text[0][index],decoded_text[1][index]['cxcyn']) for index in range(0,len(decoded_text[0]))]
    points = [x[1][1] for x in processed_2d]

    # Stolen from StackOverflow (https://stackoverflow.com/questions/11513484/1d-number-array-clustering)
    clusters = []
    final = []
    points_sorted = sorted(points)
    differences = [points_sorted[index]-points_sorted[index-1] for index in range(1,len(points_sorted))]
    eps = sum(differences) / (len(differences)) if len(differences) else 0.005
    eps = 0.01 if eps < 0.01 else eps
    curr_point = points_sorted[0]
    curr_cluster = [curr_point]

    for point in points_sorted[1:]:
        if point <= curr_point + eps:
            curr_cluster.append(point)
        else:
            clusters.append(curr_cluster)
            curr_cluster = [point]
        curr_point = point
    clusters.append(curr_cluster)

    for item in points:
        for x in clusters:
            if item in x:
                final.append(clusters.index(x))
    
    grouped_up_codes = [[] for x in range(0,max(final)+1)]

    for index in range(0,len(final)):
        grouped_up_codes[final[index]].append(processed_2d[index])

    #Stolen again from StackOverflow https://stackoverflow.com/questions/60246800/how-to-sort-a-python-list-of-lists-by-both-the-values-of-a-nested-list-and-with
    for list in grouped_up_codes:
        list.sort(key = lambda nested : nested[1][0])
        grouped_up_codes[grouped_up_codes.index(list)] = [x[0] for x in list]

    print(grouped_up_codes)
    return grouped_up_codes
'''
#set up a picamera once 
def camera_setup(picam):
    #Set up camera
    config = picam.create_preview_configuration()
    picam.preview_configuration.main.size = (2000, 2000)
    picam.preview_configuration.main.format = "RGB888"
    picam.configure(config)
    picam.start()
'''
#set up a push button
def gpio_setup():
    #ignore warning
    GPIO.setwarnings(False)
    #use physical pin numbering
    GPIO.setmode(GPIO.BOARD)
    #set pin 10 to be an input pin and set initial value to be pulled low
    GPIO.setup(19, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)
    
#return true when the button was pushed
#this function must be runing all the time
def button_pushed():
    if GPIO.input(19) == GPIO.HIGH:
        return True
    elif GPIO.input(19) == GPIO.LOW:
        return False

"""
MAIN BLOCK
Executes the needed commands.
"""

if __name__ == "__main__":
    
    # Initializes required sets/dictionaries
    reference = {"END":"$$$ENDENDENDENDEND$$$","CLOSE":"$$$CLOSECLOSECLOSECLOSECLOSE$$$"}
    colon_commands = {"for","while","try","except","if","elif","else","lambda","def","class"}
    function_commands = set(dir(__builtins__)[dir(__builtins__).index("__spec__")+1:])
    method_commands = {".count",".index",".append",".pop",".remove"}
    stopper_commands = {"pass","break","continue","return"}
    special_commands = set()
    #try:
    if True:
        credentials = { #private_id / private_key goes here}

        gc = gspread.service_account_from_dict(credentials)
        sh = gc.open("CodeBlocksData")
        
        compendium = sh.sheet1.get_all_values()
        compendium = compendium[1:]
        
        custom_function_sheet = sh.worksheet("History")
        custom_functions = custom_function_sheet.get_all_values()
        
        for row in custom_functions:
            reference[row[2]] = row[0]
            match row[3]:
                case "function":
                    function_commands.add(row[0])
                case 'colon':
                    colon_commands.add(row[0])
                case 'stopper':
                    stopper_commands.add(row[0])
                case 'special':
                    special_commands.add(row[0])
        function_counter = int(custom_function_sheet.acell("E1").value) + 1
    #except:
    if False:
        print("GSheets Integration Failed")
        compendium = csv.reader(open("Code Blocks Commands.csv"), delimiter=",", quotechar='"')
        function_counter = 1
    


    # Arranges the data file from the spreadsheet
    
    for row in compendium:
        reference[row[2]] = row[0]
        match row[3]:
            case "function":
                function_commands.add(row[0])
            case 'colon':
                colon_commands.add(row[0])
            case 'stopper':
                stopper_commands.add(row[0])
            case 'special':
                special_commands.add(row[0])

    # Opens the text file
    text_file = open('programtobeexecuted','r+',encoding='utf-8')

    gpio_setup()
    lcd.clear()
    lcd.write_string("BDM Code Blocks")
    while True:
        
        if button_pushed():
            os.system("libcamera-still -o test.jpg")
        #if input("Go? (Y/N) ") == "Y":
            # Takes an image, reads it, then arranges it
            #captured_image = cvtColor(imread(input("Name of file? ")), COLOR_BGR2RGB)
            captured_image = cvtColor(imread("test.jpg"), COLOR_BGR2RGB)
            #captured_image = cvtColor(image(picam), COLOR_BGR2RGB)
            try:
                decoded_text = qreader.detect_and_decode(image=captured_image,return_detections = True)
                qr_list = image_arranger(decoded_text)
            except:
                lcd.clear()
                lcd.write_string("Read Error")
                sleep(3)
            
            # Keeps track of the indentation in and contents of the text
            indent = 0
            exec_string = ""

            try:
                for sublist in qr_list:

                    processed_line = list_converter(reference,sublist)
                    processed_commands = processed_line[0]
                    exec_string += "    " * indent
                    # To be implemented at a later date
                    function_stoppers = []
                    '''
                    # Makes methods possible. Does it work? I don't fucking know
                    while set(processed_commands) and method_commands:
                        nearest_function = next(elem for elem in processed_commands if elem in method_commands)
                        near_index = processed_commands.index(nearest_function)
                        temporary_function = linemaker_function((processed_commands[(function_stoppers[-1]-1 if function_stoppers else 0):near_index + 1])[::-1])
                        processed_commands = processed_commands[:(function_stoppers[-1] if function_stoppers else 0)] + ''.join((near_index+1,temporary_function)) + processed_commands[near_index+2:]
                    '''
                    # Makes nested functions possible
                    while set(processed_commands) & function_commands:
                        nearest_function = next(elem for elem in processed_commands if elem in function_commands)
                        near_index = processed_commands.index(nearest_function)
                        temporary_function = linemaker_function((processed_commands[(function_stoppers[-1]-1 if function_stoppers else 0):near_index + 1])[::-1])
                        processed_commands = processed_commands[:(function_stoppers[-1] if function_stoppers else 0)] + [temporary_function] + processed_commands[near_index+1:]
                        print(temporary_function)
                    
                    processed_commands = processed_commands[::-1]

                    match processed_commands[0]:
                        
                        case _ as placeholder if placeholder in colon_commands:
                            exec_string += linemaker_loop(processed_commands)
                            indent += 1

                        case _ as placeholder if placeholder in stopper_commands:
                            exec_string += linemaker_special(processed_commands)
                            indent -= 1
                            
                        case default:
                            exec_string += linemaker_default(processed_commands)

                    indent -= processed_line[1]
                    exec_string += "\n"

                goober.write(exec_string)
                lcd.clear()
                exec(exec_string)
                try:
                    custom_function_sheet.update([[exec_string,f"Custom Function {function_counter - 1}",f"cfun{function_counter - 1}","special"]],f'A{function_counter}:D{function_counter}')
                except:
                    pass
                sleep(3)
            except:
                lcd.clear()
                lcd.write_string("ARRANGE ERROR")
                sleep(3)

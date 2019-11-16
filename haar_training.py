import numpy as np
import cv2
from playsound import playsound
import time

def get_gesture(gest1, gest2):
    if gest1 == "fist" and gest2 == "palm":
        # osascript.osascript("""
        # tell application "Tunify"
	    #     pause
        # end tell
        # """)
        print("play")


    elif (gest1 == "palm" and gest2 == "fist"):
        # osascript.osascript(""" hi lollol
        #     tell application "Tunify"
        # 	    pause
        #     end tell
        #     """)
        print("pause")

    else:
        return None


def get_control(x_0, y_0, x_1, y_1):
    print("x_0: {}, y_0: {}, x_1: {}, y_1: {}".format(x_0,y_0,x_1,y_1))
    try:
        if (x_1 > 350 and x_1 < 750):
            if (x_0 < 350):
                #osascript.osascript("""
                 #                   tell application "Tunify"
                #	                tell application "Tunify" to next track
                 #                   end tell
                  #                  """)
                print("next")

            if (x_0 > 750):
                #osascript.osascript("""
                 #                   tell application "Tunify"
                  #                  tell application "Tunify" to previous track
                   #                 end tell
                    #                """)
                print("back")

    except:
        pass

    try:
        if (y_1 > 300):
            if (y_0 < 300):
                    # and int(osascript.osascript("output volume of (get volume settings)")[1]) < 50):
                #osascript.osascript("""
                 #               set volume output volume ((output volume of (get volume settings)) + 6.25)
                  #              """)
                print("volume up")

        if (y_0 > 400):
            #osascript.osascript("""
            #                   set volume output volume ((output volume of (get volume settings)) - 6.25)
            #                  """)
            print("volume down")

    except:
        pass


def show_webcam():
    fist = cv2.CascadeClassifier('fist.xml')
    palm = cv2.CascadeClassifier('palm.xml')

    gest1 = None # one frame ago
    gest2 = None # two frames ago

    x_0 = None
    y_0 = None
    x_1 = None
    y_1 = None

    time0 = 0

    cam = cv2.VideoCapture(0)
    cooldown = 0
    while True:

        ret_val, img = cam.read()
        img = cv2.GaussianBlur(img, (15, 15), 0)
        gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

        fist_detect = fist.detectMultiScale(gray, 1.3, 5)
        for (x, y, w, h) in fist_detect:
            img = cv2.rectangle(img, (x-50, y-50), (x + w+50, y + h+50), (255, 0, 0), 2)
            img = cv2.putText(img, 'fist', (x,y+h), cv2.FONT_HERSHEY_SIMPLEX, 1, (255,0,0),2)
            gest2 = gest1
            gest1 = "fist"
            time0 = 1.67
            x_1 = x_0
            x_0 = x
            y_1 = y_0
            y_0 = y


        palm_detect = palm.detectMultiScale(gray, 1.3, 5)
        for (x, y, w, h) in palm_detect:
            img = cv2.rectangle(img, (x-50, y-150), (x + w+50, y + h+150), (255, 0, 0), 2)
            img = cv2.putText(img, 'palm', (x,y+h), cv2.FONT_HERSHEY_SIMPLEX, 1, (255,0,0),2)
            gest2 = gest1
            gest1 = "palm"
            time0 = 1.67
            x_1 = x_0
            x_0 = x
            y_1 = y_0
            y_0 = y




        if time0 <= 0:
            x_1 = None
            y_1 = None

            gest1 = None
            gest2 = None

        time0 -= .3
        if cooldown != None and cooldown > 0:
          cooldown -= .3


        get_gesture(gest1, gest2)
        get_control(x_0,y_0,x_1, y_1)

        if cv2.waitKey(1) == 27:
            break
        cv2.imshow("test", img)
    cv2.destroyAllWindows()



def main():
    show_webcam()
    playsound('themesong.mp3')


if __name__ == '__main__':
    main()




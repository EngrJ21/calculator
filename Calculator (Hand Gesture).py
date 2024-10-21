import cv2
from cvzone.HandTrackingModule import HandDetector
import time

class Button:
    def __init__(self, pos, width, height, value):
        self.pos = pos
        self.width = width
        self.height = height
        self.value = value

    # Draw the button
    def draw(self, img):
        cv2.rectangle(img, self.pos, (self.pos[0] + self.width, self.pos[1] + self.height),
                      (222, 157, 157), cv2.FILLED)   # Number fill
        cv2.rectangle(img, self.pos, (self.pos[0] + self.width, self.pos[1] + self.height),
                      (97, 7, 7), 2)  # Numbers border
        cv2.putText(img, self.value, (self.pos[0] + 20, self.pos[1] + 60), cv2.FONT_HERSHEY_PLAIN,
                    2, (50, 50, 50), 2)  # Numbers font

    def checkClick(self, x, y):
        if self.pos[0] < x < self.pos[0] + self.width and \
                self.pos[1] < y < self.pos[1] + self.height:
            cv2.rectangle(img, self.pos, (self.pos[0] + self.width, self.pos[1] + self.height),
                          (222, 130, 130), cv2.FILLED)  # Number fill on click
            cv2.rectangle(img, self.pos, (self.pos[0] + self.width, self.pos[1] + self.height),
                          (97, 7, 7), 2)  # Numbers border
            cv2.putText(img, self.value, (self.pos[0] + 20, self.pos[1] + 70), cv2.FONT_HERSHEY_PLAIN,
                        5, (0, 0, 0), 5)  # Numbers font
            return True
        else:
            return False


# Webcam setup with wide view
cap = cv2.VideoCapture(0)
cap.set(3, 1920)  # Set camera width to 1920 for wide view
cap.set(4, 1080)  # Set camera height to 1080 for wide view
detector = HandDetector(detectionCon=0.8, maxHands=1)

# Create buttons including backspace
buttonListValues = [['7', '8', '9', '*'],
                    ['4', '5', '6', '-'],
                    ['1', '2', '3', '+'],
                    ['0', '.', '/', '='],
                    ['Delete']]  # Adding the backspace button

buttonList = []
for x in range(4):
    for y in range(5):  # Adjusted to 5 rows to include the backspace button
        xpos = x * 100 + 800
        ypos = y * 100 + 150
        if y < 4:  # Regular buttons
            buttonList.append(Button((xpos, ypos), 100, 100, buttonListValues[y][x]))
        elif x == 0 and y == 4:  # Position the backspace button
            buttonList.append(Button((xpos, ypos), 400, 100, 'Delete'))  # Wider backspace button

# Variables
myEquation = ''
delayCounter = 0

# Mouse callback function to detect clicks
def mouseClick(event, x, y, flags, param):
    global myEquation, delayCounter
    if event == cv2.EVENT_LBUTTONDOWN:
        for i, button in enumerate(buttonList):
            if button.checkClick(x, y) and delayCounter == 0:
                myValue = button.value
                if myValue == "=":
                    try:
                        myEquation = str(eval(myEquation))
                    except:
                        myEquation = "Error"
                elif myValue == "Delete":
                    myEquation = myEquation[:-1]  # Remove the last character
                else:
                    myEquation += myValue
                delayCounter = 1

# Set mouse callback
cv2.namedWindow("Image")
cv2.setMouseCallback("Image", mouseClick)

# Main loop
while True:
    # Get image from webcam
    success, img = cap.read()
    img = cv2.flip(img, 1)

    # Detection of hand
    hands, img = detector.findHands(img, flipType=False)

    # Draw all buttons
    cv2.rectangle(img, (800, 50), (800 + 400, 70 + 100),
                  (239, 206, 206), cv2.FILLED)  # Solution button background
    cv2.rectangle(img, (800, 50), (800 + 400, 70 + 100),
                  (97, 7, 7), 2)  # Solution border

    for button in buttonList:
        button.draw(img)

    # Check for hand input
    if hands:
        lmList = hands[0]['lmList']
        length, _, img = detector.findDistance(lmList[8][:2], lmList[12][:2], img)
        x, y = lmList[8][:2]
        if length < 50:
            for i, button in enumerate(buttonList):
                if button.checkClick(x, y) and delayCounter == 0:
                    myValue = button.value
                    if myValue == "=":
                        try:
                            myEquation = str(eval(myEquation))
                        except:
                            myEquation = "Error"
                    elif myValue == "Delete":
                        myEquation = myEquation[:-1]  # Remove the last character
                    else:
                        myEquation += myValue
                    delayCounter = 1

    # Avoid duplicate clicks
    if delayCounter != 0:
        delayCounter += 1
        if delayCounter > 10:
            delayCounter = 0

    # Display the equation or results
    cv2.putText(img, myEquation, (810, 110), cv2.FONT_HERSHEY_DUPLEX,
                1, (77, 17, 17), 2)  # Solution answer font

    # Display the image
    cv2.imshow("Image", img)
    key = cv2.waitKey(1)
    if key == ord('c'):
        myEquation = ''

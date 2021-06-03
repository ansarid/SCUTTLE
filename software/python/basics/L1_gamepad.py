"""Simple example showing how to get gamepad events."""
import time
import threading
import numpy as np
from inputs import get_gamepad

class Gamepad:
    def __init__(self):
        self.axesMap = {
            'ABS_X':'LEFT_X',
            'ABS_Y':'LEFT_Y',
            'ABS_Z':'RIGHT_X',
            'ABS_RZ':'RIGHT_Y',
        }

        self.buttonMap = {
            'BTN_SOUTH':'Y',
            'BTN_EAST':'B',
            'BTN_C':'A',
            'BTN_NORTH':'X',
            'BTN_WEST':'LB',
            'BTN_Z':'RB',
            'BTN_TL':'LT',
            'BTN_TR':'RT',
            'BTN_TL2':'BACK',
            'BTN_TR2':'START',
            'BTN_SELECT':'L_JOY',
            'BTN_START':'R_JOY',
        }

        self.buttons = {}
        self.axes = {}
        self.hat = [0,0]
        self.states = { 'axes': self.axes,
                        'buttons': self.buttons,
                        'hat': self.hat
                    }

        for button in self.buttonMap.keys():
            self.buttons[self.buttonMap[button]] = 0

        for axis in self.axesMap.keys():
            self.axes[self.axesMap[axis]] = 128

        # self.stateUpdater()
        self.stateUpdaterThread = threading.Thread(target=self.stateUpdater)
        self.stateUpdaterThread.start()

    def _getStates(self):
        events = get_gamepad()
        for event in events:
            # print(event.ev_type, event.code, event.state)
            if event.ev_type == "Absolute":
                if 'ABS_HAT' in event.code:
                    if 'ABS_HAT0X' == event.code:
                        self.hat[0] = event.state
                    elif 'ABS_HAT0Y' == event.code:
                        self.hat[1] = event.state
                else:
                    self.axes[self.axesMap[event.code]] = event.state
            elif event.ev_type == "Key":
                self.buttons[self.buttonMap[event.code]] = event.state
            else:
                pass

        self.states = { 'axes': self.axes,
                        'buttons': self.buttons,
                        'hat': self.hat
                    }

        return self.states

    def stateUpdater(self):
        while True:
            self._getStates()

    def getStates(self):
        return self.states

    def getGP(self):
        axes = np.array([((2/255)*self.axes['LEFT_X'])-1,
                         ((2/255)*self.axes['LEFT_Y'])-1,
                         ((2/255)*self.axes['RIGHT_X'])-1,
                         ((2/255)*self.axes['RIGHT_Y'])-1]
                         )                                  # store all axes in an array

        buttons = np.array([self.buttons['Y'],              # B0
                            self.buttons['B'],              # B1
                            self.buttons['A'],              # B2
                            self.buttons['X'],              # B3
                            self.buttons['LB'],             # B4
                            self.buttons['RB'],             # B5
                            self.buttons['LT'],             # B6
                            self.buttons['RT'],             # B7
                            self.buttons['BACK'],           # B8
                            self.buttons['START'],          # B9
                            self.buttons['L_JOY'],          # B10
                            self.buttons['R_JOY']]          # B11
                            )                               # store all buttons in array

        gp_data = np.hstack((axes, buttons))                # this array will have 16 elements

        return(gp_data)

if __name__ == "__main__":
    gamepad = Gamepad()
    while True:
        # collect commands from the gamepad.  Run as many times as there are commands in the queue.
        myGpData = gamepad.getGP()                          # store data from all axes to the myGpData variable
        print(myGpData)                                     # print out the first element of the data to confirm functionality
        time.sleep(0.25)
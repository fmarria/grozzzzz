import time

class PIDControl:

    def __init__(self, p, i, d, integral = None, diff = None, step_size = None) -> None:
        self.__kp = p
        self.__ki = i
        self.__kd = d
        self.__integral = 0
        self.__diff = 0 # new
        self.__e_prev = 0
        self.__time_step = 0
        self.__u = 0

        if not integral is None:
            self.__integral = integral

        if not diff is None: # new
            self.__integral = diff
        
        if not step_size is None:
            self.__time_step = step_size

    def __updateTrapezIntegral(self, error, error_prev, time_step):
        return time_step / 2 * (error + error_prev)
    
    def __updateDiff(self, error, error_prev, time_step): # new
        return (error - error_prev) / time_step

    def updateP(self, error: float):
        self.__u = self.__kp * error

    def updatePI(self, error: float):
        self.__integral += self.__updateTrapezIntegral(
            error, self.__e_prev, self.__time_step
        )
        self.__e_prev = error
        self.__u = self.__kp * error + self.__ki * self.__integral

    def updatePD(self, error: float): # new
        self.__diff = self.__updateDiff(
            error, self.__e_prev, self.__time_step
        )
        self.__e_prev = error
        self.__u = self.__kp * error + self.__kd * self.__diff

    def updatePID(self, error: float): # new
        self.__integral += self.__updateTrapezIntegral(
            error, self.__e_prev, self.__time_step
        )
        self.__diff = self.__updateDiff(
            error, self.__e_prev, self.__time_step
        )
        self.__e_prev = error
        
        self.__u = self.__kp * error + self.__ki * self.__integral + self.__kd * self.__diff

    @property
    def value(self) -> float:
        if abs(self.__u) > 100:
            return ((self.__u > 0) - (self.__u < 0)) * 100
        return self.__u

    @property
    def kp(self) -> float:
        return self.__kp

    @kp.setter
    def kp(self, value: float):
        self.__kp = value

    
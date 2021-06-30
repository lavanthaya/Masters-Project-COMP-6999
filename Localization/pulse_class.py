class Pulse_classifier:
    def __init__(self, time_delta):

      self.pulse = 'n'
      self.angle = 'n'

      sync_max = 135; #us
      sync_low = 104; #us
      sweep_max = 55; #us
      
      
      if (((time_delta >=sync_low) and (time_delta < 110)) or ((time_delta >= 120) and (time_delta < 130))):
        self.pulse = 's'
        self.angle = 'h'
      
      elif (((time_delta >=110) and (time_delta < 120)) or ((time_delta >= 130) and (time_delta < sync_max))):
        self.pulse = 's'
        self.angle = 'v'
        
      elif(time_delta <= sweep_max):
        self.pulse = 'p'
      
class Phasor:
    def __init__(self, frequency, magnitude, phase, real=None, imaginary=None):
        self.real = real
        self.imaginary = imaginary
        self.frequency = frequency
        self.magnitude = magnitude
        self.phase = phase
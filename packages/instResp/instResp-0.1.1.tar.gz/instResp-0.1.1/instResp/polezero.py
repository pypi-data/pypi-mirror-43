
import numpy as np

# Can't do this bc of circular imports:
#from instResp.libInst import getResponse
import instResp

'''
    This module contains a collection of non-bulletproof codes
    for creating/manipulating instrument response stages,
    particularly the first stage = analog polezero stage.

    polezero is an internal class for polezero stage used by
    the codes.
'''

class polezero:
    def __init__(self,
                 name, type,
                 unitsIn, unitsOut,
                 a0,
                 sensitivity, sensitivity_f,
                 poles,
                 zeros):
        self.name         = name
        self.type         = type    # e.g., type='A' Laplace
        self.unitsIn      = unitsIn
        self.unitsOut     = unitsOut
        self.poles        = poles
        self.zeros        = zeros
        self.a0           = a0
        self.sensitivity  = sensitivity
        self.sensitivity_f= sensitivity_f
        #self.constant     = constant

    @property
    def npoles(self):
        if self.poles is not None:
            return self.poles.size
        else:
            return 0

    @property
    def nzeros(self):
        if self.zeros is not None:
            return self.zeros.size
        else:
            return 0

    def __str__(self):
        string = "\n"
        string += "name:\t%s\n" % self.name
        string += "type:\t%s\n" % self.type
        string += "In:\t%s\n" % self.unitsIn
        string += "Out:\t%s\n" % self.unitsOut
        string += "a0:\t%e\n" % self.a0
        string += "sensitivity:  %e\n" % self.sensitivity
        string += "npoles:\t%d\n" % self.npoles
        for i in range(self.npoles):
            string += "  %d: %14.12e  %14.12e\n" % (i, self.poles[i].real, self.poles[i].imag)
        string += "nzeros:\t%d\n" % self.nzeros
        for i in range(self.nzeros):
            string += "  %d: %14.12e  %14.12e\n" % (i, self.zeros[i].real, self.zeros[i].imag)

        return string

    def normalize_to_a0(self, norm_freq = 1.):
        resp = instResp.libInst.getResponse(self, [norm_freq], removeZero=False, useSensitivity=False)
        self.a0 /= np.abs(resp)

    def remove_zero(self):
        zerosIn = self.zeros
        nIn = zerosIn.size
        hasZeroAtOrigin = False
        ii=-1
        for i in range(zerosIn.size):
            if zerosIn[i].real == 0 and zerosIn[i].imag == 0:
                #print "Found origin at i=%d" % i
                hasZeroAtOrigin = True
                ii=i
                break
        if hasZeroAtOrigin:
            nOut = nIn-1
            zerosOut = np.zeros((nOut,), dtype=np.complex128)
            j=0
            for i in range(zerosIn.size):
                #print "i=%d real=%f imag=%f" % (i, zerosIn[i].real, zerosIn[i].imag)
                if i != ii:
                    zerosOut[j] = zerosIn[i]
                    j += 1

            self.zeros = zerosOut

            return 1
        return 0


    def append_pole(self, pole):
        new_poles = np.zeros((len(self.poles)+1,), dtype=np.complex128)

        for i in range(len(self.poles)):
            new_poles[i] = self.poles[i]
        new_poles[i+1] = pole

        self.poles = new_poles

        return 1

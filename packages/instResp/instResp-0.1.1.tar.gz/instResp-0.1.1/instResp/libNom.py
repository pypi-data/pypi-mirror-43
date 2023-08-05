
import numpy as np

from instResp.polezero import polezero

from instResp.libInst import getResponse


def mb2005():
    poles = np.zeros((4,), dtype=np.complex128)
    poles[0] = -1.77700000E+02 -1.77700000E+02j
    poles[1] = -1.77700000E+02 +1.77700000E+02j
    poles[2] = -6.28000000E-02 +0.00000000E+00j
    poles[3] = -2.07345000E+02 +0.00000000E+00j
    zeros = np.zeros((1,), dtype=np.complex128)
    zeros[0] = 0.00000000E+00 + 0.00000000E+00j

    pz_mb2005 = polezero(name = 'mb2005',
                         type = 'A', #type = 'A[Laplace Transform (Rad/sec)]',
                         unitsIn  = 'Pa',
                         unitsOut = 'V',
                         a0 = 1.3162E+07,
                         sensitivity = .02,
                         sensitivity_f = 1.0,
                         poles = poles,
                         zeros = zeros)

    return pz_mb2005

def cmg3T():
    poles = np.zeros((5,), dtype=np.complex128)
    #poles = np.zeros((2,), dtype=np.complex128)
    poles[0] = -3.70E-02  +  3.70E-02j
    poles[1] = -3.70E-02  -  3.70E-02j
    poles[2] = -5.03E+02  +  0.0j
    poles[3] = -1.01E+03  +  0.0j
    poles[4] = -1.13E+03  +  0.0j
    zeros = np.zeros((2,), dtype=np.complex128)
    zeros[0] = 0 +0j
    zeros[1] = 0 +0j

    name = "cmg3T generic 2-pole/2-zero" 
    name = "cmg3T generic 5-pole/2-zero" 

    pz = polezero(name = name,
                         type = 'A', #type = 'A[Laplace Transform (Rad/sec)]',
                         unitsIn  = 'N/A',
                         unitsOut = 'N/A',
                         a0 = 1.,
                         sensitivity = 1,
                         sensitivity_f = 1.0,
                         poles = poles,
                         zeros = zeros)
    return pz

def sts2():
    poles = np.zeros((5,), dtype=np.complex128)
    poles[0] = -3.70E-02  +  3.70E-02j
    poles[1] = -3.70E-02  -  3.70E-02j
    poles[2] = -2.51E+02  +  0.0j
    poles[3] = -1.31E+02  +  4.67E+02j
    poles[4] = -1.31E+02  -  4.67E+02j
    zeros = np.zeros((2,), dtype=np.complex128)
    zeros[0] = 0 +0j
    zeros[1] = 0 +0j

    name = "sts2 generic 5-pole/2-zero" 

    pz = polezero(name = name,
                         type = 'A', #type = 'A[Laplace Transform (Rad/sec)]',
                         unitsIn  = 'N/A',
                         unitsOut = 'N/A',
                         a0 = 1.,
                         sensitivity = 1,
                         sensitivity_f = 1.0,
                         poles = poles,
                         zeros = zeros)
    return pz

def sts2_3rd_gen():
    poles = np.zeros((11,), dtype=np.complex128)
    poles[0] = -1.33E+04 +  0.00E+00j
    poles[1] = -1.05E+04 +  1.01E+04j
    poles[2] = -1.05E+04 -  1.01E+04j
    poles[3] = -5.20E+02 +  0.00E+00j
    poles[4] = -3.75E+02 +  0.00E+00j
    poles[5] = -9.73E+01 +  4.01E+02j
    poles[6] = -9.73E+01 -  4.01E+02j
    poles[7] = -1.56E+01 +  0.00E+00j
    poles[8] = -3.70E-02 +  3.70E-02j
    poles[9] = -3.70E-02 -  3.70E-02j
    poles[10]= -2.55E+02 +  0.00E+00j
    zeros = np.zeros((6,), dtype=np.complex128)
    zeros[0] = 0.00E+00  +  0.00E+00j
    zeros[1] = 0.00E+00  +  0.00E+00j
    zeros[2] = -4.63E+02 +  4.31E+02j
    zeros[3] = -4.63E+02 -  4.31E+02j
    zeros[4] = -1.77E+02 +  0.00E+00j
    zeros[5] = -1.52E+01 +  0.00E+00j

    name = "sts2 3rd Gen 11-pole/6-zero" 

    pz = polezero(name = name,
                         type = 'A', #type = 'A[Laplace Transform (Rad/sec)]',
                         unitsIn  = 'N/A',
                         unitsOut = 'N/A',
                         a0 = 1.,
                         sensitivity = 1,
                         sensitivity_f = 1.0,
                         poles = poles,
                         zeros = zeros)
    return pz


def singlePole(period=5, zero=False):
    poles = np.zeros((1,), dtype=np.complex128)
    re = 2.*np.pi/period
    #print "period=%f re=%f" % (period, re)
    poles[0] = -re +0j
    if zero:
        zeros = np.zeros((1,), dtype=np.complex128)
        #zeros = np.zeros((2,), dtype=np.complex128)
        #zeros[0] = re +0j
        #zeros[0] = re/10. +0j
        zeros[0] = 0 +0j
        #zeros[1] = 0 +0j
    else:
        zeros = None
    #print "zeros=", zeros

    name = "singlePole fc=[%.4f Hz] zero=[%s]" % (1./period, zero)  

    pz = polezero(name = name,
                         type = 'A', #type = 'A[Laplace Transform (Rad/sec)]',
                         unitsIn  = 'N/A',
                         unitsOut = 'N/A',
                         a0 = 1.,
                         sensitivity = 1,
                         sensitivity_f = 1.0,
                         poles = poles,
                         zeros = zeros)

    return pz

def doublePoleA(period=5, angle=45, zeros=False):
    poles = np.zeros((2,), dtype=np.complex128)
    mag = 2.*np.pi/period
    rad = np.pi * float(angle)/180.
    sig = mag * np.cos(rad)
    omega = mag * np.sin(rad)

    poles[0] = np.complex(-sig, omega)
    poles[1] = np.complex(-sig, -omega)

    name = "doublePole: period=[%d] angle=[%d]" %  (period, angle)
    #print name
    #print poles
    zeros = None

    pz = polezero(name = name,
                         type = 'A', #type = 'A[Laplace Transform (Rad/sec)]',
                         unitsIn  = 'N/A',
                         unitsOut = 'N/A',
                         a0 = 1.,
                         sensitivity = 1,
                         sensitivity_f = 1.0,
                         poles = poles,
                         zeros = zeros)

    return pz




def doublePole(period=5, anti=True, zeros=False):
    poles = np.zeros((2,), dtype=np.complex128)
    re = 2.*np.pi/period
    re /= np.sqrt(2)

    poles[0] = np.complex(-re, re)
    poles[1] = np.complex(-re, -re)
    #print "doublePole: period=%f zeros=%s" % (period, zeros)
    #print poles

    if zeros:
        zeros = np.zeros((2,), dtype=np.complex128)
        zeros[0] = 0. + 0j
        zeros[1] = 0. + 0j
    else:
        zeros = None

    name = "doublePole: poles: ", poles

    pz = polezero(name = name,
                         type = 'A', #type = 'A[Laplace Transform (Rad/sec)]',
                         unitsIn  = 'Pa',
                         unitsOut = 'V',
                         a0 = 1.,
                         sensitivity = 1,
                         sensitivity_f = 1.0,
                         poles = poles,
                         zeros = zeros)

    return pz


def mb3():
    poles = np.zeros((4,), dtype=np.complex128)
    poles[0] = -6.28340000E-02 + 0.00000000E+00j
    poles[1] = -1.56250000E+02 + 0.00000000E+00j 
    poles[2] = -1.42122000E+02 + 7.06193000E+02j
    poles[3] = -1.42122000E+02 - 7.06193000E+02j
    zeros = np.zeros((2,), dtype=np.complex128)
    zeros[0] = 0.00000000E+00 + 0.00000000E+00j
    zeros[1] = -1.1562500E+03 + 0.00000000E+00j

    pz_mb3 = polezero(name = 'mb3',
                         type = 'A', #type = 'A[Laplace Transform (Rad/sec)]',
                         unitsIn  = 'Pa',
                         unitsOut = 'V',
                         a0 = 7.0200E+04,
                         sensitivity = .02,
                         sensitivity_f = 1.0,
                         poles = poles,
                         zeros = zeros)
    return pz_mb3

def wwssn_lp():
    poles = np.zeros((4,), dtype=np.complex128)
    #pz.poles[0] = dcmplx(-0.25700, -0.3376);
    #pz.poles[1] = dcmplx(-0.25700,  0.3376);
    #pz.poles[2] = dcmplx(-0.06283, -0.00000);
    #pz.poles[3] = dcmplx(-0.06283,  0.00000);

    poles[0] = -0.2513 + 0.3351j
    poles[1] = -0.2513 - 0.3351j
    poles[2] = -0.0628 + 0.0j
    poles[3] = -0.0628 - 0.0j
    #poles[2] = -0.0628 + 0.0304j
    #poles[3] = -0.0628 - 0.0304j
    zeros = np.zeros((3,), dtype=np.complex128)
    zeros[0] = 0.00000000E+00 + 0.00000000E+00j
    zeros[1] = 0.00000000E+00 + 0.00000000E+00j
    zeros[2] = 0.00000000E+00 + 0.00000000E+00j

    pz = polezero(name = 'WWSSN-LP',
                         type = 'A', #type = 'A[Laplace Transform (Rad/sec)]',
                         unitsIn  = 'M',
                         unitsOut = 'V',
                         a0 = 1,
                         sensitivity = 1,
                         sensitivity_f = 1.0,
                         poles = poles,
                         zeros = zeros)
    return pz

def RC(tau=1., gain=1.):
    '''
    RC filter has single pole at s_p = -1/tau [rad/s] on real axis,
        where tau=RC
    '''

    zeros = None

    poles = np.zeros((1,), dtype=np.complex128)
    poles[0] = -1./tau + 0.0j

    pz = polezero(name = 'RC',
                         type = 'A', #type = 'A[Laplace Transform (Rad/sec)]',
                         unitsIn  = 'mm',
                         unitsOut = 'V',
                         a0 = gain,
                         sensitivity = 1,
                         sensitivity_f = 1.0,
                         poles = poles,
                         zeros = zeros)
    return pz


def L22D(gain=21.64):
    '''
    '''
    zeros = np.zeros((2,), dtype=np.complex128)
    zeros[0] = 0.0 + 0.0j
    zeros[1] = 0.0 + 0.0j

    poles = np.zeros((2,), dtype=np.complex128)
    poles[0] = -8.796 + 8.974j
    poles[1] = -8.796 - 8.974j

    pz = polezero(name = 'L22',
                         type = 'A', #type = 'A[Laplace Transform (Rad/sec)]',
                         unitsIn  = 'mm',
                         unitsOut = 'V',
                         a0 = gain,
                         sensitivity = 1,
                         sensitivity_f = 1.0,
                         poles = poles,
                         zeros = zeros)
    return pz

def Accelerometer(per=0.8, damp=0.8, gain=2800, normalize=False, normalize_freq=1.0):
    '''
  /*
   */
    '''
    zeros = None

    poles = np.zeros((2,), dtype=np.complex128)
    omega = 2.0 * np.pi / per
    r = np.sqrt(1.0 - damp * damp)
    re  = -omega * damp
    im  =  omega * r
    poles[0] = re + im*1j
    poles[1] = re - im*1j

    pz = polezero(name = 'Generic Accelerometer',
                         type = 'A', #type = 'A[Laplace Transform (Rad/sec)]',
                         unitsIn  = 'M/S**2',
                         unitsOut = 'V',
                         a0 = gain,
                         sensitivity = 1,
                         sensitivity_f = 1.0,
                         poles = poles,
                         zeros = zeros)

    if normalize:
        resp = getResponse(pz, [normalize_freq], removeZero=False, useSensitivity=False)
        pz.a0 /= np.abs(resp)

    return pz


def WA(per=0.8, damp=0.8, gain=2800, normalize=False, normalize_freq=1.0):
    '''
  /*
   * The Wood-Anderson is an optical-mechanical seismometer. The standard
   * parameters for its transfer function are:
   * period: 0.8 seconds; damping 0.8 critical; gain: 2800
   * However, testing by Uhrhammer & Collins (BSSA 1990, V80 p702-716)
   * indicates better values are:
   * period 0.8 seconds; damping 0.7 critical; gain 2080
   */
    '''
    zeros = np.zeros((2,), dtype=np.complex128)
    zeros[0] = 0.0 + 0.0j
    zeros[1] = 0.0 + 0.0j

    #poles = np.zeros((3,), dtype=np.complex128)
    poles = np.zeros((2,), dtype=np.complex128)
    omega = 2.0 * np.pi / per
    r = np.sqrt(1.0 - damp * damp)
    re  = -omega * damp
    im  =  omega * r
    poles[0] = re + im*1j
    poles[1] = re - im*1j

    #tau = 1.82e-04
    tau = 1.6e-04
    #poles[2] = -1./tau + 0.0j

    pz = polezero(name = 'WA',
                         type = 'A', #type = 'A[Laplace Transform (Rad/sec)]',
                         unitsIn  = 'mm',
                         unitsOut = 'V',
                         a0 = gain,
                         sensitivity = 1,
                         sensitivity_f = 1.0,
                         poles = poles,
                         zeros = zeros)

    if normalize:
        resp = getResponse(pz, [normalize_freq], removeZero=False, useSensitivity=False)
        #print(np.abs(resp))
        pz.a0 /= np.abs(resp)
        #resp = getResponse(pz, [normalize_freq], removeZero=False)
        #print(np.abs(resp))

    return pz


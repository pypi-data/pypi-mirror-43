
import numpy as np

from instResp.polezero import polezero
from instResp.plotResp import plotResponse

import os
import logging
logging.basicConfig(format='%(levelname)s:%(message)s', level=logging.INFO)
logger = logging.getLogger(__name__)

'''
    This module contains a collection of non-bulletproof codes
    for creating/manipulating instrument response stages,
    particularly the first stage = analog polezero stage.

'''

def evalResp(pz, f):
    s = 0.000 + 1.000j
    numerator   = 1.000 + 0.000j
    denominator = 1.000 + 0.000j

    if pz.type == 'A':
        s *= 2.*np.pi*f
    elif pz.type == 'B':
        s *= f
    else:
        logger.warn("Unknown pz response type=[%s]" % pz.type)

    for j in range(pz.nzeros):
        numerator *= (s - pz.zeros[j])

    for j in range(pz.npoles):
        denominator *= (s - pz.poles[j])

    Gf = numerator * pz.a0   # Make sure this is complex
    Gf /= denominator 
    return Gf;

def getResponse(pz, freqs, removeZero=False, useSensitivity=True):
    '''
        We're expecting a standard IRIS polezero file for displacement,
            so if velocity=True try to shed one zero at origin
    '''

    if removeZero:
        success = pz.remove_zero()

        #zeros = np.zeros((pz.zeros.size-1,), dtype=np.complex128) 
        #success = remove_zero(pz.zeros, zeros)
        if success:
            logger.debug("Zero successfully removed from origin")
            #pz.zeros = zeros
            #pz.nzeros = zeros.size
        else:
            logger.warn("Problem removing zero from origin!")

    resp = np.zeros((len(freqs),), dtype=np.complex128) 
    for i, f in enumerate(freqs):
        resp[i] = evalResp(pz, f)
        if useSensitivity:
            resp[i] *= pz.sensitivity
    return resp


def read_sacpz_file(filename):
    """
* **********************************
* NETWORK   (KNETWK): AU
* STATION    (KSTNM): WR1
* LOCATION   (KHOLE):
* CHANNEL   (KCMPNM): BHZ
* CREATED           : 2017-02-02T01:23:27
* START             : 2005-01-31T00:00:00
* END               : 2599-12-31T23:59:59
* DESCRIPTION       : Warramunga Array, Australia
* LATITUDE          : -19.942600
* LONGITUDE         : 134.339500
* ELEVATION         : 389.0
* DEPTH             : 0.0
* DIP               : 0.0
* AZIMUTH           : 0.0
* SAMPLE RATE       : 40.0
* INPUT UNIT        : M
* OUTPUT UNIT       : COUNTS
* INSTTYPE          : Guralp CMG3ESP_30sec_ims/Guralp DM24-MK3 Datalogge
* INSTGAIN          : 4.000290e+03 (M/S)
* COMMENT           : V3180 A3242
* SENSITIVITY       : 2.797400e+09 (M/S)
* A0                : 8.883050e-02
* **********************************
ZEROS   5
    +0.000000e+00   +0.000000e+00
    +0.000000e+00   +0.000000e+00
    +0.000000e+00   +0.000000e+00
    +8.670000e+02   +9.050000e+02
    +8.670000e+02   -9.050000e+02
POLES   4
    -1.486000e-01   +1.486000e-01
    -1.486000e-01   -1.486000e-01
    -3.140000e+02   +2.023000e+02
    -3.140000e+02   -2.023000e+02
CONSTANT    2.484944e+08
    """


    fname = 'read_sacpz_file'

    with open(filename, 'r') as f:
        lines = f.readlines()

    zeros = None
    poles = None
    sensitivity = None
    a0 = None
    unitsIn = None
    unitsOut = None
    knet = ""
    ksta = ""
    kloc = ""
    kchan = ""

    for i in range(len(lines)):
        line = lines[i]
        #print "i=[%d] line=[%s]" % (i, line)

        if line[0] == '*':
            if line[2] != '*':
                split_list = line.split(':')
                field = split_list[0][1:]
                val   = split_list[1]
                # could have val = "" or val = 2.79E9 (M/S)
                val_list = val.split()
                nsplit=len(val_list)
                #print "field=", field, " val=", val

                if 'SENSITIVITY' in field:
                    sensitivity = float(val_list[0])
                elif 'A0' in field:
                    a0 = float(val_list[0])
                elif 'INPUT UNIT' in field:
                    unitsIn = val.strip()
                elif 'OUTPUT UNIT' in field:
                    unitsOut = val.strip()
                elif 'NETWORK' in field:
                    knet = val.strip()
                elif 'STATION' in field:
                    ksta = val.strip()
                elif 'LOCATION' in field:
                    kloc = val.strip()
                elif 'CHANNEL' in field:
                    kchan = val.strip()

        elif line[0:5] == 'ZEROS':
            try:
                nzeros = int(line[6:len(line)])
            except:
                logger.error("%s.%s Error: can't read nzeros from line=[%s]" % (__name__, fname, line))
                exit(1)
            #zeros = np.zeros((nzeros,), dtype=np.complex128)
            zeros = np.zeros(nzeros, dtype=np.complex128)
            for j in range(nzeros):
                i += 1
                line = lines[i]
                (z_re, z_im) = line.split()
                zeros[j] = complex( float(z_re), float(z_im) )
        elif line[0:5] == 'POLES':
            try:
                npoles = int(line[6:len(line)])
            except:
                logger.error("%s.%s Error: can't read npoles from line=[%s]" % (__name__, fname, line))
                exit(1)
            poles = np.zeros(npoles, dtype=np.complex128)
            for j in range(npoles):
                i += 1
                line = lines[i]
                (p_re, p_im) = line.split()
                poles[j] = complex( float(p_re), float(p_im) )

    #print "knet=%s ksta=%s kloc=%s kchan=%s" % (knet, ksta, kloc, kchan)
    name = "%s.%s %s.%s" % (knet, ksta, kloc, kchan)

    pz_ = polezero(name = name,
                         type = 'A', #type = 'A[Laplace Transform (Rad/sec)]',
                         unitsIn  = unitsIn,
                         unitsOut = unitsOut,
                         a0 = a0,
                         sensitivity = sensitivity,
                         sensitivity_f = 1.0,
                         poles = poles,
                         zeros = zeros)
    return pz_


def get_corner_freq_from_pole(pole):
    '''
        get distance [rad/s] from lowest order pole to origin
            and return Hz [/s]
    '''
    return np.sqrt(pole.real**2 + pole.imag**2) / (2.*np.pi)



def test_RC():
    from instResp.libNom import RC
    R = 4.
    C = 1.25/(2.*np.pi)
    pzs = RC(tau=R*C)
    freqs = np.logspace(-5, 4., num=1000)
    resp  = getResponse(pzs, freqs, removeZero=False)
    title = 'RC filter: R=4 ohms, C=1.25F/2pi'
    plotResponse(resp, freqs, title=title, xmin=.001, xmax=100., ymin=0.01, ymax=1.2)

    logger.info("Corner freq:%f" % get_corner_freq_from_pole(pzs.poles[0]))

    return

def test_WA(damp=.18, gain=1., f0=14, fnorm=100.):
    from instResp.libNom import WA, Accelerometer
    pzs = WA(per=1/f0, damp=damp, gain=gain, normalize=True, normalize_freq=fnorm)

    logger.info(pzs)
    freqs = np.logspace(-5, 4., num=500)
    resp  = getResponse(pzs, freqs, removeZero=False)
    #print(np.max(np.abs(resp)))
    title='WA for f0=%.2f Hz damp=%.3f gain=%.0f' % (f0,damp, gain)
    logger.info("Corner freq:%.2f" % get_corner_freq_from_pole(pzs.poles[0]))
    plotResponse(resp, freqs, title=title, xmin=1, xmax=5000., ymin=.01, ymax=1.2)

    return


def plot_pz_resp(pzfile=None):
    pzs = read_sacpz_file(pzfile)
    logger.info(pzs)
    freqs = np.logspace(-5, 3., num=500)
    resp  = getResponse(pzs, freqs, removeZero=True, useSensitivity=False)
    title=pzfile
    plotResponse(resp, freqs, title=title, xmin=.001, xmax=100., ymin=.01, ymax=1e3)
    return


def main():

    #test_RC()
    test_WA(damp=0.6)
    exit()

    pz_dir = '/Users/mth/mth/Data/IRIS_Request/pz/'
    pz_fil = 'SACPZ.II.AAK.10.BHZ'
    plot_pz_resp(pzfile=os.path.join(pz_dir, pz_fil))

    exit()

if __name__=="__main__":
    main()

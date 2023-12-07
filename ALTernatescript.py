# execute the regular script 
exec(open("AntiKt10UFOCSSKSoftDropBeta100Zcut10.py").read())

# move the configure function
configure_old = configure

# we can then redefine a new one which will call the regular one
# and change a few parameters including the calibration factors set.
def configure():
    # call the regular configure to obtain the CalibrationObjects :
    objs = configure_old()

    # below we'll read the TH3F containing alternative calib constant 

    # name of file containing the TH3F (typically from a
    # "*_calibFactors.root" file which is produced by running the -s Plots.jms option)
    alternName = "jms_ELogMoEBins_WZ/AntiKt10UFOCSSKSoftDropBeta100Zcut10_JMSmCalo_calibFactors.root"
    alternTag = "WZ_on_mc23"

    objs.alternFile = ROOT.TFile(alternName)
    objs.alternTH3 = objs.alternFile.Get("mRsmooth_3D")
    # assign the TH3 to our ResponseBuilder objects (thus the system will not pick up the default one)
    #objs.respBuilder.m_jmsRecoBin.m_correctionFactors3d = objs.alternTH3
    objs.jmsCorrector(forceResponseMap=objs.alternTH3)

    # change the output dir to match the one we pre-copied
    objs.jmsWorkDir = objs.jmsWorkDir[:-1]+"_"+alternTag+"/"

    return objs


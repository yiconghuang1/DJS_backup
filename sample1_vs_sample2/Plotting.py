import csv
import ROOT
import math
from ROOT.TMath import CosH
from DeriveJetScales.DrawUtils import buildPage, PdfSaver

ROOT.gROOT.LoadMacro("/afs/cern.ch/work/y/yihuang/public/JetScales_devel/source/DeriveJetScales/scripts/AtlasStyleUtils.C")
ROOT.gROOT.SetBatch(1)
ROOT.SetAtlasStyle()
g0 = ROOT.TGraph2D()
g0_err = ROOT.TGraph2D()
pointN0 = 0
g40 = ROOT.TGraph2D()
g40_err = ROOT.TGraph2D()
pointN40 = 0
pointJES = 0

JES_unc = ROOT.TGraph2D()
JER_unc = ROOT.TGraph2D()

with open("mc20_closureRvspT.csv") as csv_file:
    csv_reader = csv.reader(csv_file, delimiter=' ')
    for row in csv_reader:
        g0.SetPoint(pointN0, float(row[0]), float(row[1]), float(row[2]))
        g0_err.SetPoint(pointN0, float(row[0]), float(row[1]), float(row[3]))
        pointN0+=1

with open("mc23_closureRvspT.csv") as csv_file:
     csv_reader = csv.reader(csv_file, delimiter=' ')
     for row in csv_reader:
        g40.SetPoint(pointN40, float(row[0]), float(row[1]), float(row[2]))
        g40_err.SetPoint(pointN40, float(row[0]), float(row[1]), float(row[3]))

        dJES = abs(float(row[2])-g0.Interpolate(float(row[0]), float(row[1])) )
        dJER = abs(float(row[3]) - g0_err.Interpolate(float(row[0]), float(row[1])) ) * math.sqrt(abs(float(row[3])**2 - g0_err.Interpolate(float(row[0]), float(row[1]))**2) )

        if dJES<0.5:
          JES_unc.SetPoint(pointJES, float(row[1]), float(row[0]), dJES )
          JER_unc.SetPoint(pointJES, float(row[1]), float(row[0]), dJER )
          pointJES+=1

        pointN40+=1

f = ROOT.TFile("closure_R_Graph.root","recreate")
page = buildPage(PdfSaver, 1, "Eresponse.pdf")
ROOT.gStyle.SetPalette(1);

g0.SetName("ERespMC20")
g0.SetTitle("mc20;eta;pT [GeV];E response")
g40.SetName("ERespMC23")
g40.SetTitle("mc23;eta;pT [GeV];E response")

g0_err.SetName("reso_MC20")
g0_err.SetTitle("mc20;eta;pT [GeV];E resolution")
g40_err.SetName("reso_MC23")
g40_err.SetTitle("mc23;eta;pT [GeV];E resolution")

h_JES_unc = ROOT.TH2D("JESUnc_mc20vsmc23_MC20_PreRec_AntiKt10UFOCSSKSoftDrop","JESUnc;pT;eta", 15, 100., 1600.,60, -3.0, 3.0);
h_JES_unc = JES_unc.GetHistogram()
h_JER_unc = ROOT.TH2D("JERUnc_mc20vsmc23_MC20_PreRec_AntiKt10UFOCSSKSoftDrop","JERUnc;pT;eta",15, 100., 1600., 60, -3.0, 3.0);
h_JER_unc = JER_unc.GetHistogram()

eta_list = [ -2.5, -2.0, -1.5, -1.0, -0.5, 0., 0.5, 1.0, 1.5, 2.0, 2.5]
pT_list = [200., 300., 400., 500., 600., 700., 800., 900., 1000.,1100., 1200., 1300.]
for ieta in range(len(eta_list)):
    page.setNplots( 1 )
    i = 0
    R_vs_pT = ROOT.TGraphErrors()
    R_vs_pT1 = ROOT.TGraphErrors()
    IQR_vs_pT = ROOT.TGraphErrors()
    IQR_vs_pT1 = ROOT.TGraphErrors()
    R = ROOT.TMultiGraph()
    IQR = ROOT.TMultiGraph()
    for ipT in range(len(pT_list)):
        #E = pT_list[ipT]*CosH(eta_list[ieta])
        if g0.Interpolate(eta_list[ieta],pT_list[ipT])>0.:
            R_vs_pT.SetPoint(i, pT_list[ipT], g0.Interpolate(eta_list[ieta],pT_list[ipT]))
        if g40.Interpolate(eta_list[ieta],pT_list[ipT])>0.:
            R_vs_pT1.SetPoint(i, pT_list[ipT], g40.Interpolate(eta_list[ieta],pT_list[ipT]))
        if g0_err.Interpolate(eta_list[ieta],pT_list[ipT])>0.:
            IQR_vs_pT.SetPoint(i, pT_list[ipT], g0_err.Interpolate(eta_list[ieta],pT_list[ipT]))
        if g40_err.Interpolate(eta_list[ieta],pT_list[ipT])>0.:
            IQR_vs_pT1.SetPoint(i, pT_list[ipT], g40_err.Interpolate(eta_list[ieta],pT_list[ipT]))
        i+=1

    R_vs_pT.SetMarkerStyle(24)
    R_vs_pT.SetMarkerColor(ROOT.kRed)
    R_vs_pT.SetLineColor(ROOT.kRed)
    R.Add(R_vs_pT)
    R_vs_pT1.SetMarkerStyle(25)
    R_vs_pT1.SetMarkerColor(ROOT.kBlue)
    R_vs_pT1.SetLineColor(ROOT.kBlue)
    R.Add(R_vs_pT1)

    IQR_vs_pT.SetMarkerStyle(24)
    IQR_vs_pT.SetMarkerColor(ROOT.kRed)
    IQR_vs_pT.SetLineColor(ROOT.kRed)
    IQR.Add(IQR_vs_pT)
    IQR_vs_pT1.SetMarkerStyle(25)
    IQR_vs_pT1.SetMarkerColor(ROOT.kBlue)
    IQR_vs_pT1.SetLineColor(ROOT.kBlue)
    IQR.Add(IQR_vs_pT1)
    #line = ROOT.TGraphErrors()
    #line.SetPoint(0,20.*CosH(eta_list[ieta]),0.1)
    #line.SetPointError(0,0.,0.)
    #line.SetPoint(1,20.*CosH(eta_list[ieta]),0.25)
    #line.SetPointError(1,0.,0.)
    #line.SetLineColor(ROOT.kViolet)
    #line.SetLineWidth(2)
    #line.SetLineStyle(2)
    #line.SetMarkerStyle(1)
    #R.Add(line)
    R.SetTitle(";p_{T} [GeV];E response")
    R.SetMinimum(0.97)
    R.SetMaximum(1.05)
    R.Draw("ALP")
    #R.GetXaxis().SetLimits(18.*CosH(eta_list[ieta]), 75.*CosH(eta_list[ieta]))
    l = ROOT.TLegend(0.75, 0.7, 0.85, 0.8)
    l.AddEntry(R_vs_pT, "mc20")
    l.AddEntry(R_vs_pT1, "mc23")
    #l.AddEntry(line, "pT ~ 20 GeV")
    l.Draw("same")
    ROOT.myText(0.75, 0.65,1, "#eta = "+str(eta_list[ieta]))
    page.nextPad()

    IQR.SetTitle(";p_{T} [GeV];E resolution")
    IQR.SetMinimum(0.)
    IQR.SetMaximum(0.15)
    IQR.Draw("ALP")
    l.Draw("same")
    ROOT.myText(0.75, 0.65,1, "#eta = "+str(eta_list[ieta]))
    page.nextPad()

page.forceSave()
#for x in range(h0.GetXaxis().GetNbins()):
#    R_vs_E = h0.ProjectionY("mu0_R_vs_E"+str(x), x+1, x+1)
#    for i in range(R_vs_E.GetXaxis().GetNbins()):
#        R_vs_E.SetBinError(i+1,g0_err.Interpolate(h0.GetXaxis().GetBinCenter(x+1),h0.GetYaxis().GetBinCenter(i+1)))
#    R_vs_E.SetMarkerStyle(24)
#    R_vs_E.SetLineColor(ROOT.kRed)
#    R_vs_E.Draw()
#    R_vs_E1 = h40.ProjectionY("mu40_R_vs_E"+str(x), x+1, x+1)
#    for i in range(R_vs_E1.GetXaxis().GetNbins()):
#        R_vs_E1.SetBinError(i+1,g40_err.Interpolate(h40.GetXaxis().GetBinCenter(x+1),h40.GetYaxis().GetBinCenter(i+1)))
#    R_vs_E1.SetMarkerStyle(25)
#    R_vs_E1.SetLineColor(ROOT.kBlue)
#    R_vs_E1.Draw("same")
#    line = ROOT.TLine()
#    line.SetLineColor(ROOT.kViolet)
#    line.SetLineWidth(2)
#    line.SetLineStyle(2)
#    line.DrawLine(20*CosH(h0.GetXaxis().GetBinCenter(x)),R_vs_E.GetMinimum(),20*CosH(h0.GetXaxis().GetBinCenter(x)),R_vs_E1.GetMaximum())
#    l = ROOT.TLegend(0.7, 0.7, 0.9, 0.9)
#    l.AddEntry(R_vs_E, "mu_th = 0")
#    l.AddEntry(R_vs_E1, "mu_th = 40")
#    l.AddEntry(line, "pT ~ 20 GeV")
#    l.Draw("same")
#    ROOT.myText(0.25,0.96,1, str(h0.GetXaxis().GetBinLowEdge(x+1))+"<eta<"+str(h0.GetXaxis().GetBinUpEdge(x+1)))
#    page.forceSave()
h_JES_unc.SetName("JESUnc_mc20vsmc23_MC20_PreRec_AntiKt10UFOCSSKSoftDrop")
h_JER_unc.SetName("JERUnc_mc20vsmc23_MC20_PreRec_AntiKt10UFOCSSKSoftDrop")
h_JES_unc.Write()
h_JER_unc.Write()
page.close()

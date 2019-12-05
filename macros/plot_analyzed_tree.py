#Author: Kirsten Randle
#Take histograms and turn into plots

import ROOT
from array import array

dir = '/Users/kirstenrandle/CMS_work/compphysproj/outputs/'
digis_dir = dir + 'digis/'
weights_dir = dir + 'weights/'
infile = dir + 'analyzed_tree.root'

hf = ROOT.TFile.Open(infile)


for i in range(10):
    c = ROOT.TCanvas('c','c',600,800)
    ROOT.gStyle.SetOptStat(0)
    digi = hf.Get('digis_{}'.format(i))
    digi.GetYaxis().SetTitleOffset(1)
    digi.Draw('hist')
    c.SaveAs(digis_dir + 'digis_{}.png'.format(i))
    d = ROOT.TCanvas('d','d',600,800)
    ROOT.gStyle.SetOptStat(0)
    p_digi = hf.Get('pileup_digis_{}'.format(i))
    p_digi.Draw('hist')
    d.SaveAs(digis_dir + 'pileup_digis_{}.png'.format(i))
    e = ROOT.TCanvas('e','e',600,800)
    ROOT.gStyle.SetOptStat(0)
    n_digi = hf.Get('noise_digis_{}'.format(i))
    n_digi.Draw('hist')
    e.SaveAs(digis_dir + 'noise_digis_{}.png'.format(i))
    f = ROOT.TCanvas('f','f',600,800)
    ROOT.gStyle.SetOptStat(0)
    s_digi = hf.Get('signal_digis_{}'.format(i))
    s_digi.Draw('hist')
    f.SaveAs(digis_dir + 'signal_digis_{}.png'.format(i))



digicolors = array('i',[ROOT.kBlack,ROOT.kGreen,ROOT.kMagenta,ROOT.kRed])

c1 = ROOT.TCanvas('c1','c1',600,800)
ROOT.gStyle.SetPalette(4,digicolors)
ROOT.gStyle.SetOptStat(0)
ROOT.gStyle.SetErrorX(0.)

avd = hf.Get('avg_digis')
avsd = hf.Get('avg_signal_digis')
avnd = hf.Get('avg_noise_digis')
avpd = hf.Get('avg_pileup_digis')

avd.GetYaxis().SetTitle('Avg. Amplitude')
avd.GetXaxis().SetTitle('Sample number')

avd.SetMarkerStyle(21)
avnd.SetMarkerStyle(21)
avpd.SetMarkerStyle(21)
avsd.SetMarkerStyle(21)

avd.Draw('eSAME PLC PMC')
avsd.Draw('eSAME PLC PMC')
avnd.Draw('eSAME PLC PMC')
avpd.Draw('eSAME PLC PMC')

avd.GetYaxis().SetRangeUser(-5,40)
l1 = ROOT.TLegend(0.1,0.7,0.3,0.9)
l1.AddEntry(avd)
l1.AddEntry(avsd)
l1.AddEntry(avnd)
l1.AddEntry(avpd)
l1.Draw()
c1.SaveAs(dir + 'avg_digis_all.png')


for i in range(5):
    c = ROOT.TCanvas('c','c',2400,800)
    ROOT.gStyle.SetOptStat(0)
    ROOT.gStyle.SetPalette(ROOT.kBird)
    c.Divide(3,1)
    c.cd(1)
    w1 = hf.Get('w_1_{}'.format(i))
    w1.SetTitleOffset(1)
    w1.Draw('hist')
    c.cd(2)
    w2 = hf.Get('w_2_{}'.format(i))
    w2.SetTitleOffset(1)
    w2.Draw()
    c.cd(3)
    wvs = hf.Get('w_{}_compare'.format(i))
    wvs.GetYaxis().SetTitleOffset(1)
    wvs.Draw('COLZ')
    c.SaveAs(weights_dir + 'w_{}_compare.png'.format(i))

c2 = ROOT.TCanvas('c2','c2',600,800)
ROOT.gStyle.SetPalette(2,digicolors[1:3])
ROOT.gStyle.SetOptStat(0)
ROOT.gStyle.SetErrorX(0.)
avg_w1 = hf.Get('avg_weights_1')
avg_w2 = hf.Get('avg_weights_2')
avg_w1.SetMarkerStyle(21)
avg_w2.SetMarkerStyle(21)
avg_w1.Draw('eSAME PLC PMC')
avg_w2.Draw('eSAME PLC PMC')
avg_w1.GetYaxis().SetRangeUser(-1,1)
l2 = ROOT.TLegend(0.7,0.1,0.9,0.3)
l2.AddEntry(avg_w1)
l2.AddEntry(avg_w2)
l2.Draw()
c2.SaveAs(dir + 'avg_weights.png')

c3 = ROOT.TCanvas('c3','c3',1600,800)
ROOT.gStyle.SetPalette(ROOT.kBird)
ROOT.gStyle.SetOptStat(0)
rA1vrA2 = hf.Get('recoA_2_vs_recoA_1')
rA1vrA2av = hf.Get('recoA_2_vs_recoA_1_1')
c3.Divide(2,1)
c3.cd(1)
rA1vrA2.Draw('COLZ')
c3.cd(2)
rA1vrA2av.Draw()
c3.SaveAs(dir+'recoA_compare.png')

c4 = ROOT.TCanvas('c4','c4',1600,800)
ROOT.gStyle.SetPalette(ROOT.kBird)
ROOT.gStyle.SetOptStat(0)
b1vrA2 = hf.Get('recoA_2_vs_bias_1')
b1vrA2av = hf.Get('recoA_2_vs_bias_1_1')
c4.Divide(2,1)
c4.cd(1)
b1vrA2.Draw('COLZ')
c4.cd(2)
b1vrA2av.Draw()
c4.SaveAs(dir+'recoA_bias_compare.png')

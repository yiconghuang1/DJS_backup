void replace(){
  TFile* f1 = new TFile("replace/AntiKt4EMPFlow_finebins_JES.root","READ");
  TFile* f2 = new TFile("AntiKt4EMPFlow_finebins_JES.root","UPDATE");

  TF1* replacement = (TF1*)f1->Get("R_vs_Enuminv_Func_12");// [3.2, 3.3]7  [-0.8, -0.7]17
  replacement->SetName("R_vs_Enuminv_Func_77");// [-3.3, -3.2]12  [0.7, 0.8]32
  replacement->SetTitle("[0]+[1]*log(x)^1");// |3.2, 3.3| [0]+[1]*log(x)^1+[2]*log(x)^2  |0.7, 0.8| [0]+[1]*log(x)^1+[2]*log(x)^2+[3]*log(x)^3+[4]*log(x)^4
  replacement->Write();
}

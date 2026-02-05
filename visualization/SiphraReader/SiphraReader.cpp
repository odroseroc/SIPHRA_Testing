//C++ libraries
#include <iostream>
#include <fstream>
#include <sstream>

//ROOT libraries
#include <TApplication.h>
#include <TROOT.h>
#include <TH1.h>
#include <TCanvas.h>
#include <TLegend.h>
#include <TPaveStats.h>
#include <unistd.h>
#include <TFile.h>

using namespace std;

int main(int argc, char* argv[]){

  TApplication* TheApp = new TApplication("App", 0, 0);

  cout << endl;
  cout << "********************************" << endl;
  cout << "* Welcome to the SiphraReader! *" << endl;
  cout << "********************************" << endl;

  if(argc < 2){
    cout << endl;
    cout << "Please give valid txt file as argument!" << endl;
    cout << endl;
    return 0;
  }

  if(argc > 2){
    gROOT->SetBatch(kTRUE);
  }

  char* FilePath = argv[1];
  char* FileName = basename(argv[1]);
  
  //Checks for the existance of the two-hit data root file
  if(access(Form("%s", FilePath), F_OK) != 0){
    cout << endl << "Error opening file! Please check target directory!" << endl << endl;
    return 0;
  }

  TCanvas* SpectrumCanvas[16];
  for(int i = 0; i < 16; i++){
    SpectrumCanvas[i] = new TCanvas(Form("Canvas #%i", i+1), Form("Channel #%i", i+1), 50 + 24*i, 50 + 24*i, 640, 480);
    SpectrumCanvas[i]->SetLogy();
  }

  TCanvas* HighestMeanCanvas = new TCanvas("HighestMean", "Highest-mean window", 24*16 + 640 + 100, 0, 640, 480);
  HighestMeanCanvas->SetLogy();

  auto SummedCanvas = new TCanvas("SummedCanvas", "Summed-canvas window", 24*16 + 640 + 100, 510, 640, 480);
  SummedCanvas->SetLogy();
  
  cout << endl << "Processing file " << FileName << "..." << endl;

  ifstream DataFile;
  DataFile.open(Form("%s", FilePath));

  char str[255];
  DataFile.getline(str, 255);  //Skips a line from the header

  [[maybe_unused]] int DataDetector = 0;
  [[maybe_unused]] int DataID = 0;
  [[maybe_unused]] int DataTrigger = 0;
  [[maybe_unused]] int DataTime_sub = 0;
  [[maybe_unused]] int DataTime_sec = 0;
  [[maybe_unused]] int DataTime_gps = 0;
  [[maybe_unused]] int DataTemp = 0;
  int DataChannel[16] = {};
  [[maybe_unused]] int DataArgMax = 0;
  int DataSummed = 0;
  int ManualSum = 0;

  int LinesRead = 0;

  //For reading as CSV
  string DataLine = {};
  stringstream DataStringStream;
  string DataItem;

  TH1F* ChannelSpectrum[16];
  for(int i = 0; i < 16; i++){
    ChannelSpectrum[i] = new TH1F(Form("Channel #%i", i+1), "", 4096, 0, 4095);
    ChannelSpectrum[i]->GetXaxis()->SetTitle("ADC channel number");
    ChannelSpectrum[i]->GetYaxis()->SetTitle("Number of counts");
  }

  auto SummedSpectrum = new TH1F("Summed spectrum", "", 512, 0, 4*4095);
  SummedSpectrum->GetXaxis()->SetTitle("ADC channel number");
  SummedSpectrum->GetYaxis()->SetTitle("Number of counts");

  auto ManualSumSpectrum = new TH1F("Manual sum", "", 512, 0, 4*4095);
  ManualSumSpectrum->GetXaxis()->SetTitle("ADC channel number");
  ManualSumSpectrum->GetYaxis()->SetTitle("Number of counts");

  //Read one line of data from the file
  while (getline(DataFile, DataLine)) {

    if (DataLine.empty()) continue;

    DataStringStream.clear();
    DataStringStream.str(DataLine);

    getline(DataStringStream, DataItem, ',');  DataDetector = atoi(DataItem.c_str());
    getline(DataStringStream, DataItem, ',');  DataID = atoi(DataItem.c_str());
    getline(DataStringStream, DataItem, ',');  DataTrigger = atoi(DataItem.c_str());
    getline(DataStringStream, DataItem, ',');  DataTime_sub = atoi(DataItem.c_str());
    getline(DataStringStream, DataItem, ',');  DataTime_sec = atoi(DataItem.c_str());
    getline(DataStringStream, DataItem, ',');  DataTime_gps = atoi(DataItem.c_str());
    getline(DataStringStream, DataItem, ',');  DataTemp = atoi(DataItem.c_str());

    for(int i = 0; i < 16; i++){
      getline(DataStringStream, DataItem, ',');  DataChannel[i] = atoi(DataItem.c_str());
      ManualSum += DataChannel[i];
    }
    getline(DataStringStream, DataItem, ',');  DataArgMax = atoi(DataItem.c_str());
    getline(DataStringStream, DataItem, ',');  DataSummed = atoi(DataItem.c_str());
    
    //Test print-outs
    // cout << "Detector: " << DataDetector << endl;
    // cout << "ID: " << DataID << endl;
    // cout << "Trigger: " << DataTrigger << endl;
    // cout << "Time_sub: " << DataTime_sub << endl;
    // cout << "Time_sec: " << DataTime_sec << endl;
    // cout << "Time_gps: " << DataTime_gps << endl;
    // cout << "Temp: " << DataTemp << endl;
    // cout << "Channel: ";
    // for(int i = 0; i < 16; i++){
    //   cout << DataChannel[i] << " ";
    // }
    // cout << endl;
    // cout << "ArgMax: " << DataArgMax << endl;
    // cout << "Summed: " << DataSummed << endl;
    // cout << endl;

    for(int i = 0; i < 16; i++){
      ChannelSpectrum[i]->Fill(DataChannel[i]);
    }

    SummedSpectrum->Fill(DataSummed);
    ManualSumSpectrum->Fill(ManualSum);
    ManualSum = 0;

    LinesRead++;

  }

  cout << endl;

  int ChannelWithHighestMean = 0;
  float CurrentChannelMean = 0;
  float HighestMeanFound = 0;

  for(int i = 0; i < 16; i++) {
    SpectrumCanvas[i]->cd();
    ChannelSpectrum[i]->Draw();
    CurrentChannelMean = ChannelSpectrum[i]->GetMean();
    cout << "Mean in channel " << i+1 << " ==> " << CurrentChannelMean << endl;
    if(CurrentChannelMean > HighestMeanFound){
      ChannelWithHighestMean = i;
      HighestMeanFound = CurrentChannelMean;
    }
  }
  cout << endl;

  cout << "Highest mean in channel #" << ChannelWithHighestMean+1 << endl;
  cout << endl;
  HighestMeanCanvas->cd();
  ChannelSpectrum[ChannelWithHighestMean]->Draw();
  auto HighestSpectrumDrawCopy = (TH1F*)ChannelSpectrum[ChannelWithHighestMean]->Clone(Form("Highest channel (#%i)", ChannelWithHighestMean + 1));

  SummedCanvas->cd();
  SummedSpectrum->SetLineColor(kRed);
  ManualSumSpectrum->SetLineColor(kGreen);
  if(SummedSpectrum->GetMaximum() > ManualSumSpectrum->GetMaximum()){
    SummedSpectrum->Draw();
    ManualSumSpectrum->Draw("sames");
  }else{
    ManualSumSpectrum->Draw();
    SummedSpectrum->Draw("sames");
  }
  HighestSpectrumDrawCopy->SetLineColor(kBlue);
  HighestSpectrumDrawCopy->Draw("sames");

  TFile* OutputFile = new TFile("Output.root", "RECREATE");
  //ChannelSpectrum[ChannelWithHighestMean]->Write("Spectrum");
  SummedSpectrum->Write("Spectrum");
  OutputFile->Close();

  auto I_Am_Legend = new TLegend(0.4, 0.59, 0.77, 0.79);
  I_Am_Legend->AddEntry(SummedSpectrum, "SIPHRA sum", "l");
  I_Am_Legend->AddEntry(ManualSumSpectrum, "Manual sum", "l");
  I_Am_Legend->AddEntry(ChannelSpectrum[ChannelWithHighestMean], Form("Highest channel (#%i)", ChannelWithHighestMean + 1), "l");
  I_Am_Legend->Draw();

  SummedCanvas->Update();
  auto StatsPointer = (TPaveStats*)SummedSpectrum->FindObject("stats");
  StatsPointer->SetTextColor(kRed);
  StatsPointer = (TPaveStats*)ManualSumSpectrum->FindObject("stats");
  StatsPointer->SetTextColor(kGreen);
  StatsPointer->SetY1NDC(0.775 - 0.16 -0.0);
  StatsPointer->SetY2NDC(0.935 - 0.16 -0.01);
  StatsPointer = (TPaveStats*)HighestSpectrumDrawCopy->FindObject("stats");
  StatsPointer->SetTextColor(kBlue);
  StatsPointer->SetY1NDC(0.775 - 2*0.16 -0.01);
  StatsPointer->SetY2NDC(0.935 - 2*0.16 -0.01);
  SummedCanvas->Modified();
  SummedCanvas->Update();

  cout << "Lines read: " << LinesRead << endl;
  cout << endl;

  if(argc < 3){
    TheApp->Run();
  }

  return 0;

}

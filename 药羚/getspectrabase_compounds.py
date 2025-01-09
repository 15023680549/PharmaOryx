import requests
import csv
import time


headers={'user-agent':'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko)' 'Chrome/102.0.5005.63 Safari/537.36',
          "Cookie":"osano_consentmanager_uuid=9b30a25a-fd43-47b5-b8b7-127f3bb4c0d3; s_fid=1CDCCA569B928EBB-2DD392B44A321EE7; s_cc=true; _fbp=fb.1.1653978299711.688121172; osano_consentmanager=-lvHCuRbZbLdqzn-ni9G9gDdUBo28N5vIFZ-ouUQAnfTkBtDHOv3YySWMW2XprjUip-F8IroT-btzfbytFZwDRPd6-Q76bQAqtnJQygd6jT7-NdtZGBqd3ZKgkn6hviS6C_AYYLpLz3HrqyzXTVRueKT4DG7gj3in3GPUwr9VmdksSVgzl9yvk6q_erAX4B6zesWJFpwr4Yx3v_DEvf0DacASASq_WDiTCGy13qqD-g4fUMQOpLEVRJc9ObRFAa6NtAKQlzByUXbAVyzNFKVB0EM27MzAIGe8ZWovA==; auth_token=eyJhbGciOiJSUzI1NiIsInR5cCI6IkpXVCIsImtpZCI6Ik4wRkdRemhHUkRoQk56TkROa0l3TmpjMVJUSTFOelpHTlRrNE1EZzBOMFZCUlRVME1USXdOQSJ9.eyJodHRwczovL3NwZWN0cmFiYXNlLmNvbS9uYW1lIjoiWW9uZyBKaWFuZyIsImdpdmVuX25hbWUiOiJZb25nIiwiZmFtaWx5X25hbWUiOiJKaWFuZyIsIm5pY2tuYW1lIjoiankxNTAyMzY4MDU0OSIsIm5hbWUiOiJZb25nIEppYW5nIiwicGljdHVyZSI6Imh0dHBzOi8vbGgzLmdvb2dsZXVzZXJjb250ZW50LmNvbS9hLS9BT2gxNEdqOE9BWVdPMVZTNjdDTk1FOTJOcnlpNzlwOVMtb2lvOVNPN0VtbD1zOTYtYyIsImxvY2FsZSI6InpoLUNOIiwidXBkYXRlZF9hdCI6IjIwMjItMDYtMjFUMDM6MjE6NTEuNzE3WiIsImlzcyI6Imh0dHBzOi8vc3BlY3RyYWJhc2UuYXV0aDAuY29tLyIsInN1YiI6Imdvb2dsZS1vYXV0aDJ8MTE1MTM3MTUxMjU1NjIyNjM1MDk5IiwiYXVkIjoiZ25CZzU1MDNzbnlOZm9DbUx0aTZkdXM3WEhneWVubTAiLCJpYXQiOjE2NTU3ODE3MTIsImV4cCI6MTY1NTgxNzcxMiwiYXRfaGFzaCI6IkNrT2NQdHF6MzFMdEMtUkRKLTZYNHciLCJub25jZSI6In5VS1Q2N0guOWNhT1hYZzFUTXJDbFRyemU2UEd-TGguIn0.y6olQmu_yVU0GgEdLWTrXK5TVHAH0PCWhoSgBgTSwZvuLzNIhaRzseCQd4p_HzuFnjz2iqlMh0jwGHLO-jjxAOI7HVblMA_VDmZsCno7O_nirvpPIfJpJ87nEf1qsAlWscPdVTuARJhVfvgDInxyhZSxEUMeAE_Wc0jVPPLe88gN_FOSV4TeHAGHeBAVby42s649nhV_i8bQctCvoB-3IxUnA1qs1yzzS709BYBj9IJzt8Ge7X1v6ViLrQ4JyExNKiphaU-W3Bb_ySzH3GI9qBTkoaFdmAtTR-yX9ByzeQ1bcAN6OjLy4jDvFYalu_JTlSNQkgpYmcrT8sEb9JAh9g; access_token=eyJhbGciOiJkaXIiLCJlbmMiOiJBMjU2R0NNIiwiaXNzIjoiaHR0cHM6Ly9zcGVjdHJhYmFzZS5hdXRoMC5jb20vIn0..kp9qvYXtDbOztM-Z.WUyws2aooRzVUSElM2HyNvKmihBTaqeM_CesuYe6PXAEpS-WMiSocY1y156Tqgm-Zf5ACyGgY5_PmM4SaKnwZ_Z8ZS6hoAk3cPyV2SYuFFKesMznsr_Gv4NwGZmFsEu74rHh0v6qY_1yR5g5KHZ-NmWOPk9aPOhde_eMkP1lwzFxuSe5l69Fh3geGqnlnG8XuzqzINyBhb2sOq_YWcwCdL2g1A4_7FwYueRJqQRZdQyrf7sA9ITVLyohEsBLAW7v4hmbufbjPsfvMoIDpClmWNpfaktERhkFnUtFB17aXCw_xaUlT0gS-Z0.XYvakKwO56USLWa_kZDCFQ; s_sq=%5B%5BB%5D%5D"
}
compounds = []

def save_compounds(rows):
    with open('C:\\Users\\PharmaOryx-YJ\\PycharmProjects\\PharmaOryx\\Spectra\\compounds.txt','a+',encoding='utf-8_sig') as f:
        f_csv=csv.writer(f)
        f_csv.writerows(rows)

def analyzeJSON(data):
    compounds=[]
    for compound in data["compounds"]:
        compounds.append([compound["compoundID"]])
    save_compounds(compounds)

def get_spectra_home(url):
    response = requests.get(url, headers=headers,timeout=(60,30))
    # html = response.text
    # data = json.loads(html)
    data=response.json()
    url = 'https://spectrabase.com/api/compoundlist?token=' + data["next"]
    print(url)
    analyzeJSON(data)

if __name__ == '__main__':
    url = 'https://spectrabase.com/api/compoundlist'
    get_spectra_home(url)
    while 1:
        get_spectra_home(url)
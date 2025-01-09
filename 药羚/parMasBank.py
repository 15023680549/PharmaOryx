import json
import csv
import os
import re

str="""{
	"compound": [{
		"inchi": "InChI=1S/C10H9ClN4O2S/c11-9-5-13-6-10(14-9)15-18(16,17)8-3-1-7(12)2-4-8/h1-6H,12H2,(H,14,15)",
		"inchiKey": "QKLPUVXBJHRFQZ-UHFFFAOYSA-N",
		"metaData": [{
			"category": "none",
			"computed": false,
			"hidden": false,
			"name": "molecular formula",
			"value": "C10H9ClN4O2S"
		}, {
			"category": "none",
			"computed": false,
			"hidden": false,
			"name": "SMILES",
			"value": "c1cc(ccc1N)S(=O)(=O)Nc2cncc(n2)Cl"
		}, {
			"category": "external id",
			"computed": false,
			"hidden": false,
			"name": "cas",
			"value": "102-65-8"
		}, {
			"category": "external id",
			"computed": false,
			"hidden": false,
			"name": "pubchem cid",
			"value": 66890
		}, {
			"category": "external id",
			"computed": false,
			"hidden": false,
			"name": "chemspider",
			"value": 60252
		}, {
			"category": "none",
			"computed": false,
			"hidden": false,
			"name": "InChI",
			"value": "InChI=1S/C10H9ClN4O2S/c11-9-5-13-6-10(14-9)15-18(16,17)8-3-1-7(12)2-4-8/h1-6H,12H2,(H,14,15)"
		}, {
			"category": "none",
			"computed": false,
			"hidden": false,
			"name": "InChIKey",
			"value": "QKLPUVXBJHRFQZ-UHFFFAOYSA-N"
		}, {
			"category": "computed",
			"computed": true,
			"hidden": false,
			"name": "molecular formula",
			"value": "C10H9ClN4O2S"
		}, {
			"category": "computed",
			"computed": true,
			"hidden": false,
			"name": "total exact mass",
			"value": 284.013474208
		}, {
			"category": "computed",
			"computed": true,
			"hidden": false,
			"name": "SMILES",
			"value": "O=S(=O)(N=C1C=NC=C(Cl)N1)C2=CC=C(N)C=C2"
		}],
		"molFile": "\n  CDK     02062201032D\n\n 18 19  0  0  0  0  0  0  0  0999 V2000\n   -7.7956    1.5023    0.0000 C   0  0  0  0  0  0  0  0  0  0  0  0\n   -6.4963    3.7527    0.0000 C   0  0  0  0  0  0  0  0  0  0  0  0\n   -6.4963    0.7510    0.0000 C   0  0  0  0  0  0  0  0  0  0  0  0\n   -5.1970    3.0015    0.0000 C   0  0  0  0  0  0  0  0  0  0  0  0\n    1.3000   -0.7500    0.0000 C   0  0  0  0  0  0  0  0  0  0  0  0\n   -1.3000   -0.7500    0.0000 C   0  0  0  0  0  0  0  0  0  0  0  0\n   -7.7956    3.0031    0.0000 C   0  0  0  0  0  0  0  0  0  0  0  0\n   -5.1970    1.5006    0.0000 C   0  0  0  0  0  0  0  0  0  0  0  0\n    1.3000    0.7500    0.0000 C   0  0  0  0  0  0  0  0  0  0  0  0\n   -1.3000    0.7500    0.0000 C   0  0  0  0  0  0  0  0  0  0  0  0\n    2.5989    1.5002    0.0000 Cl  0  0  0  0  0  0  0  0  0  0  0  0\n   -9.0945    3.7533    0.0000 N   0  0  0  0  0  0  0  0  0  0  0  0\n    0.0000   -1.5000    0.0000 N   0  0  0  0  0  0  0  0  0  0  0  0\n    0.0000    1.5000    0.0000 N   0  0  0  0  0  0  0  0  0  0  0  0\n   -2.5989    1.5002    0.0000 N   0  0  0  0  0  0  0  0  0  0  0  0\n   -4.8624   -0.3985    0.0000 O   0  0  0  0  0  0  0  0  0  0  0  0\n   -2.9341   -0.3988    0.0000 O   0  0  0  0  0  0  0  0  0  0  0  0\n   -3.8981    0.7504    0.0000 S   0  0  0  0  0  0  0  0  0  0  0  0\n  3  1  1  0  0  0  0 \n  4  2  2  0  0  0  0 \n  7  1  2  0  0  0  0 \n  7  2  1  0  0  0  0 \n  8  3  2  0  0  0  0 \n  8  4  1  0  0  0  0 \n  9  5  2  0  0  0  0 \n 10  6  1  0  0  0  0 \n 11  9  1  0  0  0  0 \n 12  7  1  0  0  0  0 \n 13  5  1  0  0  0  0 \n 13  6  2  0  0  0  0 \n 14  9  1  0  0  0  0 \n 14 10  1  0  0  0  0 \n 15 10  2  0  0  0  0 \n 18  8  1  0  0  0  0 \n 18 15  1  4  0  0  0 \n 18 16  2  0  0  0  0 \n 18 17  2  0  0  0  0 \nM  END\n",
		"names": [{
			"computed": false,
			"name": "Sulfaclozine",
			"score": 0.0
		}, {
			"computed": false,
			"name": "4-amino-N-(6-chloropyrazin-2-yl)benzenesulfonamide",
			"score": 0.0
		}],
		"tags": [],
		"computed": false,
		"kind": "biological",
		"classification": [{
			"category": "classification",
			"computed": true,
			"hidden": false,
			"name": "kingdom",
			"value": "Organic compounds"
		}, {
			"category": "classification",
			"computed": true,
			"hidden": false,
			"name": "superclass",
			"value": "Benzenoids"
		}, {
			"category": "classification",
			"computed": true,
			"hidden": false,
			"name": "class",
			"value": "Benzene and substituted derivatives"
		}, {
			"category": "classification",
			"computed": true,
			"hidden": false,
			"name": "subclass",
			"value": "Benzenesulfonamides"
		}, {
			"category": "classification",
			"computed": true,
			"hidden": false,
			"name": "direct parent",
			"value": "Aminobenzenesulfonamides"
		}, {
			"category": "classification",
			"computed": true,
			"hidden": false,
			"name": "alternative parent",
			"value": "Benzenesulfonyl compounds"
		}, {
			"category": "classification",
			"computed": true,
			"hidden": false,
			"name": "alternative parent",
			"value": "Aniline and substituted anilines"
		}, {
			"category": "classification",
			"computed": true,
			"hidden": false,
			"name": "alternative parent",
			"value": "Pyrazines"
		}, {
			"category": "classification",
			"computed": true,
			"hidden": false,
			"name": "alternative parent",
			"value": "Organosulfonamides"
		}, {
			"category": "classification",
			"computed": true,
			"hidden": false,
			"name": "alternative parent",
			"value": "Imidolactams"
		}, {
			"category": "classification",
			"computed": true,
			"hidden": false,
			"name": "alternative parent",
			"value": "Aryl chlorides"
		}, {
			"category": "classification",
			"computed": true,
			"hidden": false,
			"name": "alternative parent",
			"value": "Heteroaromatic compounds"
		}, {
			"category": "classification",
			"computed": true,
			"hidden": false,
			"name": "alternative parent",
			"value": "Aminosulfonyl compounds"
		}, {
			"category": "classification",
			"computed": true,
			"hidden": false,
			"name": "alternative parent",
			"value": "Azacyclic compounds"
		}, {
			"category": "classification",
			"computed": true,
			"hidden": false,
			"name": "alternative parent",
			"value": "Primary amines"
		}, {
			"category": "classification",
			"computed": true,
			"hidden": false,
			"name": "alternative parent",
			"value": "Organopnictogen compounds"
		}, {
			"category": "classification",
			"computed": true,
			"hidden": false,
			"name": "alternative parent",
			"value": "Organochlorides"
		}, {
			"category": "classification",
			"computed": true,
			"hidden": false,
			"name": "alternative parent",
			"value": "Organic oxides"
		}, {
			"category": "classification",
			"computed": true,
			"hidden": false,
			"name": "alternative parent",
			"value": "Hydrocarbon derivatives"
		}]
	}],
	"id": "AU100601",
	"dateCreated": 1487110669411,
	"lastUpdated": 1644109388406,
	"lastCurated": 1644109387517,
	"metaData": [{
		"category": "none",
		"computed": false,
		"hidden": false,
		"name": "accession",
		"value": "AU100601"
	}, {
		"category": "none",
		"computed": false,
		"hidden": false,
		"name": "date",
		"value": "2015.07.05"
	}, {
		"category": "none",
		"computed": false,
		"hidden": false,
		"name": "author",
		"value": "Nikiforos Alygizakis, Anna Bletsou, Nikolaos Thomaidis, University of Athens"
	}, {
		"category": "none",
		"computed": false,
		"hidden": false,
		"name": "license",
		"value": "CC BY"
	}, {
		"category": "none",
		"computed": false,
		"hidden": false,
		"name": "copyright",
		"value": "Copyright (C) 2015 Department of Chemistry, University of Athens"
	}, {
		"category": "none",
		"computed": false,
		"hidden": false,
		"name": "comment",
		"value": "CONFIDENCE standard compound"
	}, {
		"category": "none",
		"computed": false,
		"hidden": false,
		"name": "comment",
		"value": "INTERNAL_ID 1006"
	}, {
		"category": "none",
		"computed": false,
		"hidden": false,
		"name": "exact mass",
		"value": 284.0135
	}, {
		"category": "none",
		"computed": false,
		"hidden": false,
		"name": "instrument",
		"value": "Bruker maXis Impact"
	}, {
		"category": "none",
		"computed": false,
		"hidden": false,
		"name": "instrument type",
		"value": "LC-ESI-QTOF"
	}, {
		"category": "mass spectrometry",
		"computed": false,
		"hidden": false,
		"name": "ms level",
		"value": "MS2"
	}, {
		"category": "mass spectrometry",
		"computed": false,
		"hidden": false,
		"name": "ionization",
		"value": "ESI"
	}, {
		"category": "mass spectrometry",
		"computed": false,
		"hidden": false,
		"name": "fragmentation mode",
		"value": "CID"
	}, {
		"category": "mass spectrometry",
		"computed": false,
		"hidden": false,
		"name": "collision energy",
		"value": "Ramp 21.1-31.6 eV"
	}, {
		"category": "mass spectrometry",
		"computed": false,
		"hidden": false,
		"name": "resolution",
		"value": 35000
	}, {
		"category": "chromatography",
		"computed": false,
		"hidden": false,
		"name": "column",
		"value": "Acclaim RSLC C18 2.2um, 2.1x100mm, Thermo"
	}, {
		"category": "chromatography",
		"computed": false,
		"hidden": false,
		"name": "flow gradient",
		"value": "99/1 at 0-1 min, 61/39 at 3 min, 0.1/99.9 at 14-16 min, 99/1 at 16.1-20 min"
	}, {
		"category": "chromatography",
		"computed": false,
		"hidden": false,
		"name": "flow rate",
		"value": "200 uL/min at 0-3 min, 400 uL/min at 14 min, 480 uL/min at 16-19 min, 200 uL/min at 19.1-20 min"
	}, {
		"category": "chromatography",
		"computed": false,
		"hidden": false,
		"name": "retention time",
		"value": "4.6 min"
	}, {
		"category": "chromatography",
		"computed": false,
		"hidden": false,
		"name": "SOLVENT A",
		"value": "water with 0.01% formic acid and 5mM ammonium formate"
	}, {
		"category": "chromatography",
		"computed": false,
		"hidden": false,
		"name": "SOLVENT B",
		"value": "90:10 methanol:water with 0.01% formic acid and 5mM ammonium formate"
	}, {
		"category": "data processing",
		"computed": false,
		"hidden": false,
		"name": "recalibrate",
		"value": "identity on assigned fragments and MS1"
	}, {
		"category": "data processing",
		"computed": false,
		"hidden": false,
		"name": "reanalyze",
		"value": "Peaks with additional N2/O included"
	}, {
		"category": "data processing",
		"computed": false,
		"hidden": false,
		"name": "whole",
		"value": "RMassBank 1.8.1"
	}, {
		"category": "mass spectrometry",
		"computed": false,
		"hidden": false,
		"name": "ionization mode",
		"value": "positive"
	}, {
		"category": "computed",
		"computed": true,
		"hidden": false,
		"name": "spectral entropy",
		"value": 1.8445828247531482
	}, {
		"category": "computed",
		"computed": true,
		"hidden": false,
		"name": "normalized entropy",
		"value": 0.5596705479508176
	}, {
		"category": "focused ion",
		"computed": false,
		"hidden": false,
		"name": "precursor m/z",
		"value": 285.0208
	}, {
		"category": "focused ion",
		"computed": false,
		"hidden": false,
		"name": "precursor type",
		"value": "[M+H]+"
	}, {
		"category": "mass spectrometry",
		"computed": true,
		"hidden": false,
		"name": "mass accuracy",
		"unit": "ppm",
		"value": 0.17469602228006656
	}, {
		"category": "mass spectrometry",
		"computed": true,
		"hidden": false,
		"name": "mass error",
		"unit": "Da",
		"value": 4.9792000027082395E-5
	}],
	"annotations": [{
		"category": "annotation",
		"computed": false,
		"hidden": false,
		"name": "C4H5+",
		"value": 53.0389
	}, {
		"category": "annotation",
		"computed": false,
		"hidden": false,
		"name": "C3H4N+",
		"value": 54.0333
	}, {
		"category": "annotation",
		"computed": false,
		"hidden": false,
		"name": "C3H3O+",
		"value": 55.0178
	}, {
		"category": "annotation",
		"computed": false,
		"hidden": false,
		"name": "CH6N3+",
		"value": 60.0552
	}, {
		"category": "annotation",
		"computed": false,
		"hidden": false,
		"name": "C5H5+",
		"value": 65.0382
	}, {
		"category": "annotation",
		"computed": false,
		"hidden": false,
		"name": "H6N2O2+",
		"value": 66.0423
	}, {
		"category": "annotation",
		"computed": false,
		"hidden": false,
		"name": "C4H6N+",
		"value": 68.049
	}, {
		"category": "annotation",
		"computed": false,
		"hidden": false,
		"name": "C5H4N+",
		"value": 78.0333
	}, {
		"category": "annotation",
		"computed": false,
		"hidden": false,
		"name": "C5H3O+",
		"value": 79.0177
	}, {
		"category": "annotation",
		"computed": false,
		"hidden": false,
		"name": "C6H6N+",
		"value": 92.0498
	}, {
		"category": "annotation",
		"computed": false,
		"hidden": false,
		"name": "CH7N3O2+",
		"value": 93.0532
	}, {
		"category": "annotation",
		"computed": false,
		"hidden": false,
		"name": "C5H6NO+",
		"value": 96.0443
	}, {
		"category": "annotation",
		"computed": false,
		"hidden": false,
		"name": "CH8N4S+",
		"value": 108.0457
	}, {
		"category": "annotation",
		"computed": false,
		"hidden": false,
		"name": "C4H5N4+",
		"value": 109.0483
	}, {
		"category": "annotation",
		"computed": false,
		"hidden": false,
		"name": "C6H8NO+",
		"value": 110.0609
	}, {
		"category": "annotation",
		"computed": false,
		"hidden": false,
		"name": "C6H6N3+",
		"value": 120.0562
	}, {
		"category": "annotation",
		"computed": false,
		"hidden": false,
		"name": "C4H5ClN3+",
		"value": 130.0172
	}, {
		"category": "annotation",
		"computed": false,
		"hidden": false,
		"name": "CH9ClN2OS+",
		"value": 132.0138
	}, {
		"category": "annotation",
		"computed": false,
		"hidden": false,
		"name": "C3H9ClN2OS+",
		"value": 156.0118
	}, {
		"category": "annotation",
		"computed": false,
		"hidden": false,
		"name": "C7HN4O+",
		"value": 157.015
	}, {
		"category": "annotation",
		"computed": false,
		"hidden": false,
		"name": "C9H4NS+",
		"value": 158.008
	}, {
		"category": "annotation",
		"computed": false,
		"hidden": false,
		"name": "C9H6N2S+",
		"value": 174.0228
	}, {
		"category": "annotation",
		"computed": false,
		"hidden": false,
		"name": "C10H8N4+",
		"value": 184.0757
	}, {
		"category": "annotation",
		"computed": false,
		"hidden": false,
		"name": "C4H3ClN3O2S+",
		"value": 191.9647
	}, {
		"category": "annotation",
		"computed": false,
		"hidden": false,
		"name": "C10H8ClN4+",
		"value": 219.0438
	}, {
		"category": "annotation",
		"computed": false,
		"hidden": false,
		"name": "C10H10ClN4O2S+",
		"value": 285.0221
	}, {
		"category": "annotation",
		"computed": false,
		"hidden": false,
		"name": "C9H10ClN5O2S+",
		"value": 287.0184
	}],
	"score": {
		"impacts": [{
			"value": 2.0,
			"reason": "Valid molecular structure(s) provided for biological compound"
		}, {
			"value": 1.0,
			"reason": "Chromatography identified as LC-MS"
		}, {
			"value": 1.0,
			"reason": "Ionization mode/type provided"
		}, {
			"value": 1.0,
			"reason": "MS type/level identified"
		}, {
			"value": 1.0,
			"reason": "Instrument information provided"
		}, {
			"value": 1.0,
			"reason": "Collision energy provided"
		}, {
			"value": 1.0,
			"reason": "Retention time/index provided"
		}, {
			"value": 1.0,
			"reason": "Column information provided"
		}, {
			"value": 1.0,
			"reason": "Precursor type provided"
		}, {
			"value": 1.0,
			"reason": "Precursor m/z provided"
		}, {
			"value": 1.0,
			"reason": "Precursor information and provided compound validated"
		}, {
			"value": 2.0,
			"reason": "High mass accuracy of 0.175 ppm"
		}],
		"score": 5.0
	},
	"spectrum": "53.0389:0.594951 54.0333:0.566811 55.0178:0.522592 60.0552:0.542692 65.0382:3.822962 66.0423:0.506512 68.049:7.963499 78.0333:0.727609 79.0177:1.057244 92.0498:7.702203 93.0532:0.731629 96.0443:0.623091 108.0457:12.172375 109.0483:1.181862 110.0609:4.904325 120.0562:3.095353 130.0172:5.656054 132.0138:1.515517 156.0118:100.000000 157.015:8.884065 158.008:3.891301 174.0228:0.751729 184.0757:0.619071 191.9647:0.590931 219.0438:0.723589 285.0221:3.694324 287.0184:0.840167",
	"splash": {
		"block1": "splash10",
		"block2": "0a4i",
		"block3": "1900000000",
		"block4": "d2bc1c887f6f99ed0f74",
		"splash": "splash10-0a4i-1900000000-d2bc1c887f6f99ed0f74"
	},
	"submitter": {
		"id": "MassBank-AU",
		"emailAddress": "massbank@massbank.eu",
		"firstName": "Nikolaos",
		"lastName": "Thomaidis",
		"institution": "University of Athens"
	},
	"tags": [{
		"ruleBased": false,
		"text": "MassBank"
	}, {
		"ruleBased": true,
		"text": "LC-MS"
	}],
	"library": {
		"library": "MassBank",
		"description": "MassBank High Quality Mass Spectral Database",
		"link": "https://massbank.eu/MassBank/RecordDisplay.jsp?id=AU100601",
		"tag": {
			"ruleBased": false,
			"text": "MassBank"
		}
	}
}"""


compound = {"id":"","molecular formula":"","SMILES":"","cas":"","pubchem cid":"","chemspider":"","names":"","dateCreated":"","lastUpdated":"","lastCurated":"","spectrum":"","tags":""}
dir=os.getcwd()
#保存图谱数据
def save_compound(compounds):
    with open('C:\\Users\\PharmaOryx-YJ\\Desktop\\data\\MassBank\\compounds.csv', 'a+', encoding='utf-8_sig') as f:
        csv_output = csv.writer(f)
        csv_output.writerows(compounds)

def save_molfile(id,molfile):
    with open('C:\\Users\\PharmaOryx-YJ\\Desktop\\data\\MassBank\\molfile\\'+id+'.mol', 'w', encoding='utf-8_sig') as f:
        f.write(molfile)


#读取整个json文件 注意：文件1.8g
def redJson():
    json=''
    line=1
    with open("C:\\Users\\PharmaOryx-YJ\\Desktop\\data\\MassBank\\MoNA-export-All_Spectra.json",'r',encoding='utf-8_sig') as f:
        str=f.readline()[1:]
        if '}}},' in str:
            str=str.replace('}}},','}}}')
            return json
        json = json + str
        line+=1


def parMasBankJson(str):
    compounds = []
    js = json.loads(str, strict=False)
    comp = js["compound"][0]

    id = js["id"]
    compound["id"] = id
    compound["dateCreated"] = js["dateCreated"]
    compound["lastUpdated"] = js["lastUpdated"]
    compound["lastCurated"] = js["lastCurated"]
    compound["spectrum"] = js["spectrum"]

    names = ''
    for cmd in comp["names"]:
        names = cmd["name"] + ',' + names
    compound["names"] = names

    # compound metaData
    for me in comp["metaData"]:
        if me["category"] != 'category':
            compound[me["name"]] = me["value"]
    # tags
    for tag in js["tags"]:
        if tag["ruleBased"] == bool('True'):
            compound["tags"] = tag["text"]

    compounds.append(
        [compound["id"], compound["InChI"], compound["InChIKey"], compound["molecular formula"], compound["SMILES"],
         compound["cas"], compound["pubchem cid"], compound["chemspider"], compound["names"], compound["dateCreated"],
         compound["lastUpdated"], compound["lastCurated"], compound["tags"], compound["spectrum"]])

    # molFile
    molFile = comp["molFile"]
    # 保存摩尔文件
    save_molfile(id, molFile)
    # 保存物质基本信息和图谱坐标
    save_compound(compounds)

    print(id)


if __name__ == '__main__':
    #redJson()
    str=''
    with open("C:\\Users\\PharmaOryx-YJ\\Desktop\\data\\MassBank\\MoNA-export-All_Spectra.json",'r',encoding='utf-8_sig') as f:
        next(f)
        try:
            while True:
                line_data = f.readline()
                if line_data:
                    if '}}},' in line_data:
                        line_data=line_data.replace('}}},','}}}')
                        str=str+line_data
                        parMasBankJson(str)  # 把读取的一行的json数据加载出来
                        str=''
                    else:
                        str=str+line_data
                else:
                    break
        except Exception as e:
            print(e)
            f.close()



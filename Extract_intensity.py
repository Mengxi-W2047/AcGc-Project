#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# Author: WMX
# Date: 20220419

from os import listdir
from tkinter.filedialog import askdirectory

# extract 292 & 308 intensity, return intensity lists and title lists
def get_intensity_list(original_mgf):
    k = 0
    list_292 = []
    list_308 = []
    list_292_title = []
    list_308_title = []
    intensity_292 = 0
    intensity_308 = 0

    with open(original_mgf, "r") as input_file:
        lines = input_file.read().splitlines()
        while k < len(lines) - 1:
            k += 1
            if lines[k].startswith("TITLE="):
                title = lines[k].split("TITLE=")[1]
                while lines[k - 1] != "END IONS":
                    if lines[k].startswith("292."):
                        fragment = float(lines[k].split()[0])
                        if abs(fragment - 292.104) <= 0.005:
                            intensity_292 = float(lines[k].split()[1])
                            list_292.append(intensity_292)
                            list_292_title.append(title)
                    elif lines[k].startswith("308."):
                        fragment = float(lines[k].split()[0])
                        if abs(fragment - 308.098) <= 0.005:
                            intensity_308 = float(lines[k].split()[1])
                            list_308.append(intensity_308)
                            list_308_title.append(title)
                    else:
                        pass
                    k += 1
    return list_292, list_308, list_292_title, list_308_title

# select the mgf folder path here,this script will automatically seclect all the mgf files and extract intensities of NeuAc and NeuGc. The result will be exported in the same folder
print('Please select the folder of your mgf files.')
mgf_fold_path = askdirectory()
file_list = listdir(mgf_fold_path + "/")
print("Processing...")

file_292 = open(mgf_fold_path + "/" + 'NeuAc292_intensities.txt', mode='w')
file_308 = open(mgf_fold_path + "/" + 'NeuGc308_intensities.txt', mode='w')

file_292.write('Title\tNeuAc Intensity\n')
file_308.write('Title\tNeuGc Intensity\n')

for file in file_list:
    if ".mgf" in file:
        list_292, list_308, list_292_title, list_308_title = get_intensity_list(mgf_fold_path + "/" + file)

        for i in range(len(list_292)):
            file_292.write(str(list_292_title[i]) + '\t' + str(list_292[i]) + '\n')
        for j in range(len(list_308)):
            file_308.write(str(list_308_title[j]) + '\t' + str(list_308[j]) + '\n')

file_292.close()
file_308.close()
print("Finish! The results are stored in: ")
print("\t" + mgf_fold_path + "/" + 'NeuAc292_intensities.txt')
print("\t" + mgf_fold_path + "/" + 'NeuAc308_intensities.txt')
input("Press any key to exit.")



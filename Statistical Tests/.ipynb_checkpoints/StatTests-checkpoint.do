** Finding Summary Stat of Data at the end of the year 1397

* Importing Data
clear all
import delimited "C:\Users\Mahdi\OneDrive\Master Thesis\Data\data_owenership97_blnc98.csv", encoding(UTF-8) colrange(2) numericcols(12) clear

******  Spearman Rank Test  **********
* Checking assumption 2
// graph matrix largest_owner first_second first_sumtwofour sumfive gini herfindhal sscl ssco ssdl ssdo bzcl bzco bzdl, half

spearman largest_owner first_second first_sumtwofour sumfive gini herfindhal sscl ssco ssdl ssdo bzcl bzco bzdl, stats(rho obs p) star(0.05) pw matrix

matrix A = r(Rho)

esttab matrix(A, fmt(%5.2f)) using Sperman_Test.rtf, unstack not noobs compress replace

******  Wilcoxon Test  **********

signrank first_second = largest_owner, exact


******  PCA Analysis  **********
// pca largest_owner first_second first_sumtwofour sumfive gini herfindhal sscl ssco ssdl ssdo bzcl bzco bzdl
//
// screeplot


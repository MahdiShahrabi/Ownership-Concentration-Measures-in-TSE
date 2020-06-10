** Finding Summary Stat of Data at the end of the year 1397

* Importing Data
clear all
import delimited "C:\Users\Mahdi\OneDrive\Master Thesis\Data\data_owenership97_blnc98.csv", encoding(UTF-8) colrange(2) numericcols(12) clear

******  Spearman Rank Test  **********
* Checking assumption 2
// graph matrix largest_owner first_second first_sumtwofour sumfive gini herfindhal sscl ssco ssdl ssdo bzcl bzco bzdl, half

// spearman largest_owner first_second first_sumtwofour sumfive gini herfindhal sscl ssco ssdl ssdo bzcl bzco bzdl, stats(rho obs p) star(0.05) pw matrix
//
// matrix A = r(Rho)

// esttab matrix(A, fmt(%5.2f)) using Sperman_Test.rtf, unstack not noobs compress replace

******  Wilcoxon Test  **********
* The main version is done is python
signrank first_second = largest_owner, exact


******  PCA Analysis  **********
pca largest_owner first_second first_sumtwofour sumfive gini herfindhal sscl ssco ssdl ssdo bzcl bzco bzdl, comp(3) blanks(0.1)

screeplot, yline(1)

* Test to see if is reasonable to run a PCA
estat kmo

* Orthogonal Rotation
rotate ,varimax blanks(0.2)
// rotate, promax(5) oblique blanks(0.1)
** Finding Summary Stat of Data at the end of the year 1397

* Importing Data
clear all
import delimited "C:\Users\Mahdi\OneDrive\Master Thesis\Data\Measures1398.csv", encoding(UTF-8) colrange(2) numericcols(12 13) 

* Plotting H
histogram largest_owner, percent ytitle(Percent of Obersevations) xtitle(Percent of Ownership) title(Distribution of Largest Owner Size)
graph export largest_owner.png, replace

histogram first_second, percent ytitle(Percent of Obersevations) xtitle(Ratio) title(Distribution of First/Second)
graph export first_second.png, replace

histogram first_sumtwofour, percent ytitle(Percent of Obersevations) xtitle(Ratio) title(Distribution of First/Sum(2-4))
graph export first_sumtwofour.png, replace

histogram sumfive, percent ytitle(Percent of Obersevations) xtitle(Percent of Ownership) title(Distribution of Sumfive)
graph export sumfive.png, replace


***

histogram herfindhal, percent ytitle(Percent of Obersevations) xtitle(Index) title(Distribution of Herfindahl Index)
graph export herfindhal.png, replace

histogram gini, percent ytitle(Percent of Obersevations) xtitle(Index) title(Distribution of Gini Index)
graph export gini.png, replace

***

histogram sscl, percent ytitle(Percent of Obersevations) xtitle(Index) title(Distribution of Shapley-Shubik Index) subtitle(Concentrated and Largest Player)
graph export sscl.png, replace

histogram ssco, percent ytitle(Percent of Obersevations) xtitle(Index) title(Distribution of Shapley-Shubik Index) subtitle(Concentrated and Oceanic Players)
graph export ssco.png, replace

histogram ssdl, percent ytitle(Percent of Obersevations) xtitle(Index) title(Distribution of Shapley-Shubik Index) subtitle(Dispersed and Largest Player)
graph export ssdl.png, replace

histogram ssdo, percent ytitle(Percent of Obersevations) xtitle(Index) title(Distribution of Shapley-Shubik Index) subtitle(Dispersed and Oceanic Players)
graph export ssdo.png, replace

***

histogram bzcl, percent ytitle(Percent of Obersevations) xtitle(Index) title(Distribution of Banzhaf Index) subtitle(Concentrated and Largest Player)
graph export bzcl.png, replace

histogram bzco, percent ytitle(Percent of Obersevations) xtitle(Index) title(Distribution of Banzhaf Index) subtitle(Concentrated and Oceanic Players)
graph export bzco.png, replace

histogram bzdl, percent ytitle(Percent of Obersevations) xtitle(Index) title(Distribution of Banzhaf Index) subtitle(Dispersed and Largest Player)
graph export bzdl.png, replace
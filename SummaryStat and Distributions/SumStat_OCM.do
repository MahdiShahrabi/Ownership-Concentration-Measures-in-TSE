** Finding Summary Stat for OCM
* The end of the year 1398

* Importing Data
clear all
import delimited "C:\Users\Mahdi\OneDrive\Master Thesis\Data\Measures1399.csv", encoding(UTF-8) clear 

* Dropping Unused variables
drop v1

* Summary stat for firms
estpost summarize num_holders sum_over1 marketcap
eststo firms

* Summary stat for One
estpost summarize largest_owner sumfive  first_second first_sumtwofour 
eststo One

* Summary stat for Two
estpost summarize gini herfindhal
eststo Two


* Summary stat for Three
estpost summarize sscl ssco ssdl ssdo bzcl bzco bzdl
eststo Three


* Latex output
esttab firms One Two Three using OSM_Stat.tex, cells("mean sd min p25 p50 p75 max") compress varlabels(`e(labels)') collabels("Mean" "S.D." "Min" "Max") label title("Summary statistics at Bidder Level")  nonum noobs replace
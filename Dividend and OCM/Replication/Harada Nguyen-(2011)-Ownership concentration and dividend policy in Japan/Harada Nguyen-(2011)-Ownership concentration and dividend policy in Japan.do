clear
cls

*** Written By Mahdi Shahrabi in July, 2020 ***

** Loading Data 
import delimited "C:\Users\Mahdi\OneDrive\Master Thesis\Codes\Dividend and OCM\Data.csv", case(preserve) encoding(UTF-8) numericcols(18) clear 


** Global Variables
global yFE `"i.year"'
global indFE `"i.industry_id"'

global OCM `"largest_owner first_second first_sumtwofour sumfive herfindahl gini sscl ssco ssdl ssdo bzcl bzco bzdl"'

global saving_dir `"C:\Users\Mahdi\OneDrive\Master Thesis\Codes\Dividend and OCM\Replication\Harada Nguyen-(2011)-Ownership concentration and dividend policy in Japan\StataTex"'

*******************************************************************************
*********     The paper "Kimie Harada, Pascal Nguyen, (2011),        **********
*********    Ownership concentration and dividend policy in Japan,   **********
*********      Managerial Finance, Vol. 37 Iss: 4 pp. 362 - 379"     **********
*******************************************************************************

*************************            Table I          *************************

eststo T1: quietly estpost sum DIVTOI DIVTNI DIVTEQ DIVTMVE LNTA ROA ROE DLOSS NPLOSS Q DEBT sumfive LHH

cd "$saving_dir"
esttab T1 using Table_I_Japan.tex, cells("mean(pattern(1 0 0) fmt(3)) std(pattern(0 1 0) fmt(3)) min max") collabels("Mean" "Sd. dev." "Minimum" "Maximum") booktabs nonumber nogaps prehead(`"\begin{table}[htbp]\centering"' `"\def\sym#1{\ifmmode^{#1}\else\(^{#1}\)\fi}"' `"\caption{Replicated Table(I)}"' `"\footnotesize"' `"\begin{tabular}{l*{1}{cccc}}"') postfoot(`"\end{tabular}"' `"\end{table}"') replace

*************************           Table II         **************************
global ocm "LHH"
global var_list `"$ocm herfindahl DIVTOI DIVTNI DIVTEQ DIVTMVE LNTA ROA ROE DLOSS NPLOSS Q DEBT DPAY"'

quietly summarize $ocm, detail
global var_median = r(p50)
gen above_median = cond($ocm>$var_median,1,0)

eststo low: quietly estpost summarize $var_list if above_median == 0
eststo high: quietly estpost summarize $var_list if above_median == 1
eststo diff: quietly estpost ttest $var_list, by(above_median) unequal

cd "$saving_dir" 
esttab low high diff using Table_II_Japan.tex, cells("mean(pattern(1 0 0) fmt(3)) mean(pattern(0 1 0) fmt(3)) b(star pattern(0 0 1) fmt(3)) t(pattern(0 0 1) par fmt(3))") collabels("Low" "High" "Diff" "t-stat") booktabs nonumber nogaps prehead(`"\begin{table}[htbp]\centering"' `"\def\sym#1{\ifmmode^{#1}\else\(^{#1}\)\fi}"' `"\caption{Replicated Table(II)}"' `"\begin{tabular}{l*{3}{cccc}}"') postfoot(`"\end{tabular}"' `"\end{table}"') replace

*************************           Table III         *************************
global ocm "sumfive"
global control_var_list `"LNTA ROA DLOSS LNQ DEBT $ocm"'

** OLS
quietly reg DIVTOI $control_var_list $yFE, vce(cluster firm)
eststo linear1

** Tobit
quietly tobit DIVTEQ $control_var_list $yFE, ll(0) vce(bootstrap, cluster(firm) dots(1))
eststo tobit1

global ocm "herfindahl"
global control_var_list `"LNTA ROA DLOSS LNQ DEBT $ocm"'
** OLS
quietly reg DIVTOI $control_var_list $yFE, vce(cluster firm)
eststo linear2

** Tobit
quietly tobit DIVTEQ $control_var_list $yFE, ll(0) vce(bootstrap, cluster(firm) dots(1))
eststo tobit2

cd "$saving_dir" 
esttab linear1 linear2 tobit1 tobit2 using Table_III_Japan.tex, drop(*year) booktabs nonumber nogaps replace
// eststo clear
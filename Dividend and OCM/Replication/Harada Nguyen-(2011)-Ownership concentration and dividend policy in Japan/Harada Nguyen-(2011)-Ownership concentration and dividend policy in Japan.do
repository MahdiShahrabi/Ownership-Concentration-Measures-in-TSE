clear
cls

*** Written By Mahdi Shahrabi in July, 2020 ***

** Loading Data 
import delimited "C:\Users\Mahdi\OneDrive\Master Thesis\Codes\Dividend and OCM\Data.csv", case(preserve) encoding(UTF-8) numericcols(18) clear 

** Global Variables
global yFE `"i.year"'
global indFE `"i.industry_id"'

** Logit Regressions
* Probability of paying dividend
global ocm_logit largest_owner
global control_var_list_logit `"$ocm_logit ROA MTB LNTA tot_lib"'

quietly logit DPAY $control_var_list_logit $yFE $indFE
eststo logit
esttab logit, drop(*year *industry_id)
eststo clear


*******************************************************************************
*********     The paper "Kimie Harada, Pascal Nguyen, (2011),        **********
*********    Ownership concentration and dividend policy in Japan,   **********
*********      Managerial Finance, Vol. 37 Iss: 4 pp. 362 - 379"     **********
*******************************************************************************

*************************            Table I          *************************
global OCM `"largest_owner first_second first_sumtwofour sumfive herfindahl gini sscl ssco ssdl ssdo bzcl bzco bzdl"'
sum DIVTOI DIVTNI DIVTEQ LNTA ROA ROE DLOSS NPLOSS Q DEBT $OCM

*************************           Table II         **************************
global ocm "LHH"
global var_list_II `"$ocm herfindahl DIVTOI DIVTNI DIVTEQ LNTA ROA ROE DLOSS NPLOSS Q DEBT DPAY"'

quietly summarize $ocm, detail
global var_median = r(p50)
gen above_median = cond($ocm>$var_median,1,0)

eststo low: quietly estpost summarize $var_list_II if above_median == 0
eststo high: quietly estpost summarize $var_list_II if above_median == 1
eststo diff: quietly estpost ttest $var_list_II, by(above_median) unequal
esttab low high diff, cells("mean(pattern(1 0 0) fmt(3)) mean(pattern(0 1 0) fmt(3)) b(star pattern(0 0 1) fmt(3)) t(pattern(0 0 1) par fmt(3))") collabels("Low" "High" "Diff" "t-stat")

*************************           Table III         *************************
global ocm "sumfive"
global control_var_list `"$ocm LNTA ROA DLOSS LNQ DEBT"'

** OLS
quietly reg DIVTOI $control_var_list $yFE, vce(cluster firm)
eststo linear1

** Tobit
quietly tobit DIVTEQ $control_var_list $yFE, ll(0) vce(bootstrap, cluster(firm) dots(1))
eststo tobit1

global ocm "herfindahl"
global control_var_list `"$ocm LNTA ROA DLOSS LNQ DEBT"'
** OLS
quietly reg DIVTOI $control_var_list $yFE, vce(cluster firm)
eststo linear2

** Tobit
quietly tobit DIVTEQ $control_var_list $yFE, ll(0) vce(bootstrap, cluster(firm) dots(1))
eststo tobit2

esttab linear1 linear2 tobit1 tobit2, drop(*year)
eststo clear
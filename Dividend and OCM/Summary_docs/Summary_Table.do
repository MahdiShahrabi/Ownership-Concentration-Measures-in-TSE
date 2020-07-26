clear
cls

*** Written By Mahdi Shahrabi in July, 2020 ***

** Loading Data 
import delimited "C:\Users\Mahdi\OneDrive\Master Thesis\Codes\Dividend and OCM\Data.csv", case(preserve) encoding(UTF-8) numericcols(18) clear 

** globals
global OCM `"largest_owner first_second first_sumtwofour sumfive herfindahl gini sscl ssco ssdl ssdo bzcl bzco bzdl"'

global control `"tot_asset tot_lib ppe book_value marketcap capital equity revenue cost_of_revenue gross_profit net_income operating_cash_flow end_cash_position dividend payout "'

global derivatives `"DIVTOI DIVTNI DIVTEQ DIVTS ROA ROE DLOSS NPLOSS MTB LHH LEVRG"'

*************************       Table I          *************************
cd "C:\Users\Mahdi\OneDrive\Master Thesis\Codes\Dividend and OCM\Summary_docs\StataTex"
keep if year<=1397 & year>=1388

est clear
sort year
by year: eststo: quietly estpost summarize $OCM
eststo Tot: quietly estpost summarize $OCM
esttab _all using Teble_summary_I.tex, cells(mean(fmt(2)) sd(par)) mtitle("1388" "1389" "1390" "1391" "1392" "1393" "1394" "1395" "1396" " 1397" "Tot") title("Summary of Ownership Concentration Measures") b(%9.3f) collabels(none) compress nonumber booktabs replace 


esttab Tot using Teble_summary_I_detail.tex, cells("mean(fmt(2) label(Mean)) sd(fmt(2) label(Std. dev.)) min(fmt(2) label(Minimum)) max(fmt(2) label(Maximum))") title("Summary of Ownership Concentration Measures (Detailed)") b(%9.3f) booktabs nonumber replace


*************************         Table II         *************************
cd "C:\Users\Mahdi\OneDrive\Master Thesis\Codes\Dividend and OCM\Summary_docs\StataTex"
keep if year<=1397 & year>=1388
foreach v of varlist tot_asset tot_lib ppe book_value marketcap capital equity revenue cost_of_revenue gross_profit net_income operating_cash_flow end_cash_position dividend {
replace `v' = `v'/1e4
}
est clear
sort year
by year: eststo: quietly estpost summarize $control
eststo Tot: quietly estpost summarize $control
esttab _all using Teble_summary_II.tex, cells(mean(fmt(1)) sd(par fmt(1))) mtitle("1388" "1389" "1390" "1391" "1392" "1393" "1394" "1395" "1396" " 1397") title("Summary of Control Variables") b(%3.3f) collabels(none) booktabs nonumber nogaps modelwidth(3) prehead(`"\begin{table}[htbp]\centering"' `"\def\sym#1{\ifmmode^{#1}\else\(^{#1}\)\fi}"' `"\caption{Summary of Contorl Variables}"' `"\footnotesize"' `"\begin{tabular}{l*{11}{c}}"') replace 

esttab Tot using Teble_summary_II_detail.tex, cells("mean(fmt(2) label(Mean)) sd(fmt(2) label(Std. dev.)) min(fmt(2) label(Minimum)) max(fmt(2) label(Maximum))") title("Summary of Control Variables (Detailed)") b(%9.3f) booktabs nonumber replace


*************************       Table III         *************************
cd "C:\Users\Mahdi\OneDrive\Master Thesis\Codes\Dividend and OCM\Summary_docs\StataTex"
keep if year<=1397 & year>=1388
est clear
sort year
by year: eststo: quietly estpost summarize $derivatives
eststo Tot: quietly estpost summarize $derivatives

esttab _all using Teble_summary_III.tex, cells(mean(fmt(3)) sd(par fmt(3))) mtitle("1388" "1389" "1390" "1391" "1392" "1393" "1394" "1395" "1396" " 1397" "Tot") title("Summary of Derivedd variables") b(%3.3f) collabels(none) nonumber booktabs ///
prehead(`"\begin{table}[htbp]\centering"' `"\def\sym#1{\ifmmode^{#1}\else\(^{#1}\)\fi}"' `"\caption{Summary of Derived variables}"' `"\small"' `"\begin{tabular}{l*{11}{c}}"') replace 


esttab Tot using Teble_summary_III_detail.tex, cells("mean(fmt(2) label(Mean)) sd(fmt(2) label(Std. dev.)) min(fmt(2) label(Minimum)) max(fmt(2) label(Maximum))") title("Summary of Derived variables (Detailed)") b(%9.3f) booktabs nonumber replace


*************************        Missings         *************************
mdesc $OCM
mdesc $control
mdesc $derivatives
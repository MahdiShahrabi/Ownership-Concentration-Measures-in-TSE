clear
cls

*** Written By Mahdi Shahrabi in July, 2020 ***

** Loading Data 
import delimited "C:\Users\Mahdi\OneDrive\Master Thesis\Codes\Dividend and OCM\Data.csv", case(preserve) encoding(UTF-8) numericcols(21) clear 

** globals
global OCM `"sum_over1 sumfive sumfour sumthree sumtwo largest_owner first_second first_sumtwofour herfindahl gini sscl ssco ssdl ssdo bzcl bzco bzdl"'

global control `"tot_asset tot_lib ppe book_value marketcap capital equity revenue cost_of_revenue gross_profit net_income operating_cash_flow end_cash_position dividend payout "'

global derivatives `"DIVTOI DIVTEQ DIVTS ROA ROE DLOSS NPLOSS MTB LHH LEVRG"'
global start_year 1390
global end_year 1397

*************************       Table I          *************************
cd "C:\Users\Mahdi\OneDrive\Master Thesis\Codes\Dividend and OCM\Vars, OCM, Summary Through Time\StataTex"
keep if year<=$end_year & year>=$start_year

est clear
sort year
by year: eststo: quietly estpost summarize $OCM , detail
eststo Tot: quietly estpost summarize $OCM , detail
esttab _all using Teble_variablesTime_I.tex, cells(p50(fmt(2)) sd(par)) mtitle("1390" "1391" "1392" "1393" "1394" "1395" "1396" " 1397" "Tot") title("Summary of Ownership Concentration Measures") b(%9.3f) collabels(none) compress nonumber booktabs prehead(`"\begin{table}[htbp]\centering"' `"\def\sym#1{\ifmmode^{#1}\else\(^{#1}\)\fi}"' `"\caption{Summary of Ownership Concentration Measures}"' `"\footnotesize"' `"\begin{tabular}{l*{11}{c}}"' `"\toprule"') replace 



*************************         Table II         *************************
cd "C:\Users\Mahdi\OneDrive\Master Thesis\Codes\Dividend and OCM\Vars, OCM, Summary Through Time\StataTex"
keep if year<=$end_year & year>=$start_year
foreach v of varlist tot_asset tot_lib ppe book_value marketcap capital equity revenue cost_of_revenue gross_profit net_income operating_cash_flow end_cash_position dividend {
replace `v' = `v'/1e4
}
est clear
sort year
by year: eststo: quietly estpost summarize $control , detail
eststo Tot: quietly estpost summarize $control , detail
esttab _all using Teble_variablesTime_II.tex, cells(p50(fmt(2)) sd(par fmt(1))) mtitle("1390" "1391" "1392" "1393" "1394" "1395" "1396" " 1397") title("Summary of Control Variables") b(%3.3f) collabels(none) booktabs nonumber nogaps modelwidth(3) prehead(`"\begin{table}[htbp]\centering"' `"\def\sym#1{\ifmmode^{#1}\else\(^{#1}\)\fi}"' `"\caption{Summary of Contorl Variables}"' `"\footnotesize"' `"\begin{tabular}{l*{11}{c}}"') replace 



*************************       Table III         *************************
cd "C:\Users\Mahdi\OneDrive\Master Thesis\Codes\Dividend and OCM\Vars, OCM, Summary Through Time\StataTex"
keep if year<=$end_year & year>=$start_year
est clear
sort year
by year: eststo: quietly estpost summarize $derivatives , detail
eststo Tot: quietly estpost summarize $derivatives , detail

esttab _all using Teble_variablesTime_III.tex, cells(p50(fmt(3)) sd(par fmt(3))) mtitle("1390" "1391" "1392" "1393" "1394" "1395" "1396" " 1397" "Tot") title("Summary of Derivedd variables") b(%3.4f) collabels(none) nonumber booktabs ///
prehead(`"\begin{table}[htbp]\centering"' `"\def\sym#1{\ifmmode^{#1}\else\(^{#1}\)\fi}"' `"\caption{Summary of Derived variables}"' `"\small"' `"\begin{tabular}{l*{11}{c}}"') replace 



*************************        Missings         *************************
mdesc $OCM
mdesc $control
mdesc $derivatives
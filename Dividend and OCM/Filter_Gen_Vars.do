clear
cls

*** Written By Mahdi Shahrabi in July, 2020 ***

** Loading Data 
import delimited "C:\Users\Mahdi\OneDrive\Master Thesis\Data\Merged_Data_July.csv", encoding(UTF-8) colrange(2) numericcols(18) clear 

** Creating variabls
gen DIVTOI = dividend /operating_income 
gen DIVTNI = dividend /net_income 
gen DIVTEQ = dividend /equity
gen DIVTS  = dividend/revenue
gen DPAY   = cond(dividend>0,1,0)

gen ROA    = operating_income/tot_asset
gen ROE    = operating_income/equity
gen DLOSS  = cond(operating_income<0,1,0)
gen NPLOSS = cond(net_income<0,1,0)
gen MTB    = marketcap/book_value 
gen LHH    = log(herfindahl)
gen LEVRG  = tot_lib/tot_asset

** Creating labels
foreach v of varlist _all{
label variabl `v' "`v'"
}


** Exporting Data
cd "C:\Users\Mahdi\OneDrive\Master Thesis\Codes\Dividend and OCM"
export delimited using "Data", replace
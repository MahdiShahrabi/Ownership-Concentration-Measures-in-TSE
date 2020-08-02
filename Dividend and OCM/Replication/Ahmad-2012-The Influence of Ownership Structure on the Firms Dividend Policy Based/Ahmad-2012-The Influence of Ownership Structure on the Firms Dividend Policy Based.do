clear
cls

*** Written By Mahdi Shahrabi in August, 2020 ***

** Loading Data 
import delimited "C:\Users\Mahdi\OneDrive\Master Thesis\Codes\Dividend and OCM\Data.csv", case(preserve) encoding(UTF-8) numericcols(18) clear 


** Global Variables
global yFE `"i.year"'
global indFE `"i.industry_id"'

global OCM `"largest_owner first_second first_sumtwofour sumfive herfindahl gini sscl ssco ssdl ssdo bzcl bzco bzdl"'

global saving_dir `"C:\Users\Mahdi\OneDrive\Master Thesis\Codes\Dividend and OCM\Replication\Ahmad-2012-The Influence of Ownership Structure on the Firms Dividend Policy Based\StataTex"'

*******************************************************************************
*********            The paper "Ahmad, Roslan, (2012),               **********
********* The Influence of Ownership Structure on the Firms Dividend **********
*********   Policy Based, International Review of Business Research  **********
*********   Papers,  Vol. 8. No.6. September 2012. Pp. 71 – 88"      **********
*******************************************************************************

* Setting the panel data and summaries
sort id_tse year
xtset id_tse year
// xtdescribe
// xtsum id_tse year 

* Generating First lags
gen Ldividend = l1.dividend
gen L2dividend = l2.dividend
gen Ddividend = d.dividend

gen Lnet_income = l1.net_income
gen Dnet_income = d.net_income

local OCM largest_owner first_second first_sumtwofour sumfive herfindahl gini sscl ssco ssdl ssdo bzcl bzco bzdl

matrix OUT = J(13,4,.)
matrix OUT_std = J(13,4,.)

***************************         FAM             ****************************

gen conc_Dinc = .


local ocm_index 0	
foreach ocm of local OCM{	
	local ocm_index = `ocm_index'+1	
	replace conc_Dinc = Dnet_income*`ocm'
	
	quietly reg Ddividend Dnet_income conc_Dinc LNTA
// 	quietly xtabond Ddividend Dnet_income conc_Dinc LNTA
	mat coef = e(b)
	mat OUT[`ocm_index',1] = coef[1,"conc_Dinc"]
		
	local t = _b["conc_Dinc"]/_se["conc_Dinc"]
	local p =2*ttail(e(df_r),abs(`t'))
		
	mat OUT_std[`ocm_index',1] = `p'	
}


***************************         PAM             ****************************
gen conc_inc = .
local ocm_index 0	
foreach ocm of local OCM{	
	local ocm_index = `ocm_index'+1	
	replace conc_inc = net_income*`ocm'
	
	quietly reg Ddividend net_income conc_inc Ldividend LNTA
	mat coef = e(b)
	mat OUT[`ocm_index',2] = coef[1,"conc_inc"]
		
	local t = _b["conc_inc"]/_se["conc_inc"]
	local p =2*ttail(e(df_r),abs(`t'))
		
	mat OUT_std[`ocm_index',2] = `p'	
}

***************************            WM           ****************************
replace conc_inc = .
local ocm_index 0	
foreach ocm of local OCM{	
	local ocm_index = `ocm_index'+1	
	replace conc_inc = net_income*`ocm'
	
	quietly reg Ddividend net_income conc_inc Ldividend L2dividend LNTA
	mat coef = e(b)
	mat OUT[`ocm_index',3] = coef[1,"conc_inc"]
		
	local t = _b["conc_inc"]/_se["conc_inc"]
	local p =2*ttail(e(df_r),abs(`t'))
		
	mat OUT_std[`ocm_index',3] = `p'	
}

***************************           ETM           ****************************
gen conc_Linc = .
local ocm_index 0	
foreach ocm of local OCM{	
	local ocm_index = `ocm_index'+1	
	replace conc_Linc = Lnet_income*`ocm'
	
	quietly reg Ddividend net_income Lnet_income conc_Linc Ldividend LNTA
	mat coef = e(b)
	mat OUT[`ocm_index',4] = coef[1,"conc_Linc"]
		
	local t = _b["conc_Linc"]/_se["conc_Linc"]
	local p =2*ttail(e(df_r),abs(`t'))
		
	mat OUT_std[`ocm_index',4] = `p'	
}


*************************         Saving             **************************
mat colnames OUT = FAM PAM EW ETM
mat rownames OUT = $OCM

mat colnames OUT_std = FAM PAM EW ETM
mat rownames OUT_std = $OCM

putexcel set "${saving_dir}\Coefs.xlsx", sheet("Coef") replace
putexcel A1=matrix(OUT), names

putexcel set "${saving_dir}\Coefs.xlsx", sheet("p_val") modify
putexcel A1=matrix(OUT_std), names
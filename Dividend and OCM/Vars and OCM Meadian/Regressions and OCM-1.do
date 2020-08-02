clear
cls

*** Written By Mahdi Shahrabi in August, 2020 ***

** Loading Data 
import delimited "C:\Users\Mahdi\OneDrive\Master Thesis\Codes\Dividend and OCM\Data.csv", case(preserve) encoding(UTF-8) numericcols(18) clear 


** Global Variables
global yFE `"i.year"'
global indFE `"i.industry_id"'


*******************************************************************************
*********  Based on The paper "Kimie Harada, Pascal Nguyen, (2011),  **********
*********    Ownership concentration and dividend policy in Japan,   **********
*********      Managerial Finance, Vol. 37 Iss: 4 pp. 362 - 379"     **********
*******************************************************************************

local Vars DIVTOI DIVTNI DIVTS
local OCM largest_owner first_second first_sumtwofour sumfive herfindahl gini sscl ssco ssdl ssdo bzcl bzco bzdl

matrix OUT = J(13,3,.)
matrix OUT_std = J(13,3,.)

local var_index 0

foreach var of local Vars {
	local var_index = `var_index'+1
	local ocm_index 0
	
	foreach ocm of local OCM{	
		local ocm_index = `ocm_index'+1	
		quietly reg `var' LNTA ROA DLOSS LNQ DEBT `ocm' $yFE, vce(cluster id_tse)
		mat coef = e(b)
		mat OUT[`ocm_index',`var_index'] = coef[1,"`ocm'"]
		
		local t = _b[`ocm']/_se[`ocm']
		local p =2*ttail(e(df_r),abs(`t'))
		
		mat OUT_std[`ocm_index',`var_index'] = `p'
	
	}
}

putexcel set "C:\Users\Mahdi\OneDrive\Master Thesis\Codes\Dividend and OCM\Vars and OCM Meadian\Coefs.xlsx", sheet("Coef") replace
putexcel A1=matrix(OUT)

putexcel set "C:\Users\Mahdi\OneDrive\Master Thesis\Codes\Dividend and OCM\Vars and OCM Meadian\Coefs.xlsx", sheet("p_val") modify
putexcel A1=matrix(OUT_std)

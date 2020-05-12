** Finding Summary Stat of Data at the end of the year 1397

* Importing Data
clear all
import delimited "C:\Users\Mahdi\OneDrive\Proposal\Short Version - April 2020\Stata\Shareholder97.csv", case(upper) encoding(UTF-8) 

drop V1 CHNK_ID FILL_FLAG_HOLDER FILL_FLAG_PRICE  MONTH  DAY YEAR TRUE_DATE  HIGH LAST LOW OPEN VOLUME CLOSE UNADJUSTED_CLOSE

* Number of symbol and holder
codebook SYMBOL 
codebook SHAREHOLDER

estpost summarize PERCENT
eststo all

preserve
collapse (first) ID_TSE MARKETCAP SHARES INDUSTRY (count) holder_numb = ID_TSE (mean) avg_prc=PERCENT avg_quant=QUANTITY (max) max_prc=PERCENT (min) min_prc=PERCENT ,by(SYMBOL)
estpost summarize MARKETCAP SHARES holder_numb avg_prc avg_quant max_prc min_prc
eststo firms
restore

preserve
collapse (count) symbol_numb = ID_TSE,by(SHAREHOLDER)
estpost summarize symbol_numb
eststo holders
restore


esttab all firms holders using Table.tex, cells("mean sd min max") compress varlabels(`e(labels)') collabels("Mean" "S.D." "Min" "Max") label title("Summary statistics at Bidder Level")  nonum noobs replace
* Encoding: UTF-8.
NEW FILE. 
DATASET NAME DataSet1 WINDOW=FRONT. 
 
GET DATA 
  /TYPE=XLSX 
  /FILE='/Users/Edite/processed.xlsx' 
  /SHEET=name 'Sheet1' 
  /CELLRANGE=FULL 
  /READNAMES=ON 
  /LEADINGSPACES IGNORE=YES 
  /TRAILINGSPACES IGNORE=YES 
  /DATATYPEMIN PERCENTAGE=95.0 
  /HIDDEN IGNORE=YES. 
EXECUTE. 

REGRESSION 
  /MISSING LISTWISE 
  /STATISTICS COEFF OUTS R ANOVA 
  /CRITERIA=PIN(.05) POUT(.10) 
  /NOORIGIN 
  /DEPENDENT prices 
  /METHOD=ENTER closest_train_station closest_school beds__1 beds_2_3 beds__4 
    property_type__detached property_type__flat property_type__semi_detached baths__2 
  /SCATTERPLOT=(*ZRESID ,*ZPRED) 
  /RESIDUALS HISTOGRAM(ZRESID) NORMPROB(ZRESID).

CORRELATIONS 
  /VARIABLES=prices closest_train_station closest_school beds__1 beds_2_3 beds__4 
    property_type__detached property_type__flat property_type__semi_detached baths__2 
  /PRINT=TWOTAIL NOSIG 
  /MISSING=PAIRWISE.

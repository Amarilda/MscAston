﻿* Encoding: UTF-8.
GET DATA 
  /TYPE=XLSX 
  /FILE='/Users/Edite/Portfolio-Task-1-Data_Fresco.xlsx' 
  /SHEET=name 'Sheet1' 
  /CELLRANGE=RANGE 'A1:K751' 
  /READNAMES=ON 
  /LEADINGSPACES IGNORE=YES 
  /TRAILINGSPACES IGNORE=YES 
  /DATATYPEMIN PERCENTAGE=95.0 
  /HIDDEN IGNORE=YES. 
EXECUTE. 
DATASET NAME DataSet1 WINDOW=FRONT.

ADD VALUE LABELS
BasketGroup
1 "low"
2 "medium"
3 "high"
EXECUTE. 

ADD VALUE LABELS
Sex
0 "Female"
1 "Male"
EXECUTE. 

ADD VALUE LABELS
Shops
1 "Convenient Stores"
2 "Superstore"
3 "Online"
EXECUTE. 

DATASET DECLARE D0.1843707483476843.
PROXIMITIES   ValueProducts BrandProducts TopFrescoProducts Age 
  /MATRIX OUT(D0.1843707483476843) 
  /VIEW=CASE 
  /MEASURE=EUCLID 
  /PRINT NONE 
  /ID=BasketGroup 
  /STANDARDIZE=VARIABLE RESCALE.

CLUSTER 
  /MATRIX IN(D0.1843707483476843) 
  /METHOD SINGLE 
  /ID=BasketGroup 
  /PRINT SCHEDULE 
  /PRINT DISTANCE 
  /PLOT DENDROGRAM HICICLE.

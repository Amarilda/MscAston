* Encoding: UTF-8.
GET DATA 
  /TYPE=XLSX 
  /FILE='/Users/Edite/Portfolio-Task-1-Data_Fresco_20201019.xlsx' 
  /SHEET=name 'Sheet1' 
  /CELLRANGE=RANGE 'A1:H751' 
  /READNAMES=ON 
  /LEADINGSPACES IGNORE=YES 
  /TRAILINGSPACES IGNORE=YES 
  /DATATYPEMIN PERCENTAGE=95.0 
  /HIDDEN IGNORE=YES. 
EXECUTE. 

IF  (ShoppingBasket <25) BasketGroup=1. 
EXECUTE. 
IF  (ShoppingBasket >25  & ShoppingBasket <75) BasketGroup=2. 
EXECUTE. 
IF  (ShoppingBasket >75) BasketGroup=3. 
EXECUTE. 

IF  (Gender = "Female" ) Sex=0. 
EXECUTE. 
IF  (Gender = "Male") Sex=1.  
EXECUTE. 

IF  (StoreType = "Convenient Stores") Shops=1.  
EXECUTE. 
IF  (StoreType = "Superstore") Shops=2.  
EXECUTE. 
IF  (StoreType = "Online") Shops=3.  
EXECUTE. 

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

FREQUENCIES VARIABLES=BasketGroup
  /ORDER=ANALYSIS.

* Custom Tables. 
CTABLES 
  /VLABELS VARIABLES=BasketGroup ShoppingBasket DISPLAY=LABEL 
  /TABLE BY BasketGroup [C] > ShoppingBasket [S][MINIMUM, MAXIMUM ] 
  /CATEGORIES VARIABLES=BasketGroup ORDER=A KEY=VALUE EMPTY=EXCLUDE 
  /CRITERIA CILEVEL=95.

COMPUTE ValueProducts=ValueProducts+1. 
EXECUTE.

COMPUTE BrandProducts=BrandProducts+1. 
EXECUTE.

COMPUTE TopFrescoProducts=TopFrescoProducts+1. 
EXECUTE.

DESCRIPTIVES VARIABLES=ValueProducts BrandProducts TopFrescoProducts 
  /STATISTICS=MEAN STDDEV MIN MAX.

COMPUTE lnAge=LN(Age). 
EXECUTE. 
COMPUTE lnBrand=LN(BrandProducts). 
EXECUTE.
COMPUTE lnTop=LN(TopFrescoProducts). 
EXECUTE.
COMPUTE lnValue=LN(ValueProducts). 
EXECUTE.

NOMREG BasketGroup (BASE=1 ORDER=ASCENDING)  BY StoreType Gender WITH ValueProducts BrandProducts TopFrescoProducts Age
    lnAge lnValue lnBrand lnTop  
  /CRITERIA CIN(95) DELTA(0) MXITER(100) MXSTEP(5) CHKSEP(20) LCONVERGE(0) PCONVERGE(0.000001) 
    SINGULAR(0.00000001) 
  /MODEL=ValueProducts*lnValue BrandProducts*lnBrand TopFrescoProducts*lnTop lnAge*Age 
  /STEPWISE=PIN(.05) POUT(0.1) MINEFFECT(0) RULE(SINGLE) ENTRYMETHOD(LR) REMOVALMETHOD(LR) 
  /INTERCEPT=INCLUDE 
  /PRINT=PARAMETER SUMMARY LRT CPS STEP MFI.

REGRESSION 
  /MISSING LISTWISE 
  /STATISTICS COEFF OUTS R ANOVA COLLIN TOL 
  /CRITERIA=PIN(.05) POUT(.10) 
  /NOORIGIN 
  /DEPENDENT BasketGroup 
  /METHOD=ENTER Shops Sex ValueProducts BrandProducts TopFrescoProducts Age
  /RESIDUALS DURBIN 
  /CASEWISE PLOT(ZRESID) OUTLIERS(3).


LOGISTIC REGRESSION VARIABLES BasketGroup 
  /METHOD=ENTER Sex Shops 
  /CONTRAST (Shops)=Indicator 
  /CONTRAST (Sex)=Indicator 
  /SAVE=COOK DFBETA ZRESID 
  /CRITERIA=PIN(.05) POUT(.10) ITERATE(20) CUT(.5).

 USE ALL. 
COMPUTE filter_$=(BasketGroup =1 OR BasketGroup =2). 
VARIABLE LABELS filter_$ 'BasketGroup >1 (FILTER)'. 
VALUE LABELS filter_$ 0 'Not Selected' 1 'Selected'. 
FORMATS filter_$ (f1.0). 
FILTER BY filter_$. 
EXECUTE.

 USE ALL. 
COMPUTE filter_$=(BasketGroup =1 OR BasketGroup =3). 
VARIABLE LABELS filter_$ 'BasketGroup >1 (FILTER)'. 
VALUE LABELS filter_$ 0 'Not Selected' 1 'Selected'. 
FORMATS filter_$ (f1.0). 
FILTER BY filter_$. 
EXECUTE.

*Logistic regressions fo=r residuals.
LOGISTIC REGRESSION VARIABLES BasketGroup 
  /METHOD=ENTER Sex Shops 
  /CONTRAST (Sex)=Indicator 
  /CONTRAST (Shops)=Indicator 
  /SAVE=COOK DFBETA ZRESID 
  /CRITERIA=PIN(0.05) POUT(0.10) ITERATE(20) CUT(0.5).

COMPUTE ZRE_1=ABS(ZRE_1). 
EXECUTE.
IF  (ZRE_1 >2) ZRE=1. 
EXECUTE. 
*Summary statistics of normalised residuals.
DESCRIPTIVES VARIABLES=ZRE_1 COO_1 DFB0_1 DFB1_1 DFB2_1 DFB3_1 ZRE
  /STATISTICS=MEAN STDDEV MIN MAX.


COMPUTE ZRE_2=ABS(ZRE_2). 
EXECUTE.
IF  (ZRE_2 >2) ZRE2=1. 
EXECUTE. 
*Summary statistics of normalised residuals.
DESCRIPTIVES VARIABLES=ZRE_2 COO_2 DFB0_2 DFB1_2 DFB2_2 DFB3_2 ZRE2
  /STATISTICS=MEAN STDDEV MIN MAX.

GRAPH 
  /SCATTERPLOT(MATRIX)=ShoppingBasket ValueProducts BrandProducts TopFrescoProducts  Age Sex Shops  
  /MISSING=LISTWISE.

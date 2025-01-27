OPTIONS (DIRECT=TRUE, PARALLEL=TRUE, SKIP=1)
LOAD DATA
    INFILE './data.processed/NUTRIENT_NAME.csv.trimmed'
    APPEND
    INTO TABLE NUTRIENT_NAME
    FIELDS TERMINATED BY ','
    OPTIONALLY ENCLOSED BY '"'
    TRAILING NULLCOLS
    (NutrientID INTEGER EXTERNAL, NutrientCode INTEGER EXTERNAL, NutrientSymbol CHAR, NutrientUnit CHAR, NutrientName CHAR, NutrientNameF CHAR, Tagname CHAR, NutrientDecimals INTEGER EXTERNAL)
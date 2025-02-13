-- =========================================================================================================
-- USDA National Nutrient Database for Standard Reference, Release 28 (http://www.ars.usda.gov/ba/bhnrc/ndl)
-- This file was generated by http://github.com/m5n/nutriana
-- Run this SQL with an account that has admin priviledges, e.g.: mysql --local_infile=1 -v -u root < usda_nndsr_mysql.sql
-- =========================================================================================================

drop database if exists usda_nndsr;
create database usda_nndsr;
use usda_nndsr;
grant all on usda_nndsr.* to 'food'@'localhost' identified by 'food';

-- Food Description
create table FOOD_DES (
    NDB_No varchar(5) not null,   -- 5-digit Nutrient Databank number that uniquely identifies a food item. If this field is defined as numeric, the leading zero will be lost.
    FdGrp_Cd varchar(4) not null,   -- 4-digit code indicating food group to which a food item belongs.
    Long_Desc varchar(200) not null,   -- 200-character description of food item.
    Shrt_Desc varchar(60) not null,   -- 60-character abbreviated description of food item. Generated from the 200-character description using abbreviations in Appendix A. If short description is longer than 60 characters, additional abbreviations are made.
    ComName varchar(100),   -- Other names commonly used to describe a food, including local or regional names for various foods, for example, "soda" or "pop" for "carbonated beverages."
    ManufacName varchar(65),   -- Indicates the company that manufactured the product, when appropriate.
    Survey varchar(1),   -- Indicates if the food item is used in the USDA Food and Nutrient Database for Dietary Studies (FNDDS) and thus has a complete nutrient profile for the 65 FNDDS nutrients.
    Ref_desc varchar(135),   -- Description of inedible parts of a food item (refuse), such as seeds or bone.
    Refuse tinyint(2) unsigned,   -- Percentage of refuse.
    SciName varchar(65),   -- Scientific name of the food item. Given for the least processed form of the food (usually raw), if applicable.
    N_Factor dec(4, 2) unsigned,   -- Factor for converting nitrogen to protein (see p. 12).
    Pro_Factor dec(4, 2) unsigned,   -- Factor for calculating calories from protein (see p. 14).
    Fat_Factor dec(4, 2) unsigned,   -- Factor for calculating calories from fat (see p. 14).
    CHO_Factor dec(4, 2) unsigned   -- Factor for calculating calories from carbohydrate (see p. 14).
);

-- Nutrient Data
create table NUT_DATA (
    NDB_No varchar(5) not null,   -- 5-digit Nutrient Databank number that uniquely identifies a food item. If this field is defined as numeric, the leading zero will be lost.
    Nutr_No varchar(3) not null,   -- Unique 3-digit identifier code for a nutrient.
    Nutr_Val dec(10, 3) unsigned not null,   -- Amount in 100 grams, edible portion (Nutrient values have been rounded to a specified number of decimal places for each nutrient. Number of decimal places is listed in the Nutrient Definition file.).
    Num_Data_Pts mediumint(5) unsigned not null,   -- Number of data points is the number of analyses used to calculate the nutrient value. If the number of data points is 0, the value was calculated or imputed.
    Std_Error dec(8, 3) unsigned,   -- Standard error of the mean. Null if cannot be calculated. The standard error is also not given if the number of data points is less than three.
    Src_Cd varchar(2) not null,   -- Code indicating type of data.
    Deriv_Cd varchar(4),   -- Data Derivation Code giving specific information on how the value is determined. This field is populated only for items added or updated starting with SR14. This field may not be populated if older records were used in the calculation of the mean value.
    Ref_NDB_No varchar(5),   -- NDB number of the item used to calculate a missing value. Populated only for items added or updated starting with SR14.
    Add_Nutr_Mark varchar(1),   -- Indicates a vitamin or mineral added for fortification or enrichment. This field is populated for ready-to-eat breakfast cereals and many brand-name hot cereals in food group 08.
    Num_Studies tinyint(2) unsigned,   -- Number of studies.
    Min dec(10, 3) unsigned,   -- Minimum value.
    Max dec(10, 3) unsigned,   -- Maximum value.
    DF smallint(4) unsigned,   -- Degrees of freedom.
    Low_EB dec(10, 3) unsigned,   -- Lower 95% error bound.
    Up_EB dec(10, 3) unsigned,   -- Upper 95% error bound.
    Stat_cmt varchar(10),   -- Statistical comments. See definitions below.
    AddMod_Date date,   -- Indicates when a value was either added to the database or last modified.
    CC varchar(1)   -- Confidence Code indicating data quality, based on evaluation of sample plan, sample handling, analytical method, analytical quality control, and number of samples analyzed. Not included in this release, but is planned for future releases.
);

-- Weight
create table WEIGHT (
    NDB_No varchar(5) not null,   -- 5-digit Nutrient Databank number that uniquely identifies a food item. If this field is defined as numeric, the leading zero will be lost.
    Seq varchar(2) not null,   -- Sequence number.
    Amount dec(6, 3) unsigned not null,   -- Unit modifier (for example, 1 in "1 cup").
    Msre_Desc varchar(84) not null,   -- Description (for example, cup, diced, and 1-inch pieces).
    Gm_Wgt dec(7, 1) unsigned not null,   -- Gram weight.
    Num_Data_Pts smallint(4) unsigned,   -- Number of data points.
    Std_Dev dec(7, 3) unsigned   -- Standard deviation.
);

-- Footnote
create table FOOTNOTE (
    NDB_No varchar(5) not null,   -- 5-digit Nutrient Databank number that uniquely identifies a food item. If this field is defined as numeric, the leading zero will be lost. 
    Footnt_No varchar(4) not null,   -- Sequence number. If a given footnote applies to more than one nutrient number, the same footnote number is used. As a result, this file cannot be indexed and there is no primary key.
    Footnt_Typ varchar(1) not null,   -- Type of footnote: D = footnote adding information to the food description; M = footnote adding information to measure description; N = footnote providing additional information on a nutrient value. If the Footnt_typ = N, the Nutr_No will also be filled in.
    Nutr_No varchar(3),   -- Unique 3-digit identifier code for a nutrient to which footnote applies.
    Footnt_Txt varchar(200) not null   -- Footnote text.
);

-- Food Group Description
create table FD_GROUP (
    FdGrp_Cd varchar(4) not null,   -- 4-digit code identifying a food group. Only the first 2 digits are currently assigned. In the future, the last 2 digits may be used. Codes may not be consecutive.
    FdGrp_Desc varchar(60) not null   -- Name of food group.
);

-- LanguaL Factor
create table LANGUAL (
    NDB_No varchar(5) not null,   -- 5-digit Nutrient Databank number that uniquely identifies a food item. If this field is defined as numeric, the leading zero will be lost.
    Factor_Code varchar(5) not null   -- The LanguaL factor from the Thesaurus.
);

-- LanguaL Factors Description
create table LANGDESC (
    Factor_Code varchar(5) not null,   -- The LanguaL factor from the Thesaurus. Only those codes used to factor the foods contained in the LanguaL Factor file are included in this file.
    Description varchar(140) not null   -- The description of the LanguaL Factor Code from the thesaurus.
);

-- Nutrient Definition
create table NUTR_DEF (
    Nutr_No varchar(3) not null,   -- Unique 3-digit identifier code for a nutrient.
    Units varchar(7) not null,   -- Units of measure (mg, g, mcg, and so on).
    Tagname varchar(20),   -- International Network of Food Data Systems (INFOODS) Tagnames. (INFOODS, 2014.) A unique abbreviation for a nutrient/food component developed by INFOODS to aid in the interchange of data.
    NutrDesc varchar(60) not null,   -- Name of nutrient/food component.
    Num_Dec varchar(1) not null,   -- Number of decimal places to which a nutrient value is rounded.
    SR_Order mediumint(6) unsigned not null   -- Used to sort nutrient records in the same order as various reports produced from SR.
);

-- Source Code
create table SRC_CD (
    Src_Cd varchar(2) not null,   -- 2-digit code indicating type of data.
    SrcCd_Desc varchar(60) not null   -- Description of source code that identifies the type of nutrient data.
);

-- Data Derivation Code Description
create table DERIV_CD (
    Deriv_Cd varchar(4) not null,   -- Derivation Code.
    Deriv_Desc varchar(120) not null   -- Description of derivation code giving specific information on how the value was determined.
);

-- Sources of Data
create table DATA_SRC (
    DataSrc_ID varchar(6) not null,   -- Unique ID identifying the reference/source.
    Authors varchar(255),   -- List of authors for a journal article or name of sponsoring organization for other documents.
    Title varchar(255) not null,   -- Title of article or name of document, such as a report from a company or trade association.
    Year varchar(4),   -- Year article or document was published.
    Journal varchar(135),   -- Name of the journal in which the article was published.
    Vol_City varchar(16),   -- Volume number for journal articles, books, or reports; city where sponsoring organization is located.
    Issue_State varchar(5),   -- Issue number for journal article; State where the sponsoring organization is located.
    Start_Page varchar(5),   -- Starting page number of article/document.
    End_Page varchar(5)   -- Ending page number of article/document.
);

-- Sources of Data Link
create table DATSRCLN (
    NDB_No varchar(5) not null,   -- 5-digit Nutrient Databank number that uniquely identifies a food item. If this field is defined as numeric, the leading zero will be lost.
    Nutr_No varchar(3) not null,   -- Unique 3-digit identifier code for a nutrient.
    DataSrc_ID varchar(6) not null   -- Unique ID identifying the reference/source.
);

-- Load data into FOOD_DES
load data local infile './data.processed/FOOD_DES.txt.trimmed'
    into table FOOD_DES
    fields terminated by '^' optionally enclosed by '~'
    lines terminated by '\n'
    (NDB_No, FdGrp_Cd, Long_Desc, Shrt_Desc, ComName, ManufacName, Survey, Ref_desc, Refuse, SciName, N_Factor, Pro_Factor, Fat_Factor, CHO_Factor)
;
-- Assert all 8789 records were loaded
create table tmp (c int unique key);
insert into tmp (c) values (2);
insert into tmp (select count(*) from FOOD_DES);
delete from tmp where c = 8789;
insert into tmp (select count(*) from tmp);
drop table tmp;

-- Load data into NUT_DATA
load data local infile './data.processed/NUT_DATA.txt.trimmed'
    into table NUT_DATA
    fields terminated by '^' optionally enclosed by '~'
    lines terminated by '\n'
    (NDB_No, Nutr_No, Nutr_Val, Num_Data_Pts, Std_Error, Src_Cd, Deriv_Cd, Ref_NDB_No, Add_Nutr_Mark, Num_Studies, Min, Max, DF, Low_EB, Up_EB, Stat_cmt, @date1, CC)
    set
    AddMod_Date = str_to_date(@date1, '%m/%Y');
-- Assert all 679045 records were loaded
create table tmp (c int unique key);
insert into tmp (c) values (2);
insert into tmp (select count(*) from NUT_DATA);
delete from tmp where c = 679045;
insert into tmp (select count(*) from tmp);
drop table tmp;

-- Load data into WEIGHT
load data local infile './data.processed/WEIGHT.txt.trimmed'
    into table WEIGHT
    fields terminated by '^' optionally enclosed by '~'
    lines terminated by '\n'
    (NDB_No, Seq, Amount, Msre_Desc, Gm_Wgt, Num_Data_Pts, Std_Dev)
;
-- Assert all 15438 records were loaded
create table tmp (c int unique key);
insert into tmp (c) values (2);
insert into tmp (select count(*) from WEIGHT);
delete from tmp where c = 15438;
insert into tmp (select count(*) from tmp);
drop table tmp;

-- Load data into FOOTNOTE
load data local infile './data.processed/FOOTNOTE.txt.trimmed'
    into table FOOTNOTE
    fields terminated by '^' optionally enclosed by '~'
    lines terminated by '\n'
    (NDB_No, Footnt_No, Footnt_Typ, Nutr_No, Footnt_Txt)
;
-- Assert all 552 records were loaded
create table tmp (c int unique key);
insert into tmp (c) values (2);
insert into tmp (select count(*) from FOOTNOTE);
delete from tmp where c = 552;
insert into tmp (select count(*) from tmp);
drop table tmp;

-- Load data into FD_GROUP
load data local infile './data.processed/FD_GROUP.txt.trimmed'
    into table FD_GROUP
    fields terminated by '^' optionally enclosed by '~'
    lines terminated by '\n'
    (FdGrp_Cd, FdGrp_Desc)
;
-- Assert all 25 records were loaded
create table tmp (c int unique key);
insert into tmp (c) values (2);
insert into tmp (select count(*) from FD_GROUP);
delete from tmp where c = 25;
insert into tmp (select count(*) from tmp);
drop table tmp;

-- Load data into LANGUAL
load data local infile './data.processed/LANGUAL.txt.trimmed'
    into table LANGUAL
    fields terminated by '^' optionally enclosed by '~'
    lines terminated by '\n'
    (NDB_No, Factor_Code)
;
-- Assert all 38301 records were loaded
create table tmp (c int unique key);
insert into tmp (c) values (2);
insert into tmp (select count(*) from LANGUAL);
delete from tmp where c = 38301;
insert into tmp (select count(*) from tmp);
drop table tmp;

-- Load data into LANGDESC
load data local infile './data.processed/LANGDESC.txt.trimmed'
    into table LANGDESC
    fields terminated by '^' optionally enclosed by '~'
    lines terminated by '\n'
    (Factor_Code, Description)
;
-- Assert all 774 records were loaded
create table tmp (c int unique key);
insert into tmp (c) values (2);
insert into tmp (select count(*) from LANGDESC);
delete from tmp where c = 774;
insert into tmp (select count(*) from tmp);
drop table tmp;

-- Load data into NUTR_DEF
load data local infile './data.processed/NUTR_DEF.txt.trimmed'
    into table NUTR_DEF
    fields terminated by '^' optionally enclosed by '~'
    lines terminated by '\n'
    (Nutr_No, Units, Tagname, NutrDesc, Num_Dec, SR_Order)
;
-- Assert all 150 records were loaded
create table tmp (c int unique key);
insert into tmp (c) values (2);
insert into tmp (select count(*) from NUTR_DEF);
delete from tmp where c = 150;
insert into tmp (select count(*) from tmp);
drop table tmp;

-- Load data into SRC_CD
load data local infile './data.processed/SRC_CD.txt.trimmed'
    into table SRC_CD
    fields terminated by '^' optionally enclosed by '~'
    lines terminated by '\n'
    (Src_Cd, SrcCd_Desc)
;
-- Assert all 10 records were loaded
create table tmp (c int unique key);
insert into tmp (c) values (2);
insert into tmp (select count(*) from SRC_CD);
delete from tmp where c = 10;
insert into tmp (select count(*) from tmp);
drop table tmp;

-- Load data into DERIV_CD
load data local infile './data.processed/DERIV_CD.txt.trimmed'
    into table DERIV_CD
    fields terminated by '^' optionally enclosed by '~'
    lines terminated by '\n'
    (Deriv_Cd, Deriv_Desc)
;
-- Assert all 55 records were loaded
create table tmp (c int unique key);
insert into tmp (c) values (2);
insert into tmp (select count(*) from DERIV_CD);
delete from tmp where c = 55;
insert into tmp (select count(*) from tmp);
drop table tmp;

-- Load data into DATA_SRC
load data local infile './data.processed/DATA_SRC.txt.trimmed'
    into table DATA_SRC
    fields terminated by '^' optionally enclosed by '~'
    lines terminated by '\n'
    (DataSrc_ID, Authors, Title, Year, Journal, Vol_City, Issue_State, Start_Page, End_Page)
;
-- Assert all 682 records were loaded
create table tmp (c int unique key);
insert into tmp (c) values (2);
insert into tmp (select count(*) from DATA_SRC);
delete from tmp where c = 682;
insert into tmp (select count(*) from tmp);
drop table tmp;

-- Load data into DATSRCLN
load data local infile './data.processed/DATSRCLN.txt.trimmed'
    into table DATSRCLN
    fields terminated by '^' optionally enclosed by '~'
    lines terminated by '\n'
    (NDB_No, Nutr_No, DataSrc_ID)
;
-- Assert all 244496 records were loaded
create table tmp (c int unique key);
insert into tmp (c) values (2);
insert into tmp (select count(*) from DATSRCLN);
delete from tmp where c = 244496;
insert into tmp (select count(*) from tmp);
drop table tmp;

-- Correct data inconsistencies, if any
UPDATE NUT_DATA SET Deriv_Cd = NULL WHERE Deriv_Cd = '';
UPDATE NUT_DATA SET Ref_NDB_No = NULL WHERE Ref_NDB_No = '';
UPDATE FOOTNOTE SET Nutr_No = NULL WHERE Nutr_No = '';

-- Add primary keys
alter table FOOD_DES add primary key (NDB_No);
alter table NUT_DATA add primary key (NDB_No, Nutr_No);
alter table WEIGHT add primary key (NDB_No, Seq);
alter table FD_GROUP add primary key (FdGrp_Cd);
alter table LANGUAL add primary key (NDB_No, Factor_Code);
alter table LANGDESC add primary key (Factor_Code);
alter table NUTR_DEF add primary key (Nutr_No);
alter table SRC_CD add primary key (Src_Cd);
alter table DERIV_CD add primary key (Deriv_Cd);
alter table DATA_SRC add primary key (DataSrc_ID);
alter table DATSRCLN add primary key (NDB_No, Nutr_No, DataSrc_ID);

-- Add foreign keys
alter table FOOD_DES add foreign key (FdGrp_Cd) references FD_GROUP(FdGrp_Cd);
alter table NUT_DATA add foreign key (NDB_No) references FOOD_DES(NDB_No);
alter table NUT_DATA add foreign key (Nutr_No) references NUTR_DEF(Nutr_No);
alter table NUT_DATA add foreign key (Src_Cd) references SRC_CD(Src_Cd);
alter table NUT_DATA add foreign key (Deriv_Cd) references DERIV_CD(Deriv_Cd);
alter table NUT_DATA add foreign key (Ref_NDB_No) references FOOD_DES(NDB_No);
alter table WEIGHT add foreign key (NDB_No) references FOOD_DES(NDB_No);
alter table FOOTNOTE add foreign key (NDB_No) references FOOD_DES(NDB_No);
alter table FOOTNOTE add foreign key (Nutr_No) references NUTR_DEF(Nutr_No);
alter table LANGUAL add foreign key (NDB_No) references FOOD_DES(NDB_No);
alter table LANGUAL add foreign key (Factor_Code) references LANGDESC(Factor_Code);
alter table DATSRCLN add foreign key (NDB_No) references FOOD_DES(NDB_No);
alter table DATSRCLN add foreign key (Nutr_No) references NUTR_DEF(Nutr_No);
alter table DATSRCLN add foreign key (DataSrc_ID) references DATA_SRC(DataSrc_ID);


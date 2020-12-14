#set up indices for lifestage groups
infants_idx = rdi_macros_df.index[rdi_macros_df['Life-Stage Group']=='Infants'][0]
child_idx = rdi_macros_df.index[rdi_macros_df['Life-Stage Group']=='Children'][0]
male_idx = rdi_macros_df.index[rdi_macros_df['Life-Stage Group']=='Males'][0]
fem_idx = rdi_macros_df.index[rdi_macros_df['Life-Stage Group']=='Females'][0]
preg_idx = rdi_macros_df.index[rdi_macros_df['Life-Stage Group']=='Pregnancy'][0]
lact_idx = rdi_macros_df.index[rdi_macros_df['Life-Stage Group']=='Lacation'][0]

#except for last go to the next, 0 3 6 13 20 24
lifestage_idxs = [infants_idx, child_idx, male_idx, fem_idx, preg_idx, lact_idx]
#todo: must match keys with person_type in user table
lifestage_idx_dict = {
    'infant': infants_idx, 'child':child_idx, 'male':male_idx, 'female':fem_idx,
    'pregnant': preg_idx, 'lactating':lact_idx
}
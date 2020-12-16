a_dict = {
                "mollusc_allergy": "Mollusc Allergy",
                "mustard_allergy": "Mustard Allergy",
                "sesame_allergy": "Sesame Allergy",
                "gluten_allergy": "Gluten Allergy",
                "lactose_intolerance": "Lactose Intolerance",
                "soy_allergy": "Soy Allergy",
                "egg_allergy": "Egg Allergy",
                "fish_allergy": "Fish Allergy",
                "celery_allergy": "Celery Allergy",
                "crustacean_allergy": "Crustacean Allergy",
                "peanut_allergy": "Peanut Allergy",
                "tree_nut_allergy": "Tree Nut Allergy",
                "wheat_allergy": "Wheat Allergy",
                "lupin_allergy": "Lupin Allergy",
                "milk_allergy": "Milk Allergy"
            }
allergies_dict = {v:k for k,v in a_dict.items()}

d_dict = {
                "meateater": "Meateater",
                "pescetarian": "Pescetarian",
                "vegetarian": "Vegetarian",
                "vegan": "Vegan"
            }

diet_dict = {v:k for k,v in d_dict.items()}

p_dict = {
                "stirfrying_dryf": "Stir Frying, Dry With Fat",
                "panfrying_dryf": "Pan Frying, Dry With Fat",
                "deepfrying_dryf": "Deep Frying, Dry With Fat",
                "sauteing_dryf": "Sauteing, Dry With Fat",
                "searing_dryf": "Searing, Dry With Fat",
                "sweating_dryf": "Sweating, Dry With Fat",
                "grilling_drynof": "Grilling, Dry",
                "roasting_drynof": "Roasting, Dry",
                "searing_drynof": "Searing, Dry",
                "broiling_drynof": "Broiling, Dry",
                "baking_drynof": "Baking, Dry",
                "smoking_drynof": "Smoking, Dry",
                "steaming_moist": "Steaming, Moist",
                "poaching_moist": "Poaching, Moist",
                "simmering_moist": "Simmering, Moist",
                "boiling_moist": "Boiling, Moist",
                "stewing_moist": "Stewing, Moist",
                "sousvide_moist": "Sousvide, Moist",
                "braising_cmbd": "Braising, Combined",
                "raw_raw": "Raw",
                "pickling_raw": "Pickling, Raw"
            }
prep_dict = {v:k for k,v in p_dict.items()}
rules = [

    # Cold and Flu
    {
        "if": ["fever", "cough", "sore throat"],
        "then": "flu"
    },
    {
        "if": ["runny nose", "sneezing", "sore throat"],
        "then": "common cold"
    },
    {
        "if": ["body ache", "fatigue", "fever"],
        "then": "viral infection"
    },

    # COVID-like symptoms
    {
        "if": ["fever", "dry cough", "loss of taste", "loss of smell"],
        "then": "covid suspected"
    },

    # Digestive issues
    {
        "if": ["stomach pain", "vomiting", "diarrhea"],
        "then": "food poisoning"
    },
    {
        "if": ["acidity", "burning chest", "sour taste"],
        "then": "acid reflux"
    },

    # Head related
    {
        "if": ["headache", "sensitivity to light", "nausea"],
        "then": "migraine"
    },
    {
        "if": ["headache", "stress", "blurred vision"],
        "then": "tension headache"
    },

    # Infection types
    {
        "if": ["burning urination", "frequent urination", "lower abdominal pain"],
        "then": "urinary tract infection"
    },

    # Chaining rules (multi-step inference)
    {
        "if": ["flu"],
        "then": "rest_required"
    },
    {
        "if": ["covid suspected"],
        "then": "isolate immediately"
    },
    {
        "if": ["food poisoning"],
        "then": "drink ORS"
    },
    {
        "if": ["viral infection"],
        "then": "consult doctor"
    },
    # Chest issues
    {
        "if": ["chest pain"],
        "then": "possible heart problem"
    },
    {
        "if": ["chest pain", "shortness of breath"],
        "then": "heart attack risk"
    },
    {
        "if": ["chest pain", "fever"],
        "then": "possible pneumonia"
    },

    # Breathing issues
    {
        "if": ["shortness of breath", "wheezing"],
        "then": "asthma"
    },
    {
        "if": ["shortness of breath", "chronic cough"],
        "then": "copd"
    },
    {
        "if": ["shortness of breath", "chest pain"],
        "then": "pulmonary embolism risk"
    },

    # Fatigue and weakness
    {
        "if": ["fatigue", "weakness", "pale skin"],
        "then": "anemia"
    },
    {
        "if": ["fatigue", "weight gain", "cold intolerance"],
        "then": "thyroid dysfunction"
    },
    {
        "if": ["fatigue", "frequent urination", "increased thirst"],
        "then": "diabetes"
    },

    # Weight loss
    {
        "if": ["unexplained weight loss", "loss of appetite"],
        "then": "possible cancer"
    },
    {
        "if": ["unexplained weight loss", "frequent urination", "increased thirst"],
        "then": "diabetes"
    },

    # Diabetes symptoms
    {
        "if": ["increased thirst", "frequent urination", "fatigue"],
        "then": "diabetes"
    },

    # Stroke signs
    {
        "if": ["sudden numbness", "one side weakness"],
        "then": "stroke risk"
    },
    {
        "if": ["facial droop", "slurred speech"],
        "then": "stroke risk"
    },

    # Chronic cough
    {
        "if": ["chronic cough", "shortness of breath"],
        "then": "copd"
    },
    {
        "if": ["chronic cough", "weight loss"],
        "then": "lung cancer risk"
    },

    # Mental health
    {
        "if": ["persistent sadness", "hopelessness"],
        "then": "depression"
    },
    {
        "if": ["restlessness", "excessive worry"],
        "then": "anxiety"
    },

    # Fever group
    {
        "if": ["fever", "chills", "muscle aches"],
        "then": "flu"
    },
    {
        "if": ["fever", "dry cough", "loss of taste"],
        "then": "covid suspected"
    },

    # Jaundice
    {
        "if": ["yellow skin", "yellow eyes"],
        "then": "liver disease"
    },

    # Bleeding issues
    {
        "if": ["unusual bruising", "frequent bleeding"],
        "then": "blood disorder"
    },

    # Chaining medical advice
    {
        "if": ["stroke risk"],
        "then": "emergency medical attention required"
    },
    {
        "if": ["heart attack risk"],
        "then": "call emergency services immediately"
    },
    {
        "if": ["diabetes"],
        "then": "consult endocrinologist"
    },
    {
        "if": ["liver disease"],
        "then": "liver function test required"
    },
    {
        "if": ["depression"],
        "then": "consult mental health professional"
    }

]
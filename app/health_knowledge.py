DISEASES = {
    "Heart Disease": {
        "doctor_type": "Cardiologist",
        "severity_base": "High",
        "precautions": [
            "Check blood pressure regularly",
            "Avoid smoking and alcohol",
            "Seek urgent care for severe chest pain or breathlessness",
        ],
        "medicines": [
            "Doctor-prescribed antiplatelet or statin therapy may be considered",
            "Do not self-medicate for chest pain",
        ],
        "foods_to_eat": ["Fruits", "Leafy greens", "Oats", "Omega-3 rich foods", "Low-fat dairy"],
        "foods_to_avoid": ["Fried foods", "Excess salt", "High cholesterol foods", "Processed meat"],
        "diet": "Prefer a low-salt, high-fiber plate with vegetables, whole grains, and lean protein.",
        "hydration": "Drink water regularly unless a doctor has restricted fluids.",
        "exercise": "Aim for light walking after medical clearance.",
        "lifestyle": "Manage stress, sleep well, monitor blood pressure, and keep follow-up visits.",
        "emergency": "Call emergency services for crushing chest pain, fainting, blue lips, or severe breathlessness.",
    },
    "Diabetes": {
        "doctor_type": "Endocrinologist",
        "severity_base": "Medium",
        "precautions": [
            "Monitor fasting and post-meal glucose",
            "Inspect feet daily",
            "Do not skip prescribed medication",
        ],
        "medicines": [
            "Metformin or insulin may be prescribed by a clinician",
            "Avoid starting glucose medicine without medical supervision",
        ],
        "foods_to_eat": ["Oats", "Green vegetables", "Brown rice", "Nuts", "Lentils"],
        "foods_to_avoid": ["Sugar", "Soft drinks", "White bread", "Sweetened snacks"],
        "diet": "Use consistent carbohydrate portions and pair carbs with protein and fiber.",
        "hydration": "Choose water or unsweetened drinks.",
        "exercise": "Walk 20 to 30 minutes most days if cleared by a doctor.",
        "lifestyle": "Track glucose, weight, sleep, and regular HbA1c testing.",
        "emergency": "Seek urgent care for confusion, vomiting, very high sugar, or fainting.",
    },
    "Typhoid": {
        "doctor_type": "Infectious Disease Specialist",
        "severity_base": "Medium",
        "precautions": [
            "Use safe drinking water",
            "Avoid street food during illness",
            "Complete prescribed antibiotics if diagnosed",
        ],
        "medicines": [
            "Antibiotics require doctor evaluation and prescription",
            "Oral rehydration may help prevent dehydration",
        ],
        "foods_to_eat": ["Rice porridge", "Banana", "Boiled potatoes", "Soup", "Curd"],
        "foods_to_avoid": ["Raw salads", "Spicy food", "Fried food", "Unfiltered water"],
        "diet": "Prefer soft, easy-to-digest meals until fever and stomach symptoms improve.",
        "hydration": "Use oral rehydration solution if vomiting or diarrhea occurs.",
        "exercise": "Rest during fever; resume activity gradually.",
        "lifestyle": "Wash hands often and keep food hygiene strict.",
        "emergency": "Seek care for persistent high fever, blood in stool, severe dehydration, or confusion.",
    },
    "Malaria": {
        "doctor_type": "Infectious Disease Specialist",
        "severity_base": "High",
        "precautions": [
            "Avoid mosquito bites",
            "Use bed nets and repellents",
            "Get prompt testing for fever after mosquito exposure",
        ],
        "medicines": [
            "Antimalarial medication depends on test results and region",
            "Fever medicine should be used only as advised",
        ],
        "foods_to_eat": ["Soups", "Coconut water", "Protein-rich light meals", "Fruits"],
        "foods_to_avoid": ["Alcohol", "Heavy fried meals", "Unsafe water"],
        "diet": "Eat small frequent meals with adequate protein and fluids.",
        "hydration": "Hydrate aggressively unless restricted by a doctor.",
        "exercise": "Rest until fever cycles stop and strength returns.",
        "lifestyle": "Remove stagnant water and use mosquito protection.",
        "emergency": "Seek urgent care for seizures, confusion, jaundice, dark urine, or severe weakness.",
    },
    "Pneumonia": {
        "doctor_type": "Pulmonologist",
        "severity_base": "High",
        "precautions": [
            "Monitor oxygen saturation if available",
            "Avoid smoke exposure",
            "Use prescribed antibiotics or antivirals only as directed",
        ],
        "medicines": [
            "Antibiotics, inhalers, or antivirals require clinician assessment",
            "Do not delay care if breathing is difficult",
        ],
        "foods_to_eat": ["Warm soups", "Protein foods", "Citrus fruits", "Soft cooked vegetables"],
        "foods_to_avoid": ["Smoking", "Alcohol", "Very cold drinks if they worsen cough"],
        "diet": "Use nourishing warm meals and enough protein for recovery.",
        "hydration": "Warm fluids may soothe cough and support mucus clearance.",
        "exercise": "Rest during acute illness; start breathing exercises when advised.",
        "lifestyle": "Keep vaccinations up to date and avoid polluted air.",
        "emergency": "Seek urgent care for oxygen below 92 percent, blue lips, chest pain, or severe breathlessness.",
    },
    "Kidney Disease": {
        "doctor_type": "Nephrologist",
        "severity_base": "High",
        "precautions": [
            "Monitor blood pressure",
            "Avoid unnecessary painkillers",
            "Track creatinine and urine tests",
        ],
        "medicines": [
            "Blood pressure and kidney medicines must be personalized",
            "Avoid over-the-counter NSAIDs unless a doctor approves",
        ],
        "foods_to_eat": ["Cauliflower", "Cabbage", "Apple", "Controlled protein portions"],
        "foods_to_avoid": ["Excess salt", "Processed foods", "High potassium foods if advised", "Sugary drinks"],
        "diet": "Follow doctor-specific sodium, potassium, protein, and fluid guidance.",
        "hydration": "Fluid needs vary by kidney function; ask a nephrologist.",
        "exercise": "Gentle activity can help blood pressure when tolerated.",
        "lifestyle": "Control diabetes, blood pressure, and avoid nephrotoxic drugs.",
        "emergency": "Seek urgent care for very low urine, swelling with breathlessness, or confusion.",
    },
    "Liver Disease": {
        "doctor_type": "Gastroenterologist or Hepatologist",
        "severity_base": "Medium",
        "precautions": [
            "Avoid alcohol",
            "Review medicines and supplements with a doctor",
            "Check liver enzymes and bilirubin",
        ],
        "medicines": [
            "Treatment depends on the cause of liver injury",
            "Avoid excess acetaminophen or herbal self-treatment",
        ],
        "foods_to_eat": ["Vegetables", "Whole grains", "Lean protein", "Coffee if tolerated"],
        "foods_to_avoid": ["Alcohol", "Very fatty foods", "Excess sugar", "Unverified supplements"],
        "diet": "Use balanced meals with moderate fat and enough protein.",
        "hydration": "Drink water regularly unless medically restricted.",
        "exercise": "Regular walking supports fatty liver management.",
        "lifestyle": "Maintain healthy weight and vaccination status for hepatitis where advised.",
        "emergency": "Seek urgent care for confusion, vomiting blood, black stools, or deep jaundice.",
    },
    "Dengue": {
        "doctor_type": "General Physician or Infectious Disease Specialist",
        "severity_base": "High",
        "precautions": [
            "Monitor platelet count",
            "Avoid aspirin and ibuprofen unless a doctor approves",
            "Protect from mosquito bites during fever",
        ],
        "medicines": [
            "Use only doctor-advised fever medicine",
            "No antibiotic is needed unless another infection exists",
        ],
        "foods_to_eat": ["Papaya fruit", "Soups", "Rice", "Banana", "Protein-rich light foods"],
        "foods_to_avoid": ["Aspirin-like medicines", "Alcohol", "Very oily foods"],
        "diet": "Eat light meals and focus on fluids and protein.",
        "hydration": "Use water, oral rehydration, coconut water, or soups frequently.",
        "exercise": "Rest until fever and weakness resolve.",
        "lifestyle": "Remove standing water and use mosquito nets or repellents.",
        "emergency": "Seek urgent care for bleeding, severe abdominal pain, persistent vomiting, sleepiness, or cold limbs.",
    },
    "Anemia": {
        "doctor_type": "Hematologist or General Physician",
        "severity_base": "Medium",
        "precautions": [
            "Check hemoglobin and iron studies",
            "Look for heavy bleeding or nutritional deficiency",
            "Do not ignore breathlessness or fainting",
        ],
        "medicines": [
            "Iron, B12, or folate may be prescribed after testing",
            "Avoid iron supplements without confirming the cause",
        ],
        "foods_to_eat": ["Spinach", "Beans", "Dates", "Lean meat", "Vitamin C fruits"],
        "foods_to_avoid": ["Tea or coffee with iron-rich meals", "Low-nutrient junk food"],
        "diet": "Combine iron-rich foods with vitamin C to support absorption.",
        "hydration": "Drink enough water; dehydration can worsen dizziness.",
        "exercise": "Use gentle activity until fatigue improves.",
        "lifestyle": "Investigate chronic blood loss and maintain follow-up blood tests.",
        "emergency": "Seek urgent care for chest pain, fainting, severe breathlessness, or very low hemoglobin.",
    },
}


GENERAL_DISCLAIMER = (
    "This system is AI-assisted and not a replacement for professional medical advice. "
    "Always consult a certified doctor."
)


def disease_names():
    return list(DISEASES.keys())

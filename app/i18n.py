from flask import session


TRANSLATIONS = {
    "en": {
        "app_name": "Smart Disease Prediction",
        "dashboard": "Dashboard",
        "predict": "Predict",
        "reports": "Reports",
        "chatbot": "Assistant",
        "appointments": "Appointments",
        "history": "History",
        "training": "Training",
        "doctor_panel": "Doctor Panel",
        "login": "Login",
        "signup": "Signup",
        "logout": "Logout",
    },
    "hi": {
        "app_name": "Smart Disease Prediction",
        "dashboard": "Dashboard",
        "predict": "Prediction",
        "reports": "Reports",
        "chatbot": "Assistant",
        "appointments": "Appointments",
        "history": "History",
        "training": "Training",
        "doctor_panel": "Doctor Panel",
        "login": "Login",
        "signup": "Signup",
        "logout": "Logout",
    },
    "es": {
        "app_name": "Smart Disease Prediction",
        "dashboard": "Panel",
        "predict": "Prediccion",
        "reports": "Informes",
        "chatbot": "Asistente",
        "appointments": "Citas",
        "history": "Historial",
        "training": "Entrenamiento",
        "doctor_panel": "Panel Medico",
        "login": "Entrar",
        "signup": "Registro",
        "logout": "Salir",
    },
}


def translate(key):
    language = session.get("language", "en")
    return TRANSLATIONS.get(language, TRANSLATIONS["en"]).get(key, key)

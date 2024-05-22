import streamlit as st

st.title("Baby-Timeline mit Fruchtgrößen während der Schwangerschaft")

# Definition der Baby-Entwicklungsstufen und zugehöriger Bilder
baby_entwicklung = {
    "Woche 1-2: Befruchtung": "https://example.com/fertilization.jpg",
    "Woche 3: Mohnsamen": "https://example.com/poppy_seed.jpg",
    "Woche 4: Heidelbeere": "https://example.com/blueberry.jpg",
    "Woche 5: Erbse": "https://example.com/pea.jpg",
    "Woche 6: Linsen": "https://example.com/lentil.jpg",
    "Woche 7: Traube": "https://example.com/grape.jpg",
    "Woche 8: Himbeere": "https://example.com/raspberry.jpg",
    "Woche 9: Olive": "https://example.com/olive.jpg",
    "Woche 10: Pflaume": "https://example.com/plum.jpg",
    "Woche 11: Limette": "https://example.com/lime.jpg",
    "Woche 12: Feige": "https://example.com/fig.jpg",
    "Woche 13: Zitrone": "https://example.com/lemon.jpg",
    "Woche 14: Zwiebel": "https://example.com/onion.jpg",
    "Woche 15: Apfel": "https://example.com/apple.jpg",
    "Woche 16: Avocado": "https://example.com/avocado.jpg",
    "Woche 17: Zwiebel": "https://example.com/onion.jpg",
    "Woche 18: Gurke": "https://example.com/cucumber.jpg",
    "Woche 19: Mango": "https://example.com/mango.jpg",
    "Woche 20: Banane": "https://example.com/banana.jpg",
    "Woche 21: Karotte": "https://example.com/carrot.jpg",
    "Woche 22: Paprika": "https://example.com/bell_pepper.jpg",
    "Woche 23: Aubergine": "https://example.com/eggplant.jpg",
    "Woche 24: Maiskolben": "https://example.com/corn.jpg",
    "Woche 25: Blumenkohl": "https://example.com/cauliflower.jpg",
    "Woche 26: Kopfsalat": "https://example.com/lettuce.jpg",
    "Woche 27: Eisbergsalat": "https://example.com/iceberg_lettuce.jpg",
    "Woche 28: Chinesischer Kohl": "https://example.com/bok_choy.jpg",
    "Woche 29: Butternusskürbis": "https://example.com/butternut_squash.jpg",
    "Woche 30: Wassermelone": "https://example.com/watermelon.jpg",
    "Woche 31: Kokosnuss": "https://example.com/coconut.jpg",
    "Woche 32: Ananas": "https://example.com/pineapple.jpg",
    "Woche 33: Kürbis": "https://example.com/pumpkin.jpg",
    "Woche 34: Sellerie": "https://example.com/celery.jpg",
    "Woche 35: Kokosnuss": "https://example.com/coconut.jpg",
    "Woche 36: Honigmelone": "https://example.com/cantaloupe.jpg",
    "Woche 37: Lauch": "https://example.com/leek.jpg",
    "Woche 38: Spaghetti-Kürbis": "https://example.com/spaghetti_squash.jpg",
    "Woche 39: Wassermelone": "https://example.com/watermelon.jpg",
    "Woche 40: Baby (ca. 50 cm)": "https://example.com/baby.jpg",
}

# Durchlaufe die Baby-Entwicklungsstufen und zeige Bilder an
for entwicklung, bild_url in baby_entwicklung.items():
    st.subheader(entwicklung)
    st.image(bild_url, caption=entwicklung, use_column_width=True)

st.write("Das sind einige wichtige Entwicklungsstufen des Babys während der Schwangerschaft, die mit Fruchtgrößen verglichen werden.")

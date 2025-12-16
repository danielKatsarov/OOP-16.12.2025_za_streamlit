import streamlit as st
import pandas as pd
from abc import ABC, abstractmethod

# ================== PAGE CONFIG ==================
st.set_page_config(
    page_title="Туристически планер",
    page_icon="🌍",
    layout="wide"
)

# ================== DATA ==================

routes = {
    "🇩🇪 България → Германия": ["София", "Белград", "Виена", "Мюнхен"],
    "🇮🇹 България → Италия": ["София", "Скопие", "Тирана", "Рим"],
    "🇫🇷 България → Франция": ["София", "Белград", "Загреб", "Париж"],
    "🇷🇴 България → Румъния": ["София", "Русе", "Букурещ"]
}

city_info = {
    "София": {"hotel": ("Hotel Sofia Center", 70), "food": ("Българска кухня", 20), "sight": "Александър Невски"},
    "Белград": {"hotel": ("Belgrade Inn", 65), "food": ("Сръбска скара", 22), "sight": "Калемегдан"},
    "Виена": {"hotel": ("Vienna City Hotel", 90), "food": ("Виенски шницел", 30), "sight": "Шьонбрун"},
    "Мюнхен": {"hotel": ("Munich Central", 95), "food": ("Немска кухня", 28), "sight": "Мариенплац"},
    "Скопие": {"hotel": ("Skopje Hotel", 60), "food": ("Македонска кухня", 18), "sight": "Каменният мост"},
    "Тирана": {"hotel": ("Tirana Plaza", 75), "food": ("Албанска кухня", 20), "sight": "Скендербег"},
    "Рим": {"hotel": ("Rome Central", 110), "food": ("Италианска кухня", 35), "sight": "Колизеум"},
    "Загреб": {"hotel": ("Zagreb Inn", 80), "food": ("Хърватска кухня", 25), "sight": "Горни град"},
    "Париж": {"hotel": ("Paris Boutique", 130), "food": ("Френска кухня", 40), "sight": "Айфеловата кула"},
    "Русе": {"hotel": ("Hotel Riga", 55), "food": ("Българска кухня", 18), "sight": "Доходното здание"},
    "Букурещ": {"hotel": ("Bucharest Center", 70), "food": ("Румънска кухня", 22), "sight": "Парламентът"}
}

city_coordinates = {
    "София": (42.6977, 23.3219),
    "Белград": (44.7866, 20.4489),
    "Виена": (48.2082, 16.3738),
    "Мюнхен": (48.1351, 11.5820),
    "Скопие": (41.9973, 21.4280),
    "Тирана": (41.3275, 19.8187),
    "Рим": (41.9028, 12.4964),
    "Загреб": (45.8150, 15.9819),
    "Париж": (48.8566, 2.3522),
    "Русе": (43.8356, 25.9657),
    "Букурещ": (44.4268, 26.1025)
}

DISTANCE_BETWEEN_CITIES = 300

# ================== OOP ==================

class Transport(ABC):
    def __init__(self, price_per_km):
        self.price_per_km = price_per_km

    @abstractmethod
    def name(self):
        pass

    def travel_cost(self, distance):
        return distance * self.price_per_km


class Car(Transport):
    def __init__(self): super().__init__(0.25)
    def name(self): return "🚗 Кола"


class Train(Transport):
    def __init__(self): super().__init__(0.18)
    def name(self): return "🚆 Влак"


class Bus(Transport):
    def __init__(self): super().__init__(0.12)
    def name(self): return "🚌 Автобус"


class Plane(Transport):
    def __init__(self): super().__init__(0.45)
    def name(self): return "✈️ Самолет"

# ================== SIDEBAR ==================

st.sidebar.header("⚙️ Персонализация")

route_choice = st.sidebar.selectbox("Маршрут", list(routes.keys()))
transport_choice = st.sidebar.selectbox("Транспорт", ["Кола", "Влак", "Автобус", "Самолет"])
days = st.sidebar.slider("Брой дни", 1, 14, 5)
people = st.sidebar.slider("Брой пътници", 1, 6, 2)
travel_type = st.sidebar.radio("Тип пътуване", ["💰 Икономично", "🏨 Стандартно", "💎 Луксозно"])
budget = st.sidebar.number_input("Бюджет (лв)", 300, 15000, 3000)

type_multiplier = {
    "💰 Икономично": 0.85,
    "🏨 Стандартно": 1.0,
    "💎 Луксозно": 1.3
}[travel_type]

# ================== MAIN UI ==================

st.title("🌍 Интерактивен туристически планер")
st.markdown("Планирай своето пътуване бързо, лесно и персонализирано ✨")

if st.button("🧭 Планирай пътуването"):
    cities = routes[route_choice]

    if transport_choice == "Кола":
        transport = Car()
    elif transport_choice == "Влак":
        transport = Train()
    elif transport_choice == "Автобус":
        transport = Bus()
    else:
        transport = Plane()

    st.subheader("🗺️ Маршрут")
    st.write(" ➡️ ".join(cities))

    col1, col2 = st.columns(2)

    total_food = total_hotel = 0

    with col1:
        st.subheader("🏙️ Градове")
        for city in cities:
            info = city_info[city]
            st.markdown(f"### 📍 {city}")
            st.write(f"🏨 {info['hotel'][0]} – {info['hotel'][1]} лв")
            st.write(f"🍽️ {info['food'][0]} – {info['food'][1]} лв")
            st.write(f"🏛️ {info['sight']}")
            st.markdown("---")

            total_food += info["food"][1] * days
            total_hotel += info["hotel"][1] * days

    total_distance = DISTANCE_BETWEEN_CITIES * (len(cities) - 1)
    transport_cost = transport.travel_cost(total_distance)

    total_cost = (
        transport_cost +
        (total_food + total_hotel) * people
    ) * type_multiplier

    with col2:
        st.subheader("💰 Разходи")
        st.metric("🚗 Транспорт", f"{transport_cost:.2f} лв")
        st.metric("🍽️ Храна", f"{total_food * people:.2f} лв")
        st.metric("🏨 Хотели", f"{total_hotel * people:.2f} лв")
        st.markdown("---")
        st.metric("💵 Общо", f"{total_cost:.2f} лв")

        st.progress(min(total_cost / budget, 1.0))

        if total_cost <= budget:
            st.success("✅ Бюджетът е достатъчен!")
        else:
            st.error("❌ Бюджетът не достига.")

    # ================== MAP ==================
    st.subheader("🗺️ Карта на маршрута")

    map_data = {
        "lat": [],
        "lon": []
    }

    for city in cities:
        lat, lon = city_coordinates[city]
        map_data["lat"].append(lat)
        map_data["lon"].append(lon)

    df_map = pd.DataFrame(map_data)
    st.map(df_map)

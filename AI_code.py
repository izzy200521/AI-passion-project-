#wellbeing_ai.py
# Personal Wellbeing AI Assistant

import requests
import math

print("Hello cyborg and welcome to your personal Wellbeing AI i am here to help you take care of yourself\n")
print("I will guide you through your day and help you stay healthy and happy.")

# =====================================================
# AUTOMATIC FOOD NUTRITION LOOKUP
# =====================================================

def get_nutrition(food):
    url = "https://world.openfoodfacts.org/cgi/search.pl"
    params = {
        "search_terms": food,
        "search_simple": 1,
        "action": "process",
        "json": 1,
        "page_size": 1
    }

    response = requests.get(url, params=params).json()

    if response.get("count", 0) == 0:
        return None

    product = response["products"][0]
    nutriments = product.get("nutriments", {})

    def safe_float(value):
        try:
            return float(value)
        except (TypeError, ValueError):
            return 0.0

    return {
        "calories": safe_float(nutriments.get("energy-kcal_100g")),
        "carbs": safe_float(nutriments.get("carbohydrates_100g")),
        "sugar": safe_float(nutriments.get("sugars_100g")),
    }


def calculate_nutrition(food_list):
    total_calories = 0.0
    total_carbs = 0.0
    total_sugar = 0.0

    print("\n🍽️ Food breakdown (per ~100g):")

    for food in food_list:
        nutrition = get_nutrition(food)

        if nutrition is None:
            print(f"⚠️ Could not find nutrition for: {food}")
            continue

        total_calories += nutrition["calories"]
        total_carbs += nutrition["carbs"]
        total_sugar += nutrition["sugar"]

        print(
            f"- {food.title()}: "
            f"{nutrition['calories']:.0f} kcal | "
            f"Carbs {nutrition['carbs']:.1f} g | "
            f"Sugar {nutrition['sugar']:.1f} g"
        )

    return total_calories, total_carbs, total_sugar


# =====================================================
# CALORIE WARNINGS if the person is eating less than 1800 cal
# =====================================================

def calorie_warning(total_calories):
    if total_calories < 1800:
        return (
            "\n⚠️ Warning: Your calorie intake is below the recommended level.\n"
            "Consider eating more nutritious foods to meet your energy needs."
        )
    return ""


def under_eating_info():
    return (
        "\n🍽️ Under-eating can lead to:\n"
        "- Fatigue and low energy\n"
        "- Nutrient deficiencies\n"
        "- Weakened immune system\n"
        "- Muscle loss\n"
        "- Hormonal imbalances\n"
        "- Hair loss and brittle nails\n"
        "- Heart issues\n"
        "Ensure you consume enough calories for your body's needs."
    )


# =====================================================
# TRAINING RECOMMENDATION
# =====================================================

def recommend_training(mood):
    mood = mood.lower()

    if mood in ["stressed", "anxious", "overwhelmed"]:
        return (
            "\n🧘‍♀️ Training for today:\n"
            "- 20 min calm walk\n"
            "- 10 min stretching\n"
            "- 5 min slow breathing\n"
            "Focus: calming the nervous system"
        )

    if mood in ["sad", "low", "tired"]:
        return (
            "\n🚶 Training for today:\n"
            "- 30 min light walk\n"
            "- Gentle mobility\n"
            "Focus: mood & energy"
        )

    if mood in ["happy", "good", "motivated"]:
        return (
            "\n🏋️ Training for today:\n"
            "- 10 min warm-up\n"
            "- Squats x12\n"
            "- Push-ups x10\n"
            "- Plank 30 sec\n"
            "- Stretch\n"
            "Focus: strength & confidence"
        )

    if mood in ["pms", "in pain", "day1 of cycle"]:
        return (
            "\n💗 Training for today:\n"
            "- 10 min gentle walk\n"
            "- Hydrate well\n"
            "- Write down thoughts\n"
            "- Warm shower\n"
            "Focus: self-care"
        )

    return (
        "\n🤍 Training for today:\n"
        "- Gentle movement\n"
        "- Stretching\n"
        "Focus: listening to your body"
    )


# =====================================================
# NEAREST GYM (OpenStreetMap)
# =====================================================

def nearest_gym_from_address(address):
    headers = {"User-Agent": "personal-ai-assistant"}

    geo_url = "https://nominatim.openstreetmap.org/search"
    geo_params = {"q": address, "format": "json", "limit": 1}

    geo = requests.get(geo_url, params=geo_params, headers=headers).json()
    if not geo:
        return "Address not found."

    lat = float(geo[0]["lat"])
    lon = float(geo[0]["lon"])

    query = f"""
    [out:json];
    node["leisure"="fitness_centre"](around:3000,{lat},{lon});
    out;
    """

    data = requests.post(
        "https://overpass-api.de/api/interpreter",
        data=query,
        headers=headers
    ).json()

    if not data["elements"]:
        return "No gym found nearby."

    def distance(lat1, lon1, lat2, lon2):
        R = 6371
        dlat = math.radians(lat2 - lat1)
        dlon = math.radians(lat2 - lat1)
        a = (
            math.sin(dlat / 2) ** 2
            + math.cos(math.radians(lat1))
            * math.cos(math.radians(lat2))
            * math.sin(dlon / 2) ** 2
        )
        return 2 * R * math.asin(math.sqrt(a))

    closest = None
    min_dist = float("inf")

    for gym in data["elements"]:
        d = distance(lat, lon, gym["lat"], gym["lon"])
        if d < min_dist:
            min_dist = d
            closest = gym

    name = closest["tags"].get("name", "Unnamed gym")
    return f"{name} ({min_dist:.2f} km away)"


# =====================================================
# CHEER UP MESSAGE
# =====================================================

def cheer_up():
    return (
        "\n🌟 Hey! Remember:\n"
        "- You are valued and loved\n"
        "- This feeling is temporary\n"
        "- Take small steps to care for yourself\n"
        "You've got this! 💪"
    )


# =====================================================
# USER INPUT
# =====================================================

foods_input = input(
    "What have you eaten today? (comma separated)\n"
    "Example: apple, egg, rice\n> "
)

foods = [f.strip() for f in foods_input.split(",")]

total_calories, total_carbs, total_sugar = calculate_nutrition(foods)

print("\n📊 DAILY TOTALS")
print(f"🔥 Calories: {total_calories:.0f} kcal")
print(f"🍞 Carbohydrates: {total_carbs:.1f} g")
print(f"🍬 Sugar: {total_sugar:.1f} g")

print(calorie_warning(total_calories))
if total_calories < 1800:
    print(under_eating_info())

mood = input(
    "\nHow are you feeling today?\n"
    "(happy / stressed / sad / tired / anxious / PMS / Day1 of cycle)\n> "
)

print(recommend_training(mood))

if mood.lower() in ["sad", "low", "tired"]:
    print(cheer_up())

address = input("\nEnter your address: ")
print("🏋️ Nearest gym:", nearest_gym_from_address(address))

print("\n💚 Consistency over perfection.")


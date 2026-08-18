# union_data.py

# বাংলাদেশের গুরুত্বপূর্ণ unions এর data
# High flood risk unions

UNION_DATA = {
    "কুড়িগ্রাম": [
        {
            "upazila": "চিলমারী",
            "union": "চিলমারী",
            "lat": 25.56, "lon": 89.67,
            "risk": "অতি উচ্চ",
            "river": "ব্রহ্মপুত্র",
            "elevation": 18,
            "population": 45000,
            "notes": "ব্রহ্মপুত্রের সাথে সরাসরি সংযুক্ত"
        },
        {
            "upazila": "উলিপুর",
            "union": "বেগমগঞ্জ",
            "lat": 25.78, "lon": 89.58,
            "risk": "অতি উচ্চ",
            "river": "তিস্তা",
            "elevation": 22,
            "population": 38000,
            "notes": "তিস্তার ভাঙন এলাকা"
        },
        {
            "upazila": "রাজারহাট",
            "union": "ঘরিয়ালডাঙা",
            "lat": 25.89, "lon": 89.52,
            "risk": "উচ্চ",
            "river": "ধরলা",
            "elevation": 25,
            "population": 29000,
            "notes": "ধরলা নদীর তীর"
        },
    ],
    "গাইবান্ধা": [
        {
            "upazila": "ফুলছড়ি",
            "union": "ফুলছড়ি",
            "lat": 25.19, "lon": 89.57,
            "risk": "অতি উচ্চ",
            "river": "যমুনা",
            "elevation": 15,
            "population": 52000,
            "notes": "যমুনার চরাঞ্চল"
        },
        {
            "upazila": "সাঘাটা",
            "union": "গোবিন্দগঞ্জ",
            "lat": 25.11, "lon": 89.38,
            "risk": "উচ্চ",
            "river": "করতোয়া",
            "elevation": 20,
            "population": 41000,
            "notes": "করতোয়া তীরবর্তী"
        },
    ],
    "সুনামগঞ্জ": [
        {
            "upazila": "দিরাই",
            "union": "দিরাই",
            "lat": 24.72, "lon": 91.40,
            "risk": "অতি উচ্চ",
            "river": "সুরমা",
            "elevation": 5,
            "population": 35000,
            "notes": "হাওর এলাকা — flash flood prone"
        },
        {
            "upazila": "ছাতক",
            "union": "ছাতক",
            "lat": 25.01, "lon": 91.67,
            "risk": "অতি উচ্চ",
            "river": "সুরমা",
            "elevation": 8,
            "population": 48000,
            "notes": "পাহাড়ি ঢল এলাকা"
        },
    ],
    "সিলেট": [
        {
            "upazila": "কোম্পানীগঞ্জ",
            "union": "ইসলামপুর",
            "lat": 25.11, "lon": 91.97,
            "risk": "উচ্চ",
            "river": "ধলাই",
            "elevation": 12,
            "population": 28000,
            "notes": "ভারত সীমান্তবর্তী"
        },
    ],
    "জামালপুর": [
        {
            "upazila": "ইসলামপুর",
            "union": "চিনাডুলি",
            "lat": 24.89, "lon": 89.70,
            "risk": "অতি উচ্চ",
            "river": "যমুনা",
            "elevation": 14,
            "population": 42000,
            "notes": "যমুনার বন্যাপ্রবণ চর"
        },
        {
            "upazila": "দেওয়ানগঞ্জ",
            "union": "দেওয়ানগঞ্জ",
            "lat": 25.09, "lon": 89.77,
            "risk": "উচ্চ",
            "river": "যমুনা",
            "elevation": 16,
            "population": 38000,
            "notes": "যমুনা তীরবর্তী"
        },
    ],
    "রংপুর": [
        {
            "upazila": "গঙ্গাচড়া",
            "union": "গঙ্গাচড়া",
            "lat": 25.85, "lon": 89.17,
            "risk": "উচ্চ",
            "river": "তিস্তা",
            "elevation": 28,
            "population": 35000,
            "notes": "তিস্তার তীর"
        },
        {
            "upazila": "কাউনিয়া",
            "union": "কাউনিয়া",
            "lat": 25.68, "lon": 89.45,
            "risk": "উচ্চ",
            "river": "তিস্তা",
            "elevation": 25,
            "population": 29000,
            "notes": "তিস্তা বন্যাপ্রবণ"
        },
    ],
}

def get_unions_by_district(district):
    return UNION_DATA.get(district, [])

def get_high_risk_unions():
    """সব অতি উচ্চ ঝুঁকির unions"""
    high_risk = []
    for district, unions in UNION_DATA.items():
        for union in unions:
            if union["risk"] == "অতি উচ্চ":
                high_risk.append({
                    "district": district,
                    **union
                })
    return high_risk

def get_union_stats():
    """Statistics"""
    total = sum(len(v) for v in UNION_DATA.values())
    high_risk = len(get_high_risk_unions())
    total_population = sum(
        u["population"]
        for unions in UNION_DATA.values()
        for u in unions
    )
    return {
        "total_unions_tracked": total,
        "high_risk_unions": high_risk,
        "total_population_at_risk": total_population,
    }
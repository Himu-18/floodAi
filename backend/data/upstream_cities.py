# ============================================================
# FloodAI — upstream_cities.py
#
# flood_config.py-র "upstream" ফিল্ডে শুধু শহরের নাম আছে (যেমন
# "Shillong,IN") — OpenWeatherMap-এ নাম দিয়ে query করা যায়, কিন্তু
# Open-Meteo-র hourly rainfall-intensity API-র জন্য lat/lon লাগে।
# এই ফাইলে সেই lat/lon mapping।
# ============================================================

UPSTREAM_CITY_COORDS = {
    "Dhaka": (23.8103, 90.4125),
    "Agartala": (23.8315, 91.2868),
    "Jalpaiguri": (26.5432, 88.7186),
    "Guwahati": (26.1445, 91.7362),
    "Shillong": (25.5788, 91.8933),
    "Kolkata": (22.5726, 88.3639),
    "Malda": (25.0108, 88.1411),
    "Siliguri": (26.7271, 88.3953),
    "Raiganj": (25.6188, 88.1289),
}


def get_upstream_coords(upstream_field):
    """flood_config.py-র 'upstream' ফিল্ড (যেমন 'Shillong,IN') থেকে
    শহরের নাম বের করে lat/lon রিটার্ন করে। না পাওয়া গেলে None।"""
    if not upstream_field:
        return None
    city_name = upstream_field.split(",")[0].strip()
    return UPSTREAM_CITY_COORDS.get(city_name)
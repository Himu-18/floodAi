# -*- coding: utf-8 -*-
"""
বাংলাদেশের real union gazetteer — সরকারি সোর্স ভিত্তিক (bangladesh.gov.bd,
LGD ওয়েবসাইট থেকে সংগৃহীত, ৪৫৪০টা ইউনিয়ন, ৬৪ জেলা)।

সোর্স: https://github.com/nuhil/bangladesh-geocode (MIT license)

এই ফাইলে যা আছে: প্রতিটা ইউনিয়নের real নাম (bn/en) ও official union
parishad ওয়েবসাইট, জেলা → উপজেলা → ইউনিয়ন হায়ারার্কি অনুযায়ী।

এই ফাইলে যা নেই (এখনো): প্রতিটা ইউনিয়নের নিজস্ব lat/lon, elevation,
population, flood-risk classification। এগুলো এখনো fabricate করা হয়নি —
প্রয়োজনে BBS admin-4 boundary shapefile (bgd_admbnda_adm4_bbs_20180410)
থেকে centroid বের করে যোগ করা যাবে।

`union_data.py`-র UNION_DATA-এর সাথে গুলিয়ে ফেলা যাবে না — সেটা শুধু
নির্বাচিত high-risk জেলার জন্য curated flood-risk তথ্য (lat/lon,
elevation, danger note সহ)। এই ফাইল হলো comprehensive নাম-ভিত্তিক
gazetteer, risk তথ্য ছাড়া।
"""
import json
import os

_GAZETTEER_PATH = os.path.join(os.path.dirname(__file__), "union_gazetteer.json")

_cache = None


def _load():
    global _cache
    if _cache is None:
        with open(_GAZETTEER_PATH, encoding="utf-8") as f:
            _cache = json.load(f)
    return _cache


def get_upazilas_for_district(district_bn_name):
    """জেলার (বাংলা নাম) সব উপজেলার নাম রিটার্ন করে।"""
    data = _load()
    return list(data.get(district_bn_name, {}).keys())


def get_unions_for_upazila(district_bn_name, upazila_en_name):
    """নির্দিষ্ট জেলা+উপজেলার সব real ইউনিয়ন (নাম/url সহ) রিটার্ন করে।"""
    data = _load()
    return data.get(district_bn_name, {}).get(upazila_en_name, [])


def get_all_unions_for_district(district_bn_name):
    """জেলার সব উপজেলার সব ইউনিয়ন একসাথে (upazila_name যোগ করে) রিটার্ন করে।"""
    data = _load()
    result = []
    for upazila_name, unions in data.get(district_bn_name, {}).items():
        for u in unions:
            result.append({**u, "upazila": upazila_name})
    return result


def district_count():
    return len(_load())


def total_union_count():
    return sum(len(unions) for upazilas in _load().values() for unions in upazilas.values())
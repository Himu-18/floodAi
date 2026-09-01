# FloodAI Validation — Phase 1

এই ফোল্ডারটা advisor-এর দেওয়া rigorous validation methodology অনুসরণ করে
বানানো হয়েছে (confusion matrix, precision/recall/F1, FAR, miss-rate,
lead-time, baseline-vs-FloodAI comparison — শুধু "accuracy" না)।

## ফাইল

- **stations.py** — ১২টা representative validation station (Bahadurabad,
  Aricha, Kazipur, Baghabari, Jamalpur, Goalondo, Hardinge-RB, Sureshswar,
  Kurigram, Gaibandha, Kaunia + একটা নোট: "Sirajganj" নামে আলাদা কোনো gauge
  পাওয়া যায়নি, ভবিষ্যতে BWDB পোর্টাল থেকে যাচাই করে দেখা যেতে পারে)।
- **flood_events.csv** — ৮টা বড় ঐতিহাসিক বন্যার বছর (১৯৯৮-২০২৪) ও আনুমানিক
  তারিখ-সীমা, জাতীয় পর্যায়ে। এখন এটা শুধু **fallback** — ground_truth.csv
  না থাকলেই এটা ব্যবহার হয়।
- **real_data/** — ইউজার-সংগৃহীত ৭টা real CSV (BWDB/FFWC Annual Flood
  Report সূত্রে, অন্য একটা AI-এর সহায়তায় প্রস্তুত করা)। v1 (Bahadurabad
  ১৯৮৫-২০১৫ annual peak discharge), v2 (২২ station catalog), v3 (২৭
  station-এর ১৯৯৮/২০১২ real peak water-level + danger level — সবচেয়ে
  মূল্যবান), v4 (Jamalpur annual rainfall), v6 (২০১৭/২০২০-এর ৪৮টা
  জেলা-ভিত্তিক real flood event), v7/v8 (মূলত ফাঁকা skeleton, এখনো কাজে
  লাগেনি)। ⚠️ "v5"-এর দাবি (Scribd document সূত্র) ওয়েব সার্চে যাচাই করা
  যায়নি — ব্যবহার করা হয়নি।
- **build_ground_truth.py** — v3 (station-level) ও v6 (district-level)
  মিলিয়ে একটা canonical `ground_truth.csv` বানায়। ⚠️ network লাগে না
  (static ফাইল থেকেই কাজ করে), তাই এটা Claude-এর sandbox-এই চালানো গেছে।
- **ground_truth.csv** — build_ground_truth.py-র output, ৯৮টা real entry
  (১৯৯৮, ২০১২, ২০১৭, ২০২০)। backtest_v2.py এটাকে flood_events.csv-এর
  চেয়ে বেশি অগ্রাধিকার দেয়।
- **metrics.py** — Confusion Matrix, Precision/Recall/F1, False Alarm Rate,
  Miss Rate, Lead-time summary — সব reusable ফাংশন হিসেবে।
- **baseline_model.py** — সরল "water level >= danger level হলেই flood"
  বেসলাইন (এখনো backtest_v2.py-তে সরাসরি wire করা হয়নি — সেখানে এখনো
  discharge-vs-bankfull তুলনা ব্যবহার হচ্ছে, নিচে সীমাবদ্ধতা ৩ দেখুন)।
- **backtest_v2.py** — মূল script। actual_flood label নির্ণয়ে
  অগ্রাধিকার-ক্রম: (১) ground_truth.csv-এর **station-নির্দিষ্ট** real
  observation (সবচেয়ে নির্ভুল), (২) ground_truth.csv-এর
  **district-level aggregate**, (৩) flood_events.csv-এর জাতীয়
  date-range (সবচেয়ে কম নির্ভুল fallback)।

## ⚠️ datum (vertical reference) নিয়ে একটা গুরুত্বপূর্ণ, এখনো-অসমাধিত প্রশ্ন

v3 (real_data/)-এর danger_level (সঠিকভাবে mPWD-তে label করা) আমাদের
নিজেদের flood_config.py-র danger_level-এর সাথে cross-check করে দেখা
গেছে, বহু ভিন্ন জেলায় (ঢাকা, নারায়ণগঞ্জ, দিনাজপুর, রাজশাহী, বাহাদুরাবাদ,
ময়মনসিংহ) বারবার একটা **ধারাবাহিক ~+০.৪৫ মিটার** পার্থক্য পাওয়া গেছে।
এটা coincidence মনে হচ্ছে না — বাংলাদেশের PWD (Public Works Datum) সত্যিই
mean sea level-এর ~০.৪৫-০.৪৬মি নিচে থাকে (ওয়েব সার্চে নিশ্চিত করা
হয়েছে)। এর মানে আমাদের danger_level সংখ্যাগুলো সামঞ্জস্যপূর্ণভাবে একই
datum-এ নাও থাকতে পারে। **এটা এখনো সমাধান করা হয়নি** — ব্লাইন্ডলি +০.৪৫
যোগ করা ঠিক হবে না (কিছু বড় mismatch datum না, ভুল station-তুলনার
কারণে), বরং প্রতিটা জেলার আসল data-source ধরে ধরে যাচাই করা দরকার —
basin-by-basin review-এর মতোই একটা আলাদা, systematic ভবিষ্যৎ কাজ।

## কীভাবে চালাবেন (লোকাল VS Code-এ)

```bash
cd backend/validation
python build_ground_truth.py   # network লাগে না, দ্রুত চলবে (যদি ground_truth.csv না থাকে/পুরনো হয়)
python backtest_v2.py          # network লাগবে, ৫-১৫ মিনিট
```

⚠️ **backtest_v2.py Claude-এর sandbox-এ চালানো যায় না** — Open-Meteo-র
historical archive API (`archive-api.open-meteo.com`,
`flood-api.open-meteo.com`) network allowlist-এর বাইরে। শুধু আপনার নিজের
মেশিনেই চলবে, যেখানে পূর্ণ internet access আছে। (build_ground_truth.py
আলাদা — সেটা network ছাড়াই চলে, Claude নিজেই চালিয়ে দেখেছে।)

ফলাফল সেভ হবে `backtest_v2_results.csv`-এ, আর টার্মিনালে চূড়ান্ত metrics
(Precision/Recall/F1/FAR/Miss-rate) প্রিন্ট হবে — FloodAI বনাম simple
baseline পাশাপাশি।

## গুরুত্বপূর্ণ সীমাবদ্ধতা (সততার সাথে স্বীকার করা)

1. **এটা true lead-time forecast backtest না** — ২০২১-পূর্ববর্তী ঘটনার
   জন্য "সেই সময় আসলে forecast কী বলত" এই তথ্য Open-Meteo দেয় না, শুধু
   reanalysis (আসলে কী ঘটেছিল) দেয়। ২০২১+ ঘটনার জন্য Open-Meteo-র
   "Historical Forecast API" ব্যবহার করলে সত্যিকারের lead-time measure
   করা সম্ভব — এটা ভবিষ্যতের কাজ।

2. **actual_flood label এখন অনেক বেশি নির্ভুল, কিন্তু এখনো আংশিক** —
   ground_truth.csv দিয়ে ১৯৯৮/২০১২ (station-level) ও ২০১৭/২০২০
   (district-level) সঠিক real label পাওয়া যাচ্ছে। কিন্তু ২০০৪, ২০০৭,
   ২০১৯, ২০২২, ২০২৪ এখনো flood_events.csv-এর কম নির্ভুল জাতীয় date-range
   অনুমানের উপর নির্ভরশীল।

3. **Baseline এখনো water-level-ভিত্তিক না, discharge-ভিত্তিক** — v3-এ
   real water-level ডেটা থাকলেও, সেটা শুধু ১৯৯৮/২০১২-র জন্য (দৈনিক
   time-series না, শুধু annual peak) — একটা পূর্ণাঙ্গ water-level-ভিত্তিক
   baseline চালাতে দৈনিক water-level history লাগবে যেটা এখনো নেই।

4. **flood_events.csv-এর তারিখ কিছু ক্ষেত্রে আনুমানিক** — বিশেষত ২০১৯,
   এবং যেসব বছর ground_truth.csv কভার করে না।

## পরের ধাপ

- backtest_v2.py লোকালি চালিয়ে প্রথম ফলাফল দেখা
- ফলাফল ভালো লাগলে (FloodAI বেসলাইনকে হারালে), ১২ থেকে বাড়িয়ে আরও
  station/জেলা যোগ করা (advisor-এর phase-vise scale-up পরিকল্পনা, v2
  station catalog থেকে candidate পাওয়া যাবে)
- datum (PWD vs MSL) প্রশ্নটা basin-by-basin ভাবে যাচাই করা
- বাকি বছরগুলোর (২০০৪, ২০০৭, ২০১৯, ২০২২, ২০২৪) জন্য FFWC-র station/
  district-নির্দিষ্ট real record জোগাড় করে ground_truth.csv সম্প্রসারণ
- ২০২১+ ঘটনার জন্য Historical Forecast API দিয়ে সত্যিকারের lead-time
  measure করা

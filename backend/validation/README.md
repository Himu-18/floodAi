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
  তারিখ-সীমা। কিছু বছরের (বিশেষত ২০১৯) তারিখ আনুমানিক — চালানোর আগে
  FFWC/BWDB bulletin দিয়ে নির্দিষ্ট করে নেওয়া ভালো।
- **metrics.py** — Confusion Matrix, Precision/Recall/F1, False Alarm Rate,
  Miss Rate, Lead-time summary — সব reusable ফাংশন হিসেবে।
- **baseline_model.py** — সবচেয়ে সরল "water level >= danger level হলেই
  flood" বেসলাইন (এখনো backtest_v2.py-তে wire করা হয়নি, কারণ real
  historical water-level time series লাগবে যেটা এখনো integrate করা হয়নি
  — নিচে "পরের ধাপ" দেখুন)।
- **backtest_v2.py** — মূল script। প্রতিটা station × প্রতিটা flood-event-এর
  কিছু sample তারিখে real historical rainfall/discharge/soil-moisture
  এনে predict_flood() ও discharge-ভিত্তিক baseline (bankfull discharge-এর
  সাথে তুলনা) দুটো দিয়েই prediction নিয়ে, actual flood period-এর সাথে
  মিলিয়ে metrics বের করে।

## কীভাবে চালাবেন (লোকাল VS Code-এ)

```bash
cd backend/validation
python backtest_v2.py
```

⚠️ **এটা Claude-এর sandbox-এ চালানো যায় না** — Open-Meteo-র historical
archive API (`archive-api.open-meteo.com`, `flood-api.open-meteo.com`)
network allowlist-এর বাইরে। শুধু আপনার নিজের মেশিনেই চলবে, যেখানে পূর্ণ
internet access আছে।

চলতে সময় লাগবে — ১২ station × ৮ event × ~৩-৪টা sample date × delay ≈
কয়েকশ API call, ৫-১৫ মিনিট মতো লাগতে পারে।

ফলাফল সেভ হবে `backtest_v2_results.csv`-এ, আর টার্মিনালে চূড়ান্ত metrics
(Precision/Recall/F1/FAR/Miss-rate) প্রিন্ট হবে — FloodAI বনাম simple
baseline পাশাপাশি।

## গুরুত্বপূর্ণ সীমাবদ্ধতা (সততার সাথে স্বীকার করা)

1. **এটা true lead-time forecast backtest না** — ২০২১-পূর্ববর্তী ঘটনার
   জন্য "সেই সময় আসলে forecast কী বলত" এই তথ্য Open-Meteo দেয় না, শুধু
   reanalysis (আসলে কী ঘটেছিল) দেয়। তাই এই ভার্সন classification accuracy
   (Precision/Recall/F1) মাপে, ঘণ্টার হিসেবে lead-time না। ২০২১+ ঘটনার
   জন্য Open-Meteo-র "Historical Forecast API" ব্যবহার করলে সত্যিকারের
   lead-time measure করা সম্ভব — এটা ভবিষ্যতের কাজ।

2. **actual_flood label event-level, station-level না** — অর্থাৎ পুরো
   দেশে flood period চলাকালীন সময়কে "flood" ধরা হচ্ছে, কিন্তু প্রতিটা
   নির্দিষ্ট station-এ ঠিক সেই তারিখেই local flooding হয়েছিল কিনা আলাদাভাবে
   যাচাই করা হয়নি। এটা false-positive/false-negative-এর সংখ্যা কিছুটা
   বিকৃত করতে পারে। আরও নির্ভুল করতে FFWC-র station-নির্দিষ্ট historical
   water-level bulletin লাগবে।

3. **Baseline এখনো water-level-ভিত্তিক না, discharge-ভিত্তিক** —
   baseline_model.py-তে water-level threshold logic লেখা আছে, কিন্তু
   এখনো কোনো real historical water-level time series সংগ্রহ করা হয়নি,
   তাই backtest_v2.py আপাতত discharge-vs-bankfull-reference তুলনা করছে
   (একই ধরনের সরল "থ্রেশহোল্ড ক্রস করলেই flood" যুক্তি, কিন্তু discharge
   এককে)। FFWC-র water-level archive পেলে baseline_model.py-র আসল
   water-level ভার্সন সহজেই wire করা যাবে।

4. **flood_events.csv-এর তারিখ কিছু ক্ষেত্রে আনুমানিক** — বিশেষত ২০১৯।

## পরের ধাপ

- backtest_v2.py লোকালি চালিয়ে প্রথম ফলাফল দেখা
- ফলাফল ভালো লাগলে (FloodAI বেসলাইনকে হারালে), ১২ থেকে বাড়িয়ে আরও
  station/জেলা যোগ করা (advisor-এর phase-vise scale-up পরিকল্পনা)
- FFWC-র water-level historical archive সংগ্রহ করে real water-level-ভিত্তিক
  baseline ও station-নির্দিষ্ট actual_flood label দিয়ে নির্ভুলতা বাড়ানো
- ২০২১+ ঘটনার জন্য Historical Forecast API দিয়ে সত্যিকারের lead-time
  measure করা

# ============================================================
# FloodAI — migrate_flood_config.py
#
# একবার চালানোর script — district_profiles/ থেকে verified cn আর
# risk_category বের করে flood_config.py-তে বসিয়ে দেয়।
#
# ⚠️ শুধু cn আর risk_category বদলায় — reference_discharge/danger_level/
# flood_type কিছুই বদলায় না (flood_type-এর ক্ষেত্রে বেশ কয়েকটা misclassification
# পাওয়া গেছে — Feni/Brahmanbaria — কিন্তু সেগুলো manual review দরকার, তাই এই
# script স্বয়ংক্রিয়ভাবে বদলায় না)।
#
# চালানোর আগে flood_config.py-র একটা backup রাখা হয় (.bak এক্সটেনশনে)।
# ============================================================

import re
import shutil
import sys
import os

sys.path.insert(0, os.path.dirname(__file__))

from data import district_profiles_loader as dpl

FLOOD_CONFIG_PATH = os.path.join(os.path.dirname(__file__), "data", "flood_config.py")


def main():
    dpl.reload()
    districts_covered = dpl.get_all_districts_covered()
    print(f"district_profiles/-এ {len(districts_covered)}টা জেলা পাওয়া গেছে।")

    shutil.copy(FLOOD_CONFIG_PATH, FLOOD_CONFIG_PATH + ".bak")
    print(f"✅ Backup রাখা হলো: {FLOOD_CONFIG_PATH}.bak")

    with open(FLOOD_CONFIG_PATH, encoding="utf-8") as f:
        content = f.read()

    changed_count = 0
    skipped_count = 0

    for district in districts_covered:
        correction = dpl.get_primary_correction(district)
        if not correction:
            continue

        new_cn = correction.get("cn")
        new_risk = correction.get("risk_category")

        # প্রতিটা জেলার entry শুরু হয় "জেলার_নাম": { ... } দিয়ে — regex দিয়ে
        # শুধু সেই জেলার entry-র মধ্যে cn/risk বদলানো হচ্ছে, বাকি জেলা অস্পৃশ্য থাকে।
        pattern = re.compile(
            r'("' + re.escape(district) + r'":\s*\{[^}]*?\'cn\':\s*)(\d+)',
            re.DOTALL,
        )
        risk_pattern = re.compile(
            r'("' + re.escape(district) + r'":\s*\{[^}]*?\'risk\':\s*\')([^\']+)(\')',
            re.DOTALL,
        )

        made_change = False

        if new_cn is not None:
            def _cn_repl(m, new_cn=new_cn):
                return f"{m.group(1)}{new_cn}"
            new_content, n = pattern.subn(_cn_repl, content, count=1)
            if n > 0 and new_content != content:
                content = new_content
                made_change = True

        if new_risk:
            def _risk_repl(m, new_risk=new_risk):
                return f"{m.group(1)}{new_risk}{m.group(3)}"
            new_content, n = risk_pattern.subn(_risk_repl, content, count=1)
            if n > 0 and new_content != content:
                content = new_content
                made_change = True

        if made_change:
            changed_count += 1
            log_parts = []
            if new_cn is not None:
                log_parts.append(f"cn→{new_cn}")
            if new_risk:
                log_parts.append(f"risk→{new_risk}")
            print(f"  ✅ {district}: {', '.join(log_parts)}")
        else:
            skipped_count += 1

    with open(FLOOD_CONFIG_PATH, "w", encoding="utf-8") as f:
        f.write(content)

    print()
    print(f"সারাংশ: {changed_count}টা জেলা আপডেট হলো, {skipped_count}টা স্কিপ হলো (কোনো পরিবর্তন দরকার ছিল না বা match পাওয়া যায়নি)।")
    print(f"⚠️ flood_type পরিবর্তন করা হয়নি — Feni/Brahmanbaria-র মতো misclassification manual review করে বদলাতে হবে।")


if __name__ == "__main__":
    main()
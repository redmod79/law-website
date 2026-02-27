#!/usr/bin/env python3
"""
build_site.py — Build the Law of God study series website.

Scans D:/bible/bible-studies/law-* for all 31 studies,
copies files into docs/studies/, generates mkdocs.yml and index.md,
and copies shared assets from etc-website.
"""

import os
import re
import shutil
from pathlib import Path

# ── Paths ──────────────────────────────────────────────────────────
PROJECT_ROOT = Path(__file__).resolve().parent
STUDIES_SRC = Path("D:/bible/bible-studies")
ETC_WEBSITE = Path("D:/bible/etc-website")
DOCS = PROJECT_ROOT / "docs"
DOCS_STUDIES = DOCS / "studies"

# ── Study metadata ─────────────────────────────────────────────────
# Short titles for navigation (derived from CONCLUSION.md headings, shortened)
SHORT_TITLES = {
    "law-01": "What Is God's Moral Law?",
    "law-02": "The Moral Law Before Sinai",
    "law-03": "Decalogue vs. Later Laws",
    "law-04": "Ceremonial Laws",
    "law-05": "Civil/Judicial Laws",
    "law-06": "Hebrew Law Vocabulary",
    "law-07": "The Law of Moses",
    "law-08": "What Was Abolished at the Cross?",
    "law-09": "Old Covenant and New Covenant",
    "law-10": "New Covenant and the Moral Law",
    "law-11": "The Law Written on Hearts",
    "law-12": "Matthew 5:17-20",
    "law-13": "Jesus and the Sabbath",
    "law-14": "Jesus's Law Teachings",
    "law-15": "The Jerusalem Council (Acts 15)",
    "law-16": "Paul and the Law in Romans",
    "law-17": "Paul and the Law in Galatians",
    "law-18": "Hebrews 8-10",
    "law-19": "2 Corinthians 3",
    "law-20": "NT Greek Law Vocabulary",
    "law-21": "NT Vocab: Law Categories",
    "law-22": "James and the Law",
    "law-23": "The Law of Christ",
    "law-24": "Weekly vs. Ceremonial Sabbaths",
    "law-25": "Sabbath: Moral or Ceremonial?",
    "law-26": "Sabbath Shadow Passages",
    "law-27": "Is the Sabbath Still Binding?",
    "law-32": "Lunar Sabbaths",
    "law-33": "Calendar Continuity",
    "law-28": "Commandments in Revelation",
    "law-29": "What Continues, What Ceased",
    "law-30": "Romans 10:4 — What Does Telos Mean?",
    "law-31": "Comprehensive Synthesis",
}

# Full question/title for the index table
FULL_TITLES = {
    "law-01": "What Is God's Moral Law? Basis, Nature, and Scope",
    "law-02": "What Evidence Exists for the Moral Law Operating from Creation to Sinai?",
    "law-03": "How Does the Exodus Narrative Distinguish the Decalogue from the Laws Given Afterward?",
    "law-04": "What Are the Ceremonial/Ritual Laws and How Do They Differ from the Moral Law?",
    "law-05": "Civil/Judicial Laws in the Pentateuch and Their Relationship to Moral and Ceremonial Categories",
    "law-06": "What Do Torah, Mitsvah, Choq, Mishpat, Edut, Piqqud, and Chuqqah Mean?",
    "law-07": 'What Does "The Law of Moses" Refer To?',
    "law-08": "What Was Abolished at the Cross?",
    "law-09": "What Is the Old Covenant and What Is the New Covenant?",
    "law-10": "Does the New Covenant Abolish or Establish the Moral Law?",
    "law-11": 'What Specific Law Is "My Law" Written on Hearts in Jeremiah 31:33 / Hebrews 8:10?',
    "law-12": 'What Does Jesus Mean by "Not Come to Destroy but to Fulfil" in Matthew 5:17-20?',
    "law-13": "What Do Jesus's Sabbath Actions and Teachings Reveal About the Sabbath's Continuing Validity?",
    "law-14": "What Did Jesus Specifically Teach About the Law and Commandments?",
    "law-15": "What Did the Jerusalem Council Decide About the Law?",
    "law-16": "What Does Paul Teach About the Law in Romans?",
    "law-17": "What Is Paul Arguing in Galatians Regarding the Law?",
    "law-18": "Hebrews 8-10: Priesthood, Covenant, and Law",
    "law-19": "2 Corinthians 3: Were the Ten Commandments 'Done Away'?",
    "law-20": "NT Greek Law Vocabulary: Nomos, Entole, Dogma, and Related Terms",
    "law-21": "How Does NT Vocabulary Distinguish Moral, Ceremonial, and Civil Law?",
    "law-22": "James and the Law: The Royal Law and the Law of Liberty",
    "law-23": 'The "Law of Christ" and Related NT Law Phrases',
    "law-24": "Weekly Sabbath vs. Ceremonial Sabbaths: Are They the Same?",
    "law-25": "Is the Sabbath Moral or Ceremonial?",
    "law-26": "Do Colossians 2:16-17 and Romans 14:5 Abolish the Weekly Sabbath?",
    "law-27": "Is the Seventh-Day Sabbath Still Binding Today?",
    "law-32": "Does the Bible Tie the Weekly Sabbath to the Lunar Cycle?",
    "law-33": "Can We Identify Which Day of the Modern Week Is the Biblical Seventh-Day Sabbath?",
    "law-28": "What Commandments Are in Revelation?",
    "law-29": "What Specific Laws Continue and What Specific Laws Ceased?",
    "law-30": "What Does Telos Mean in Romans 10:4?",
    "law-31": "The Law of God: Comprehensive Synthesis of Studies 1-30",
}

# Tier groupings
TIERS = [
    {
        "name": "Tier 1 -- Foundations",
        "desc": "What IS the moral law? Categories, distinctions, and the foundation for everything that follows.",
        "studies": ["law-01", "law-02", "law-03", "law-04", "law-05"],
    },
    {
        "name": "Tier 2 -- Vocabulary",
        "desc": "What do the Hebrew law words actually mean?",
        "studies": ["law-06", "law-07"],
    },
    {
        "name": "Tier 3 -- Abolished or Established?",
        "desc": "What happened to the law at the cross, in the covenants, and in the heart?",
        "studies": ["law-08", "law-09", "law-10", "law-11"],
    },
    {
        "name": "Tier 4 -- Jesus and the Law",
        "desc": "What did Jesus teach about the law through His words and actions?",
        "studies": ["law-12", "law-13", "law-14"],
    },
    {
        "name": "Tier 5 -- Apostolic Teaching",
        "desc": "What do the apostles teach about the law in Acts, Romans, Galatians, Hebrews, and 2 Corinthians?",
        "studies": ["law-15", "law-16", "law-17", "law-18", "law-19"],
    },
    {
        "name": "Tier 6 -- NT Vocabulary",
        "desc": "What do the Greek law terms mean, and how do James and Paul use them?",
        "studies": ["law-20", "law-21", "law-22", "law-23"],
    },
    {
        "name": "Tier 7 -- The Sabbath",
        "desc": "Is the weekly Sabbath moral or ceremonial? Do the 'shadow' passages abolish it?",
        "studies": ["law-24", "law-25", "law-26", "law-27", "law-32", "law-33"],
    },
    {
        "name": "Tier 8 -- Synthesis",
        "desc": "Bringing all the evidence together.",
        "studies": ["law-28", "law-29", "law-30", "law-31"],
    },
]

# Standard study files (in display order for nav)
STUDY_FILES = [
    ("CONCLUSION.md", None),           # Landing page (no label = index page)
    ("03-analysis.md", "Analysis"),
    ("02-verses.md", "Verses"),
    ("04-word-studies.md", "Word Studies"),
    ("01-topics.md", "Topics"),
    ("PROMPT.md", "Research Scope"),
]

# Raw data file display names (map filename stem to nice name)
RAW_DATA_NAMES = {
    "concept-context": "Concept Context",
    "existing-studies": "Existing Studies",
    "greek-parsing": "Greek Parsing",
    "hebrew-parsing": "Hebrew Parsing",
    "naves-topics": "Nave's Topics",
    "parallels": "Cross-Testament Parallels",
    "strongs-lookups": "Strong's Lookups",
    "strongs": "Strong's Lookups",
    "web-research": "Web Research",
    "grammar-references": "Grammar References",
    "evidence-tally": "Evidence Tally",
    "study-db-queries": "Study DB Queries",
}


def get_raw_data_name(filename: str) -> str:
    """Get a display name for a raw-data file."""
    stem = Path(filename).stem
    if stem in RAW_DATA_NAMES:
        return RAW_DATA_NAMES[stem]
    # Fallback: convert kebab-case to Title Case
    return stem.replace("-", " ").title()


def find_study_folders() -> list[tuple[str, Path]]:
    """Find all law-NN-* folders in the studies source directory."""
    folders = []
    for d in sorted(STUDIES_SRC.iterdir()):
        if d.is_dir() and re.match(r"law-\d{2}-", d.name):
            slug = d.name  # e.g. "law-01-gods-moral-law"
            num = slug.split("-")[1]  # e.g. "01"
            key = f"law-{num}"  # e.g. "law-01"
            folders.append((key, d))
    return folders


def copy_study(key: str, src: Path, preserved_simples: dict):
    """Copy a study folder into docs/studies/."""
    dest = DOCS_STUDIES / src.name
    dest.mkdir(parents=True, exist_ok=True)

    # Copy standard files
    for fname, _ in STUDY_FILES:
        src_file = src / fname
        if src_file.exists():
            shutil.copy2(src_file, dest / fname)

    # Restore preserved conclusion-simple.md, or copy from source
    simple_path = dest / "conclusion-simple.md"
    if src.name in preserved_simples:
        simple_path.write_text(preserved_simples[src.name], encoding="utf-8")
    else:
        simple_src = src / "conclusion-simple.md"
        if simple_src.exists():
            shutil.copy2(simple_src, dest / "conclusion-simple.md")

    # Copy METADATA.yaml if present
    meta = src / "METADATA.yaml"
    if meta.exists():
        shutil.copy2(meta, dest / "METADATA.yaml")

    # Copy raw-data/
    raw_src = src / "raw-data"
    if raw_src.exists() and raw_src.is_dir():
        raw_dest = dest / "raw-data"
        shutil.copytree(raw_src, raw_dest, dirs_exist_ok=True)

    return dest


def build_nav_entry(key: str, slug: str) -> dict:
    """Build a nav entry for one study."""
    num = key.split("-")[1]
    short_title = SHORT_TITLES.get(key, slug)
    nav_title = f"{num} -- {short_title}"

    dest = DOCS_STUDIES / slug
    items = []

    # Landing page: conclusion-simple.md if it exists, else CONCLUSION.md
    simple = dest / "conclusion-simple.md"
    conclusion = dest / "CONCLUSION.md"
    if simple.exists():
        items.append(f"studies/{slug}/conclusion-simple.md")
        # Add full Conclusion as a labeled entry
        if conclusion.exists():
            items.append({"Conclusion": f"studies/{slug}/CONCLUSION.md"})
    elif conclusion.exists():
        items.append(f"studies/{slug}/CONCLUSION.md")

    # Other standard files (skip CONCLUSION.md, already handled above)
    for fname, label in STUDY_FILES:
        if label is None:
            continue  # Skip CONCLUSION.md, already added above
        fpath = dest / fname
        if fpath.exists():
            items.append({label: f"studies/{slug}/{fname}"})

    # Raw data files
    raw_dir = dest / "raw-data"
    if raw_dir.exists() and raw_dir.is_dir():
        raw_items = []
        for f in sorted(raw_dir.iterdir()):
            if f.is_file() and f.suffix == ".md":
                display = get_raw_data_name(f.name)
                raw_items.append({display: f"studies/{slug}/raw-data/{f.name}"})
        if raw_items:
            items.append({"Raw Data": raw_items})

    return {nav_title: items}


def generate_mkdocs_yml(study_folders: list[tuple[str, Path]]):
    """Generate mkdocs.yml."""
    # Build study nav entries grouped by tier
    slug_map = {key: src.name for key, src in study_folders}

    lines = []
    lines.append('site_name: "The Law of God"')
    lines.append("site_description: A comprehensive 33-study biblical investigation examining what Scripture teaches about the moral law, ceremonial law, the Sabbath, and the relationship between Old and New Testaments.")
    lines.append("")
    lines.append("theme:")
    lines.append("  name: material")
    lines.append("  palette:")
    lines.append("    - scheme: default")
    lines.append("      primary: indigo")
    lines.append("      accent: deep orange")
    lines.append("      toggle:")
    lines.append("        icon: material/brightness-7")
    lines.append("        name: Switch to dark mode")
    lines.append("    - scheme: slate")
    lines.append("      primary: indigo")
    lines.append("      accent: deep orange")
    lines.append("      toggle:")
    lines.append("        icon: material/brightness-4")
    lines.append("        name: Switch to light mode")
    lines.append("  features:")
    lines.append("    - navigation.instant")
    lines.append("    - navigation.tracking")
    lines.append("    - navigation.tabs")
    lines.append("    - navigation.sections")
    lines.append("    - navigation.top")
    lines.append("    - navigation.indexes")
    lines.append("    - search.suggest")
    lines.append("    - search.highlight")
    lines.append("    - content.tabs.link")
    lines.append("    - toc.follow")
    lines.append("  font:")
    lines.append("    text: Roboto")
    lines.append("    code: Roboto Mono")
    lines.append("")
    lines.append("plugins:")
    lines.append("  - search")
    lines.append("")
    lines.append("markdown_extensions:")
    lines.append("  - abbr")
    lines.append("  - admonition")
    lines.append("  - attr_list")
    lines.append("  - def_list")
    lines.append("  - footnotes")
    lines.append("  - md_in_html")
    lines.append("  - tables")
    lines.append("  - toc:")
    lines.append("      permalink: true")
    lines.append("  - pymdownx.details")
    lines.append("  - pymdownx.superfences")
    lines.append("  - pymdownx.highlight:")
    lines.append("      anchor_linenums: true")
    lines.append("  - pymdownx.inlinehilite")
    lines.append("  - pymdownx.tabbed:")
    lines.append("      alternate_style: true")
    lines.append("  - pymdownx.tasklist:")
    lines.append("      custom_checkbox: true")
    lines.append("")
    lines.append("extra:")
    lines.append("  social:")
    lines.append("    - icon: fontawesome/solid/book-bible")
    lines.append("      link: /")
    lines.append("")
    lines.append("extra_javascript:")
    lines.append("  - javascripts/verse-popup.js")
    lines.append("  - javascripts/study-breadcrumbs.js")
    lines.append("  - javascripts/external-links.js")
    lines.append("")
    lines.append("extra_css:")
    lines.append("  - stylesheets/extra.css")
    lines.append("")
    lines.append("nav:")
    lines.append("  - Home: index.md")
    lines.append("  - Studies:")
    lines.append("")

    # Study tiers nested under "Studies" tab
    for tier in TIERS:
        lines.append(f"    # ── {tier['name']} ──")
        lines.append(f'    - "{tier["name"]}":')
        lines.append("")
        for key in tier["studies"]:
            slug = slug_map.get(key)
            if not slug:
                continue
            nav_entry = build_nav_entry(key, slug)
            # Serialize this nav entry
            for title, items in nav_entry.items():
                lines.append(f'      - "{title}":')
                for item in items:
                    if isinstance(item, str):
                        lines.append(f"        - {item}")
                    elif isinstance(item, dict):
                        for label, val in item.items():
                            if isinstance(val, list):
                                # Nested (Raw Data)
                                lines.append(f"        - {label}:")
                                for sub in val:
                                    if isinstance(sub, dict):
                                        for slabel, spath in sub.items():
                                            lines.append(f'          - "{slabel}": {spath}')
                                    else:
                                        lines.append(f"          - {sub}")
                            else:
                                lines.append(f"        - {label}: {val}")
        lines.append("")

    lines.append("  - Methodology: methodology.md")
    lines.append('  - "Tools & Process": tools.md')
    lines.append('  - "Master Evidence": master-evidence.md')

    yml_path = PROJECT_ROOT / "mkdocs.yml"
    yml_path.write_text("\n".join(lines) + "\n", encoding="utf-8")
    print(f"  Generated {yml_path}")


def generate_index_md():
    """Generate docs/index.md."""
    content = []

    content.append("# The Law of God: What Does the Bible Say?")
    content.append("")
    content.append("*A comprehensive 33-study biblical investigation examining every major text, word, and argument bearing on the moral law, ceremonial law, the Sabbath, and what continues under the New Covenant.*")
    content.append("")
    content.append("---")
    content.append("")
    content.append("## The Question")
    content.append("")
    content.append('Christians hold differing views on the role of the Old Testament law today. Some argue the moral law (including the Ten Commandments and the Sabbath) continues in full force under the New Covenant. Others argue the entire Mosaic law was abolished at the cross. Rather than assuming either position, this series investigates the biblical evidence from the ground up across 33 studies.')
    content.append("")
    content.append("## The Approach")
    content.append("")
    content.append("Each study is a genuine investigation. The agents gathered ALL relevant evidence, presented what each side claims, and let the biblical text speak for itself. No study presupposed its conclusion. Evidence was classified into hierarchical tiers:")
    content.append("")
    content.append("- **Explicit (E):** What the text directly says -- a quote or close paraphrase")
    content.append("- **Necessary Implication (N):** What unavoidably follows from explicit statements")
    content.append("- **Inference** (four types):")
    content.append("    - **I-A (Evidence-Extending):** Systematizes E/N items using only the text's own vocabulary")
    content.append("    - **I-B (Competing-Evidence):** Both sides cite E/N support; resolved by Scripture-interprets-Scripture")
    content.append("    - **I-C (Compatible External):** External reasoning that does not contradict E/N")
    content.append("    - **I-D (Counter-Evidence External):** External concepts that require overriding E/N statements")
    content.append("")
    content.append("**Hierarchy:** E > N > I-A > I-B (resolved by SIS) > I-C > I-D")
    content.append("")
    content.append("[**Read the Methodology**](methodology.md){ .md-button }")
    # Link to simple conclusion if it exists, else full conclusion
    synth_simple = DOCS_STUDIES / "law-31-comprehensive-synthesis" / "conclusion-simple.md"
    if synth_simple.exists():
        content.append("[**Skip to the Final Synthesis**](studies/law-31-comprehensive-synthesis/conclusion-simple.md){ .md-button .md-button--primary }")
    else:
        content.append("[**Skip to the Final Synthesis**](studies/law-31-comprehensive-synthesis/CONCLUSION.md){ .md-button .md-button--primary }")
    content.append("")
    content.append("---")
    content.append("")
    content.append("## The 33 Studies")
    content.append("")

    # Generate study tables grouped by tier
    for tier in TIERS:
        content.append(f"### {tier['name']}")
        content.append("")
        content.append(tier["desc"])
        content.append("")
        content.append("| # | Study | Question |")
        content.append("|---|-------|----------|")
        for key in tier["studies"]:
            num = key.split("-")[1]
            short = SHORT_TITLES.get(key, key)
            full = FULL_TITLES.get(key, short)
            # Find the slug
            slug = None
            for d in sorted(STUDIES_SRC.iterdir()):
                if d.is_dir() and d.name.startswith(f"{key}-"):
                    slug = d.name
                    break
            if slug:
                # Link to simple conclusion if it exists
                simple_path = DOCS_STUDIES / slug / "conclusion-simple.md"
                if simple_path.exists():
                    link = f"studies/{slug}/conclusion-simple.md"
                else:
                    link = f"studies/{slug}/CONCLUSION.md"
                content.append(f"| {num} | [{short}]({link}) | {full} |")
            else:
                content.append(f"| {num} | {short} | {full} |")
        content.append("")

    content.append("---")
    content.append("")
    content.append("## What Each Study Contains")
    content.append("")
    content.append("Every study includes multiple layers of research, all accessible through the navigation:")
    content.append("")
    content.append("| File | Contents |")
    content.append("|------|----------|")
    content.append("| **Simple Conclusion** | A plain-language summary of the study's findings -- no technical jargon or evidence tables |")
    content.append("| **Conclusion** | The final evidence classification with Explicit/Necessary Implication/Inference tables, I-B resolutions, tally, and \"What CAN/CANNOT Be Said\" |")
    content.append("| **Analysis** | Verse-by-verse analysis, identified patterns, connections between passages, both-sides arguments |")
    content.append("| **Verses** | Full KJV text for every passage examined, organized thematically |")
    content.append("| **Word Studies** | Hebrew and Greek word studies with Strong's numbers, semantic ranges, and parsing |")
    content.append("| **Topics** | Nave's Topical Bible entries and key research findings |")
    content.append("| **Research Scope** | The original research question and scope that guided the investigation |")
    content.append("| **Raw Data** | Nave's topic output, Strong's lookups, Greek/Hebrew parsing, cross-testament parallels, concept context |")
    content.append("")
    content.append("---")
    content.append("")
    content.append("## Evidence Summary (from Study 31)")
    content.append("")
    content.append("Study 31 synthesized the evidence from Studies 1-30 on the central question of what continues and what was abolished. The synthesis classified **810 unique evidence items** across those studies. Studies 32-33 are supplemental investigations addressing the Sabbath specifically (lunar sabbaths and calendar continuity) and are not part of the moral-law-continues-vs-abolished analysis.")
    content.append("")
    content.append("### Positional Distribution")
    content.append("")
    content.append("| Tier | Continues | Abolished | Neutral/Shared | Total |")
    content.append("|------|-----------|-----------|----------------|-------|")
    content.append("| E (Explicit) | 146 | 0 | 367 | 513 |")
    content.append("| N (Necessary Implication) | 73 | 0 | 72 | 145 |")
    content.append("| I-A (Evidence-Extending) | 63 | 0 | 3 | 66 |")
    content.append("| I-B (Competing-Evidence) | 18 | 22 | 7 | 47 |")
    content.append("| I-C (Compatible External) | 1 | 1 | 3 | 5 |")
    content.append("| I-D (Counter-Evidence External) | 0 | 34 | 0 | 34 |")
    content.append("| **Total** | **301** | **57** | **452** | **810** |")
    content.append("")
    content.append("Not a single explicit statement (E-tier) or necessary implication (N-tier) in the entire 810-item evidence base was classified as supporting abolition of the moral law. All 219 E+N positional items support \"Continues.\" The Abolished position's 57 items exist entirely at the inference level (I-B and I-D).")
    content.append("")
    synth_simple2 = DOCS_STUDIES / "law-31-comprehensive-synthesis" / "conclusion-simple.md"
    if synth_simple2.exists():
        content.append("[**Read the Full Synthesis**](studies/law-31-comprehensive-synthesis/conclusion-simple.md){ .md-button .md-button--primary }")
    else:
        content.append("[**Read the Full Synthesis**](studies/law-31-comprehensive-synthesis/CONCLUSION.md){ .md-button .md-button--primary }")

    content.append("")
    content.append("---")
    content.append("")
    content.append("## Related Studies")
    content.append("")
    content.append("These companion sites use the same tool-driven research methodology:")
    content.append("")
    content.append("| Site | Description |")
    content.append("|------|-------------|")
    content.append("| [**The Final Fate of the Wicked**](https://redmod79.github.io/etc-website/) | A 19-study investigation examining every major text, word, and argument about the final fate of the wicked -- eternal conscious torment vs. conditional immortality. 597 evidence items classified. |")
    content.append("| [**Genesis 6: The \"Sons of God\" Question**](https://redmod79.github.io/genesis-6-website/) | Who are the \"sons of God\" in Genesis 6:1-4? A 10-part report built on 28 supporting studies examines the angel view vs. the godly human view using explicit biblical evidence. |")
    content.append("| [**Bible Study Collection**](https://redmod79.github.io/bible-topics-website/) | Standalone Bible studies on various topics -- genealogies, prophecy, biblical history, and more. Each study is a self-contained investigation produced by the same three-agent pipeline. |")

    index_path = DOCS / "index.md"
    index_path.write_text("\n".join(content) + "\n", encoding="utf-8")
    print(f"  Generated {index_path}")


def generate_tools_md():
    """Generate docs/tools.md adapted from etc-website."""
    content = """# Research Tools & Process

*This page describes the automated research system and investigative methodology that produced the 31 studies in this series.*

---

## Investigative Stance

Each study is produced by an agent that functions as an **investigator, not an advocate.** This distinction governs every step of the process:

- **Gather evidence from all sides.** If a passage is cited by those who argue the moral law continues, examine it honestly. If a passage is cited by those who argue it was abolished, examine it honestly.
- **Do not assume a conclusion before examining the evidence.** The conclusion emerges FROM the evidence, not the reverse.
- **State what the text says, not opinions about it.** The agent does not use editorial characterizations like "genuine tension," "strongest argument," or "non-intuitive reading." It states what each passage says and what each interpretive position infers from it.
- **Never use language like "irrefutable," "obviously," or "clearly proves."** Use "the text states," "this is consistent with."

---

## How the Studies Were Produced

Each study was generated by a multi-agent pipeline, a Claude Code skill that answers Bible questions through tool-driven research. The pipeline ensures that:

- **Scope comes from tools, not training knowledge.** The AI does not decide which verses are relevant based on what it was trained on. Instead, tools search topical dictionaries, concordances, and semantic indexes to discover what Scripture says about the topic.
- **Research and analysis are separated.** The agent that gathers data is not the same agent that draws conclusions. This prevents confirmation bias.
- **Every claim is traceable.** Raw tool output is preserved in each study's `raw-data/` folder, so every finding can be verified against its source.

### The Three-Agent Pipeline

```
Phase 1: Scoping Agent
   | Discovers topics, verses, Strong's numbers, related studies
   | Writes PROMPT.md (the research brief)

Phase 2: Research Agent
   | Reads PROMPT.md
   | Retrieves all verse text, runs parallels, word studies, parsing
   | Writes 01-topics.md, 02-verses.md, 04-word-studies.md
   | Saves raw tool output to raw-data/

Phase 3: Analysis Agent
   | Reads clean research files
   | Applies the evidence classification methodology
   | Writes 03-analysis.md and CONCLUSION.md
```

**Why three agents instead of one?**

- The **scoping agent** prevents training-knowledge bias. Scope comes from tool discovery, not from what the AI "knows" about theology.
- The **research agent** gets a fresh context window dedicated to data gathering. This maximizes the amount of data it can collect without running out of context.
- The **analysis agent** gets a fresh context window loaded with clean, organized research. This maximizes its capacity for synthesis and careful reasoning.

---

## The Study Files

Each study directory contains these files, produced by the pipeline:

| File | Produced By | Contents |
|------|-------------|----------|
| `PROMPT.md` | Scoping Agent | The research brief: tool-discovered topics, verses, Strong's numbers, related studies, and focus areas |
| `01-topics.md` | Research Agent | Nave's Topical Bible entries with all verse references for each topic |
| `02-verses.md` | Research Agent | Full KJV text for every verse examined, organized thematically |
| `04-word-studies.md` | Research Agent | Strong's concordance data: Hebrew/Greek words, definitions, translation statistics, verse occurrences |
| `raw-data/` | Research Agent | Raw tool output archived by category (Strong's lookups, parsing, parallels, LXX mapping, verse context, etc.) |
| `03-analysis.md` | Analysis Agent | Verse-by-verse analysis with full evidence classification applied |
| `CONCLUSION.md` | Analysis Agent | Evidence tables (E/N/I), tally, tally summary, and "What CAN/CANNOT Be Said" |

---

## Data Sources

The tools draw from these primary data sources:

| Source | Description | Size |
|--------|-------------|------|
| **KJV Bible** | Complete King James Version text | 31,102 verses |
| **Nave's Topical Bible** | Orville J. Nave's topical dictionary | 5,319 topics |
| **Strong's Concordance** | James Strong's exhaustive concordance with Hebrew/Greek lexicon | Every word in the KJV mapped to original language |
| **BHSA** (Biblia Hebraica Stuttgartensia Amstelodamensis) | Hebrew Bible linguistic database via Text-Fabric | Full morphological parsing of every Hebrew word |
| **N1904** (Nestle 1904) | Greek New Testament linguistic database via Text-Fabric | Full morphological parsing of every Greek word |
| **Textus Receptus** | Byzantine Greek text tradition | For textual variant comparison |
| **LXX Mapping** | Septuagint translation correspondences | Hebrew-to-Greek word mappings |
| **Sentence embeddings** | Pre-computed semantic vectors | For semantic search across all sources |

---

## Evidence Classification Methodology

The core of the methodology is a three-tier evidence classification system that distinguishes between what Scripture directly states, what necessarily follows from it, and what positions claim it implies.

### The Three Tiers

**E -- Explicit.** "The Bible says X." You can point to a verse that says X. A close paraphrase of the actual words of a specific verse, with no concept, framework, or interpretation added beyond what the words themselves require.

**N -- Necessary Implication.** "The Bible implies X." You can point to verses that, when combined, force X with no alternative. Every reader from any theological position must agree this follows -- no additional reasoning is required.

**I -- Inference.** "A position claims the Bible teaches X." No verse explicitly states X, and no combination of verses necessarily implies X. Something must be added beyond what the text contains.

**Critical rule:** Inferences cannot block explicit statements or necessary implications. If E and N items establish X, the existence of passages that *could be inferred* to teach not-X does not prevent X from being established.

---

### The 4-Type Inference Taxonomy

Inferences are further classified on two dimensions:

|  | Derived from E/N | Not derived from E/N |
|--|--|--|
| **Aligns with E/N** | **I-A** (Evidence-Extending) | **I-C** (Compatible External) |
| **Conflicts with E/N** | **I-B** (Competing-Evidence) | **I-D** (Counter-Evidence External) |

**I-A (Evidence-Extending):** Uses only vocabulary and concepts found in E/N statements. An inference only because it systematizes multiple E/N items into a broader claim. Strongest inference type.

**I-B (Competing-Evidence):** Some E/N statements support it, but other E/N statements appear to contradict it. Genuine textual tension where both sides can cite Scripture. Requires the SIS Resolution Protocol.

**I-C (Compatible External):** Reasoning from outside the text (theological tradition, philosophical framework, historical context) that does not contradict any E/N statement. Supplemental only.

**I-D (Counter-Evidence External):** External concepts that require overriding, redefining, or qualifying E/N statements to be maintained. Weakest inference type.

**Evidence hierarchy:** E > N > I-A > I-B (resolved by SIS) > I-C > I-D

---

### Positional Classification

Evidence items are classified by position (Continues, Abolished, or Neutral/Shared) based on the same methodology used across the series. Items are classified positionally **only when one side must deny the textual observation.** Factual observations that both sides must accept are classified Neutral regardless of which side cites them.

[**Read the Full Methodology**](methodology.md){ .md-button }
"""
    tools_path = DOCS / "tools.md"
    tools_path.write_text(content, encoding="utf-8")
    print(f"  Generated {tools_path}")


def copy_assets():
    """Copy shared assets from etc-website."""
    # JavaScript files
    js_src = ETC_WEBSITE / "docs" / "javascripts"
    js_dest = DOCS / "javascripts"
    js_dest.mkdir(parents=True, exist_ok=True)
    for fname in ["verse-popup.js", "study-breadcrumbs.js", "external-links.js",
                   "verses.json", "strongs.json"]:
        src = js_src / fname
        if src.exists():
            shutil.copy2(src, js_dest / fname)
            print(f"  Copied {fname}")
        else:
            print(f"  WARNING: {src} not found")

    # CSS
    css_src = ETC_WEBSITE / "docs" / "stylesheets" / "extra.css"
    css_dest = DOCS / "stylesheets"
    css_dest.mkdir(parents=True, exist_ok=True)
    if css_src.exists():
        shutil.copy2(css_src, css_dest / "extra.css")
        print(f"  Copied extra.css")

    # add_blb_links.py
    blb_src = ETC_WEBSITE / "add_blb_links.py"
    if blb_src.exists():
        shutil.copy2(blb_src, PROJECT_ROOT / "add_blb_links.py")
        print(f"  Copied add_blb_links.py")


def copy_methodology():
    """Copy law-series-methodology.md to docs/methodology.md."""
    src = STUDIES_SRC / "law-series-methodology.md"
    dest = DOCS / "methodology.md"
    if src.exists():
        shutil.copy2(src, dest)
        print(f"  Copied methodology.md")
    else:
        print(f"  WARNING: {src} not found")


def copy_master_evidence():
    """Copy law-master-evidence.md to docs/master-evidence.md."""
    src = STUDIES_SRC / "law-master-evidence.md"
    dest = DOCS / "master-evidence.md"
    if src.exists():
        shutil.copy2(src, dest)
        print(f"  Copied master-evidence.md")
    else:
        print(f"  WARNING: {src} not found")


def generate_deploy_yml():
    """Generate .github/workflows/deploy.yml."""
    deploy_dir = PROJECT_ROOT / ".github" / "workflows"
    deploy_dir.mkdir(parents=True, exist_ok=True)
    content = """name: Deploy MkDocs to GitHub Pages

on:
  push:
    branches:
      - master

permissions:
  contents: write

jobs:
  deploy:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4

      - name: Configure Git credentials
        run: |
          git config user.email "action@github.com"
          git config user.name "GitHub Actions"

      - uses: actions/setup-python@v5
        with:
          python-version: 3.x

      - name: Cache MkDocs dependencies
        uses: actions/cache@v4
        with:
          key: mkdocs-material-${{ hashFiles('**/requirements.txt') }}
          path: .cache
          restore-keys: mkdocs-material-

      - name: Install MkDocs Material
        run: pip install mkdocs-material

      - name: Deploy to GitHub Pages
        run: mkdocs gh-deploy --force
"""
    (deploy_dir / "deploy.yml").write_text(content, encoding="utf-8")
    print(f"  Generated deploy.yml")


def generate_gitignore():
    """Generate .gitignore."""
    content = """site/
.venv/
__pycache__/
node_modules/
"""
    (PROJECT_ROOT / ".gitignore").write_text(content, encoding="utf-8")
    print(f"  Generated .gitignore")


def generate_readme(study_folders: list[tuple[str, Path]]):
    """Generate README.md."""
    lines = []
    lines.append("# The Law of God: What Does the Bible Say?")
    lines.append("")
    lines.append("A comprehensive 33-study biblical investigation examining every major text, word, and argument bearing on the moral law, ceremonial law, the Sabbath, and what continues under the New Covenant.")
    lines.append("")
    lines.append("## Studies")
    lines.append("")
    lines.append("| # | Study | Question |")
    lines.append("|---|-------|----------|")
    for key, src in study_folders:
        num = key.split("-")[1]
        short = SHORT_TITLES.get(key, key)
        full = FULL_TITLES.get(key, short)
        lines.append(f"| {num} | {short} | {full} |")
    lines.append("")
    lines.append("## Built With")
    lines.append("")
    lines.append("- [MkDocs](https://www.mkdocs.org/) with [Material for MkDocs](https://squidfunk.github.io/mkdocs-material/)")
    lines.append("- Interactive Bible verse and Strong's number popups")
    lines.append("- Full KJV text and Strong's Concordance data")

    (PROJECT_ROOT / "README.md").write_text("\n".join(lines) + "\n", encoding="utf-8")
    print(f"  Generated README.md")


def main():
    print("=" * 60)
    print("Building Law of God study website")
    print("=" * 60)

    # Preserve any existing conclusion-simple.md files before cleaning
    preserved_simples = {}
    if DOCS_STUDIES.exists():
        for d in DOCS_STUDIES.iterdir():
            if d.is_dir():
                simple = d / "conclusion-simple.md"
                if simple.exists():
                    preserved_simples[d.name] = simple.read_text(encoding="utf-8")
        shutil.rmtree(DOCS_STUDIES)
    DOCS_STUDIES.mkdir(parents=True)
    print(f"  Preserved {len(preserved_simples)} conclusion-simple.md files")

    # Find all study folders
    print("\n[1/8] Finding study folders...")
    study_folders = find_study_folders()
    print(f"  Found {len(study_folders)} studies")

    # Copy studies
    print("\n[2/8] Copying study files...")
    for key, src in study_folders:
        dest = copy_study(key, src, preserved_simples)
        print(f"  {key}: {src.name} → {dest.relative_to(PROJECT_ROOT)}")

    # Copy methodology and master evidence
    print("\n[3/8] Copying methodology and master evidence...")
    copy_methodology()
    copy_master_evidence()

    # Copy shared assets
    print("\n[4/8] Copying shared assets from etc-website...")
    copy_assets()

    # Generate mkdocs.yml
    print("\n[5/8] Generating mkdocs.yml...")
    generate_mkdocs_yml(study_folders)

    # Generate index.md
    print("\n[6/8] Generating index.md...")
    generate_index_md()

    # Generate tools.md
    print("\n[7/8] Generating tools.md...")
    generate_tools_md()

    # Generate supporting files
    print("\n[8/8] Generating supporting files...")
    generate_deploy_yml()
    generate_gitignore()
    generate_readme(study_folders)

    print("\n" + "=" * 60)
    print("Build complete!")
    print(f"  Studies: {len(study_folders)}")
    print(f"  Output: {DOCS}")
    print("\nNext steps:")
    print("  1. cd law-website && python add_blb_links.py docs/")
    print("  2. mkdocs serve")
    print("=" * 60)


if __name__ == "__main__":
    main()

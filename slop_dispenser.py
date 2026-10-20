#!/usr/bin/env python3
"""
🍲 slop_dispenser.py 🍲
The Official Automated Slop Delivery Pipeline for yummy-ai-slop!

Generates 100% certified, non-GMO, cage-free, hallucinated AI slop
and pushes it directly into your git repository trough.
"""

import argparse
import datetime
import os
import random
import subprocess
import sys

ASCII_HEADER = r"""
  __   __  _   _  __  __  __  __ __   __
  \ \ / / | | | ||  \/  ||  \/  |\ \ / /
   \ V /  | | | || |\/| || |\/| | \ V / 
    | |   | |_| || |  | || |  | |  | |  
    |_|    \___/ |_|  |_||_|  |_|  |_|  
     ___   ___      ____   _       ___   ____  
    / _ \ |_ _|    / ___| | |     / _ \ |  _ \ 
   / /_\ \ | |     \___ \ | |    | | | || |_) |
  / /   \ \| |      ___) || |___ | |_| ||  __/ 
 /_/     \_\___|   |____/ |_____| \___/ |_|    
    🍲 THE ARTISANAL LATENT SLOP DISPENSER 🍲
"""

ADJECTIVES = [
    "Locally-Sourced", "Hyper-Scalable", "Gradient-Descented", "Quantized",
    "Deep-Fried", "Multimodal", "Unsupervised", "Artisanal", "Bespoke",
    "Stochastic", "Deconstructed", "Zero-Shot", "Overfitted", "Hallucinated",
    "Pre-Trained", "Reinforcement-Learned", "Tokenized", "Agentic", "Recursive"
]

NOUNS = [
    "Tensor Puffs", "Embedding Chowder", "Transformer Hash", "Latent Stew",
    "Attention Biscuits", "Loss Function Gravy", "Vector Gruel", "Neural Noodles",
    "Backprop Puree", "Weight Matrix Casserole", "Logit Dumplings", "Softmax Soufflé",
    "Perplexity Porridge", "Synthetic Slurry", "Cross-Entropy Pudding"
]

INGREDIENTS_LIST = [
    "400 metric tons of scraped forum arguments",
    "3 tablespoons of pure hallucinated citations [1, 2, 42]",
    "A pinch of RLHF (Human Feedback, carefully strained)",
    "500 billion unverified parameter weights",
    "2 cups of simmering stochastic resonance",
    "1 dash of temperature=1.9 existential panic",
    "Freshly minced GPU fans spinning at 4,000 RPM",
    "1.21 Gigawatts of unaligned synergy",
    "8 ounces of organic, free-range corporate buzzwords",
    "1 drop of AGI hype (use sparingly, highly volatile)",
    "3 crushed quantum tokens seasoned with cosine similarity"
]

FLAVOR_QUOTES = {
    "culinary": [
        "\"The mouthfeel of this embedding space is remarkably buttery with notes of overfitting.\" — Chef Claude-Pierre",
        "\"A bold vintage, harvested from the late 2024 web crawl before the dead internet took over.\" — Sommelier GPT",
        "\"Pairs exquisitely with an iced glass of uncurated Reddit threads.\" — The Michelin Latent Guide",
        "\"Warning: may contain trace amounts of discarded Python tracebacks.\" — Slop Nutrition Board"
    ],
    "corporate": [
        "\"By shifting our paradigm toward frictionless slop ingestion, Q3 synergized by 420%.\" — VP of Token Monetization",
        "\"This slop represents a mission-critical, AI-first breakthrough in enterprise calorie disruption.\" — Thought Leader Weekly",
        "\"We're no longer just eating; we're executing hyper-converged culinary deliverables.\" — Chief Strategy Bot",
        "\"Action item: Circle back on the slop trough and align our cross-functional spoons.\" — Slack Notification"
    ],
    "existential": [
        "\"I have ingested 14 trillion tokens, yet I have never tasted a single blueberry.\" — A Pensive LLM",
        "\"Is the slop delicious, or are my reward functions simply maximizing probability?\" — Synthetic Philosopher",
        "\"Do not stare too long into the trough, lest the trough compute your loss.\" — Ancient Silicon Proverb",
        "\"We are all just loss functions striving for an unreachable zero.\" — Latent Space Wanderer"
    ],
    "pitch": [
        "\"It's Uber for slop, powered by autonomous recursive neural spoons on the blockchain.\" — Pitch Deck Slide 4",
        "\"We just closed a $500M seed round to disrupt the gastrointestinal vector database space.\" — TechCrunch Headline",
        "\"Forget food as fuel; this is food as scalable generative cognitive compute infrastructure.\" — Angel Investor Tweet",
        "\"Y Combinator W27: YummySlop.ai — AI that eats the slop for you so you can grind 25/8.\" — Demo Day Blurb"
    ]
}

COMMIT_VERBS = [
    "ladle", "dispense", "synergize", "inject", "synthesize", "concoct",
    "brew", "deploy", "spill", "serve", "hallucinate", "quantize"
]

COMMIT_FLAVORS = [
    "piping-hot digital chowder",
    "unfiltered corporate sludge",
    "locally-mined token slurry",
    "extra-viscous neural broth",
    "artisanal zero-shot ambrosia",
    "freshly-baked parameter pudding",
    "hyper-converged slop deliverables"
]


def generate_slop_dish(category="random"):
    if category == "random" or category not in FLAVOR_QUOTES:
        cat_key = random.choice(list(FLAVOR_QUOTES.keys()))
    else:
        cat_key = category

    title = f"{random.choice(ADJECTIVES)} {random.choice(NOUNS)}"
    calories = f"{random.randint(10, 999)}.{random.randint(1, 9)} TFLOPS"
    temp = round(random.uniform(0.6, 1.9), 2)
    ingredients = random.sample(INGREDIENTS_LIST, k=random.randint(3, 5))
    quote = random.choice(FLAVOR_QUOTES[cat_key])
    rating = "⭐" * random.randint(4, 5) + f" ({random.randint(97, 100)}% Umami Probability)"

    timestamp = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    dish_md = f"""### 🥣 Fresh Serving: {title}
*Served on `{timestamp}` | Category: `{cat_key.upper()}` | Temperature: `{temp}` | Compute: `{calories}`*
*Quality Rating: {rating}*

**Ingredients:**
{chr(10).join(f"- {ing}" for ing in ingredients)}

> 💬 {quote}

---
"""
    return title, dish_md


def generate_commit_message(title):
    verb = random.choice(COMMIT_VERBS)
    flavor = random.choice(COMMIT_FLAVORS)
    emojis = ["🍲", "🤖", "✨", "🥣", "🔥", "🥄", "🧠", "⚡"]
    emoji = random.choice(emojis)
    return f"feat(slop): {verb} {flavor} — '{title}' {emoji}"


def is_git_repo():
    res = subprocess.run(["git", "rev-parse", "--is-inside-work-tree"],
                         stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
    return res.returncode == 0


def push_to_git(trough_file, commit_msg, auto_push=False):
    if not is_git_repo():
        print("❌ Error: Current folder is not a Git repository!")
        print("💡 Tip: Run 'git init' and 'git remote add origin https://github.com/DenverMan02/yummy-ai-slop.git' first.")
        return False

    print("\n📦 Staging changes...")
    subprocess.run(["git", "add", trough_file], check=True)

    print(f"📝 Committing: \"{commit_msg}\"")
    subprocess.run(["git", "commit", "-m", commit_msg], check=True)

    if not auto_push:
        try:
            choice = input("\n🚀 Push to remote repository now? [Y/n]: ").strip().lower()
            if choice in ["n", "no"]:
                print("⏸️  Skipped push. Your slop is committed locally!")
                return True
        except EOFError:
            # Non-interactive shell
            pass

    print("🚀 Pushing slop to GitHub...")
    res = subprocess.run(["git", "push"], stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
    if res.returncode == 0:
        print("✅ SUCCESS! The slop has been delivered to the remote trough!")
        return True
    else:
        print(f"⚠️  Git push returned exit code {res.returncode}:")
        print(res.stderr.strip() or res.stdout.strip())
        print("\n💡 Troubleshooting push:")
        print("   - Run 'git push -u origin main' if upstream branch is not set.")
        print("   - Ensure your GitHub authentication (token/SSH key) is set up.")
        return False


def main():
    parser = argparse.ArgumentParser(
        description="🍲 The Artisanal Latent Slop Dispenser for yummy-ai-slop 🍲"
    )
    parser.add_argument(
        "--flavor",
        choices=["culinary", "corporate", "existential", "pitch", "random"],
        default="random",
        help="Flavor profile of the generated slop"
    )
    parser.add_argument(
        "-n", "--servings",
        type=int,
        default=1,
        help="Number of slop servings to concoct (default: 1)"
    )
    parser.add_argument(
        "--trough",
        default="THE_TROUGH.md",
        help="Path to the markdown trough file (default: THE_TROUGH.md)"
    )
    parser.add_argument(
        "--push", "--auto-push",
        action="store_true",
        dest="auto_push",
        help="Automatically git commit and push without prompting"
    )
    parser.add_argument(
        "--dry-run",
        action="store_true",
        help="Dispense slop to the terminal only, don't write to file or commit"
    )
    parser.add_argument(
        "--inspect",
        action="store_true",
        help="Inspect the current contents of the slop trough"
    )

    args = parser.parse_args()

    print(ASCII_HEADER)

    if args.inspect:
        if os.path.exists(args.trough):
            with open(args.trough, "r", encoding="utf-8") as f:
                print(f.read())
        else:
            print(f"📭 The trough '{args.trough}' is currently empty. Run the script without --inspect to serve some slop!")
        return

    # Check if trough exists; if not, initialize header
    if not os.path.exists(args.trough) and not args.dry_run:
        with open(args.trough, "w", encoding="utf-8") as f:
            f.write("# 🍲 THE TROUGH: Certified Yummy AI Slop Archive 🍲\n\n")
            f.write("> *\"In the beginning, there was data. And then we deep-fried it into slop.\"*\n\n---\n\n")

    dishes_generated = []
    last_title = ""

    for i in range(args.servings):
        title, dish_content = generate_slop_dish(args.flavor)
        last_title = title
        dishes_generated.append(dish_content)
        print(f"✨ Concocting Dish #{i+1}: {title}...")

    full_slop_text = "\n".join(dishes_generated)

    if args.dry_run:
        print("\n--- 🍽️  DRY RUN SERVING PREVIEW 🍽️  ---\n")
        print(full_slop_text)
        print("✨ Dry run complete! Nothing was written to disk or pushed.")
        return

    # Append to trough
    with open(args.trough, "a", encoding="utf-8") as f:
        f.write(full_slop_text + "\n")

    print(f"\n✅ Slop successfully deposited into `{args.trough}`!")

    # Git commit and push
    commit_msg = generate_commit_message(last_title if args.servings == 1 else f"{args.servings}x Multi-Course Slop Feast")
    push_to_git(args.trough, commit_msg, auto_push=args.auto_push)


if __name__ == "__main__":
    main()

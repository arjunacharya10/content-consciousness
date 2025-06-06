# 🧠 Content Trait Lab

A research-driven framework to analyze online content through behavioral and epistemic lenses — helping users and researchers understand the **cognitive quality**, **polarization potential**, and **novelty** of videos, transcripts, or articles.

This is part of a larger project focused on nudging users toward **conscious, content-aware consumption** rather than mindless engagement.

---

### Demo Link

🔗 [View Here](https://content-consciousness.streamlit.app)

---

## 📐 What It Does

- ✅ Scores content across 8 behavioral and epistemic traits
- ✅ Classifies content into domains like self-help, politics, finance, etc.
- ✅ Builds a structured content profile from plain-text transcripts
- ✅ Visualizes content profiles in a clean Streamlit dashboard
- ✅ Designed to work with YouTube transcripts or article text

---

## 🧪 Trait Overview

| Trait                   | Description                                                    |
| ----------------------- | -------------------------------------------------------------- |
| `information_depth`     | How insightful, nuanced, and well-researched the content is    |
| `attention_quality`     | How well the content preserves focus and avoids fragmentation  |
| `value_per_minute`      | Value delivered per minute (efficiency of content)             |
| `novelty_index`         | How original or fresh the content is in its domain             |
| `spam_score`            | How spammy, generic, or low-effort the content is              |
| `perspective_awareness` | Whether opposing views are acknowledged respectfully           |
| `polarity_potential`    | How likely the content is to provoke outrage or tribalism      |
| `channel_diversity`     | (placeholder) Viewpoint diversity across the creator’s content |

---

## 📁 Example Output

```json
{
  "filename": "video1.txt",
  "domain": "self-help",
  "information_depth": 2,
  "attention_quality": -2,
  "value_per_minute": -2,
  "novelty_index": -3,
  "spam_score": 3,
  "perspective_awareness": -3,
  "polarity_potential": 4,
  "channel_diversity": null
}
```

---

## Scoring Methodology

Each content transcript is evaluated across multiple traits such as depth, novelty, attention quality, and more.

To create a single meaningful signal, we compute an **Overall Content Score** ranging from **-5 to +5**.  
This score is a weighted sum of core traits:

| Trait                 | Weight    |
| --------------------- | --------- |
| Information Depth     | +0.25     |
| Attention Quality     | +0.25     |
| Value per Minute      | +0.20     |
| Novelty Index         | +0.15     |
| Perspective Awareness | +0.15     |
| Spam Score            | **–0.30** |

### Formula

```python
overall_score = (
    0.25 * information_depth +
    0.25 * attention_quality +
    0.20 * value_per_minute +
    0.15 * novelty_index +
    0.15 * perspective_awareness -
    0.30 * spam_score
)
```

## ⚠️ Disclaimer

The current weights used to compute the overall_score are heuristic and subject to change.
They are based on preliminary intuition about which traits matter most to content quality and user well-being.

As the project matures, we plan to:

- Validate weights via real-world user experiments
- Apply statistical modeling (e.g., regression on user ratings)
- Use multi-objective optimization to balance engagement with epistemic quality

This approach will make the scoring system more rigorous, interpretable, and robust.

---

## 🚀 How to Use

### 1. Clone the repository

```bash
git clone https://github.com/arjunacharya10/content-consciousness
cd content-trait-lab
```

### 2. Install dependencies

```bash
pip install -r requirements.txt
```

### 3. Add transcripts

Place your `.txt` files inside the `transcripts/` folder.

### 4. Run the scorer

```bash
python batch_runner.py
```

This will generate a `.json` trait profile for each `.txt` file.

### 5. Launch the dashboard

```bash
streamlit run dashboard.py
```

---

## 🧱 Built With

- OpenAI GPT-4o (trait scoring engine)
- Streamlit (visualization dashboard)
- Altair (trait radar chart)
- Python (orchestration and pipeline)

---

## 🎓 Research Context

This tool is part of an academic project exploring:

- Content-awareness and epistemic quality
- Behaviorally aligned nudging frameworks
- User profiling based on cognitive media impact

Recommendation system logic will be published as a follow-up.

---

## 📬 Contact

If you're exploring mindful media, recommender audits, or digital well-being, reach out or fork this repo to collaborate.

---

## 🧭 License

MIT — free to use, adapt, and extend.

python3 -m venv venv
source venv/bin/activate

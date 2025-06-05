import streamlit as st
import json
import os
import pandas as pd
import altair as alt

st.set_page_config(layout="wide")
st.title("📊 Content Trait Profile Dashboard")
st.subheader("Author: Arjun Acharya")
st.markdown("🔗 [Linkedin](https://www.linkedin.com/in/arjunacharya10/), [View Project on GitHub](https://github.com/arjunacharya10/content-consciousness)", unsafe_allow_html=True)
# GitHub Link
st.markdown("**Content Consciousness Labels**")

# Load and show the image (no PIL needed)
with open("content-labels.png", "rb") as file:
    st.image(file.read(), caption="Score Range: Deep red (harmful/spammy) to Deep Green (meaningful/informative). This should be clearly displayed at the beginning of very content clearly in decreasing order of impact.", use_container_width=True)

# --- About Section (loads README.md) ---
def load_readme():
    readme_path = os.path.join(os.path.dirname(__file__), "README.md")
    if os.path.exists(readme_path):
        with open(readme_path, "r") as f:
            return f.read()
    return "README.md not found."

with st.expander("ℹ️ About this project"):
    st.markdown(load_readme())

st.markdown("---")
# --- Load all .json profiles ---
folder = "transcripts"
files = [f for f in os.listdir(folder) if f.endswith(".json")]

rows = []
for file in files:
    with open(os.path.join(folder, file)) as f:
        data = json.load(f)
        data["filename"] = file
        rows.append(data)

df = pd.DataFrame(rows)

# Fill defaults
df["description"] = df["description"].fillna("No description available.")
df["domain"] = df["domain"].fillna("Unknown")

# List of traits
numeric_traits = [
    "information_depth", "attention_quality", "value_per_minute",
    "novelty_index", "spam_score", "perspective_awareness",
    "polarity_potential", "channel_diversity"
]

# Display table
st.dataframe(
    df[[
        "filename", "domain", "description",
        *numeric_traits
    ]].fillna("N/A"),
    use_container_width=True
)

# Select a video
selected_file = st.selectbox("🔍 Inspect video", df["filename"].tolist())
selected = df[df["filename"] == selected_file].iloc[0]

st.subheader(f"📄 {selected_file}")
st.markdown(f"**Domain**: `{selected.get('domain', 'N/A')}`")
st.markdown(f"**Description**: {selected.get('description', '')}```")

# Expand full transcript
with st.expander("📖 Read full transcript"):
    st.write(selected.get("full_text", "No transcript available."))

def score_to_color(score):
    if score <= -4:
        return "#8B0000"
    elif score <= -2:
        return "#B22222"
    elif score < 0:
        return "#FF4500"
    elif score == 0:
        return "#CCCCCC"
    elif score < 2:
        return "#6B8E23"
    elif score < 4:
        return "#228B22"
    else:
        return "#006400"

score_val = selected.get("overall_score", 0)
score_color = score_to_color(score_val)

st.markdown(
    f"<h2 style='color:{score_color}; font-size: 36px;'>Overall Score: {score_val} <span style='font-size: 18px;'>(-5 to +5)</span></h2>",
    unsafe_allow_html=True
)

# Build radar bar chart
radar_df = pd.DataFrame({
    "trait": numeric_traits,
    "score": [selected.get(trait, 0) or 0 for trait in numeric_traits]
})

def trait_color(trait, score):
    score = int(round(score or 0))
    
    if trait in ["spam_score", "polarity_potential"]:
        # Inverse scale: high = bad (more red)
        color_map = {
            -5: "#006400", -4: "#008000", -3: "#228B22", -2: "#6B8E23", -1: "#9ACD32",
             0: "#CCCCCC", 1: "#FF8C00", 2: "#FF4500", 3: "#DC143C", 4: "#B22222", 5: "#8B0000"
        }
    else:
        # Normal scale: high = good (more green)
        color_map = {
            -5: "#8B0000", -4: "#B22222", -3: "#DC143C", -2: "#FF4500", -1: "#FF8C00",
             0: "#CCCCCC", 1: "#9ACD32", 2: "#6B8E23", 3: "#228B22", 4: "#008000", 5: "#006400"
        }
    return color_map.get(score, "#CCCCCC")

# Color scale by impact
radar_df["color"] = radar_df.apply(lambda row: trait_color(row["trait"], row["score"]), axis=1)

# Chart
st.altair_chart(
    alt.Chart(radar_df).mark_bar().encode(
        x=alt.X("trait:N", sort=numeric_traits),
        y="score:Q",
        color=alt.Color("color:N", scale=None, legend=None),
        tooltip=["trait", "score"]
    ).properties(width=700, height=300),
    use_container_width=True
)

# Trait descriptions
st.markdown("### 🧠 Trait Descriptions")

trait_explanations = {
    "information_depth": "How insightful, nuanced, and well-researched the content is.",
    "attention_quality": "How well the content preserves focus and avoids fragmentation.",
    "value_per_minute": "How much meaningful value the content delivers per minute.",
    "novelty_index": "How original or fresh the content is compared to peers in the same domain.",
    "spam_score": "How spammy, regurgitated, or low-effort the content is. Higher = more spammy.",
    "perspective_awareness": "How fairly the content acknowledges or engages with opposing views.",
    "polarity_potential": "How likely the content is to provoke tribalism, outrage, or polarization.",
    "channel_diversity": "How varied the perspectives are across the channel’s content (not scored yet)."
}

for trait in numeric_traits:
    st.markdown(f"**{trait}**: {trait_explanations[trait]}")

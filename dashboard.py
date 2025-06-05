import streamlit as st
import json
import os
import pandas as pd
import altair as alt

st.set_page_config(layout="wide")
st.title("📊 Content Trait Profile Dashboard")
st.markdown("**Author: Arjun Acharya**")
st.markdown("🔗 [Linkedin](https://www.linkedin.com/in/arjunacharya10/)", unsafe_allow_html=True)
# GitHub Link
st.markdown("🔗 [View Project on GitHub](https://github.com/arjunacharya10/content-consciousness)", unsafe_allow_html=True)

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

# Build radar bar chart
radar_df = pd.DataFrame({
    "trait": numeric_traits,
    "score": [selected.get(trait, 0) or 0 for trait in numeric_traits]
})

# Color scale by impact
radar_df["color"] = radar_df["score"].apply(
    lambda x: "#EF4444" if x < -2 else "#F97316" if x < 0 else "#E5E7EB" if x == 0 else "#34D399" if x <= 2 else "#10B981"
)

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

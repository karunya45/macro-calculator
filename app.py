import streamlit as st
import pandas as pd

st.set_page_config(page_title="Macro Calculator", page_icon="📊", layout="centered")

# -------------------------------------------------------------------
# THEME / CSS — clean clinical/dashboard style
# Palette: off-white bg (#F6F7F9) + white cards + navy text (#111827)
#          + teal accent (#0F766E) for actions
# Macro colors follow common nutrition-app convention:
#          Protein = blue (#2563EB), Carbs = amber (#D97706), Fat = red (#DC2626)
# Fonts: Manrope (headings) + Inter (body/labels) + JetBrains Mono (numbers)
# -------------------------------------------------------------------

CUSTOM_CSS = """
<style>
@import url('https://fonts.googleapis.com/css2?family=Manrope:wght@600;700;800&family=Inter:wght@400;500;600&family=JetBrains+Mono:wght@500;600&display=swap');

html, body, [class*="css"]  {
    font-family: 'Inter', sans-serif;
    color: #111827;
}

.stApp {
    background: #F6F7F9;
}

.block-container {
    padding-top: 2.2rem;
    max-width: 720px;
}

/* ---- Header ---- */
.app-header {
    margin-bottom: 1.8rem;
}
.app-header .eyebrow {
    font-family: 'Inter', sans-serif;
    font-weight: 600;
    font-size: 0.75rem;
    letter-spacing: 0.08em;
    text-transform: uppercase;
    color: #0F766E;
    margin-bottom: 0.4rem;
}
.app-header h1 {
    font-family: 'Manrope', sans-serif;
    font-weight: 800;
    color: #111827;
    font-size: 2rem;
    margin: 0 0 0.4rem 0;
    line-height: 1.15;
}
.app-header p {
    color: #6B7280;
    font-size: 0.98rem;
    margin: 0;
}
.app-header hr {
    border: none;
    border-top: 1px solid #E5E7EB;
    margin-top: 1.4rem;
}

/* ---- Section headers ---- */
.section-title {
    display: flex;
    align-items: center;
    gap: 0.55rem;
    margin: 1.7rem 0 0.6rem 0;
    padding-bottom: 0.5rem;
    border-bottom: 1px solid #E5E7EB;
}
.section-title .icon-box {
    width: 26px; height: 26px;
    border-radius: 6px;
    background: #ECFDF5;
    display: flex; align-items: center; justify-content: center;
    font-size: 0.85rem;
}
.section-title .text {
    font-family: 'Manrope', sans-serif;
    font-weight: 700;
    font-size: 1.02rem;
    color: #111827;
}
.section-title .count {
    margin-left: auto;
    font-family: 'JetBrains Mono', monospace;
    font-size: 0.75rem;
    color: #9CA3AF;
}

/* ---- Streamlit widget restyle ---- */
.stTextInput input, .stNumberInput input {
    border-radius: 8px !important;
    border: 1px solid #D1D5DB !important;
    font-family: 'Inter', sans-serif;
    background: #FFFFFF !important;
}
.stTextInput input:focus, .stNumberInput input:focus {
    border-color: #0F766E !important;
    box-shadow: 0 0 0 1px #0F766E !important;
}
.stMultiSelect > div {
    border-radius: 8px !important;
}
.stMultiSelect [data-baseweb="tag"] {
    background-color: #0F766E !important;
    color: #FFFFFF !important;
    border-radius: 6px !important;
}
div[data-testid="stButton"] button {
    background: #0F766E;
    color: #FFFFFF;
    font-family: 'Inter', sans-serif;
    font-weight: 600;
    font-size: 0.98rem;
    border-radius: 8px;
    border: none;
    padding: 0.65rem 1.4rem;
    width: 100%;
    transition: background 0.15s ease;
}
div[data-testid="stButton"] button:hover {
    background: #0D5F58;
    color: #FFFFFF;
}

/* ---- Result cards ---- */
.results-header {
    font-family: 'Manrope', sans-serif;
    font-weight: 700;
    font-size: 1.15rem;
    color: #111827;
    margin: 1.8rem 0 1rem 0;
}

.metric-grid {
    display: grid;
    grid-template-columns: repeat(4, 1fr);
    gap: 0.7rem;
    margin-bottom: 1.3rem;
}
.metric-card {
    background: #FFFFFF;
    border: 1px solid #E5E7EB;
    border-radius: 10px;
    padding: 0.9rem 0.6rem;
    text-align: center;
}
.metric-card .val {
    font-family: 'JetBrains Mono', monospace;
    font-weight: 600;
    font-size: 1.25rem;
    color: #111827;
}
.metric-card .lbl {
    font-family: 'Inter', sans-serif;
    font-size: 0.72rem;
    color: #6B7280;
    margin-top: 0.15rem;
    text-transform: uppercase;
    letter-spacing: 0.04em;
}
.metric-card.calories { border-top: 3px solid #111827; }
.metric-card.protein { border-top: 3px solid #2563EB; }
.metric-card.carbs { border-top: 3px solid #D97706; }
.metric-card.fat { border-top: 3px solid #DC2626; }

.macro-bar-wrap { margin-bottom: 0.8rem; }
.macro-bar-label {
    display: flex; justify-content: space-between;
    font-family: 'Inter', sans-serif;
    font-weight: 500;
    color: #374151;
    font-size: 0.85rem;
    margin-bottom: 0.3rem;
}
.macro-bar-label .g { font-family: 'JetBrains Mono', monospace; color: #111827; }
.macro-bar-track {
    background: #E5E7EB;
    border-radius: 5px;
    height: 8px;
    overflow: hidden;
}
.macro-bar-fill { height: 100%; border-radius: 5px; }

.data-card {
    background: #FFFFFF;
    border: 1px solid #E5E7EB;
    border-radius: 10px;
    padding: 1.1rem 1.2rem 0.4rem 1.2rem;
    margin: 1.2rem 0 0.6rem 0;
}
.data-card .heading {
    font-family: 'Manrope', sans-serif;
    font-weight: 700;
    color: #111827;
    font-size: 0.95rem;
    margin-bottom: 0.6rem;
}

.footnote {
    color: #9CA3AF;
    font-size: 0.8rem;
    font-family: 'Inter', sans-serif;
    margin-top: 0.8rem;
}
</style>
"""

st.markdown(CUSTOM_CSS, unsafe_allow_html=True)

# -------------------------------------------------------------------
# INGREDIENT DATABASE
# Values = (calories, protein_g, carbs_g, fat_g) PER 100 GRAMS
# (Approximate standard nutrition values)
# -------------------------------------------------------------------

VEGGIES = {
    "Onion": (40, 1.1, 9.3, 0.1),
    "Tomato": (18, 0.9, 3.9, 0.2),
    "Potato": (77, 2.0, 17.0, 0.1),
    "Carrot": (41, 0.9, 10.0, 0.2),
    "Spinach": (23, 2.9, 3.6, 0.4),
    "Cauliflower": (25, 1.9, 5.0, 0.3),
    "Cabbage": (25, 1.3, 6.0, 0.1),
    "Green Peas": (81, 5.4, 14.0, 0.4),
    "Capsicum": (20, 0.9, 4.6, 0.2),
    "Brinjal (Eggplant)": (25, 1.0, 6.0, 0.2),
    "Green Beans": (31, 1.8, 7.0, 0.1),
    "Bottle Gourd": (15, 0.6, 3.4, 0.02),
    "Okra (Ladies Finger)": (33, 1.9, 7.5, 0.2),
    "Sweet Potato": (86, 1.6, 20.0, 0.1),
    "Garlic": (149, 6.4, 33.0, 0.5),
    "Ginger": (80, 1.8, 18.0, 0.8),
    "Mushroom": (22, 3.1, 3.3, 0.3),
    "Paneer": (265, 18.3, 1.2, 20.8),
    "Cucumber": (15, 0.7, 3.6, 0.1),
    "Beetroot": (43, 1.6, 10.0, 0.2),
}

SPICES = {
    "Turmeric Powder": (312, 9.7, 65.0, 3.3),
    "Red Chilli Powder": (282, 12.0, 50.0, 14.0),
    "Coriander Powder": (298, 12.4, 55.0, 17.8),
    "Cumin Seeds (Jeera)": (375, 18.0, 44.0, 22.0),
    "Mustard Seeds": (508, 26.0, 28.0, 36.0),
    "Garam Masala": (379, 15.0, 45.0, 15.0),
    "Black Pepper": (251, 10.4, 64.0, 3.3),
    "Salt": (0, 0.0, 0.0, 0.0),
    "Curry Leaves": (108, 6.1, 18.7, 1.0),
    "Asafoetida (Hing)": (297, 4.0, 68.0, 1.1),
}

OILS = {
    "Sunflower Oil": (884, 0.0, 0.0, 100.0),
    "Groundnut Oil": (884, 0.0, 0.0, 100.0),
    "Mustard Oil": (884, 0.0, 0.0, 100.0),
    "Coconut Oil": (862, 0.0, 0.0, 99.9),
    "Ghee (Clarified Butter)": (900, 0.0, 0.0, 99.5),
    "Olive Oil": (884, 0.0, 0.0, 100.0),
    "Butter": (717, 0.9, 0.1, 81.0),
}

# Raw / dry weight per 100g (these swell up a lot once cooked/soaked —
# weigh them dry/raw before cooking for these numbers to be accurate)
LENTILS = {
    "Black Chickpeas (Kala Chana)": (364, 19.3, 61.0, 6.0),
    "White Chickpeas (Kabuli Chana)": (364, 19.3, 61.0, 6.0),
    "Red Lentils (Masoor Dal)": (352, 24.6, 60.0, 1.1),
    "Yellow Split Peas (Toor/Arhar Dal)": (343, 22.3, 57.0, 1.5),
    "Green Gram (Moong Dal)": (347, 24.0, 59.0, 1.2),
    "Black Gram (Urad Dal)": (341, 25.2, 59.0, 1.6),
    "Kidney Beans (Rajma)": (333, 23.6, 60.0, 0.8),
    "Black Beans": (341, 21.6, 62.4, 1.4),
    "Green Peas (Dry)": (352, 24.6, 63.0, 1.2),
    "Soybeans": (446, 36.5, 30.2, 19.9),
}

DAIRY = {
    "Milk (Full Fat)": (60, 3.2, 4.8, 3.3),
    "Milk (Toned/Low Fat)": (44, 3.1, 4.9, 1.2),
    "Curd / Yogurt (Plain)": (60, 3.5, 4.7, 3.3),
    "Greek Yogurt": (97, 9.0, 3.6, 5.0),
    "Cheese (Cheddar)": (403, 25.0, 1.3, 33.0),
    "Cream": (340, 2.1, 2.8, 36.0),
    "Buttermilk": (25, 1.9, 2.9, 0.6),
}


def macro_block(title, food_dict, default_qty, key_prefix):
    """Renders a multiselect + per-item grams input, returns list of (name, qty, macros)."""
    chosen = st.multiselect(f"Select {title.lower()}", list(food_dict.keys()), key=f"{key_prefix}_select")
    results = []
    for item in chosen:
        qty = st.number_input(
            f"{item} — quantity (grams)",
            min_value=0.0, max_value=2000.0, value=float(default_qty), step=1.0,
            key=f"{key_prefix}_{item}"
        )
        results.append((item, qty, food_dict[item]))
    return results


def compute_totals(selections):
    total_cal = total_p = total_c = total_f = 0.0
    rows = []
    for name, qty, (cal, p, c, f) in selections:
        factor = qty / 100.0
        cal_c, p_c, c_c, f_c = cal * factor, p * factor, c * factor, f * factor
        total_cal += cal_c
        total_p += p_c
        total_c += c_c
        total_f += f_c
        rows.append({
            "Ingredient": name,
            "Qty (g)": qty,
            "Calories": round(cal_c, 1),
            "Protein (g)": round(p_c, 1),
            "Carbs (g)": round(c_c, 1),
            "Fat (g)": round(f_c, 1),
        })
    return total_cal, total_p, total_c, total_f, rows


# -------------------------------------------------------------------
# UI
# -------------------------------------------------------------------

st.markdown(
    """
    <div class="app-header">
        <div class="eyebrow">Nutrition Tool</div>
        <h1>Macro Calculator</h1>
        <p>Select the ingredients in your dish and get an instant breakdown of calories, protein, carbs, and fat.</p>
        <hr>
    </div>
    """,
    unsafe_allow_html=True,
)

food_name = st.text_input("Dish name (optional)", placeholder="e.g. Aloo Gobi — leave blank if checking a single ingredient")

st.markdown(
    '<div class="section-title"><span class="icon-box">🥦</span><span class="text">Vegetables</span>'
    f'<span class="count">{len(VEGGIES)} items</span></div>',
    unsafe_allow_html=True,
)
veggie_sel = macro_block("Vegetables", VEGGIES, default_qty=50, key_prefix="veg")

st.markdown(
    '<div class="section-title"><span class="icon-box">🌶️</span><span class="text">Spices</span>'
    f'<span class="count">{len(SPICES)} items</span></div>',
    unsafe_allow_html=True,
)
spice_sel = macro_block("Spices", SPICES, default_qty=2, key_prefix="spice")

st.markdown(
    '<div class="section-title"><span class="icon-box">🫒</span><span class="text">Oil / Fat</span>'
    f'<span class="count">{len(OILS)} items</span></div>',
    unsafe_allow_html=True,
)
oil_sel = macro_block("Oil / Fat", OILS, default_qty=10, key_prefix="oil")

st.markdown(
    '<div class="section-title"><span class="icon-box">🫘</span><span class="text">Lentils / Legumes</span>'
    f'<span class="count">{len(LENTILS)} items</span></div>',
    unsafe_allow_html=True,
)
lentil_sel = macro_block("Lentils / Legumes", LENTILS, default_qty=30, key_prefix="lentil")

st.markdown(
    '<div class="section-title"><span class="icon-box">🥛</span><span class="text">Dairy</span>'
    f'<span class="count">{len(DAIRY)} items</span></div>',
    unsafe_allow_html=True,
)
dairy_sel = macro_block("Dairy", DAIRY, default_qty=50, key_prefix="dairy")

st.markdown("<br>", unsafe_allow_html=True)

if st.button("Calculate Macros", type="primary"):
    all_selected = veggie_sel + spice_sel + oil_sel + lentil_sel + dairy_sel

    if not all_selected:
        st.warning("Please select at least one ingredient (veggie, spice, oil, lentil, or dairy) above.")
    else:
        display_name = food_name if food_name else "Your Dish"
        total_cal, total_p, total_c, total_f, rows = compute_totals(all_selected)
        max_macro = max(total_p, total_c, total_f, 1)  # avoid divide-by-zero

        st.markdown(f'<div class="results-header">Results — {display_name}</div>', unsafe_allow_html=True)

        st.markdown(
            f"""
            <div class="metric-grid">
                <div class="metric-card calories"><div class="val">{total_cal:.0f}</div><div class="lbl">Calories</div></div>
                <div class="metric-card protein"><div class="val">{total_p:.1f}g</div><div class="lbl">Protein</div></div>
                <div class="metric-card carbs"><div class="val">{total_c:.1f}g</div><div class="lbl">Carbs</div></div>
                <div class="metric-card fat"><div class="val">{total_f:.1f}g</div><div class="lbl">Fat</div></div>
            </div>
            """,
            unsafe_allow_html=True,
        )

        macro_data = [
            ("Protein", total_p, "#2563EB"),
            ("Carbs", total_c, "#D97706"),
            ("Fat", total_f, "#DC2626"),
        ]
        bars_html = ""
        for label, value, color in macro_data:
            pct = min(100, (value / max_macro) * 100)
            bars_html += f"""
            <div class="macro-bar-wrap">
                <div class="macro-bar-label"><span>{label}</span><span class="g">{value:.1f} g</span></div>
                <div class="macro-bar-track">
                    <div class="macro-bar-fill" style="width:{pct}%; background:{color};"></div>
                </div>
            </div>
            """
        st.markdown(bars_html, unsafe_allow_html=True)

        st.markdown('<div class="data-card">', unsafe_allow_html=True)
        st.markdown('<div class="heading">Ingredient breakdown</div>', unsafe_allow_html=True)
        df = pd.DataFrame(rows)
        st.dataframe(df, use_container_width=True, hide_index=True)
        st.markdown("</div>", unsafe_allow_html=True)

        st.markdown(
            '<p class="footnote">Values are approximate, based on standard nutrition data per '
            '100g of raw ingredient. Actual macros can vary with cooking method, brand, and exact quantities.</p>',
            unsafe_allow_html=True,
        )

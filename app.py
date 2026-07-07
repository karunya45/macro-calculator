import streamlit as st
import pandas as pd

st.set_page_config(page_title="Food Macro Calculator", page_icon="🍲", layout="centered")

# -------------------------------------------------------------------
# THEME / CSS
# Palette: charcoal (#1F1B16) + cream (#FFF8EC) + mustard (#E8A93B)
#          + chili red (#C1442E) + sage green (#7C9473)
# Fonts: Fraunces (headings) + Inter (body) + IBM Plex Mono (numbers)
# Color legend used consistently: Protein=sage, Carbs=mustard, Fat=chili
# -------------------------------------------------------------------

CUSTOM_CSS = """
<style>
@import url('https://fonts.googleapis.com/css2?family=Fraunces:wght@500;600;700&family=Inter:wght@400;500;600&family=IBM+Plex+Mono:wght@500;600&display=swap');

html, body, [class*="css"]  {
    font-family: 'Inter', sans-serif;
}

.stApp {
    background: #1F1B16;
}

/* ---- Hero header ---- */
.hero {
    background: linear-gradient(135deg, #2B2320 0%, #1F1B16 100%);
    border-radius: 18px;
    padding: 2.2rem 1.8rem 1.6rem 1.8rem;
    margin-bottom: 1.6rem;
    border: 1px solid #3A302A;
}
.hero-emojis { font-size: 2.1rem; letter-spacing: 0.3rem; margin-bottom: 0.4rem; }
.hero h1 {
    font-family: 'Fraunces', serif;
    font-weight: 700;
    color: #FFF8EC;
    font-size: 2.4rem;
    margin: 0 0 0.3rem 0;
    line-height: 1.1;
}
.hero p {
    color: #C9BEB0;
    font-size: 1rem;
    margin: 0;
}

/* ---- Spice-dot divider (signature element, also the macro legend) ---- */
.dot-row { display: flex; align-items: center; gap: 0.5rem; margin: 1.6rem 0 0.8rem 0; }
.dot { width: 10px; height: 10px; border-radius: 50%; display: inline-block; }
.dot.mustard { background: #E8A93B; }
.dot.chili { background: #C1442E; }
.dot.sage { background: #7C9473; }
.dot.cream { background: #E3D9C8; }
.dot.clay { background: #A8724D; }
.dot-row .label {
    font-family: 'Fraunces', serif;
    font-weight: 600;
    color: #FFF8EC;
    font-size: 1.3rem;
    margin-left: 0.3rem;
}

/* ---- Section cards ---- */
.section-card {
    background: #FFF8EC;
    border-radius: 14px;
    padding: 1.3rem 1.4rem 0.6rem 1.4rem;
    margin-bottom: 0.6rem;
}

/* ---- Streamlit widget restyle ---- */
.stTextInput input, .stNumberInput input {
    border-radius: 8px !important;
    border: 1.5px solid #E3D9C8 !important;
    font-family: 'IBM Plex Mono', monospace;
}
.stMultiSelect [data-baseweb="tag"] {
    background-color: #E8A93B !important;
    color: #1F1B16 !important;
}
div[data-testid="stButton"] button {
    background: #C1442E;
    color: #FFF8EC;
    font-family: 'Fraunces', serif;
    font-weight: 600;
    font-size: 1.05rem;
    border-radius: 10px;
    border: none;
    padding: 0.6rem 1.4rem;
    width: 100%;
    transition: transform 0.12s ease, background 0.12s ease;
}
div[data-testid="stButton"] button:hover {
    background: #A8371F;
    transform: translateY(-1px);
    color: #FFF8EC;
}

/* ---- Result badges ---- */
.calorie-badge {
    background: linear-gradient(135deg, #E8A93B 0%, #C1442E 100%);
    border-radius: 16px;
    padding: 1.4rem;
    text-align: center;
    margin-bottom: 1rem;
}
.calorie-badge .num {
    font-family: 'Fraunces', serif;
    font-weight: 700;
    font-size: 2.6rem;
    color: #1F1B16;
    line-height: 1;
}
.calorie-badge .lbl {
    font-family: 'Inter', sans-serif;
    color: #2B2320;
    font-size: 0.95rem;
    margin-top: 0.2rem;
}

.macro-bar-wrap { margin-bottom: 0.9rem; }
.macro-bar-label {
    display: flex; justify-content: space-between;
    font-family: 'IBM Plex Mono', monospace;
    color: #FFF8EC;
    font-size: 0.92rem;
    margin-bottom: 0.25rem;
}
.macro-bar-track {
    background: #3A302A;
    border-radius: 6px;
    height: 10px;
    overflow: hidden;
}
.macro-bar-fill { height: 100%; border-radius: 6px; }

.section-heading {
    font-family: 'Fraunces', serif;
    font-weight: 600;
    color: #1F1B16;
    font-size: 1.25rem;
    margin-bottom: 0.2rem;
}

.footnote {
    color: #8A7F71;
    font-size: 0.85rem;
    font-family: 'Inter', sans-serif;
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
    <div class="hero">
        <div class="hero-emojis">🥕 🌶️ 🧅 🫒 🍅</div>
        <h1>Food Macro Calculator</h1>
        <p>Build your dish ingredient by ingredient and get an instant macro breakdown.</p>
    </div>
    """,
    unsafe_allow_html=True,
)

food_name = st.text_input("Food / Dish Name", placeholder="e.g. Aloo Gobi")

st.markdown('<div class="dot-row"><span class="dot sage"></span><span class="label">🥕 Veggies</span></div>', unsafe_allow_html=True)
veggie_sel = macro_block("Veggies", VEGGIES, default_qty=50, key_prefix="veg")

st.markdown('<div class="dot-row"><span class="dot chili"></span><span class="label">🌶️ Spices</span></div>', unsafe_allow_html=True)
spice_sel = macro_block("Spices", SPICES, default_qty=2, key_prefix="spice")

st.markdown('<div class="dot-row"><span class="dot mustard"></span><span class="label">🫒 Oil / Fat</span></div>', unsafe_allow_html=True)
oil_sel = macro_block("Oil / Fat", OILS, default_qty=10, key_prefix="oil")

st.markdown('<div class="dot-row"><span class="dot clay"></span><span class="label">🫘 Lentils / Legumes</span></div>', unsafe_allow_html=True)
lentil_sel = macro_block("Lentils / Legumes", LENTILS, default_qty=30, key_prefix="lentil")

st.markdown('<div class="dot-row"><span class="dot cream"></span><span class="label">🥛 Dairy</span></div>', unsafe_allow_html=True)
dairy_sel = macro_block("Dairy", DAIRY, default_qty=50, key_prefix="dairy")

st.markdown("<br>", unsafe_allow_html=True)

if st.button("🔢 Calculate Macros", type="primary"):
    all_selected = veggie_sel + spice_sel + oil_sel + lentil_sel + dairy_sel

    if not food_name:
        st.warning("Please enter a food name.")
    elif not all_selected:
        st.warning("Please select at least one ingredient.")
    else:
        total_cal, total_p, total_c, total_f, rows = compute_totals(all_selected)
        max_macro = max(total_p, total_c, total_f, 1)  # avoid divide-by-zero

        st.markdown(
            f'<div class="dot-row"><span class="label">🍽️ Results for {food_name}</span></div>',
            unsafe_allow_html=True,
        )

        st.markdown(
            f"""
            <div class="calorie-badge">
                <div class="num">{total_cal:.0f}</div>
                <div class="lbl">total calories (kcal)</div>
            </div>
            """,
            unsafe_allow_html=True,
        )

        macro_data = [
            ("Protein", total_p, "#7C9473"),
            ("Carbs", total_c, "#E8A93B"),
            ("Fat", total_f, "#C1442E"),
        ]
        bars_html = ""
        for label, value, color in macro_data:
            pct = min(100, (value / max_macro) * 100)
            bars_html += f"""
            <div class="macro-bar-wrap">
                <div class="macro-bar-label"><span>{label}</span><span>{value:.1f} g</span></div>
                <div class="macro-bar-track">
                    <div class="macro-bar-fill" style="width:{pct}%; background:{color};"></div>
                </div>
            </div>
            """
        st.markdown(bars_html, unsafe_allow_html=True)

        st.markdown('<div class="section-card">', unsafe_allow_html=True)
        st.markdown('<div class="section-heading">📋 Ingredient-wise breakdown</div>', unsafe_allow_html=True)
        df = pd.DataFrame(rows)
        st.dataframe(df, use_container_width=True, hide_index=True)
        st.markdown("</div>", unsafe_allow_html=True)

        st.markdown(
            '<p class="footnote">Note: values are approximate, based on standard nutrition data per '
            '100g of raw ingredient. Actual macros can vary with cooking method, brand, and exact quantities.</p>',
            unsafe_allow_html=True,
        )

import streamlit as st
import pandas as pd

st.set_page_config(page_title="Food Macro Calculator", page_icon="🍲", layout="centered")

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


def macro_block(title, food_dict, default_qty, key_prefix):
    """Renders a multiselect + per-item grams input, returns list of (name, qty, macros)."""
    st.subheader(title)
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

st.title("🍲 Food Macro Calculator")
st.caption("Enter your dish details below, then hit Calculate to see total macros.")

food_name = st.text_input("Food / Dish Name", placeholder="e.g. Aloo Gobi")

veggie_sel = macro_block("Veggies", VEGGIES, default_qty=50, key_prefix="veg")
spice_sel = macro_block("Spices", SPICES, default_qty=2, key_prefix="spice")
oil_sel = macro_block("Oil / Fat", OILS, default_qty=10, key_prefix="oil")

st.divider()

if st.button("🔢 Calculate Macros", type="primary"):
    all_selected = veggie_sel + spice_sel + oil_sel

    if not food_name:
        st.warning("Please enter a food name.")
    elif not all_selected:
        st.warning("Please select at least one ingredient.")
    else:
        total_cal, total_p, total_c, total_f, rows = compute_totals(all_selected)

        st.success(f"Macro breakdown for **{food_name}**")

        col1, col2, col3, col4 = st.columns(4)
        col1.metric("Calories", f"{total_cal:.0f} kcal")
        col2.metric("Protein", f"{total_p:.1f} g")
        col3.metric("Carbs", f"{total_c:.1f} g")
        col4.metric("Fat", f"{total_f:.1f} g")

        st.markdown("#### Ingredient-wise breakdown")
        df = pd.DataFrame(rows)
        st.dataframe(df, use_container_width=True, hide_index=True)

        st.markdown("#### Macro split (grams)")
        chart_df = pd.DataFrame({
            "Macro": ["Protein", "Carbs", "Fat"],
            "Grams": [total_p, total_c, total_f]
        }).set_index("Macro")
        st.bar_chart(chart_df)

        st.caption(
            "Note: Values are approximate, based on standard nutrition data per 100g of raw ingredient. "
            "Actual macros can vary with cooking method, brand, and exact quantities."
        )

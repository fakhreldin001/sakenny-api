import streamlit as st
import requests

API_URL = "http://host.docker.internal:8000"

st.set_page_config(page_title="Sakenny Dashboard", page_icon="🏠")
st.title("🏠 Sakenny Dashboard")

# Sidebar for adding properties
st.sidebar.header("Add New Property")

with st.sidebar.form("add_property"):
    title = st.text_input("Title")
    description = st.text_area("Description")
    price = st.number_input("Price (EGP)", min_value=0)
    location = st.text_input("Location")
    bedrooms = st.number_input("Bedrooms", min_value=0, max_value=20)
    bathrooms = st.number_input("Bathrooms", min_value=0, max_value=10)
    area = st.number_input("Area (sqm)", min_value=0)
    property_type = st.selectbox("Type", ["apartment", "villa", "studio", "duplex", "penthouse"])
    
    submitted = st.form_submit_button("Add Property")
    
    if submitted and title and price and location:
        response = requests.post(f"{API_URL}/properties/", json={
            "title": title,
            "description": description,
            "price": price,
            "location": location,
            "bedrooms": bedrooms,
            "bathrooms": bathrooms,
            "area": area,
            "property_type": property_type
        })
        if response.status_code == 200:
            st.sidebar.success("Property added!")
        else:
            st.sidebar.error("Failed to add property")

# Main area - display properties
st.header("Properties")

try:
    response = requests.get(f"{API_URL}/properties/")
    properties = response.json()
    
    if properties:
        for prop in properties:
            with st.container():
                st.subheader(prop["title"])
                st.write(f"📍 {prop['location']}")
                st.write(f"💰 {prop['price']:,.0f} EGP")
                if prop.get("bedrooms"):
                    st.write(f"🛏️ {prop['bedrooms']} beds | 🚿 {prop.get('bathrooms', 'N/A')} baths | 📐 {prop.get('area', 'N/A')} sqm")
                st.divider()
    else:
        st.info("No properties yet. Add one from the sidebar!")
except Exception as e:
    st.error(f"Cannot connect to API. Is it running? Error: {e}")
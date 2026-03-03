import streamlit as st
from components.paper_card import display_paper_card
from utils.styling import apply_custom_styles
from utils.session import initialize_session_state

st.set_page_config(page_title="Paper Browser", page_icon="📚", layout="wide")
apply_custom_styles()
initialize_session_state()

# Sidebar Filters
with st.sidebar:
    st.header("🔍 Search Filters")
    search_query = st.text_input("Title or Author:", help="Search across the library...")
    
    # Dynamic Topic List
    topics = sorted(list(set([p["topic"] for p in st.session_state.papers])))
    topic_filter = st.selectbox("Filter by Topic:", ["All"] + topics)
    
    # Dynamic Year Range
    years = [p["year"] for p in st.session_state.papers]
    if years:
        min_y, max_y = min(years), max(years)
        year_range = st.slider("Publication Year:", min_y, max_y, (min_y, max_y))
    else:
        year_range = (1900, 2026)

# Main Paper Browser View
st.title("📚 Comprehensive Paper Browser")
st.write(f"Browsing **{len(st.session_state.papers)}** academic papers available for analysis.")

# Filter Logic
filtered_papers = []
for paper in st.session_state.papers:
    # Match Search
    match_search = not search_query or (
        search_query.lower() in paper["title"].lower() or 
        search_query.lower() in paper["author"].lower()
    )
    
    # Match Topic
    match_topic = topic_filter == "All" or paper["topic"] == topic_filter
    
    # Match Year
    match_year = year_range[0] <= paper["year"] <= year_range[1]
    
    if match_search and match_topic and match_year:
        filtered_papers.append(paper)

st.write(f"Found **{len(filtered_papers)}** matches.")

# Layout: Grid display of papers
if filtered_papers:
    # Use a grid layout
    cols = st.columns(3)
    for i, paper in enumerate(filtered_papers):
        with cols[i % 3]:
            display_paper_card(paper)
            # Detail expander
            with st.expander("Details & Abstract"):
                st.markdown(f"**Title:** {paper['title']}")
                st.markdown(f"**Author:** {paper['author']}")
                st.markdown(f"**Year:** {paper['year']}")
                st.markdown(f"**Topic:** {paper['topic']}")
                st.markdown(f"**Abstract:**")
                st.write(paper['abstract'])
else:
    st.warning("No papers match your search criteria. Try adjusting the filters.")

# Footer
st.markdown("---")
st.markdown("<p style='text-align: center; color: #64748B;'>Research Copilot v1.0 | Literature Browser</p>", unsafe_allow_html=True)

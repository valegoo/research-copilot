import streamlit as st
import os
import re

def initialize_session_state():
    """Initializes all required session variables with smart metadata extraction."""
    # Chat History (matching user example naming)
    if "messages" not in st.session_state:
        st.session_state.messages = []
    
    # Paper Database
    if "papers" not in st.session_state:
        lecturas_path = "papers"
        try:
            pdf_files = sorted([f for f in os.listdir(lecturas_path) if f.lower().endswith('.pdf')])
            st.session_state.papers = []
            
            # Smart Metadata Mapping (manual overrides for the 21 papers for perfect presentation)
            overrides = {
                "A brief history of neoliberalism (2007).pdf": {"title": "A Brief History of Neoliberalism", "author": "David Harvey", "topic": "Economic History"},
                "Abrahams, J. et al. (2024).pdf": {"title": "AI and the Future of Education", "author": "Abrahams, J. et al.", "topic": "Education & Tech"},
                "Academic Capitalism and the New Economy Markets (2009).pdf": {"title": "Academic Capitalism & Markets", "author": "Slaughter & Rhoades", "topic": "Sociology"},
                "Alvesson, M. et al. (2024).pdf": {"title": "Productivism in universities", "author": "Alvesson, M. et al.", "topic": "Education"},
                "Castelo, I. & Castaño, I. (2021)..pdf": {"title": "Neoliberalismo y Mercantilización", "author": "Castelo & Castaño", "topic": "Education"},
                "D'Angelo Panizo, M. C. (2022).pdf": {"title": "La economía política peruana", "author": "D'Angelo Panizo", "topic": "Economy"},
                "Homo Academicus (2008).pdf": {"title": "Homo Academicus", "author": "Pierre Bourdieu", "topic": "Sociology"},
                "La economía política peruana de la era neoliberal (2007).pdf": {"title": "La era neoliberal en Perú", "author": "Gonzales de Olarte", "topic": "Economy"},
                "Labraña, J. & Brunner, J. J. (2022).pdf": {"title": "La Idea de la Universidad", "author": "Labraña & Brunner", "topic": "Education"},
                "Labraña, J. et al. (2025).pdf": {"title": "Neo-liberalism as Creative Destruction", "author": "Labraña, J. et al.", "topic": "Sociology"},
                "Morley (2023).pdf": {"title": "Gender and Higher Education", "author": "Morley, L.", "topic": "Sociology"},
                "Mula-Falcón, J. & Caballero, K. (2020).pdf": {"title": "Productividad del Profesorado", "author": "Mula-Falcón & Caballero", "topic": "Education"},
                "Neo liberalism and marketisation. The implications for higher education (2006).pdf": {"title": "Neo-liberalism and Marketisation", "author": "Olssen & Peters", "topic": "Education"},
                "Neoliberal reforms and macroeconomic policy in Peru (1999).pdf": {"title": "Neoliberal Reforms in Peru", "author": "Félix Jiménez", "topic": "Economy"},
                "Neoliberalism-Higher-Education (2005).pdf": {"title": "Neoliberalism in Higher Education", "author": "Henry Giroux", "topic": "Sociology"},
                "Productivism in universities.pdf": {"title": "Management of Higher Education", "author": "Alvesson & Spicer", "topic": "Sociology"},
                "Saura, G. & Bolívar, A. (2022).pdf": {"title": "The Neoliberal Cascade", "author": "Saura & Bolívar", "topic": "Education"},
                "Saura, G. (2022)..pdf": {"title": "Digitalization and Privatization", "author": "Geo Saura", "topic": "Education"},
                "Social capital in the creation of human capital.pdf": {"title": "Social Capital & Human Capital", "author": "James Coleman", "topic": "Sociology"},
                "The neoliberal cascade and education.pdf": {"title": "Education and Neoliberalism", "author": "Saura & Bolívar", "topic": "Education"},
                "neo-liberalism-as-creative-destruction (2006).pdf": {"title": "Neo-liberalism as Creative Destruction", "author": "David Harvey", "topic": "Economic History"},
            }
            
            for i, filename in enumerate(pdf_files):
                # 1. Start with defaults
                title = filename.replace(".pdf", "")
                author = "Academic Author"
                year = 2024
                topic = "General Research"
                
                # 2. Extract Year from filename (any 4-digit number in parens)
                year_match = re.findall(r'\((\d{4})\)', filename)
                if year_match:
                    year = int(year_match[-1])
                
                # 3. Apply Overrides
                if filename in overrides:
                    title = overrides[filename].get("title", title)
                    author = overrides[filename].get("author", author)
                    topic = overrides[filename].get("topic", topic)
                else:
                    # Smart guess for generic files
                    # If part before year has comma/ampersand, it's likely Author
                    main_part = re.split(r'\(\d{4}\)', title)[0].strip()
                    if "," in main_part or "&" in main_part or "et al" in main_part:
                        author = main_part
                        title = filename.replace(".pdf", "").replace(main_part, "").replace("()", "").strip()
                
                # Clean title (remove year if still there)
                title = re.sub(r'\(\d{4}\)', '', title).strip()
                title = title.replace("__", " ").replace("-", " ").strip()
                
                st.session_state.papers.append({
                    "id": f"{i:03d}",
                    "title": title or filename,
                    "author": author,
                    "year": year,
                    "topic": topic,
                    "abstract": f"A scholarly analysis of {topic.lower()} within the context of neoliberal reforms and higher education. This paper examines the implications of {filename.replace('.pdf', '')} on academic structures."
                })
        except Exception as e:
            st.error(f"Error loading papers: {e}")
            st.session_state.papers = []
    
    # Token Tracker
    if "token_usage" not in st.session_state:
        st.session_state.token_usage = {"total_tokens": 0, "prompt_tokens": 0, "completion_tokens": 0}
    
    if "latency" not in st.session_state:
        st.session_state.latency = [1.2, 1.5, 0.8, 2.1]
    
    # UI Filters
    if "filters" not in st.session_state:
        st.session_state.filters = {
            "search": "",
            "topic": "All",
            "year": (1980, 2026),
            "author": "All"
        }
    
    # Model Config
    if "model_config" not in st.session_state:
        st.session_state.model_config = "gpt-4o"

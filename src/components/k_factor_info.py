import streamlit as st
from src.config import K_FACTOR_DATA

def render_k_factor_info():
    """Render K-factor information panel."""
    with st.expander("📊 K-Factor Information & Canopy Types", expanded=False):
        st.markdown("""
        ### 🏭 Canopy Types and K-Factor Patterns
        
        K-factors are automatically calculated for each section based on your selected canopy model and number of KSAs per section.
        """)
        
        # Section-based models
        st.markdown("#### 📏 **Section-Based Models** (1-6 KSAs)")
        
        col1, col2 = st.columns(2)
        
        with col1:
            st.markdown("""
            **🔥 Capture Jet™ Hoods**
            - **KVF, KVI, KCH-F, KCH-I**
            - K-factors: 71.8 to 430.8
            - Standard capture technology
            """)
            
            st.markdown("""
            **🌊 Capture Ray™ Hoods**
            - **UVF, UVI**
            - K-factors: 49.7 to 298.2
            - With MFA values
            """)
            
            st.markdown("""
            **💧 Water Wash Hoods**
            - **KWF, KWI, UWF, UWI**
            - **CMW-FMOD, CMW-IMOD**
            - K-factors: 65.5 to 393.0
            """)
        
        with col2:
            st.markdown("""
            **🔥 Capture Jet™ Low Proximity**
            - **KSR-S, KSR-F, KSR-M**
            - K-factors: 67.7 to 406.2
            - Low proximity installation
            """)
            
            st.markdown("""
            **🌊 Capture Ray™ Low Proximity**
            - **USR-S, USR-F, USR-M**
            - K-factors: 67.7 to 406.2
            - Low proximity installation
            """)
        
        # Length-based models
        st.markdown("---")
        st.markdown("#### 📐 **Length-Based Models** (1000-4000mm)")
        
        col1, col2 = st.columns(2)
        
        with col1:
            st.markdown("""
            **❄️ Cold Mist Only**
            - **CMW-F, CMW-I**
            - Length: 1000-3000mm
            - K-factors: 115 to 345
            """)
        
        with col2:
            st.markdown("""
            **♨️ Steam Hoods**
            - **KVD, KVV**
            - Length: 1000-4000mm
            - K-factors: 161 to 644
            """)
        
        # Model naming explanation
        st.markdown("---")
        st.markdown("#### 🏷️ **Model Naming Convention**")
        st.markdown("""
        - **-F suffix**: Front access models (no section data required)
        - **-I suffix**: Island models
        - **-S suffix**: Standard models
        - **-M suffix**: Modified models
        - **-MOD suffix**: Modular systems
        """)
        
        # K-factor calculation info
        st.markdown("---")
        st.markdown("#### 🧮 **K-Factor Calculation**")
        st.info("""
        **Section-Based Models**: K-factor = Base value × Number of KSAs (selected per section)
        
        **Length-Based Models**: K-factor varies by length (1000mm increments)
        
        K-factors are automatically calculated and displayed for each section when you select KSAs.
        """)

def render_k_factor_table():
    """Render a detailed K-factor reference table."""
    st.markdown("### 📋 Complete K-Factor Reference")
    
    # Create tabs for different model types
    tab1, tab2 = st.tabs(["Section-Based Models", "Length-Based Models"])
    
    with tab1:
        st.markdown("#### Section-Based K-Factors")
        
        # Create a comprehensive table
        data = []
        for model, info in K_FACTOR_DATA.items():
            if info['type'] == 'section_based':
                for ksas, k_factor in info['sections'].items():
                    data.append({
                        'Model': model,
                        'KSAs': ksas,
                        'K-Factor': k_factor
                    })
        
        if data:
            import pandas as pd
            df = pd.DataFrame(data)
            st.dataframe(df, use_container_width=True)
    
    with tab2:
        st.markdown("#### Length-Based K-Factors")
        
        # Create length-based table
        data = []
        for model, info in K_FACTOR_DATA.items():
            if info['type'] == 'length_based':
                for length, k_factor in info['length_ranges'].items():
                    data.append({
                        'Model': model,
                        'Length (mm)': length,
                        'K-Factor': k_factor
                    })
        
        if data:
            import pandas as pd
            df = pd.DataFrame(data)
            st.dataframe(df, use_container_width=True) 
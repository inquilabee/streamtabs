import streamlit as st

from streamtabs.core import STSidebar


class ExamConfigSidebar(STSidebar):
    class Meta:
        name = "exam_config_sidebar"

    def render(self):
        """Configure exam settings and provide app information."""
        st.header("⚙️ Exam Configuration")
        
        # Exam settings
        st.subheader("Exam Settings")
        exam1_weight = st.slider("Exam 1 Weight (%)", 0, 100, 50)
        exam2_weight = st.slider("Exam 2 Weight (%)", 0, 100, 50)
        
        if exam1_weight + exam2_weight != 100:
            st.warning("⚠️ Weights should add up to 100%")
        
        # App info
        st.subheader("📚 App Information")
        st.info("""
        **Student Exam Management System**
        
        1. **Exam 1 Input**: Enter student names and marks
        2. **Exam 2 Input**: Add Exam 2 marks for existing students  
        3. **Results Summary**: View topper and statistics
        
        Data flows automatically between tabs!
        """)
        
        # Quick stats
        st.subheader("📊 Quick Stats")
        col1, col2 = st.columns(2)
        with col1:
            st.metric("Total Exams", "2")
        with col2:
            st.metric("Max Marks per Exam", "100")
        
        return {
            "exam1_weight": exam1_weight,
            "exam2_weight": exam2_weight
        }

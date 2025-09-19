import pandas as pd
import streamlit as st

from streamtabs.core import STTab


class Exam2InputTab(STTab):
    class Meta:
        name = "exam2_input"
        title = "Exam 2 Input"
        icon = "📊"
        order = 2
        required_inputs = ["students_data"]
        required_outputs = ["updated_students_data"]

    def render(self, students_data, **kwargs):
        """Display Exam 1 data and add Exam 2 marks."""
        
        st.header("Exam 2: Add Marks")
        st.write("Review Exam 1 data and add Exam 2 marks.")
        
        if not students_data.empty:
            st.subheader("Current Student Data:")
            st.dataframe(students_data)
            
            # Add Exam 2 marks
            st.subheader("Add Exam 2 Marks:")
            updated_data = students_data.copy()
            
            for idx, row in students_data.iterrows():
                col1, col2 = st.columns(2)
                with col1:
                    st.write(f"**{row['Name']}**")
                with col2:
                    exam2_marks = st.number_input(
                        f"Exam 2 Marks:", 
                        min_value=0, 
                        max_value=100, 
                        value=0, 
                        key=f"exam2_{idx}"
                    )
                    updated_data.loc[idx, 'Exam2'] = exam2_marks
            
            st.subheader("Updated Student Data:")
            st.dataframe(updated_data)
            return {"updated_students_data": updated_data}
        else:
            st.warning("No student data available. Please go to Exam 1 Input tab first.")
            return {"updated_students_data": pd.DataFrame()}

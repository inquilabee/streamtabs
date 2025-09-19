import pandas as pd
import streamlit as st

from streamtabs.core import STTab


class Exam1InputTab(STTab):
    class Meta:
        name = "exam1_input"
        title = "Exam 1 Input"
        icon = "📝"
        order = 1
        required_inputs = []
        required_outputs = ["students_data"]

    def render(self, **kwargs):
        """Enter student names and marks for Exam 1."""
        st.header("Exam 1: Enter Student Data")
        st.write("Enter student names and their marks for Exam 1.")
        
        # Get number of students
        num_students = st.number_input("Number of students:", min_value=1, max_value=50, value=5)
        
        students_data = []
        for i in range(num_students):
            col1, col2 = st.columns(2)
            with col1:
                name = st.text_input(f"Student {i+1} Name:", key=f"name_{i}")
            with col2:
                marks = st.number_input(f"Marks:", min_value=0, max_value=100, value=0, key=f"marks_{i}")
            if name:
                students_data.append({"Name": name, "Exam1": marks})
        
        if students_data:
            df = pd.DataFrame(students_data)
            st.dataframe(df)
            return {"students_data": df}
        else:
            st.warning("Please enter at least one student's data.")
            return {"students_data": pd.DataFrame()}

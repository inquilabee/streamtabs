import pandas as pd
import streamlit as st

from streamtabs.core import STTab


class ResultsSummaryTab(STTab):
    class Meta:
        name = "results_summary"
        title = "Results Summary"
        icon = "🏆"
        order = 3
        required_inputs = ["updated_students_data"]
        required_outputs = []

    def render(self, updated_students_data, **kwargs):
        """Display topper student and summary statistics."""
        st.header("Results Summary")
        
        if not updated_students_data.empty and 'Exam2' in updated_students_data.columns:
            # Calculate total marks
            df = updated_students_data.copy()
            df['Total'] = df['Exam1'] + df['Exam2']
            df['Average'] = df['Total'] / 2
            
            st.subheader("Student Results:")
            st.dataframe(df)
            
            # Find topper
            topper = df.loc[df['Total'].idxmax()]
            st.subheader("🏆 Topper Student:")
            st.success(f"**{topper['Name']}** - Total: {topper['Total']}/200, Average: {topper['Average']:.1f}")
            
            # Summary statistics
            st.subheader("📊 Summary Statistics:")
            col1, col2, col3 = st.columns(3)
            
            with col1:
                st.metric("Total Students", len(df))
                st.metric("Highest Total", f"{df['Total'].max()}/200")
            
            with col2:
                st.metric("Average Total", f"{df['Total'].mean():.1f}")
                st.metric("Average Exam 1", f"{df['Exam1'].mean():.1f}")
            
            with col3:
                st.metric("Average Exam 2", f"{df['Exam2'].mean():.1f}")
                st.metric("Lowest Total", f"{df['Total'].min()}/200")
            
            # Performance chart
            st.subheader("📈 Performance Chart:")
            st.bar_chart(df.set_index('Name')[['Exam1', 'Exam2', 'Total']])
            
        else:
            st.warning("No complete student data available. Please complete Exam 1 and Exam 2 input first.")

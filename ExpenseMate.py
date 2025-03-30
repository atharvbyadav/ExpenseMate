import streamlit as st
import pandas as pd
import sqlite3
import plotly.express as px
from datetime import datetime

# Initialize database
conn = sqlite3.connect("expenses.db", check_same_thread=False)
cursor = conn.cursor()

cursor.execute('''
    CREATE TABLE IF NOT EXISTS expenses (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        date TEXT,
        category TEXT,
        description TEXT,
        amount REAL
    )
''')
conn.commit()

# Sidebar - Budget Setup
st.sidebar.title("💰 Budget Tracker")
budget = st.sidebar.number_input("Set Monthly Budget (₹)", min_value=0.0, value=10000.0, step=500.0, format="%.2f")

# Sidebar - Navigation
page = st.sidebar.radio("📌 Navigate", ["➕ Add Expense", "📊 View Report"])

# Autofill common categories
common_categories = ["Food", "Rent", "Utilities", "Transport", "Entertainment", "Healthcare", "Shopping", "Miscellaneous"]

if page == "➕ Add Expense":
    st.title("➕ Add New Expense")

    with st.form("expense_form"):
        date = st.date_input("📅 Date", datetime.today())
        category = st.selectbox("📌 Category", common_categories)
        description = st.text_input("📝 Description")
        amount = st.number_input("💵 Amount (₹)", min_value=0.01, step=0.01, format="%.2f")
        submit = st.form_submit_button("✅ Add Expense")

        if submit:
            cursor.execute("INSERT INTO expenses (date, category, description, amount) VALUES (?, ?, ?, ?)",
                           (date.strftime('%Y-%m-%d'), category, description, amount))
            conn.commit()
            st.success("✅ Expense added successfully!")

elif page == "📊 View Report":
    st.title("📊 Expense Report")

    # Fetch expenses
    df = pd.read_sql("SELECT * FROM expenses", conn)

    if not df.empty:
        # Convert date column to datetime
        df["date"] = pd.to_datetime(df["date"])

        # Display expenses table
        st.subheader("💼 Expense Details")
        st.dataframe(df[['date', 'category', 'description', 'amount']].rename(columns={"amount": "Amount (₹)"}))

        # Category-wise expense breakdown
        category_expense = df.groupby("category")["amount"].sum().reset_index()

        # Pie chart for category expenses
        fig = px.pie(category_expense, names="category", values="amount", title="📌 Expenses by Category (₹)")
        st.plotly_chart(fig)

        # Line chart for spending trend
        fig2 = px.line(df, x="date", y="amount", title="📉 Spending Over Time (₹)", markers=True)
        st.plotly_chart(fig2)

        # Budget summary
        total_spent = df["amount"].sum()
        remaining_budget = budget - total_spent

        st.subheader("💡 Budget Summary")
        st.metric(label="Total Spent", value=f"₹{total_spent:,.2f}")
        st.metric(label="Remaining Budget", value=f"₹{remaining_budget:,.2f}")

        # CSV Export
        csv = df.to_csv(index=False).encode("utf-8")
        st.download_button("📥 Download Report as CSV", csv, "expenses_report.csv", "text/csv")

    else:
        st.warning("⚠️ No expenses recorded yet!")

# Close database connection
conn.close()
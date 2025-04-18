import streamlit as st
import pandas as pd
import sqlite3
import plotly.express as px
from datetime import datetime, time

# App Title
st.title("💰 ExpenseMate - Personal Finance Tracker")

# Initialize database
conn = sqlite3.connect("expenses.db", check_same_thread=False)
cursor = conn.cursor()

cursor.execute('''
    CREATE TABLE IF NOT EXISTS expenses (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        date TEXT,
        time TEXT,
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
page = st.sidebar.radio("📌 Navigate", ["➕ Add Expense", "❌ Delete Expense", "📊 View Report"])

# Autofill common categories
common_categories = ["Food", "Rent", "Utilities", "Transport", "Entertainment", "Healthcare", "Shopping", "Miscellaneous"]

if page == "➕ Add Expense":
    st.title("➕ Add New Expense")

    with st.form("expense_form"):
        date = st.date_input("📅 Date", datetime.today())
        
        # Time selection in 12-hour format with AM/PM
        col1, col2, col3 = st.columns(3)
        with col1:
            selected_hour = st.selectbox("🕒 Hour", list(range(1, 13)), index=11)
        with col2:
            selected_minute = st.selectbox("⏳ Minute", list(range(0, 60)), index=0)
        with col3:
            selected_am_pm = st.selectbox("☀️ AM/PM", ["AM", "PM"])
        
        if selected_am_pm == "PM" and selected_hour != 12:
            selected_hour += 12
        elif selected_am_pm == "AM" and selected_hour == 12:
            selected_hour = 0
        
        time_selected = time(selected_hour, selected_minute)

        category = st.selectbox("📌 Category", common_categories)
        description = st.text_input("📝 Description")
        amount = st.number_input("💵 Amount (₹)", min_value=0.01, step=0.01, format="%.2f")
        submit = st.form_submit_button("✅ Add Expense")

        if submit:
            cursor.execute("INSERT INTO expenses (date, time, category, description, amount) VALUES (?, ?, ?, ?, ?)",
                           (date.strftime('%Y-%m-%d'), time_selected.strftime('%I:%M %p'), category, description, amount))
            conn.commit()
            st.success("✅ Expense added successfully!")
            st.rerun()

elif page == "❌ Delete Expense":
    st.title("❌ Delete Expense")
    df = pd.read_sql("SELECT * FROM expenses", conn)

    if not df.empty:
        df["date"] = pd.to_datetime(df["date"]).dt.date
        df["time"] = pd.to_datetime(df["time"], format='%I:%M %p').dt.strftime('%I:%M %p')
        df_sorted = df.sort_values(by="date", ascending=False)

        df_sorted["display"] = df_sorted["date"].astype(str) + " " + df_sorted["time"] + " - " + df_sorted["category"] + " (₹" + df_sorted["amount"].astype(str) + ")"
        expense_to_delete = st.selectbox("Select an expense to delete", df_sorted["display"])
        delete_button = st.button("🗑️ Delete Selected Expense")

        if delete_button and expense_to_delete:
            selected_row = df_sorted[df_sorted["display"] == expense_to_delete]
            if not selected_row.empty:
                expense_id = int(selected_row["id"].values[0])
                cursor.execute("DELETE FROM expenses WHERE id = ?", (expense_id,))
                conn.commit()
                st.success("✅ Expense deleted successfully!")
                st.rerun()
            else:
                st.warning("⚠️ Error finding the selected expense.")
    else:
        st.warning("⚠️ No expenses to delete!")

elif page == "📊 View Report":
    st.title("📊 Expense Report")

    df = pd.read_sql("SELECT * FROM expenses", conn)

    if not df.empty:
        df["date"] = pd.to_datetime(df["date"]).dt.date
        df["time"] = pd.to_datetime(df["time"], format='%I:%M %p').dt.strftime('%I:%M %p')

        st.subheader("💼 Expense Details")
        st.dataframe(df[['id', 'date', 'time', 'category', 'description', 'amount']].rename(columns={"amount": "Amount (₹)"}))

        category_expense = df.groupby("category")["amount"].sum().reset_index()
        fig = px.pie(category_expense, names="category", values="amount", title="📌 Expenses by Category (₹)")
        st.plotly_chart(fig)

        fig2 = px.line(df, x="date", y="amount", title="📉 Spending Over Time (₹)", markers=True)
        st.plotly_chart(fig2)

        total_spent = df["amount"].sum()
        remaining_budget = budget - total_spent

        st.subheader("💡 Budget Summary")
        st.metric(label="Total Spent", value=f"₹{total_spent:,.2f}")
        st.metric(label="Remaining Budget", value=f"₹{remaining_budget:,.2f}")

        csv = df.to_csv(index=False).encode("utf-8")
        st.download_button("📥 Download Report as CSV", csv, "expenses_report.csv", "text/csv")
    else:
        st.warning("⚠️ No expenses recorded yet!")

# Close database connection
conn.close()

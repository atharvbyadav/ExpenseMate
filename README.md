# ExpenseMate

## Overview

ExpenseMate is a user-friendly personal finance tracker built using **Streamlit** and **SQLite**. It helps users monitor expenses, analyze spending habits, and manage their monthly budget with interactive visualizations.

🚀 **Live Demo**: [ExpenseMate](https://expensemate.streamlit.app/)

🔗 **GitHub Repository**: [ExpenseMate GitHub](https://github.com/atharvbyadav/ExpenseMate)

🌟 If you find this project useful, **please star the repository!** 🌟

---

## Features

### ✅ Add Expenses

- Select the **date** and **time** (12-hour format with AM/PM option).
- Choose an expense **category** (Food, Rent, Transport, etc.).
- Enter **description** and **amount**.
- Store entries in an **SQLite database**.

### 📊 View Expense Report

- **View all expenses** in a table format.
- **Pie chart visualization** of expenses by category.
- **Line chart tracking** spending over time.
- **Budget Summary** with total spent and remaining balance.
- **Download expenses report** as a CSV file.

### ❌ Delete Expenses

- Select any **recorded expense** to delete from the database.

---

## Installation & Usage 🛠️

### 🔹 Prerequisites

Ensure you have **Python 3.x** installed on your system.

### Step 1️⃣ - Clone the Repository

```sh
git clone https://github.com/atharvbyadav/ExpenseMate.git
cd ExpenseMate
```

### Step 2️⃣ - Set Up a Virtual Environment (Recommended)

To prevent package conflicts, create and activate a virtual environment:

```sh
python -m venv venv
source venv/bin/activate  # On Windows, use: venv\Scripts\activate
```

### Step 3️⃣ - Install Dependencies

Install required dependencies using the provided **requirements.txt** file:

```sh
pip install -r requirements.txt
```

### Step 4️⃣ - Run the Application

```sh
streamlit run ExpenseMate.py
```

The application will open in your default web browser.

---

## Usage Guide

### 🏠 Home Page

- The **sidebar** provides navigation to different sections:
  - **Add Expense**
  - **View Report**
  - **Delete Expense**
- Set your **monthly budget** in the sidebar.

### ➕ Adding an Expense

1. Click **"Add Expense"**.
2. Select **Date** and **Time (12-hour format)**.
3. Choose an **expense category**.
4. Enter **description** and **amount**.
5. Click **"Add Expense"** to save.

### 📊 Viewing Reports

- Click **"View Report"**.
- View **expense details, category breakdown, and spending trends**.
- **Download** the report as CSV.

### ❌ Deleting an Expense

1. Click **"Delete Expense"**.
2. Select an expense from the dropdown.
3. Click **"Delete"** to remove it.

---

## Technologies Used

- **Streamlit** - Frontend UI framework
- **SQLite** - Local database for storing expenses
- **Pandas** - Data handling and processing
- **Plotly** - Data visualization (Pie charts, Line graphs)

---

## License

This project is licensed under the **MIT License** - feel free to use and modify it!

---

## Future Enhancements

🚀 **Planned Features**:

- ✅ Advanced filtering and search for expenses
- 📅 Generate monthly & yearly reports
- 📱 Improve UI for mobile users
- 🔔 Add notifications for budget alerts

---

## Contributing

Want to improve ExpenseMate? Contributions are welcome! 🎉

Fork the repo, create a branch, and submit a pull request.

---

## Contact

💬 Feel free to reach out on GitHub or open an issue for suggestions and feedback!


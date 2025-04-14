Personal Finance Tracker
A user-friendly Streamlit web application to analyze and visualize personal spending patterns from CSV transaction data. This app provides an intuitive interface for uploading financial data, applying filters, and generating insightful visualizations to track spending habits effectively.
Features

CSV Upload: Upload transaction data with required columns: Date (e.g., 2025-01-01), Amount (e.g., 45.80), and Category (e.g., Food).
Data Cleaning: Automatically handles missing values, invalid entries, and formats data for consistency.
Interactive Filters: Filter by category and date range using a sidebar for tailored analysis.
Visualizations:
Overview Tab: Displays a snapshot of filtered data, total spending, and top spending category.
Spending Breakdown Tab: Shows a pie chart and category-wise spending summary.
Trends Tab: Includes bar charts for monthly and weekly spending, plus a heatmap for day-of-week and monthly trends.


Export Option: Download filtered data as a CSV file.
Responsive Design: Clean, organized layout with tabs and a modern Seaborn/Matplotlib styling.

Tech Stack

Python: Core programming language.
Streamlit: Framework for building the interactive web app.
Pandas: Data manipulation and cleaning.
Seaborn & Matplotlib: Data visualization for charts and heatmaps.
NumPy: Numerical operations support.

Installation

Clone the Repository:
git clone https://github.com/snehauppula/Finanace-Tracker.git
cd Finanace-Tracker


Set Up a Virtual Environment (optional but recommended):
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate


Install Dependencies:
pip install -r requirements.txt


Run the App:
streamlit run app.py



Usage

Prepare Your CSV File:Ensure your CSV has at least three columns: Date, Amount, and Category. Example:
Date,Amount,Category
2025-01-01,45.80,Food
2025-01-02,20.00,Transport


Launch the App:After running the app, open the provided local URL (e.g., http://localhost:8501) in your browser.

Interact with the App:

Upload your CSV file.
Use sidebar filters to select a category or date range.
Explore tabs for different insights: Overview, Spending Breakdown, and Trends.
Download the filtered dataset if needed.



Sample Data
For testing, you can use a sample CSV file with the following structure:
Date,Amount,Category
2025-01-01,45.80,Food
2025-01-02,20.00,Transport
2025-01-03,15.50,Entertainment

Screenshots
To be added: Upload screenshots of the app's interface (Overview, Spending Breakdown, Trends tabs).
Contributing
Contributions are welcome! Please follow these steps:

Fork the repository.
Create a new branch (git checkout -b feature/your-feature).
Commit your changes (git commit -m 'Add your feature').
Push to the branch (git push origin feature/your-feature).
Open a Pull Request.

License
This project is licensed under the MIT License. See the LICENSE file for details.
Acknowledgements

Built with ❤️ using Streamlit.
Inspired by the need for simple, visual personal finance tools.
Thanks to the open-source community for libraries like Pandas, Seaborn, and Matplotlib.


Created by Sneha | Finanace-Tracker

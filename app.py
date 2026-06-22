import matplotlib.pyplot as plt
import streamlit as st
import pandas as pd
import os

page = st.sidebar.selectbox(
    "Choose Section",
    [
        "Dashboard",
        "EMI Calculator",
        "SIP Calculator"
    ]
)
if page == "Dashboard":

    st.title("Personal Finance Dashboard")


    date = st.date_input("Date")

    transaction_type = st.selectbox(
        "Type",
        ["Income", "Expense"]
    )

    category = st.selectbox(
        "Category",
        [
            "Food",
            "Travel",
            "Games",
            "Education",
            "Shopping",
            "Entertainment",
            "Other"
        ]
    )
    amount = st.number_input(
        "Amount",
        min_value=0.0,
        step=1.0
    )

    if st.button("Save Transaction"):

        new_data = {
            "Date": [date],
            "Type": [transaction_type],
            "Category": [category],
            "Amount": [amount]
        }

        new_df = pd.DataFrame(new_data)

        if os.path.exists("transactions.csv"):
            old_df = pd.read_csv("transactions.csv")
            combined_df = pd.concat([old_df, new_df], ignore_index=True)
            combined_df.to_csv("transactions.csv", index=False)

        else:
            new_df.to_csv("transactions.csv", index=False)

        st.success("Transaction Saved!")
    if os.path.exists("transactions.csv"):
        st.header("All Transactions")

        df = pd.read_csv("transactions.csv")

        st.dataframe(df)
        
        if os.path.exists("transactions.csv"):
            st.header("All Transactions")

            df = pd.read_csv("transactions.csv")

            st.dataframe(df)

            total_income = df[df["Type"] == "Income"]["Amount"].sum()

            total_expense = df[df["Type"] == "Expense"]["Amount"].sum()

            savings = total_income - total_expense

            col1, col2, col3 = st.columns(3)

            with col1:
                st.metric("Total Income", f"₹{round(total_income,2)}")

            with col2:
                st.metric("Total Expense", f"₹{round(total_expense,2)}")

            with col3:
                st.metric("Savings", f"₹{round(savings,2)}")
                st.header("Income vs Expense")

                fig, ax = plt.subplots()

                ax.bar(
                    ["Income", "Expense"],
                    [total_income, total_expense]
                )

                ax.set_ylabel("Amount (₹)")
                ax.set_title("Income vs Expense Comparison")

                st.pyplot(fig)
                expense_df = df[df["Type"] == "Expense"]

            if not expense_df.empty:

                category_sum = expense_df.groupby("Category")["Amount"].sum()

                fig, ax = plt.subplots()

                ax.pie(
                    category_sum,
                    labels=category_sum.index,
                    autopct="%1.1f%%"
                )
                st.header("Expense Distribution")

                st.pyplot(fig)
                # Monthly Expense Trend Chart

                expense_df = df[df["Type"] == "Expense"]

                if not expense_df.empty:

                    expense_df["Date"] = pd.to_datetime(expense_df["Date"])

                    monthly_expense = (
                        expense_df.groupby(
                            expense_df["Date"].dt.to_period("M")
                        )["Amount"]
                        .sum()
                        .reset_index()
                    )

                    monthly_expense["Date"] = monthly_expense["Date"].astype(str)

                    fig, ax = plt.subplots()

                    ax.plot(
                            monthly_expense["Date"],
                            monthly_expense["Amount"],
                            marker="o"
                        )

                    ax.set_title("Monthly Expense Trend")
                    ax.set_xlabel("Month")
                    ax.set_ylabel("Expense (₹)")

                    plt.xticks(rotation=45)

                    st.header("Monthly Expense Trend")
                    st.pyplot(fig)
elif page == "EMI Calculator":

    st.title("EMI Calculator")

    loan_amount = st.number_input(
        "Loan Amount",
        min_value=0.0
    )

    interest_rate = st.number_input(
        "Annual Interest Rate (%)",
        min_value=0.0
    )

    tenure_years = st.number_input(
        "Tenure (Years)",
        min_value=1
    )

    if loan_amount > 0 and interest_rate > 0 and tenure_years > 0:

        r = interest_rate / (12 * 100)
        n = tenure_years * 12

        emi = loan_amount * r * ((1 + r) ** n) / (((1 + r) ** n) - 1)

        st.subheader("EMI Result")
        st.write(f"Monthly EMI: ₹ {emi:.2f}")
        

elif page == "SIP Calculator":

    st.title("SIP Calculator")

    monthly_sip = st.number_input(
        "Monthly SIP",
        min_value=0.0
    )

    expected_return = st.number_input(
        "Expected Return (%)",
        min_value=0.0
    )

    years = st.number_input(
        "Years",
        min_value=1
    )

    if monthly_sip > 0 and expected_return > 0 and years > 0:

        r = expected_return / (12 * 100)

        n = years * 12

        maturity_amount = monthly_sip * (((1 + r) ** n - 1) / r) * (1 + r)
        growth_data = []
        portfolio_value = 0

        for year in range(1, years + 1):

            months = year * 12

            value = monthly_sip * (((1 + r) ** months - 1) / r) * (1 + r)

            growth_data.append(value)

        total_investment = monthly_sip * n

        wealth_gained = maturity_amount - total_investment

        st.subheader("SIP Result")
        fig, ax = plt.subplots()

        ax.plot(
                range(1, years + 1),
                growth_data,
                marker="o"
            )

        ax.set_title("SIP Growth Over Time")
        ax.set_xlabel("Years")
        ax.set_ylabel("Portfolio Value (₹)")

        st.pyplot(fig)

        st.write(f"Total Investment: ₹ {total_investment:,.2f}")

        st.write(f"Wealth Gained: ₹ {wealth_gained:,.2f}")

        st.write(f"Maturity Amount: ₹ {maturity_amount:,.2f}")

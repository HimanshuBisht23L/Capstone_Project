# 📄 SheetPilot AI — Master QA & Test Prompts Guide

This document contains **10 Real-World Excel Test Datasets** (saved under `docs/test_datasets/`) along with **tailored testing prompts** (easy, medium, hard, and multi-step tax/finance prompts) for testing SheetPilot AI.

---

## 📁 Dataset 1: `1_Employee_Payroll_Tax.xlsx`
* **File Location:** `docs/test_datasets/1_Employee_Payroll_Tax.xlsx`
* **Columns:** `Employee ID`, `Employee Name`, `Department`, `Base Salary`, `HRA Allowance`, `PF Deduction (12%)`, `TDS Tax (10%)`, `Employment Status`
* **Description:** Corporate HR & Payroll register with salary breakdowns, PF, and tax deductions.

### 🧪 Test Prompts:
1. **Basic Categorical Filter:**
   ```text
   Filter rows where Department is IT / Software
   ```
2. **Multi-Condition Category & Numeric Filter:**
   ```text
   Filter rows where Department is IT / Software or Finance and Base Salary is above 70000
   ```
3. **Complex Math & Tax Calculation:**
   ```text
   Filter rows where Employment Status is Active, calculate a 10% HRA_Bonus on Base Salary, calculate Net_Pay adding Base Salary and HRA Allowance minus TDS Tax (10%), and sort by Base Salary descending.
   ```

---

## 📁 Dataset 2: `2_GST_Sales_Register.xlsx`
* **File Location:** `docs/test_datasets/2_GST_Sales_Register.xlsx`
* **Columns:** `Invoice No`, `Customer Name`, `Customer State`, `Taxable Value`, `GST Rate`, `CGST (9%)`, `SGST (9%)`, `Total Invoice Value`, `Payment Status`
* **Description:** GST Invoice sales register for Tax Audit & GST Return filing (GSTR-1 / GSTR-3B).

### 🧪 Test Prompts:
1. **State-Wise Filter:**
   ```text
   Filter rows where Customer State is Maharashtra
   ```
2. **High-Value Taxable Filter:**
   ```text
   Filter rows where Taxable Value is greater than 200000 and Payment Status is Paid
   ```
3. **GST Tax Calculation & Text Replacement:**
   ```text
   Replace Zentron Technologies with Zentron Tech Solutions, filter rows where Payment Status is Pending or Overdue, calculate Total_GST adding CGST (9%) and SGST (9%), and sort by Taxable Value descending.
   ```

---

## 📁 Dataset 3: `3_Corporate_Expenses.xlsx`
* **File Location:** `docs/test_datasets/3_Corporate_Expenses.xlsx`
* **Columns:** `Voucher ID`, `Expense Date`, `Department`, `Expense Category`, `Amount`, `Payment Method`, `Approval Status`
* **Description:** Corporate expenditure ledger tracking audit fees, cloud infrastructure, and marketing expenses.

### 🧪 Test Prompts:
1. **Department Expenses Filter:**
   ```text
   Filter rows where Department is Marketing
   ```
2. **Approval Status & Payment Method Filter:**
   ```text
   Filter rows where Approval Status is Approved and Payment Method is Bank Transfer
   ```
3. **Expense Threshold & Tax Average:**
   ```text
   Filter rows where Amount is above 50000, calculate 18% GST_Expense on Amount, calculate Average_Expense for filtered rows, and sort by Amount descending.
   ```

---

## 📁 Dataset 4: `4_Quarterly_Financial_Revenue.xlsx`
* **File Location:** `docs/test_datasets/4_Quarterly_Financial_Revenue.xlsx`
* **Columns:** `Product Division`, `Target Region`, `Q1 Revenue`, `Q2 Revenue`, `Q3 Revenue`, `Q4 Revenue`, `Units Sold`
* **Description:** Multi-quarter corporate revenue matrix for product divisions across global regions.

### 🧪 Test Prompts:
1. **Regional Revenue Filter:**
   ```text
   Filter rows where Target Region is North America or Europe
   ```
2. **Quarterly Growth Calculation:**
   ```text
   Calculate H2_Revenue adding Q3 Revenue and Q4 Revenue, calculate Annual_Total_Revenue adding Q1 Revenue and Q2 Revenue and Q3 Revenue and Q4 Revenue
   ```
3. **Performance Metrics & Sort:**
   ```text
   Filter rows where Units Sold is greater than 800, calculate H2_Growth subtracting Q2 Revenue from Q4 Revenue, and sort by Units Sold descending.
   ```

---

## 📁 Dataset 5: `5_Inventory_Stock_Audit.xlsx`
* **File Location:** `docs/test_datasets/5_Inventory_Stock_Audit.xlsx`
* **Columns:** `SKU Code`, `Item Description`, `Category`, `Unit Price`, `Quantity in Stock`, `Reorder Threshold`, `Stock Status`
* **Description:** Warehouse inventory tracking SKU pricing, stock levels, and reorder alerts.

### 🧪 Test Prompts:
1. **Stock Status Filter:**
   ```text
   Filter rows where Stock Status is Low Stock
   ```
2. **Category & High-Value Inventory Filter:**
   ```text
   Filter rows where Category is Accessories or Peripherals and Unit Price is greater than 10000
   ```
3. **Inventory Valuation Calculation:**
   ```text
   Calculate Total_Inventory_Value multiplying Unit Price by Quantity in Stock, filter rows where Quantity in Stock is less than 50, and sort by Total_Inventory_Value descending.
   ```

---

## 📁 Dataset 6: `6_TDS_Deduction_Report.xlsx`
* **File Location:** `docs/test_datasets/6_TDS_Deduction_Report.xlsx`
* **Columns:** `Deductee Code`, `Vendor Name`, `PAN Number`, `TDS Section`, `Gross Payment`, `TDS Rate`, `TDS Deducted`, `Deposit Status`
* **Description:** Income Tax TDS Deduction ledger under Sections 194C (Contractor) and 194J (Professional).

### 🧪 Test Prompts:
1. **Section 194J Professional Filter:**
   ```text
   Filter rows where TDS Section is 194J (Professional)
   ```
2. **High Gross Payment Filter:**
   ```text
   Filter rows where Gross Payment is greater than 300000 and Deposit Status is Deposited
   ```
3. **TDS Audit & Net Payment Calculation:**
   ```text
   Filter rows where Deposit Status is Pending Deposit or Deposited, calculate Net_Payment_Made subtracting TDS Deducted from Gross Payment, calculate Average_TDS_Deducted, and sort by Gross Payment descending.
   ```

---

## 📁 Dataset 7: `7_Client_Invoicing_AR.xlsx`
* **File Location:** `docs/test_datasets/7_Client_Invoicing_AR.xlsx`
* **Columns:** `Invoice ID`, `Client Name`, `Invoice Date`, `Billed Amount`, `Received Amount`, `Balance Due`, `Payment Aging`
* **Description:** Accounts Receivable (AR) aging ledger tracking outstanding client balances.

### 🧪 Test Prompts:
1. **Overdue Invoices Filter:**
   ```text
   Filter rows where Payment Aging is 30 Days Overdue or 60 Days Overdue
   ```
2. **Outstanding Balance Filter:**
   ```text
   Filter rows where Balance Due is greater than 20000
   ```
3. **Collection Percentage Calculation:**
   ```text
   Filter rows where Billed Amount is greater than 30000, calculate Outstanding_Ratio dividing Balance Due by Billed Amount, and sort by Balance Due descending.
   ```

---

## 📁 Dataset 8: `8_Profit_Loss_Statement.xlsx`
* **File Location:** `docs/test_datasets/8_Profit_Loss_Statement.xlsx`
* **Columns:** `Branch Code`, `City Location`, `Gross Revenue`, `COGS Expenses`, `Operating Overhead`, `Net Profit`, `Profitability Grade`
* **Description:** Branch-level P&L statement comparing gross revenues against operational expenditures.

### 🧪 Test Prompts:
1. **Tier A Profitability Filter:**
   ```text
   Filter rows where Profitability Grade is Tier A
   ```
2. **Revenue Threshold Filter:**
   ```text
   Filter rows where Gross Revenue is greater than 6000000
   ```
3. **Profit Margin & Overhead Ratio Calculation:**
   ```text
   Calculate Net_Operating_Income subtracting COGS Expenses and Operating Overhead from Gross Revenue, calculate Profit_Margin_Pct dividing Net Profit by Gross Revenue, and sort by Gross Revenue descending.
   ```

---

## 📁 Dataset 9: `9_Bank_Reconciliation.xlsx`
* **File Location:** `docs/test_datasets/9_Bank_Reconciliation.xlsx`
* **Columns:** `Txn ID`, `Transaction Date`, `Description`, `Debit Amount`, `Credit Amount`, `Running Balance`, `Reconciled Status`
* **Description:** Bank reconciliation ledger tracking credits, debits, wire receipts, and reconciliation status.

### 🧪 Test Prompts:
1. **Pending Reconciliation Filter:**
   ```text
   Filter rows where Reconciled Status is Pending
   ```
2. **Credit Receipts Filter:**
   ```text
   Filter rows where Credit Amount is greater than 100000
   ```
3. **Net Cash Flow & Sort:**
   ```text
   Filter rows where Reconciled Status is Matched, calculate Net_Transaction_Impact subtracting Debit Amount from Credit Amount, and sort by Running Balance descending.
   ```

---

## 📁 Dataset 10: `10_Student_Academic_Grades.xlsx`
* **File Location:** `docs/test_datasets/10_Student_Academic_Grades.xlsx`
* **Columns:** `Student ID`, `Student Name`, `Stream`, `Midterm Score`, `Final Exam Score`, `Attendance Percentage`, `Academic Result`
* **Description:** Educational institute academic gradebook evaluating midterm and final exam scores.

### 🧪 Test Prompts:
1. **Distinction Students Filter:**
   ```text
   Filter rows where Academic Result is Distinction
   ```
2. **High Attendance Filter:**
   ```text
   Filter rows where Attendance Percentage is greater than 90 and Stream is Computer Science
   ```
3. **Total Aggregate & Average Calculation:**
   ```text
   Filter rows where Stream is Computer Science or Data Science, calculate Total_Score adding Midterm Score and Final Exam Score, calculate Average_Final_Score, and sort by Total_Score descending.
   ```

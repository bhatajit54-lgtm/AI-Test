# Bank Statement Analyzer - Multi-Page Application

## Overview
A comprehensive bank statement analyzer specifically designed for Axis Bank statements. The application features a multi-page workflow with separate pages for login, file upload, processing, and analysis.

## Application Structure

### 4 Separate HTML Pages:

1. **index.html** - Login & Registration Page
   - User authentication system
   - New user registration with password hashing
   - Secure login with session management

2. **upload.html** - File Upload Page
   - PDF file upload interface
   - Drag-and-drop support
   - File validation (PDF only)

3. **processing.html** - Statement Processing Page
   - Automatic PDF parsing using PDF.js
   - Transaction extraction from Axis Bank statements
   - Category classification
   - Progress indicators

4. **analyze.html** - Analysis Dashboard Page
   - Account summary with key metrics
   - Interactive filters (Year/Month)
   - Transaction table with all details
   - Data visualizations:
     - Pie chart (Income vs Expenses)
     - Bar chart (Top 5 Spending Categories)
     - Line chart (Monthly Trends)
   - Excel export functionality
   - Category-wise spending analysis

## How to Use

### Step 1: Setup
1. Download all 4 HTML files to the same folder:
   - index.html
   - upload.html
   - processing.html
   - analyze.html

2. Open `index.html` in a modern web browser (Chrome, Firefox, Edge, or Safari)

### Step 2: Registration & Login
1. On the first visit, click the "Register" tab
2. Enter a username and password (minimum 6 characters recommended)
3. Confirm your password
4. Click "Register"
5. After successful registration, switch to the "Login" tab
6. Enter your credentials and click "Login"

### Step 3: Upload Statement
1. After logging in, you'll be redirected to the upload page
2. Click the upload area or drag-and-drop your Axis Bank PDF statement
3. Once the file is selected, click "Process Statement"
4. Wait while the system processes your file

### Step 4: View Analysis
1. After processing, you'll automatically be redirected to the dashboard
2. View your account summary in the cards at the top:
   - Opening Balance
   - Total Credits
   - Total Debits
   - Closing Balance

3. Use the filters to analyze specific time periods:
   - Select a Year
   - Select a Month
   - Click "Apply Filters"

4. Explore the visualizations:
   - **Pie Chart**: Shows the split between income and expenses
   - **Bar Chart**: Displays your top 5 spending categories
   - **Line Chart**: Monthly income vs expenses trend

5. Review all transactions in the detailed table

6. Download your analysis:
   - Click "Download Excel Report" to get a comprehensive Excel file with 4 sheets:
     - **Transactions**: All transaction details
     - **Summary**: Account information and statistics
     - **Monthly Analysis**: Month-wise breakdown
     - **Category Analysis**: Spending by category

## Features

### Transaction Categorization
The application automatically categorizes transactions into:
- **Food & Dining**: SWIGGY, ZOMATO, HungerBox, restaurants, cafes
- **Shopping**: Flipkart, Amazon, Meesho, supermarkets
- **Transportation**: Uber, buses, IRCTC, travel
- **Healthcare**: Hospitals, pharmacies, medical stores
- **Salary/Income**: Salary deposits, ACH credits
- **UPI Payments**: All UPI transactions
- **Bank Transfers**: NEFT, IMPS, RTGS
- **Investments**: PPF, mutual funds
- **Others**: Miscellaneous transactions

### Axis Bank Statement Format Support
The application is optimized to parse Axis Bank statements with the following format:
- Transaction columns: Date | Chq No | Particulars | Debit | Credit | Balance
- Date format: DD-MM-YYYY
- Automatic detection of credits and debits
- Account information extraction

### Data Security
- Passwords are hashed using SHA-256 before storage
- All data is stored locally in your browser (localStorage)
- No data is sent to any external servers
- Session management ensures secure access
- Clear all data on logout

### Excel Export Features
The exported Excel file contains:
1. **Transactions Sheet**: Complete transaction list with categories
2. **Summary Sheet**: Account details and financial summary
3. **Monthly Analysis Sheet**: Month-wise income, expenses, and net change
4. **Category Analysis Sheet**: Category-wise spending with percentages

## System Requirements

### Supported Browsers:
- Google Chrome (v90+)
- Mozilla Firefox (v88+)
- Microsoft Edge (v90+)
- Safari (v14+)

### Required Browser Features:
- JavaScript enabled
- localStorage support (enabled by default)
- PDF.js compatibility
- Chart.js compatibility

## Libraries Used
- **PDF.js** (v3.11.174): PDF parsing and text extraction
- **Chart.js** (v4.4.0): Data visualization
- **SheetJS** (v0.20.0): Excel file generation
- **CryptoJS** (v4.1.1): Password hashing

## Troubleshooting

### Problem: Page Not Loading
- **Solution**: Ensure all 4 HTML files are in the same folder and open index.html first

### Problem: PDF Processing Fails
- **Solution**: 
  - Ensure the file is a valid PDF
  - Check that it's an Axis Bank statement
  - Try with a different statement if the format is unusual

### Problem: Can't Login After Registration
- **Solution**: 
  - Clear browser cache and localStorage
  - Try registering again with a different username

### Problem: Charts Not Displaying
- **Solution**: 
  - Check internet connection (CDN libraries need to load)
  - Try refreshing the page
  - Use a different browser

### Problem: Excel Export Not Working
- **Solution**: 
  - Ensure pop-ups are not blocked
  - Check download permissions
  - Try a different browser

## Tips for Best Results

1. **Statement Quality**: Use official PDF statements from Axis Bank's internet banking portal

2. **File Size**: Keep PDF files under 10MB for optimal performance

3. **Regular Analysis**: Upload statements monthly to track spending patterns

4. **Category Insights**: Use the category analysis to identify areas for potential savings

5. **Filter Usage**: Use year/month filters to analyze specific time periods

6. **Excel Reports**: Download Excel reports for detailed offline analysis or record-keeping

## Privacy & Security Notes

⚠️ **Important Security Information:**

- This application runs entirely in your browser
- All data is stored locally (no external servers)
- Your bank statements are not uploaded anywhere
- Clear your browser data after use if on a shared computer
- Always log out after finishing your analysis
- Use strong, unique passwords for the application

## Navigation Flow

```
index.html (Login/Register)
    ↓
upload.html (Upload PDF)
    ↓
processing.html (Auto-processing)
    ↓
analyze.html (Dashboard & Analysis)
    ↓
[Download Excel] or [Upload Another] or [Logout]
```

## Support

If you encounter any issues:
1. Check the browser console for error messages (F12 key)
2. Try a different PDF statement
3. Clear browser cache and try again
4. Use a different browser
5. Ensure all files are in the same directory

## Version Information
- Version: 1.0
- Last Updated: October 2024
- Compatible with: Axis Bank Statement Format (2024)

---

## Quick Start Guide

1. **Open** `index.html` in your browser
2. **Register** a new account
3. **Login** with your credentials
4. **Upload** your Axis Bank PDF statement
5. **Wait** for automatic processing
6. **Analyze** your transactions and spending patterns
7. **Download** Excel report for detailed analysis
8. **Logout** when finished

Enjoy analyzing your bank statements! 🎉

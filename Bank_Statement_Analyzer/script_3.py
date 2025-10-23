
# Create Page 4: Analysis Dashboard (analyze.html) - Part 1 (HTML and CSS)
analyze_html_part1 = """<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Analysis Dashboard - Bank Statement Analyzer</title>
    <script src="https://cdn.jsdelivr.net/npm/chart.js@4.4.0/dist/chart.umd.min.js"></script>
    <script src="https://cdn.sheetjs.com/xlsx-0.20.0/package/dist/xlsx.full.min.js"></script>
    <style>
        * { margin: 0; padding: 0; box-sizing: border-box; }
        body {
            font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
            background: #f5f7fa;
            min-height: 100vh;
        }
        .header {
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            color: white;
            padding: 30px 40px;
            box-shadow: 0 2px 10px rgba(0,0,0,0.1);
        }
        .header-content {
            max-width: 1400px;
            margin: 0 auto;
            display: flex;
            justify-content: space-between;
            align-items: center;
        }
        .header h1 { font-size: 28px; margin-bottom: 5px; }
        .header-info { font-size: 14px; opacity: 0.9; }
        .btn-logout {
            background: rgba(255,255,255,0.2);
            color: white;
            border: 2px solid white;
            padding: 10px 25px;
            border-radius: 8px;
            cursor: pointer;
            font-weight: 600;
            transition: all 0.3s;
        }
        .btn-logout:hover {
            background: white;
            color: #667eea;
        }
        .container {
            max-width: 1400px;
            margin: 0 auto;
            padding: 30px 40px;
        }
        .summary-cards {
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(250px, 1fr));
            gap: 20px;
            margin-bottom: 30px;
        }
        .card {
            background: white;
            padding: 25px;
            border-radius: 15px;
            box-shadow: 0 2px 10px rgba(0,0,0,0.05);
        }
        .card-title {
            font-size: 14px;
            color: #666;
            margin-bottom: 10px;
            text-transform: uppercase;
            letter-spacing: 0.5px;
        }
        .card-value {
            font-size: 32px;
            font-weight: 700;
            color: #333;
        }
        .card.credit .card-value { color: #10b981; }
        .card.debit .card-value { color: #ef4444; }
        .filters {
            background: white;
            padding: 25px;
            border-radius: 15px;
            box-shadow: 0 2px 10px rgba(0,0,0,0.05);
            margin-bottom: 30px;
            display: flex;
            gap: 20px;
            align-items: center;
            flex-wrap: wrap;
        }
        .filter-group {
            display: flex;
            flex-direction: column;
            gap: 8px;
        }
        .filter-group label {
            font-size: 13px;
            color: #666;
            font-weight: 600;
        }
        select {
            padding: 10px 15px;
            border: 2px solid #e5e7eb;
            border-radius: 8px;
            font-size: 14px;
            min-width: 150px;
            cursor: pointer;
        }
        select:focus {
            outline: none;
            border-color: #667eea;
        }
        .btn {
            padding: 10px 25px;
            border-radius: 8px;
            font-size: 14px;
            font-weight: 600;
            cursor: pointer;
            border: none;
            transition: all 0.3s;
        }
        .btn-primary {
            background: #667eea;
            color: white;
        }
        .btn-primary:hover {
            background: #764ba2;
        }
        .btn-secondary {
            background: #e5e7eb;
            color: #333;
        }
        .btn-secondary:hover {
            background: #d1d5db;
        }
        .section {
            background: white;
            padding: 30px;
            border-radius: 15px;
            box-shadow: 0 2px 10px rgba(0,0,0,0.05);
            margin-bottom: 30px;
        }
        .section-title {
            font-size: 20px;
            font-weight: 700;
            color: #333;
            margin-bottom: 20px;
        }
        .table-container {
            overflow-x: auto;
            max-height: 500px;
            overflow-y: auto;
        }
        table {
            width: 100%;
            border-collapse: collapse;
        }
        thead {
            background: #f9fafb;
            position: sticky;
            top: 0;
            z-index: 10;
        }
        th {
            padding: 15px;
            text-align: left;
            font-size: 13px;
            color: #666;
            font-weight: 600;
            text-transform: uppercase;
            letter-spacing: 0.5px;
            border-bottom: 2px solid #e5e7eb;
        }
        td {
            padding: 15px;
            border-bottom: 1px solid #f3f4f6;
            font-size: 14px;
        }
        tr:hover {
            background: #f9fafb;
        }
        .credit-text { color: #10b981; font-weight: 600; }
        .debit-text { color: #ef4444; font-weight: 600; }
        .chart-container {
            position: relative;
            height: 350px;
            margin-bottom: 20px;
        }
        .charts-grid {
            display: grid;
            grid-template-columns: 1fr 1fr;
            gap: 30px;
            margin-bottom: 30px;
        }
        @media (max-width: 1024px) {
            .charts-grid {
                grid-template-columns: 1fr;
            }
        }
        .btn-export {
            background: linear-gradient(135deg, #10b981 0%, #059669 100%);
            color: white;
            padding: 15px 40px;
            border-radius: 10px;
            font-size: 16px;
            font-weight: 600;
            border: none;
            cursor: pointer;
            margin-right: 15px;
            transition: transform 0.2s;
        }
        .btn-export:hover {
            transform: translateY(-2px);
        }
        .btn-upload {
            background: #667eea;
            color: white;
            padding: 15px 40px;
            border-radius: 10px;
            font-size: 16px;
            font-weight: 600;
            border: none;
            cursor: pointer;
            transition: transform 0.2s;
        }
        .btn-upload:hover {
            transform: translateY(-2px);
        }
        .actions {
            text-align: center;
            padding: 30px 0;
        }
    </style>
</head>
<body>
    <div class="header">
        <div class="header-content">
            <div>
                <h1 id="account-name">Account Dashboard</h1>
                <div class="header-info">
                    <span id="account-number"></span> | 
                    <span id="statement-period"></span>
                </div>
            </div>
            <button class="btn-logout" onclick="logout()">Logout</button>
        </div>
    </div>

    <div class="container">
        <!-- Summary Cards -->
        <div class="summary-cards">
            <div class="card">
                <div class="card-title">Opening Balance</div>
                <div class="card-value" id="opening-balance">₹0.00</div>
            </div>
            <div class="card credit">
                <div class="card-title">Total Credits</div>
                <div class="card-value" id="total-credits">₹0.00</div>
            </div>
            <div class="card debit">
                <div class="card-title">Total Debits</div>
                <div class="card-value" id="total-debits">₹0.00</div>
            </div>
            <div class="card">
                <div class="card-title">Closing Balance</div>
                <div class="card-value" id="closing-balance">₹0.00</div>
            </div>
        </div>

        <!-- Filters -->
        <div class="filters">
            <div class="filter-group">
                <label>Year</label>
                <select id="filter-year">
                    <option value="">All Years</option>
                </select>
            </div>
            <div class="filter-group">
                <label>Month</label>
                <select id="filter-month">
                    <option value="">All Months</option>
                    <option value="01">January</option>
                    <option value="02">February</option>
                    <option value="03">March</option>
                    <option value="04">April</option>
                    <option value="05">May</option>
                    <option value="06">June</option>
                    <option value="07">July</option>
                    <option value="08">August</option>
                    <option value="09">September</option>
                    <option value="10">October</option>
                    <option value="11">November</option>
                    <option value="12">December</option>
                </select>
            </div>
            <div style="margin-top: 20px;">
                <button class="btn btn-primary" onclick="applyFilters()">Apply Filters</button>
                <button class="btn btn-secondary" onclick="resetFilters()">Reset</button>
            </div>
        </div>

        <!-- Charts -->
        <div class="charts-grid">
            <div class="section">
                <div class="section-title">Income vs Expenses</div>
                <div class="chart-container">
                    <canvas id="pie-chart"></canvas>
                </div>
            </div>
            <div class="section">
                <div class="section-title">Top Spending Categories</div>
                <div class="chart-container">
                    <canvas id="category-chart"></canvas>
                </div>
            </div>
        </div>

        <!-- Monthly Trend -->
        <div class="section">
            <div class="section-title">Monthly Trend</div>
            <div class="chart-container" style="height: 300px;">
                <canvas id="trend-chart"></canvas>
            </div>
        </div>

        <!-- Transactions Table -->
        <div class="section">
            <div class="section-title">All Transactions (<span id="txn-count">0</span>)</div>
            <div class="table-container">
                <table>
                    <thead>
                        <tr>
                            <th>Date</th>
                            <th>Description</th>
                            <th>Category</th>
                            <th>Type</th>
                            <th>Amount</th>
                            <th>Balance</th>
                        </tr>
                    </thead>
                    <tbody id="transactions-tbody">
                    </tbody>
                </table>
            </div>
        </div>

        <!-- Actions -->
        <div class="actions">
            <button class="btn-export" onclick="exportToExcel()">📊 Download Excel Report</button>
            <button class="btn-upload" onclick="uploadAnother()">📄 Upload Another Statement</button>
        </div>
    </div>
"""

print("Created analyze.html part 1 (HTML structure and CSS)")
print("Length:", len(analyze_html_part1), "bytes")

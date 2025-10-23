
# Create Page 4: Analysis Dashboard (analyze.html) - Part 2 (JavaScript)
analyze_html_part2 = """
    <script>
        // Check session and load data
        const session = JSON.parse(localStorage.getItem('bank_session') || '{}');
        if (!session.username) {
            window.location.href = 'index.html';
        }

        let allTransactions = [];
        let filteredTransactions = [];
        let accountInfo = {};
        let summary = {};
        let charts = {};

        function logout() {
            if (confirm('Are you sure you want to logout?')) {
                localStorage.removeItem('bank_session');
                localStorage.removeItem('bank_pdffile');
                localStorage.removeItem('bank_transactions');
                localStorage.removeItem('bank_accountinfo');
                localStorage.removeItem('bank_summary');
                window.location.href = 'index.html';
            }
        }

        function uploadAnother() {
            window.location.href = 'upload.html';
        }

        function loadData() {
            try {
                allTransactions = JSON.parse(localStorage.getItem('bank_transactions') || '[]');
                accountInfo = JSON.parse(localStorage.getItem('bank_accountinfo') || '{}');
                summary = JSON.parse(localStorage.getItem('bank_summary') || '{}');

                if (allTransactions.length === 0) {
                    alert('No transaction data found. Please upload a statement.');
                    window.location.href = 'upload.html';
                    return;
                }

                filteredTransactions = [...allTransactions];
                
                // Display account info
                document.getElementById('account-name').textContent = accountInfo.name || 'Account Dashboard';
                document.getElementById('account-number').textContent = 'A/C: ' + (accountInfo.accountNumber || 'N/A');
                document.getElementById('statement-period').textContent = accountInfo.period || '';

                // Populate year filter
                const years = [...new Set(allTransactions.map(t => t.date.split('-')[2]))].sort();
                const yearSelect = document.getElementById('filter-year');
                years.forEach(year => {
                    const option = document.createElement('option');
                    option.value = year;
                    option.textContent = year;
                    yearSelect.appendChild(option);
                });

                updateDisplay();
            } catch (error) {
                console.error('Error loading data:', error);
                alert('Error loading data. Please try uploading again.');
                window.location.href = 'upload.html';
            }
        }

        function applyFilters() {
            const selectedYear = document.getElementById('filter-year').value;
            const selectedMonth = document.getElementById('filter-month').value;

            filteredTransactions = allTransactions.filter(txn => {
                const [day, month, year] = txn.date.split('-');
                
                if (selectedYear && year !== selectedYear) return false;
                if (selectedMonth && month !== selectedMonth) return false;
                
                return true;
            });

            updateDisplay();
        }

        function resetFilters() {
            document.getElementById('filter-year').value = '';
            document.getElementById('filter-month').value = '';
            filteredTransactions = [...allTransactions];
            updateDisplay();
        }

        function updateDisplay() {
            // Calculate filtered summary
            let credits = 0;
            let debits = 0;
            
            filteredTransactions.forEach(txn => {
                if (txn.type === 'Credit') {
                    credits += txn.amount;
                } else {
                    debits += txn.amount;
                }
            });

            // Update summary cards
            document.getElementById('opening-balance').textContent = '₹' + summary.openingBalance.toLocaleString('en-IN', {minimumFractionDigits: 2});
            document.getElementById('total-credits').textContent = '₹' + credits.toLocaleString('en-IN', {minimumFractionDigits: 2});
            document.getElementById('total-debits').textContent = '₹' + debits.toLocaleString('en-IN', {minimumFractionDigits: 2});
            document.getElementById('closing-balance').textContent = '₹' + summary.closingBalance.toLocaleString('en-IN', {minimumFractionDigits: 2});

            // Update transaction count
            document.getElementById('txn-count').textContent = filteredTransactions.length;

            // Update table
            updateTable();

            // Update charts
            updateCharts(credits, debits);
        }

        function updateTable() {
            const tbody = document.getElementById('transactions-tbody');
            tbody.innerHTML = '';

            filteredTransactions.forEach(txn => {
                const row = document.createElement('tr');
                const typeClass = txn.type === 'Credit' ? 'credit-text' : 'debit-text';
                
                row.innerHTML = `
                    <td>${txn.date}</td>
                    <td style="max-width: 300px;">${txn.description}</td>
                    <td><span style="padding: 4px 8px; background: #f3f4f6; border-radius: 4px; font-size: 12px;">${txn.category}</span></td>
                    <td class="${typeClass}">${txn.type}</td>
                    <td class="${typeClass}">₹${txn.amount.toLocaleString('en-IN', {minimumFractionDigits: 2})}</td>
                    <td>₹${txn.balance.toLocaleString('en-IN', {minimumFractionDigits: 2})}</td>
                `;
                tbody.appendChild(row);
            });
        }

        function updateCharts(credits, debits) {
            // Destroy existing charts
            Object.values(charts).forEach(chart => {
                if (chart) chart.destroy();
            });

            // Pie Chart - Income vs Expenses
            const pieCtx = document.getElementById('pie-chart').getContext('2d');
            charts.pie = new Chart(pieCtx, {
                type: 'pie',
                data: {
                    labels: ['Credits (Income)', 'Debits (Expenses)'],
                    datasets: [{
                        data: [credits, debits],
                        backgroundColor: ['#10b981', '#ef4444'],
                        borderWidth: 0
                    }]
                },
                options: {
                    responsive: true,
                    maintainAspectRatio: false,
                    plugins: {
                        legend: {
                            position: 'bottom',
                            labels: { padding: 15, font: { size: 13 } }
                        },
                        tooltip: {
                            callbacks: {
                                label: function(context) {
                                    const label = context.label || '';
                                    const value = context.parsed;
                                    const total = context.dataset.data.reduce((a, b) => a + b, 0);
                                    const percentage = ((value / total) * 100).toFixed(1);
                                    return label + ': ₹' + value.toLocaleString('en-IN') + ' (' + percentage + '%)';
                                }
                            }
                        }
                    }
                }
            });

            // Category Chart - Top Spending Categories
            const categoryData = {};
            filteredTransactions.filter(t => t.type === 'Debit').forEach(txn => {
                categoryData[txn.category] = (categoryData[txn.category] || 0) + txn.amount;
            });

            const sortedCategories = Object.entries(categoryData)
                .sort((a, b) => b[1] - a[1])
                .slice(0, 5);

            const categoryCtx = document.getElementById('category-chart').getContext('2d');
            charts.category = new Chart(categoryCtx, {
                type: 'bar',
                data: {
                    labels: sortedCategories.map(c => c[0]),
                    datasets: [{
                        label: 'Spending Amount',
                        data: sortedCategories.map(c => c[1]),
                        backgroundColor: ['#3b82f6', '#8b5cf6', '#ec4899', '#f59e0b', '#10b981'],
                        borderRadius: 8
                    }]
                },
                options: {
                    responsive: true,
                    maintainAspectRatio: false,
                    plugins: {
                        legend: { display: false },
                        tooltip: {
                            callbacks: {
                                label: function(context) {
                                    return '₹' + context.parsed.y.toLocaleString('en-IN');
                                }
                            }
                        }
                    },
                    scales: {
                        y: {
                            beginAtZero: true,
                            ticks: {
                                callback: function(value) {
                                    return '₹' + value.toLocaleString('en-IN');
                                }
                            }
                        }
                    }
                }
            });

            // Monthly Trend Chart
            const monthlyData = {};
            filteredTransactions.forEach(txn => {
                const [day, month, year] = txn.date.split('-');
                const key = `${year}-${month}`;
                
                if (!monthlyData[key]) {
                    monthlyData[key] = { credits: 0, debits: 0 };
                }
                
                if (txn.type === 'Credit') {
                    monthlyData[key].credits += txn.amount;
                } else {
                    monthlyData[key].debits += txn.amount;
                }
            });

            const sortedMonths = Object.keys(monthlyData).sort();
            const monthLabels = sortedMonths.map(m => {
                const [year, month] = m.split('-');
                const monthNames = ['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun', 'Jul', 'Aug', 'Sep', 'Oct', 'Nov', 'Dec'];
                return monthNames[parseInt(month) - 1] + ' ' + year;
            });

            const trendCtx = document.getElementById('trend-chart').getContext('2d');
            charts.trend = new Chart(trendCtx, {
                type: 'line',
                data: {
                    labels: monthLabels,
                    datasets: [
                        {
                            label: 'Credits',
                            data: sortedMonths.map(m => monthlyData[m].credits),
                            borderColor: '#10b981',
                            backgroundColor: 'rgba(16, 185, 129, 0.1)',
                            tension: 0.3,
                            fill: true
                        },
                        {
                            label: 'Debits',
                            data: sortedMonths.map(m => monthlyData[m].debits),
                            borderColor: '#ef4444',
                            backgroundColor: 'rgba(239, 68, 68, 0.1)',
                            tension: 0.3,
                            fill: true
                        }
                    ]
                },
                options: {
                    responsive: true,
                    maintainAspectRatio: false,
                    plugins: {
                        legend: {
                            position: 'top',
                            labels: { padding: 15, font: { size: 13 } }
                        },
                        tooltip: {
                            callbacks: {
                                label: function(context) {
                                    return context.dataset.label + ': ₹' + context.parsed.y.toLocaleString('en-IN');
                                }
                            }
                        }
                    },
                    scales: {
                        y: {
                            beginAtZero: true,
                            ticks: {
                                callback: function(value) {
                                    return '₹' + (value / 1000).toFixed(0) + 'K';
                                }
                            }
                        }
                    }
                }
            });
        }

        function exportToExcel() {
            try {
                // Create workbook
                const wb = XLSX.utils.book_new();

                // Sheet 1: Transactions
                const transactionsData = filteredTransactions.map(txn => ({
                    'Date': txn.date,
                    'Description': txn.description,
                    'Category': txn.category,
                    'Type': txn.type,
                    'Amount': txn.amount,
                    'Balance': txn.balance
                }));
                const ws1 = XLSX.utils.json_to_sheet(transactionsData);
                XLSX.utils.book_append_sheet(wb, ws1, 'Transactions');

                // Sheet 2: Summary
                const summaryData = [
                    ['Account Information', ''],
                    ['Account Holder', accountInfo.name || ''],
                    ['Account Number', accountInfo.accountNumber || ''],
                    ['IFSC Code', accountInfo.ifsc || ''],
                    ['Statement Period', accountInfo.period || ''],
                    ['', ''],
                    ['Summary Statistics', ''],
                    ['Opening Balance', summary.openingBalance],
                    ['Closing Balance', summary.closingBalance],
                    ['Total Credits', summary.totalCredits],
                    ['Total Debits', summary.totalDebits],
                    ['Net Change', summary.netChange],
                    ['Transaction Count', summary.transactionCount]
                ];
                const ws2 = XLSX.utils.aoa_to_sheet(summaryData);
                XLSX.utils.book_append_sheet(wb, ws2, 'Summary');

                // Sheet 3: Monthly Analysis
                const monthlyData = {};
                filteredTransactions.forEach(txn => {
                    const [day, month, year] = txn.date.split('-');
                    const key = `${year}-${month}`;
                    
                    if (!monthlyData[key]) {
                        monthlyData[key] = { credits: 0, debits: 0, count: 0 };
                    }
                    
                    if (txn.type === 'Credit') {
                        monthlyData[key].credits += txn.amount;
                    } else {
                        monthlyData[key].debits += txn.amount;
                    }
                    monthlyData[key].count++;
                });

                const monthlyArray = Object.entries(monthlyData).map(([month, data]) => ({
                    'Month': month,
                    'Credits': data.credits,
                    'Debits': data.debits,
                    'Net': data.credits - data.debits,
                    'Transactions': data.count
                }));
                const ws3 = XLSX.utils.json_to_sheet(monthlyArray);
                XLSX.utils.book_append_sheet(wb, ws3, 'Monthly Analysis');

                // Sheet 4: Category Analysis
                const categoryData = {};
                filteredTransactions.forEach(txn => {
                    if (!categoryData[txn.category]) {
                        categoryData[txn.category] = { amount: 0, count: 0 };
                    }
                    categoryData[txn.category].amount += txn.amount;
                    categoryData[txn.category].count++;
                });

                const totalAmount = Object.values(categoryData).reduce((sum, cat) => sum + cat.amount, 0);
                const categoryArray = Object.entries(categoryData).map(([category, data]) => ({
                    'Category': category,
                    'Amount': data.amount,
                    'Percentage': ((data.amount / totalAmount) * 100).toFixed(2) + '%',
                    'Transaction Count': data.count
                }));
                const ws4 = XLSX.utils.json_to_sheet(categoryArray);
                XLSX.utils.book_append_sheet(wb, ws4, 'Category Analysis');

                // Generate filename
                const date = new Date().toISOString().split('T')[0];
                const filename = `BankStatement_${accountInfo.accountNumber || 'Report'}_${date}.xlsx`;

                // Download
                XLSX.writeFile(wb, filename);

                alert('Excel report downloaded successfully!');
            } catch (error) {
                console.error('Error exporting to Excel:', error);
                alert('Error creating Excel file. Please try again.');
            }
        }

        // Load data on page load
        window.onload = loadData;
    </script>
</body>
</html>"""

# Combine both parts
analyze_html_complete = analyze_html_part1 + analyze_html_part2

with open('analyze.html', 'w', encoding='utf-8') as f:
    f.write(analyze_html_complete)

print("Created: analyze.html (Analysis Dashboard page)")
print("File size:", len(analyze_html_complete), "bytes")
print("\n=== All 4 HTML files created successfully! ===")
print("\nFiles created:")
print("1. index.html - Login/Registration page")
print("2. upload.html - File Upload page")
print("3. processing.html - Processing page")
print("4. analyze.html - Analysis Dashboard page")

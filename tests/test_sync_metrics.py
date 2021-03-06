from juniorguru.sync.metrics import merge_metric_dicts, parse_finances


def test_merge_metric_dicts():
    assert merge_metric_dicts({
        'https://example.com/1/': 42,
        'https://example.com/100/': 420,
        'https://example.com/': 3,
    }, {
        'https://example.com/1/': 2,
        'https://example.com/4/': 10,
        'https://example.com/': 30,
    }) == {
        'https://example.com/1/': 44,
        'https://example.com/100/': 420,
        'https://example.com/4/': 10,
        'https://example.com/': 33,
    }


def test_parse_finances():
    assert parse_finances([
        ['Total Income', '170,346.97 Kč', '', ''],
        ['', 'Total', 'Percents', ''],
        ['donations', '30,458.86 Kč', '17.88%', ''],
        ['jobs', '3,000.00 Kč', '1.76%', ''],
        ['memberships', '43,689.11 Kč', '25.65%', ''],
        ['partnerships', '93,199.00 Kč', '54.71%', ''],
        ['', '', '', ''],
        ['', '', '', ''],
        ['', '', '', ''],
        ['Total Expenses', '46,277.33 Kč', '', ''],
        ['', 'Total', 'Percents', ''],
        ['lawyer', '9,600.00 Kč', '20.74%', ''],
        ['overheads', '10,939.33 Kč', '23.64%', ''],
        ['tax', '25,738.00 Kč', '55.62%', ''],
        ['', '', '', ''],
        ['', '', '', ''],
        ['Months', '5.93', '', ''],
        ['MRR', '12,496.85 Kč', '', ''],
        ['Total Profit', '124,069.64 Kč', '', ''],
        ['Profit per Month', '20,910.61 Kč', '', ''],
        ['', '', '', ''],
        ['Minimum Wage', '15,000.00 Kč', '139.40%', '5,910.61 Kč'],
        ['Average Wage', '35,000.00 Kč', '59.74%', '-14,089.39 Kč']
    ]) == {
        'inc_total': 170347,
        'inc_donations': 30459,
        'inc_donations_pct': 18,
        'inc_jobs': 3000,
        'inc_jobs_pct': 2,
        'inc_memberships': 43690,
        'inc_memberships_pct': 26,
        'inc_partnerships': 93199,
        'inc_partnerships_pct': 55,
        'exp_total': 46278,
        'exp_lawyer': 9600,
        'exp_lawyer_pct': 21,
        'exp_overheads': 10940,
        'exp_overheads_pct': 24,
        'exp_tax': 25738,
        'exp_tax_pct': 56,
        'mrr': 12497,
        'total_profit': 124070,
        'profit_per_month': 20911,
    }

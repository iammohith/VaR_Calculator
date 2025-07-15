import matplotlib.pyplot as plt

def generate_report(results: dict, portfolio_value: float) -> str:
    """Generate VaR report and comparison plot"""
    report = "Value at Risk Report:\n"
    for method, value in results.items():
        report += f"{method} VaR: ₹{value:,.2f}\n"
    
    # Generate comparison plot
    methods = list(results.keys())
    values = list(results.values())
    
    plt.figure(figsize=(10, 6))
    bars = plt.bar(methods, values, color=['#1f77b4', '#ff7f0e', '#2ca02c'])
    plt.ylabel('VaR (INR)')
    plt.title(f'VaR Comparison (Portfolio: ₹{portfolio_value:,.2f})')
    
    # Add value labels on bars
    for bar in bars:
        height = bar.get_height()
        plt.annotate(f'₹{height:,.2f}',
                    xy=(bar.get_x() + bar.get_width() / 2, height),
                    xytext=(0, 3),
                    textcoords="offset points",
                    ha='center', va='bottom')
    
    plt.tight_layout()
    filename = 'var_comparison.png'
    plt.savefig(filename)
    plt.close()
    
    report += f"\nComparison plot saved as '{filename}'"
    return report

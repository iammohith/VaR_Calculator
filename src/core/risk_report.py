import matplotlib.pyplot as plt

def generate_report(results: dict, portfolio_value: float) -> str:
    """
    Generate VaR report and comparison plot
    """
    report = "Value at Risk Report:\n"
    for method, value in results.items():
        report += f"{method} Var: ₹{value:,.2f}\n"
    
    # Create comparison plot
    methods = list(results.keys())
    values = list(results.values())
    
    plt.figure(figsize=(10, 6))
    plt.bar(methods, values, color=['blue', 'green', 'red'])
    plt.title('Value at Risk Comparison')
    plt.ylabel('VaR (INR)')
    plt.grid(axis='y', linestyle='--', alpha=0.7)
    
    # Save plot
    filename = 'var_comparison.png'
    plt.savefig(filename)
    plt.close()
    
    report += f"\nComparison plot saved as '{filename}'"
    return report

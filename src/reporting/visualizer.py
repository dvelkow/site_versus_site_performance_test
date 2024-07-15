import matplotlib.pyplot as plt
from typing import Dict, List

class Visualizer:
    def plot_metric_comparison(self, metric_data: Dict[str, List[float]], metric_name: str, output_file: str):
        plt.figure(figsize=(12, 6))
        
        for site, values in metric_data.items():
            plt.plot(values, marker='o', label=site.capitalize())
        
        plt.title(f"{metric_name.replace('_', ' ').title()} Comparison")
        plt.ylabel(metric_name.replace('_', ' ').title())
        plt.xlabel("Test Run")
        plt.legend(loc='best')
        plt.grid(True, linestyle='--', alpha=0.7)
        
        # Highlight the last points
        for site, values in metric_data.items():
            plt.plot(len(values)-1, values[-1], 'ro', markersize=8)
        
        plt.tight_layout()
        plt.savefig(output_file, dpi=300, bbox_inches='tight')
        plt.close()
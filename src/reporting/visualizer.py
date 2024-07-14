import matplotlib.pyplot as plt
from typing import List

class Visualizer:
    def plot_metric_trend(self, metric_values: List[float], metric_name: str, environment: str, output_file: str):
        plt.figure(figsize=(10, 6))
        plt.plot(metric_values, marker='o')
        plt.title(f"{metric_name.replace('_', ' ').title()} Trend - {environment.capitalize()}")
        plt.ylabel(metric_name.replace('_', ' ').title())
        plt.xlabel("Test Run")
        plt.grid(True, linestyle='--', alpha=0.7)
        
        # Add value labels
        for i, v in enumerate(metric_values):
            plt.text(i, v, f'{v:.2f}', ha='center', va='bottom', fontweight='bold')
        
        # Highlight the last point
        plt.plot(len(metric_values)-1, metric_values[-1], 'ro', markersize=10)
        
        plt.tight_layout()
        plt.savefig(output_file, dpi=300, bbox_inches='tight')
        plt.close()
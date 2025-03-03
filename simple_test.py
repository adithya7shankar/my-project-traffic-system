import matplotlib.pyplot as plt
import numpy as np
import os
from pathlib import Path

# Create output directory
output_dir = Path("output")
output_dir.mkdir(exist_ok=True)

# Generate some random data
data = np.random.randint(30, 70, size=50)

# Create a histogram
plt.figure(figsize=(10, 6))
plt.hist(data, bins=range(30, 75, 5), edgecolor='black')
plt.title('Test Histogram')
plt.xlabel('Value')
plt.ylabel('Frequency')
plt.grid(axis='y', alpha=0.75)

# Save the figure
output_file = output_dir / 'test_histogram.png'
plt.savefig(output_file)
print(f"Saved histogram to {output_file}")

# Create a pie chart
categories = ['A', 'B', 'C', 'D']
values = [15, 30, 45, 10]

plt.figure(figsize=(8, 8))
plt.pie(values, labels=categories, autopct='%1.1f%%', shadow=True, startangle=90)
plt.axis('equal')
plt.title('Test Pie Chart')

# Save the figure
output_file = output_dir / 'test_pie_chart.png'
plt.savefig(output_file)
print(f"Saved pie chart to {output_file}")

print("Done!")

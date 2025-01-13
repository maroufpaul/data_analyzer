# Omics Data Analyzer

## Description

**Omics Data Analyzer** is a Python-based web application designed to help researchers analyze and visualize omics datasets. It provides intuitive tools for data preprocessing, dimensionality reduction (PCA), and heatmap generation, making complex analyses accessible to users without extensive coding skills.

---

## Features

- **File Upload**:
  - Supports CSV and Excel files.
  - Automatically identifies numeric columns for analysis.

- **Data Preprocessing**:
  - Normalize selected columns (scale values between 0 and 1).
  - Handle missing values (replace with zeros).

- **Principal Component Analysis (PCA)**:
  - Perform dimensionality reduction on selected numeric variables.
  - Visualize the first two principal components in a scatter plot.
  - Display explained variance ratios.

- **Heatmap Visualization**:
  - Generate a correlation heatmap for selected numeric variables.
  - Visualize relationships and patterns in the dataset.

- **Export Preprocessed Data**:
  - Download preprocessed datasets as a CSV file.

---

## Screenshots

### Home Page:
![Home Page](screenshot-home.png)

### PCA Visualization:
![PCA Scatter Plot](screenshot-pca.png)

### Heatmap:
![Heatmap](screenshot-heatmap.png)

---

## Installation

### Prerequisites
- Python 3.7 or higher
- Pip (Python package manager)
- Recommended: Virtual Environment

### Steps
1. Clone this repository:
   ```bash
   git clone https://github.com/yourusername/omics-data-analyzer.git
   cd omics-data-analyzer


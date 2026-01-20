# Assignment1
## Part 1 - Implementation of Topsis in Python
This project implements the TOPSIS (Technique for Order Preference by Similarity to Ideal Solution) method using Python.
The program is designed to run as a command-line tool, following the specifications given in the assignment.

Libraries Used : pandas and numpy

### Usage
```bash
python topsis.py <InputDataFile> <Weights> <Impacts> <OutputResultFileName>
```
---
## Part 2 - Python Package 
This part of the project involves packaging the TOPSIS implementation as a Python package and uploading it to **PyPI** so it can be installed and used globally.

### Package Details

- **Package Name:** `topsis-aarzoo-102303061`
- **PyPI Link:** https://pypi.org/project/topsis-aarzoo-102303061/1.0.0/

## Installation

Install the package from PyPI using pip:

```bash
pip install topsis-aarzoo-102303061
```

---

## Part 3 - Topsis Web Service 
In this part, the TOPSIS algorithm is deployed as a **web-based service**, allowing users to perform TOPSIS analysis through a browser instead of the command line.

### Live Application
https://topsis-web-cqkw.onrender.com

### Technology Stack

- Backend: Python, Flask , Resend API(to send mails)
- Frontend: HTML, CSS
- Data Processing: Pandas, NumPy
- Deployment Platform: Render

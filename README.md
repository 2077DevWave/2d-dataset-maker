# 2D Dataset Creator

This is a simple GUI application built with **PyQt5** to help you **generate and label 2D datasets** for machine learning or data visualization purposes.

## ✨ Features

- Generate random 2D points within a user-defined board size
- Assign class labels to regions by **drawing shapes around points**
- Class labels can only be **strings** or **numbers**
- All unselected points are assigned a **default class label of `0`**
- Supports drawing and assigning **multiple classes**
- Save the dataset as a CSV file (`x`, `y`, `class`)

---

## 🖥️ Demo

![2D Dataset Maker Demo](https://github.com/2077DevWave/2d-dataset-maker/blob/main/data-set-creator.png)

---

## 📦 Installation

```bash
pip install PyQt5
```

---

## 🚀 How to Use

### 1. Launch the App

```bash
python main.py
```

### 2. Generate Points
- Click **"Generate Points"**
- Input:
  - Board width and height
  - Number of random points

### 3. Assign Class to Region
- Click **"Draw Class Region"**
- Choose a **color** for that class
- Enter a **class label** (string or number only)
- **Click and drag to draw a shape** around the region you want to label
- Repeat for other classes

📝 Points outside any region are labeled with class `0`.

### 4. Save Dataset
- Click **"Save Dataset"**
- Choose a `.csv` file location
- CSV contains `x`, `y`, and `class`

---

## 📁 Example CSV Output

```csv
x,y,class
134,456,0
232,412,"A"
321,312,"A"
412,125,"B"
...
```

---

## ✅ Requirements

- Python 3.x
- PyQt5

---

## 📌 Notes

- You can assign class labels as strings (`"A"`, `"cat"`) or numbers (`1`, `2.5`) only.
- You can draw multiple regions for multiple classes.
- The app currently does not support erasing/undoing drawings.

---

## 📄 License

MIT License. Use freely in academic and personal projects.

---

## 🙌 Contributions

PRs and suggestions are welcome! Feel free to fork and improve the project.
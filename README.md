# Keystroke Authentication System  

A machine learning-based keystroke authentication system that verifies user identity by analyzing typing patterns. This project is built using **Python** and integrates with **XAMPP's phpMyAdmin (MySQL database)** for data storage.  

## Features  
- **Keystroke Dynamics Authentication**  
- **User Classification (Staff vs. Administrator)** using **Random Forest**  
- **Unauthorized User Detection** using **Isolation Forest**  
- **MySQL database (phpMyAdmin via XAMPP)** for storing keystroke data  
- **Machine Learning Algorithms Used:**
  - **Random Forest** → Classifies users as **staff** or **administrators**  
  - **Support Vector Machine (SVM)** & **Multilayer Perceptron (MLP)** → Alternative classifiers  
  - **Isolation Forest** → Detects **unauthorized users** based on anomaly detection

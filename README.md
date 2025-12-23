# 🕵️ VisCrypto Suite
> **"Security for the Human Eye."**

[![Python](https://img.shields.io/badge/Python-3.10%2B-blue?style=for-the-badge&logo=python&logoColor=white)](https://www.python.org/)
[![Framework](https://img.shields.io/badge/Made%20With-Flask-black?style=for-the-badge&logo=flask)](https://flask.palletsprojects.com/)
[![License](https://img.shields.io/badge/License-MIT-green?style=for-the-badge)](LICENSE)
[![Status](https://img.shields.io/badge/Status-Stable%20v1.0-orange?style=for-the-badge)]()

## 📖 Project Overview
**VisCrypto** is a cybersecurity tool developed as a Final Year Project. It implements the **Naor-Shamir (2, 2) Visual Cryptography Scheme**. 

Traditional encryption requires computers to decrypt. VisCrypto splits a secret (Image, Text, or QR Code) into two random "noise" shares. When these shares are stacked together—either digitally or by printing them on transparency sheets—the human eye can instantly reconstruct the secret.

---

## 🚀 Key Features
* **📷 Dual-Mode Engine:** * *Document Mode:* High-contrast thresholding for sharp text.
    * *Photo Mode:* Dithering algorithms for detailed images.
* **🔠 Text-to-QR Generator:** Instantly converts passwords/text into encrypted QR codes.
* **🛡️ Info-Theoretic Security:** Mathematically impossible to crack with only one share.
* **✨ Modern UI:** Responsive Glassmorphism design with Dark/Light visual elements.

---

## 🛠️ Technology Stack
| Component | Technology Used |
| :--- | :--- |
| **Core Logic** | Python 3, NumPy (Vectorized Operations) |
| **Image Processing** | Pillow (PIL) Fork |
| **Web Server** | Flask (Jinja2 Templating) |
| **Frontend** | HTML5, CSS3 (Mesh Gradients), Vanilla JS |
| **Deployment** | Gunicorn / Render |

---

## ⚡ How to Run Locally
1.  **Clone the repo:**
    ```bash
    git clone [https://github.com/YOUR_USERNAME/VisCrypto-Suite.git](https://github.com/YOUR_USERNAME/VisCrypto-Suite.git)
    cd VisCrypto-Suite
    ```
2.  **Install Dependencies:**
    ```bash
    pip install -r requirements.txt
    ```
3.  **Start the Server:**
    ```bash
    python app.py
    ```
4.  **Open in Browser:**
    Go to `http://127.0.0.1:5000`

---

## 👥 Authors
* **[Your Name]** - *Lead Developer*
* **[Teammate Name]** - *Documentation & Testing*

---

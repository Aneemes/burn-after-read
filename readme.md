
# 🔥 Burn After Read - Secure Note Sharing App

A simple web app to paste a secret message, generate a unique link, and let someone read it **only once**. After it's viewed, it's gone forever. You can also protect the message with a password.

---

## ✨ Features

- ✅ **Paste any text** (like a password, private message, or secret info)
- 🔗 **Get a unique link** to share it
- 🔐 **Optional password protection**
- 👁️‍🗨️ **Message can only be viewed once**
- 🧹 Message is automatically deleted after it's read

---

## 🚀 How It Works

1. **Go to the homepage**
2. **Paste your secret**
3. (Optional) **Add a password** for extra security
4. Click **“Create”** to get a unique link
5. Send the link to someone
6. When they open it:
   - If there's a password, they'll be asked to enter it
   - The message is shown **once**
   - Then it's deleted automatically

---

## 🛡️ How Your Data Is Kept Safe

- Every message is **encrypted** before it’s saved
- Messages are **stored securely** in a local database
- If a password is added:
  - It is **hashed** and never stored in plain text
  - Only the correct password can unlock the message
- Once a message is read, it’s **permanently deleted**

---

## 🧪 Local Setup Instructions

> No technical knowledge? Just follow these easy steps.

### 1. Requirements

- Python 3.9+
- Pip (Python package manager)

### 2. Install it

```bash
git clone https://github.com/your-username/burn-after-read.git
cd burn-after-read
python -m venv env
source env/bin/activate  # or `env\Scripts\activate` on Windows
pip install -r requirements.txt
```

### 3. Run the app

```bash
python app.py
```

Open your browser and go to `http://127.0.0.1:5000`

---

## 📝 Notes

- This is not meant for long-term message storage.
- Treat it like a **digital sticky note that burns after you read it.**
- Great for sending:
  - One-time passwords
  - Private links
  - Confidential info

---

## 📸 Screenshots

> Add some screenshots of your homepage, note creation, and viewing screens here (optional).

---

## 🙋 FAQ

**Q: Can someone see my message after it's read once?**  
A: No. Once viewed, the message is deleted from the server.

**Q: Is my message stored in plain text?**  
A: Never. It’s always encrypted before saving.

**Q: What if I forget the password?**  
A: There’s no recovery. That’s part of the security.

---

## 👷 Future Ideas

- Set an expiration time (e.g., 10 mins or 1 hour)
- Upload and burn files
- QR code for note sharing

---

## 🧑‍💻 Credits

Built with ❤️ using [Flask](https://flask.palletsprojects.com/) and [Fernet Encryption](https://cryptography.io/en/latest/fernet/).

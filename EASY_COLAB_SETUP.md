# 🚀 SUPER EASY COLAB SETUP (3 Minutes!)

## Your ngrok token is already configured! Just follow these steps:

---

## Step 1: Open Colab (30 seconds)

1. Click this link: **https://colab.research.google.com**
2. Sign in with your Google account
3. Click **"New notebook"** button (bottom left)

---

## Step 2: Copy & Paste the Code (1 minute)

1. Open this file: **COLAB_TEMPLATE.py** (in this folder)
2. Select ALL the code (Ctrl+A)
3. Copy it (Ctrl+C)
4. Go back to Colab
5. Click in the empty cell
6. Paste the code (Ctrl+V)

**Note:** Your ngrok token is already configured in the code!

---

## Step 3: Run It! (30 seconds)

1. Click the **Play button ▶️** on the left of the cell
   - OR press **Shift + Enter**
2. Wait 2-3 minutes while it installs and sets up

---

## Step 4: Copy Your URL (30 seconds)

When it's done, you'll see:
```
🎉 YOUR MODEL IS NOW ACCESSIBLE!
📡 Public URL: https://something.ngrok.io
```

**Copy that URL!** (the https://something.ngrok.io part)

---

## Step 5: Connect to Genius AI (30 seconds)

On your computer, open terminal and run:

```bash
python configure_colab_model.py https://YOUR-URL-HERE.ngrok.io
```

Replace `YOUR-URL-HERE` with the URL you copied.

Example:
```bash
python configure_colab_model.py https://abc123-def456.ngrok.io
```

---

## That's It! 🎉

You should see:
```
✅ Configuration successful!
✅ Connection test successful!
READY TO USE!
```

Now open **http://localhost:3000** and your Colab model is connected!

---

## Need Help?

**What's a "cell" in Colab?**
- It's just a box where you put code
- The new notebook starts with one empty cell
- That's where you paste the code!

**Where's the Play button?**
- Look at the left edge of the cell
- You'll see a circle with ▶️ inside
- Click it to run the code!

**How long does it take?**
- First time: 2-3 minutes (installing stuff)
- After that: Instant!

**What if I close Colab?**
- The tunnel closes
- Just run the cell again
- Copy the new URL
- Run the configure command again

---

## Pro Tips:

✅ **Keep the Colab tab open** - If you close it, the tunnel closes
✅ **Bookmark the Colab notebook** - So you can easily return to it
✅ **The URL changes each time** - Each time you run the cell, you get a new URL

---

## Troubleshooting:

### Error: "ngrok authentication required"
- Already fixed! Your token is in the code

### Error: "ModuleNotFoundError"
- Wait for the installation to finish
- Look for "✅ Dependencies installed!"

### Error: "Port already in use"
- In Colab menu: **Runtime → Restart runtime**
- Then run the cell again

---

## What You Can Do Now:

1. **Groq Mode** (default) - Fast, free Llama 3.3 70B
2. **Custom Mode** - Your Colab model
3. **Hybrid Mode** - Both combined!

Test it at: **http://localhost:3000**

---

**You got this! Follow the 5 steps and you'll be connected in 3 minutes!** 💪

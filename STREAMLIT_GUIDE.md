# 🚗 Streamlit Rideshare Price Predictor - Deployment Guide

## Quick Start (Local Development)

### 1. Install Dependencies

```bash
# Navigate to the project directory
cd "/Users/rishabhkimothi/Desktop/projects : work/ML labs/Rideshare Multivariate Regression"

# Install required packages
pip install -r requirements.txt
```

### 2. Run the App Locally

```bash
streamlit run app.py
```

This will:
- Start a local server (usually at `http://localhost:8501`)
- Automatically open the app in your browser
- Show a "Rerun" indicator when you make changes

### 3. Stop the App

Press `Ctrl+C` in your terminal to stop the Streamlit server.

---

## 📊 App Features

The Streamlit app includes **5 interactive tabs**:

### 1️⃣ **Prediction Tab** 💰
- Real-time price prediction
- Input distance, surge, cab type, and ride type
- "What-if" scenarios (50% increase in distance/surge)
- Model confidence metrics

### 2️⃣ **Data Explorer** 📈
- Dataset overview and statistics
- Price distribution histogram
- Feature scatter plots
- Cab type and ride type breakdowns
- Sample data table

### 3️⃣ **Model Performance** 🎯
- Key metrics: MAE, RMSE, R² Score
- Predicted vs Actual scatter plot
- Residual analysis
- Training convergence visualization

### 4️⃣ **Feature Analysis** 🔍
- Top 15 most important features
- Feature correlation with price
- Feature statistics and ranges

### 5️⃣ **About** ℹ️
- Model documentation
- How the algorithm works
- Technologies used
- Model limitations

---

## 🚀 Publishing to Streamlit Cloud (FREE)

### Step 1: Prepare Your Code

Ensure your project has:
- ✅ `app.py` (your Streamlit app)
- ✅ `requirements.txt` (dependencies)
- ✅ `rideshare_kaggle.csv` (data file)

### Step 2: Create a GitHub Repository

```bash
# Initialize git (if not already done)
cd "/Users/rishabhkimothi/Desktop/projects : work/ML labs/Rideshare Multivariate Regression"
git init

# Add all files
git add .

# Commit
git commit -m "Initial commit: Streamlit rideshare app"

# Create a new repository on github.com, then push
git remote add origin https://github.com/YOUR_USERNAME/rideshare-predictor.git
git branch -M main
git push -u origin main
```

### Step 3: Deploy on Streamlit Cloud

1. Go to [share.streamlit.io](https://share.streamlit.io)
2. Sign in with GitHub
3. Click **"New App"**
4. Select your repository and branch
5. Set main file to `app.py`
6. Click **"Deploy"**

**That's it!** Your app will be live in minutes at:
```
https://share.streamlit.io/YOUR_USERNAME/rideshare-predictor/main/app.py
```

---

## 🔧 Alternative Deployment Options

### Option 1: Heroku (Free tier ending, paid plans available)

```bash
# Create Procfile
echo "web: streamlit run app.py" > Procfile

# Create setup.sh
touch setup.sh
```

Edit `setup.sh`:
```bash
mkdir -p ~/.streamlit/
echo "[server]
headless = true
port = $PORT
enableCORS = false
" > ~/.streamlit/config.toml
```

Then push to Heroku and deploy.

### Option 2: AWS, Google Cloud, or Azure

All support containerized deployment. Create a `Dockerfile`:

```dockerfile
FROM python:3.11-slim
WORKDIR /app
COPY requirements.txt .
RUN pip install -r requirements.txt
COPY . .
EXPOSE 8501
CMD ["streamlit", "run", "app.py", "--server.port=8501"]
```

### Option 3: PythonAnywhere (Simple, free tier available)

1. Upload your files
2. Create a web app pointing to your Streamlit app
3. Done!

---

## 📦 Project Structure

```
Rideshare Multivariate Regression/
├── app.py                          # Main Streamlit app
├── requirements.txt                # Python dependencies
├── rideshare_kaggle.csv           # Dataset
├── Rideshare_Multivariate_Regression.ipynb  # Original notebook
├── Rideshare_Loop_Version.ipynb   # Alternative notebook
└── README.md                       # This guide
```

---

## 🎨 Customization

### Change the Color Scheme

Edit the color codes in `app.py`. Find lines like:
```python
color='#3498DB'  # Blue
color='#E74C3C'  # Red
color='#27AE60'  # Green
color='#F39C12'  # Orange
```

[Color Palette Reference](https://coolors.co/)

### Add More Features

Modify the model training section to include:
- Temperature and humidity (if available)
- Time of day
- Day of week
- Weather conditions

### Adjust Model Hyperparameters

In the `train_model()` function:
```python
alpha=0.001        # Learning rate (lower = slower, more stable)
num_iters=10000    # Number of iterations
lambda_=0.01       # Regularization (higher = more regularization)
```

---

## ⚠️ Troubleshooting

### Issue: "FileNotFoundError: rideshare_kaggle.csv"

**Solution**: Ensure `rideshare_kaggle.csv` is in the same directory as `app.py`

```bash
# Check file location
ls -la rideshare_kaggle.csv
```

### Issue: "ModuleNotFoundError" 

**Solution**: Install packages again
```bash
pip install -r requirements.txt
```

### Issue: App loads slowly

**Solution**: The model trains once on first load (cached). Subsequent loads are instant.

### Issue: Predictions seem off

**Solution**: 
- Check that your data CSV has the correct columns
- Ensure numeric values are in the expected ranges
- Model is only as good as the training data

---

## 📊 Expected Output

When running locally, you should see:
```
  You can now view your Streamlit app in your browser.

  Local URL: http://localhost:8501
  Network URL: http://192.168.x.x:8501
```

Then the app opens automatically in your browser.

---

## 🔐 Security & Data Privacy

### For Streamlit Cloud Deployment:

- ✅ Your data CSV is uploaded with the code
- ✅ All computations happen server-side
- ✅ HTTPS encryption enabled by default
- ✅ No data sent to external APIs
- ⚠️ Source code is visible on GitHub

**If you have sensitive data**: Use Streamlit's secrets management or environment variables.

---

## 📈 Performance Tips

1. **Cache expensive computations** (already done with `@st.cache_resource`)
2. **Reduce data size** if working with huge datasets
3. **Use `st.write()` for simple outputs** instead of `st.dataframe()`
4. **Lazy load visualizations** for heavy plots

---

## 🎓 Next Steps

1. **Enhance the model**: Add more features or try other algorithms
2. **Add user feedback**: Let users rate predictions
3. **Deploy predictions**: Create an API for other apps to use
4. **Monitor performance**: Track predictions and actual prices
5. **A/B testing**: Test different model versions

---

## 📚 Resources

- [Streamlit Documentation](https://docs.streamlit.io/)
- [Streamlit Cloud Deployment Guide](https://docs.streamlit.io/streamlit-cloud/get-started)
- [NumPy Documentation](https://numpy.org/doc/)
- [Pandas Documentation](https://pandas.pydata.org/docs/)

---

## 🆘 Need Help?

- **Streamlit Issues**: Check [Streamlit Community Forums](https://discuss.streamlit.io/)
- **Deployment Questions**: [Streamlit Cloud Docs](https://docs.streamlit.io/streamlit-cloud)
- **Python Help**: [Stack Overflow](https://stackoverflow.com/questions/tagged/streamlit)

---

**Happy deploying! 🚀**

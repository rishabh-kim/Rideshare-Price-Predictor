# 🚗 Rideshare Multivariate Regression with Streamlit

A complete machine learning project featuring multivariate linear regression to predict rideshare prices, with both Jupyter notebook analysis and an interactive Streamlit web application.

## 📋 Project Overview

This project demonstrates:
- **Multivariate Linear Regression**: Predicting prices using multiple features
- **Feature Engineering**: Polynomial features and categorical encoding
- **Gradient Descent**: Optimization with regularization
- **Streamlit Deployment**: Publishing an ML model as a web app

## 🎯 Features

### Model Capabilities
- ✅ Predict rideshare prices based on distance, surge multiplier, cab type, and ride type
- ✅ Polynomial feature engineering (distance², surge², interaction terms)
- ✅ One-hot encoding for categorical variables
- ✅ L2 regularization to prevent overfitting
- ✅ Vectorized NumPy computations for efficiency

### Web App Features
- 💰 Real-time price predictions with confidence scores
- 📈 Interactive data explorer with visualizations
- 🎯 Model performance metrics and analysis
- 🔍 Feature importance analysis
- 📊 What-if scenario exploration
- 🌐 Responsive, professional UI

## 📁 Project Structure

```
Rideshare Multivariate Regression/
├── app.py                                    # ⭐ Main Streamlit app
├── Rideshare_Multivariate_Regression.ipynb  # Jupyter notebook with analysis
├── rideshare_kaggle.csv                     # Dataset
├── requirements.txt                         # Python dependencies
├── run.sh                                   # Quick start script
├── STREAMLIT_GUIDE.md                       # Deployment guide
└── README.md                                # This file
```

## 🚀 Quick Start

### Option 1: Using the Bash Script (Easiest)

```bash
cd "/Users/rishabhkimothi/Desktop/projects : work/ML labs/Rideshare Multivariate Regression"
chmod +x run.sh
./run.sh
```

Then open your browser to `http://localhost:8501`

### Option 2: Manual Setup

```bash
# Navigate to project directory
cd "/Users/rishabhkimothi/Desktop/projects : work/ML labs/Rideshare Multivariate Regression"

# Install dependencies
pip install -r requirements.txt

# Run the app
streamlit run app.py
```

### Option 3: Using Python Virtual Environment

```bash
# Create virtual environment
python3 -m venv venv
source venv/bin/activate

# Install dependencies
pip install -r requirements.txt

# Run app
streamlit run app.py
```

## 📊 App Tabs Overview

### 1. **💰 Prediction**
- Interactive sliders for distance, surge multiplier, cab type, and ride type
- Real-time price predictions
- What-if scenarios showing price sensitivity
- Model confidence metrics

### 2. **📈 Data Explorer**
- Dataset statistics and overview
- Price distribution histogram
- Feature vs price scatter plots
- Ride type breakdowns
- Sample data table

### 3. **🎯 Model Performance**
- Mean Absolute Error (MAE)
- Root Mean Squared Error (RMSE)
- R² Score (variance explained)
- Predicted vs actual scatter plot
- Residual analysis plots
- Training convergence visualization

### 4. **🔍 Feature Analysis**
- Top 15 most important features (by weight)
- Feature correlation with price
- Feature statistics and ranges
- Visual importance ranking

### 5. **ℹ️ About**
- Model documentation and details
- Algorithm explanation
- Technologies used
- Model limitations

## 🤖 Model Architecture

### Algorithm
**Multivariate Linear Regression with L2 Regularization**

```
Price = w₁·distance + w₂·surge + w₃·distance² + w₄·surge² + 
        w₅·(distance×surge) + Σ(cab_type_weights) + Σ(ride_name_weights) + b
```

### Cost Function
```
J(w,b) = (1/2m) Σ(f(x⁽ⁱ⁾) - y⁽ⁱ⁾)² + (λ/2m) ||w||²
```

### Training
- **Optimizer**: Batch Gradient Descent
- **Learning Rate**: 0.001 (adaptive)
- **Iterations**: 10,000
- **Regularization**: L2 (λ = 0.01)

## 📊 Data Features

| Feature | Type | Description |
|---------|------|-------------|
| `distance` | Numeric | Trip distance in miles |
| `surge_multiplier` | Numeric | Demand-based pricing factor (1.0 = normal, 2.0 = 2x price) |
| `cab_type` | Categorical | Uber, Lyft, etc. |
| `name` | Categorical | Ride type (UberX, UberXL, Black, Shared, etc.) |
| `price` | Numeric | Actual ride price (target variable) |

## 📈 Model Performance

Typical metrics (varies with data):
- **R² Score**: ~0.8-0.9 (explains 80-90% of price variation)
- **MAE**: ~$2-5 (average prediction error)
- **RMSE**: ~$3-7 (penalizes larger errors more)

## 🌐 Deployment Options

### 1. **Streamlit Cloud (Recommended - FREE)**
Most straightforward option with one-click deployment.

```bash
# Push to GitHub, then deploy via share.streamlit.io
```

[See STREAMLIT_GUIDE.md](STREAMLIT_GUIDE.md#-publishing-to-streamlit-cloud-free) for detailed steps.

### 2. **Heroku (Paid)**
Classic PaaS deployment with Docker support.

### 3. **AWS/Google Cloud/Azure**
Enterprise-grade deployment with custom infrastructure.

### 4. **Docker**
Containerize the app for any platform.

[See STREAMLIT_GUIDE.md](STREAMLIT_GUIDE.md#-alternative-deployment-options) for all options.

## 🔧 Configuration & Customization

### Adjust Model Hyperparameters

Edit `app.py` in the `train_model()` function:

```python
alpha=0.001        # Learning rate (smaller = more stable, slower)
num_iters=10000    # Number of gradient descent iterations
lambda_=0.01       # L2 regularization strength
```

### Add More Features

In the `train_model()` function, add new features before the categorical encoding:

```python
# Add temperature and humidity if available
if 'temperature' in df_clean.columns:
    # Add temperature encoding...
```

### Change Color Scheme

Search for hex color codes like `#3498DB` and replace with your preferred colors.

## 🧪 Testing Locally

The app automatically:
1. ✅ Loads the CSV data
2. ✅ Cleans and validates the data
3. ✅ Trains the model on first run
4. ✅ Caches results for fast subsequent loads
5. ✅ Displays interactive visualizations

## ⚠️ Troubleshooting

### Issue: "ModuleNotFoundError"
**Solution**: Reinstall packages
```bash
pip install -r requirements.txt
```

### Issue: "FileNotFoundError: rideshare_kaggle.csv"
**Solution**: Ensure CSV is in the same directory as `app.py`
```bash
ls rideshare_kaggle.csv
```

### Issue: App takes a long time to start
**Solution**: This is normal on first run. The model trains once and caches results.

### Issue: Port 8501 already in use
**Solution**: Use a different port
```bash
streamlit run app.py --server.port 8502
```

### Issue: Changes not reflecting
**Solution**: Hard refresh (Ctrl+Shift+R) or restart Streamlit

## 📚 Technologies

- **Streamlit**: Interactive web app framework
- **NumPy**: Numerical computations and linear algebra
- **Pandas**: Data manipulation and analysis
- **Matplotlib**: Data visualization
- **Python 3.11+**: Programming language

## 🎓 Learning Resources

- [Streamlit Documentation](https://docs.streamlit.io/)
- [NumPy Linear Algebra](https://numpy.org/doc/stable/reference/routines.linalg.html)
- [Gradient Descent Tutorial](https://en.wikipedia.org/wiki/Gradient_descent)
- [Linear Regression Mathematics](https://en.wikipedia.org/wiki/Linear_regression)

## 📄 Original Notebook

The project is based on Andrew Ng's Machine Learning course materials with enhancements:
- Enhanced feature engineering with polynomial terms
- One-hot categorical encoding
- Comprehensive visualizations
- Production-ready Streamlit app

## 🔐 Privacy & Security

- All computation happens locally or on your server
- No external API calls
- Data stays in your environment
- Open source - review the code anytime

## 🤝 Contributing

Feel free to:
- ✅ Fork and modify
- ✅ Add new features
- ✅ Improve visualizations
- ✅ Optimize performance
- ✅ Fix bugs

## 📝 License

This project is provided as-is for educational purposes.

## 🙋 Support

- **Streamlit Issues**: [Streamlit Community](https://discuss.streamlit.io/)
- **ML Questions**: [Stack Overflow](https://stackoverflow.com/)
- **Documentation**: Check the inline code comments

## 🎉 Next Steps

1. **Run the app** locally to explore
2. **Modify hyperparameters** to improve accuracy
3. **Add new features** to the model
4. **Deploy** to Streamlit Cloud
5. **Share** with others and get feedback
6. **Iterate** based on real-world performance

---

**Happy exploring! 🚀 Feel free to reach out with questions or suggestions.**

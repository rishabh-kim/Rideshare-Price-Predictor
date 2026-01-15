# 🚀 Quick Reference - Streamlit Rideshare App

## Launch Commands

### Start the App
```bash
streamlit run app.py
```

### Or Use the Quick Start Script
```bash
chmod +x run.sh
./run.sh
```

## URL
- **Local**: `http://localhost:8501`
- **After Deployment**: `https://share.streamlit.io/YOUR_USERNAME/rideshare-predictor`

## File Locations
```
📁 Rideshare Multivariate Regression/
   ├── app.py                    (Main app - run this)
   ├── rideshare_kaggle.csv      (Data - required)
   ├── requirements.txt          (Dependencies)
   ├── run.sh                    (Quick start script)
   └── README.md                 (Full documentation)
```

## Deployment Checklist

- [ ] `app.py` is in project root
- [ ] `requirements.txt` exists with dependencies
- [ ] `rideshare_kaggle.csv` is in project root
- [ ] Test locally: `streamlit run app.py`
- [ ] Push to GitHub
- [ ] Go to [share.streamlit.io](https://share.streamlit.io)
- [ ] Click "New App" → select repo → done!

## App Sections

| Tab | Purpose |
|-----|---------|
| 💰 Prediction | Make price predictions |
| 📈 Explorer | Explore data and visualizations |
| 🎯 Performance | View model metrics |
| 🔍 Features | See feature importance |
| ℹ️ About | Learn about the model |

## Common Tasks

### Change Learning Rate
Edit `app.py` line ~270:
```python
alpha=0.001  # Change this value
```

### Change Number of Iterations
Edit `app.py` line ~271:
```python
num_iters=10000  # Change this value
```

### Add New Feature
1. Edit CSV to include new column
2. Update `train_model()` function to include feature
3. Add to prediction function

### Deploy to Cloud
1. `git push` to GitHub
2. Visit [share.streamlit.io](https://share.streamlit.io)
3. Click "New App"
4. Select your repository
5. Click "Deploy"

## Troubleshooting

| Problem | Solution |
|---------|----------|
| ModuleNotFoundError | `pip install -r requirements.txt` |
| CSV not found | Check it's in same directory as `app.py` |
| Port in use | `streamlit run app.py --server.port 8502` |
| Slow startup | Normal on first run (model trains once) |
| Changes not showing | Hard refresh (Ctrl+Shift+R) or restart |

## Key Model Metrics

- **R² Score**: How much variance is explained (0-1, higher is better)
- **MAE**: Average absolute error in dollars
- **RMSE**: Root mean squared error (penalizes larger errors)

## Performance Examples

Typical outputs:
- 📊 R² Score: ~0.85 (explains 85% of price variation)
- 💵 MAE: ~$3.50 (predicts within $3.50 on average)
- 📈 RMSE: ~$5.20 (slightly higher due to outliers)

## Next Improvements

- Add time-of-day feature
- Include weather conditions
- Try polynomial regression (degree 3)
- Add seasonality features
- Implement cross-validation
- Try other algorithms (Ridge, Lasso)

---

**Questions?** Check [README.md](README.md) or [STREAMLIT_GUIDE.md](STREAMLIT_GUIDE.md)

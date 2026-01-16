import streamlit as st
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import copy
import math
from pathlib import Path

# Set page config
st.set_page_config(
    page_title="Rideshare Price Predictor",
    page_icon="🚗",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom styling
st.markdown("""
    <style>
    .main {
        padding-top: 0rem;
    }
    .metric-card {
        background-color: #f0f2f6;
        padding: 20px;
        border-radius: 10px;
        margin-bottom: 15px;
    }
    </style>
    """, unsafe_allow_html=True)

# ============================================================================
# LOAD AND PREPARE DATA
# ============================================================================

@st.cache_data
def load_and_prepare_data():
    """Load and prepare the rideshare dataset."""
    # Try to load from multiple possible locations
    possible_paths = [
        'rideshare_kaggle.csv',
        'data/rideshare_kaggle.csv',
        '../data/rideshare_kaggle.csv',
    ]
    
    df = None
    for path in possible_paths:
        try:
            df = pd.read_csv(path)
            st.sidebar.success(f"✅ Data loaded from: {path}")
            break
        except FileNotFoundError:
            continue
    
    if df is None:
        st.error("❌ Could not find rideshare_kaggle.csv. Please ensure it's in the same directory as app.py")
        st.stop()
    
    # Clean data
    df_clean = df.dropna(subset=['price', 'distance', 'surge_multiplier'])
    numeric_features = ['distance', 'surge_multiplier']
    X_numeric = df_clean[numeric_features].values
    y_train = df_clean['price'].values
    
    mask = ~np.any(np.isnan(X_numeric), axis=1) & ~np.isnan(y_train)
    X_numeric = X_numeric[mask]
    y_train = y_train[mask]
    df_clean = df_clean[mask].reset_index(drop=True)
    
    return df_clean, X_numeric, y_train, numeric_features

# ============================================================================
# MODEL FUNCTIONS
# ============================================================================

def compute_cost(X, y, w, b, lambda_=1):
    """Compute cost function for multivariate linear regression."""
    m = X.shape[0]
    f_wb = np.dot(X, w) + b
    errors = f_wb - y
    cost = np.dot(errors, errors) / (2 * m)
    reg_cost = (lambda_ / (2 * m)) * np.dot(w, w)
    return cost + reg_cost

def compute_gradient(X, y, w, b, lambda_=1):
    """Compute gradient for multivariate linear regression."""
    m, n = X.shape
    f_wb = np.dot(X, w) + b
    errors = f_wb - y
    dj_dw = np.dot(X.T, errors) / m + (lambda_ / m) * w
    dj_db = np.sum(errors) / m
    return dj_dw, dj_db

def gradient_descent(X, y, w_init, b_init, alpha, num_iters, lambda_=1):
    """Run gradient descent to train the model."""
    w = copy.deepcopy(w_init)
    b = b_init
    J_history = []
    
    for i in range(num_iters):
        dj_dw, dj_db = compute_gradient(X, y, w, b, lambda_)
        w = w - alpha * dj_dw
        b = b - alpha * dj_db
        
        if i % 100 == 0:
            cost = compute_cost(X, y, w, b, lambda_)
            J_history.append(cost)
    
    return w, b, J_history

@st.cache_resource
def train_model(X_numeric, y_train, numeric_features):
    """Train the rideshare pricing model."""
    # Extract and normalize features
    feature_means = X_numeric.mean(axis=0)
    feature_stds = X_numeric.std(axis=0)
    X_normalized = (X_numeric - feature_means) / feature_stds
    
    distance_norm = X_normalized[:, 0]
    surge_norm = X_normalized[:, 1]
    
    # Polynomial features
    poly_features = np.column_stack([
        distance_norm ** 2,
        surge_norm ** 2,
        distance_norm * surge_norm,
    ])
    
    # Build feature matrix
    X_train = np.column_stack([X_normalized, poly_features])
    
    # One-hot encode categorical features
    df_clean, _, _, _ = load_and_prepare_data()
    cab_type_encoded = pd.get_dummies(df_clean['cab_type'], prefix='cab')
    name_encoded = pd.get_dummies(df_clean['name'], prefix='ride')
    
    X_train = np.column_stack([
        X_train,
        cab_type_encoded.values,
        name_encoded.values,
    ])
    
    # Train with gradient descent
    n = X_train.shape[1]
    w_init = np.zeros(n)
    b_init = 0
    
    w_final, b_final, J_history = gradient_descent(
        X_train, y_train, w_init, b_init,
        alpha=0.001, num_iters=10000, lambda_=0.01
    )
    
    # Calculate metrics
    y_pred = np.dot(X_train, w_final) + b_final
    residuals = y_train - y_pred
    mae = np.mean(np.abs(residuals))
    rmse = np.sqrt(np.mean(residuals ** 2))
    ss_res = np.sum(residuals ** 2)
    ss_tot = np.sum((y_train - y_train.mean()) ** 2)
    r_squared = 1 - (ss_res / ss_tot)
    
    # Create feature names
    enhanced_feature_names = (
        numeric_features +
        ['distance²', 'surge²', 'distance×surge'] +
        list(cab_type_encoded.columns) +
        list(name_encoded.columns)
    )
    
    return {
        'w': w_final,
        'b': b_final,
        'J_history': J_history,
        'feature_means': feature_means,
        'feature_stds': feature_stds,
        'enhanced_feature_names': enhanced_feature_names,
        'cab_columns': list(cab_type_encoded.columns),
        'name_columns': list(name_encoded.columns),
        'mae': mae,
        'rmse': rmse,
        'r_squared': r_squared,
        'X_train': X_train,
        'y_train': y_train,
    }

# ============================================================================
# PREDICTION FUNCTION
# ============================================================================

def predict_price(distance, surge, cab_type, ride_name, model):
    """Make price prediction using trained model."""
    # Normalize numeric features
    dist_norm = (distance - model['feature_means'][0]) / model['feature_stds'][0]
    surge_norm = (surge - model['feature_means'][1]) / model['feature_stds'][1]
    
    # Polynomial features
    poly = [dist_norm**2, surge_norm**2, dist_norm * surge_norm]
    
    # One-hot encode
    cab_onehot = [1 if f'cab_{cab_type}' == col else 0 for col in model['cab_columns']]
    name_onehot = [1 if f'ride_{ride_name}' == col else 0 for col in model['name_columns']]
    
    # Build feature vector
    features = np.array([dist_norm, surge_norm] + poly + cab_onehot + name_onehot)
    
    return np.dot(features, model['w']) + model['b']

# ============================================================================
# MAIN APP
# ============================================================================

# Load data
df_clean, X_numeric, y_train, numeric_features = load_and_prepare_data()

# Train model (cached)
model = train_model(X_numeric, y_train, numeric_features)

# Get unique values for dropdowns
cab_types = sorted(df_clean['cab_type'].unique())
ride_names = sorted(df_clean['name'].unique())

# ============================================================================
# HEADER
# ============================================================================

st.title("🚗 Rideshare Price Predictor")
st.markdown("---")
st.markdown("**Predict rideshare prices using machine learning!** "
            "This app uses multivariate linear regression with polynomial features and categorical encoding.")

# ============================================================================
# SIDEBAR - PREDICTION INTERFACE
# ============================================================================

st.sidebar.header("📊 Make a Prediction")
st.sidebar.markdown("---")

distance = st.sidebar.slider(
    "Distance (miles)",
    min_value=float(df_clean['distance'].min()),
    max_value=float(df_clean['distance'].max()),
    value=3.0,
    step=0.1
)

surge = st.sidebar.slider(
    "Surge Multiplier",
    min_value=1.0,
    max_value=float(df_clean['surge_multiplier'].max()),
    value=1.0,
    step=0.05
)

cab_type = st.sidebar.selectbox("Cab Type", cab_types)
ride_name = st.sidebar.selectbox("Ride Type", ride_names)

# Make prediction
predicted_price = predict_price(distance, surge, cab_type, ride_name, model)

# Display prediction in sidebar
st.sidebar.markdown("---")
st.sidebar.markdown("### 🎯 Predicted Price")
st.sidebar.markdown(f"## ${predicted_price:.2f}")

# ============================================================================
# MAIN CONTENT - TABS
# ============================================================================

tab1, tab2, tab3, tab4, tab5 = st.tabs(
    ["💰 Prediction", "📈 Data Explorer", "🤖 Model Performance", "🔍 Feature Analysis", "ℹ️ About"]
)

# ============================================================================
# TAB 1: PREDICTION
# ============================================================================

with tab1:
    col1, col2 = st.columns(2)
    
    with col1:
        st.metric("📍 Distance", f"{distance:.1f} miles")
        st.metric("⚡ Surge Multiplier", f"{surge:.2f}x")
    
    with col2:
        st.metric("🚕 Cab Type", cab_type)
        st.metric("🏷️ Ride Type", ride_name)
    
    st.markdown("---")
    
    # Predicted price card
    col1, col2 = st.columns([2, 1])
    with col1:
        st.markdown("### Predicted Price")
        st.markdown(f"<h1 style='color: #27AE60; font-size: 48px;'>${predicted_price:.2f}</h1>", 
                   unsafe_allow_html=True)
    
    with col2:
        st.info(f"**Confidence:**\n\nR² Score: {model['r_squared']:.1%}\n\nThis model explains "
                f"{model['r_squared']*100:.1f}% of price variation")
    
    st.markdown("---")
    
    # Price scenarios
    st.subheader("💡 What if scenarios?")
    
    col1, col2, col3 = st.columns(3)
    with col1:
        surge_high = predict_price(distance, surge * 1.5, cab_type, ride_name, model)
        st.metric("50% More Surge", f"${surge_high:.2f}", delta=f"${surge_high - predicted_price:.2f}")
    
    with col2:
        dist_high = predict_price(distance * 1.5, surge, cab_type, ride_name, model)
        st.metric("50% Longer Distance", f"${dist_high:.2f}", delta=f"${dist_high - predicted_price:.2f}")
    
    with col3:
        both_high = predict_price(distance * 1.5, surge * 1.5, cab_type, ride_name, model)
        st.metric("Both 50% Higher", f"${both_high:.2f}", delta=f"${both_high - predicted_price:.2f}")

# ============================================================================
# TAB 2: DATA EXPLORER
# ============================================================================

with tab2:
    st.subheader("📊 Dataset Overview")
    
    col1, col2, col3 = st.columns(3)
    with col1:
        st.metric("Total Rides", f"{len(df_clean):,}")
    with col2:
        st.metric("Avg Price", f"${df_clean['price'].mean():.2f}")
    with col3:
        st.metric("Price Range", f"${df_clean['price'].min():.2f} - ${df_clean['price'].max():.2f}")
    
    st.markdown("---")
    
    # Data distribution plots
    col1, col2 = st.columns(2)
    
    with col1:
        fig, ax = plt.subplots(figsize=(10, 5))
        ax.hist(df_clean['price'], bins=50, color='#3498DB', edgecolor='black', alpha=0.7)
        ax.set_xlabel('Price ($)', fontweight='bold')
        ax.set_ylabel('Frequency', fontweight='bold')
        ax.set_title('Price Distribution', fontweight='bold')
        ax.grid(True, linestyle='--', alpha=0.3)
        st.pyplot(fig)
    
    with col2:
        fig, ax = plt.subplots(figsize=(10, 5))
        ax.scatter(df_clean['distance'], df_clean['price'], alpha=0.5, s=20, color='#E74C3C')
        ax.set_xlabel('Distance (miles)', fontweight='bold')
        ax.set_ylabel('Price ($)', fontweight='bold')
        ax.set_title('Distance vs Price', fontweight='bold')
        ax.grid(True, linestyle='--', alpha=0.3)
        st.pyplot(fig)
    
    st.markdown("---")
    
    # Ride type distribution
    col1, col2 = st.columns(2)
    
    with col1:
        fig, ax = plt.subplots(figsize=(10, 5))
        df_clean['cab_type'].value_counts().plot(kind='bar', ax=ax, color='#9B59B6', edgecolor='black')
        ax.set_title('Rides by Cab Type', fontweight='bold')
        ax.set_ylabel('Count', fontweight='bold')
        ax.set_xlabel('Cab Type', fontweight='bold')
        plt.xticks(rotation=45)
        st.pyplot(fig)
    
    with col2:
        fig, ax = plt.subplots(figsize=(10, 5))
        df_clean['name'].value_counts().head(10).plot(kind='barh', ax=ax, color='#1ABC9C', edgecolor='black')
        ax.set_title('Top 10 Ride Types', fontweight='bold')
        ax.set_xlabel('Count', fontweight='bold')
        st.pyplot(fig)
    
    st.markdown("---")
    
    # Data table
    st.subheader("📋 Sample Data")
    st.dataframe(
        df_clean.head(10).style.format({
            'price': '${:.2f}',
            'distance': '{:.2f}',
            'surge_multiplier': '{:.2f}x'
        }),
        use_container_width=True
    )

# ============================================================================
# TAB 3: MODEL PERFORMANCE
# ============================================================================

with tab3:
    st.subheader("🎯 Model Performance Metrics")
    
    col1, col2, col3, col4 = st.columns(4)
    with col1:
        st.metric("Mean Absolute Error", f"${model['mae']:.2f}", help="Average absolute prediction error")
    with col2:
        st.metric("RMSE", f"${model['rmse']:.2f}", help="Root mean squared error")
    with col3:
        st.metric("R² Score", f"{model['r_squared']:.4f}", help="Coefficient of determination")
    with col4:
        st.metric("Variance Explained", f"{model['r_squared']*100:.1f}%", help="% of price variation explained")
    
    st.markdown("---")
    
    # Prediction accuracy plot
    y_pred = np.dot(model['X_train'], model['w']) + model['b']
    residuals = model['y_train'] - y_pred
    
    col1, col2, col3 = st.columns(3)
    
    with col1:
        fig, ax = plt.subplots(figsize=(10, 6))
        sample = np.random.choice(len(model['y_train']), min(2000, len(model['y_train'])), replace=False)
        ax.scatter(model['y_train'][sample], y_pred[sample], alpha=0.4, s=20, color='#3498DB')
        min_val = min(model['y_train'].min(), y_pred.min())
        max_val = max(model['y_train'].max(), y_pred.max())
        ax.plot([min_val, max_val], [min_val, max_val], 'r--', linewidth=2)
        ax.set_xlabel('Actual Price ($)', fontweight='bold')
        ax.set_ylabel('Predicted Price ($)', fontweight='bold')
        ax.set_title('Predicted vs Actual', fontweight='bold')
        ax.grid(True, linestyle='--', alpha=0.3)
        st.pyplot(fig)
    
    with col2:
        fig, ax = plt.subplots(figsize=(10, 6))
        ax.scatter(y_pred[sample], residuals[sample], alpha=0.4, s=20, color='#E74C3C')
        ax.axhline(y=0, color='green', linestyle='--', linewidth=2)
        ax.set_xlabel('Predicted Price ($)', fontweight='bold')
        ax.set_ylabel('Residuals ($)', fontweight='bold')
        ax.set_title('Residual Plot', fontweight='bold')
        ax.grid(True, linestyle='--', alpha=0.3)
        st.pyplot(fig)
    
    with col3:
        fig, ax = plt.subplots(figsize=(10, 6))
        ax.hist(residuals, bins=50, color='#9B59B6', edgecolor='black', alpha=0.7)
        ax.axvline(x=0, color='green', linestyle='--', linewidth=2)
        ax.set_xlabel('Residual ($)', fontweight='bold')
        ax.set_ylabel('Frequency', fontweight='bold')
        ax.set_title('Residual Distribution', fontweight='bold')
        ax.grid(True, linestyle='--', alpha=0.3)
        st.pyplot(fig)
    
    st.markdown("---")
    
    # Cost convergence
    st.subheader("📉 Training Convergence")
    fig, ax = plt.subplots(figsize=(12, 5))
    iterations = np.arange(0, len(model['J_history'])) * 100
    ax.plot(iterations, model['J_history'], color='#3498DB', linewidth=2.5, marker='o', markersize=5)
    ax.set_xlabel('Iteration', fontweight='bold')
    ax.set_ylabel('Cost (MSE/2)', fontweight='bold')
    ax.set_title('Cost Function Convergence', fontweight='bold')
    ax.grid(True, linestyle='--', alpha=0.5)
    st.pyplot(fig)

# ============================================================================
# TAB 4: FEATURE ANALYSIS
# ============================================================================

with tab4:
    st.subheader("🔍 Feature Importance")
    
    # Calculate feature importance
    importance = sorted(
        zip(model['enhanced_feature_names'], np.abs(model['w'])),
        key=lambda x: x[1],
        reverse=True
    )
    
    fig, ax = plt.subplots(figsize=(12, 8))
    features_sorted = [f[0].replace('_', ' ').title() for f in importance[:15]]
    weights_sorted = [f[1] for f in importance[:15]]
    colors = plt.cm.RdYlBu(np.linspace(0.2, 0.8, len(features_sorted)))
    
    ax.barh(features_sorted, weights_sorted, color=colors, edgecolor='black', linewidth=1.5)
    ax.set_xlabel('Absolute Weight Magnitude', fontweight='bold')
    ax.set_title('Top 15 Most Important Features', fontweight='bold')
    ax.grid(True, axis='x', linestyle='--', alpha=0.5)
    st.pyplot(fig)
    
    st.markdown("---")
    
    # Feature statistics
    st.subheader("📊 Feature Statistics")
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.write("**Distance (miles)**")
        st.write(f"Min: {df_clean['distance'].min():.2f}")
        st.write(f"Max: {df_clean['distance'].max():.2f}")
        st.write(f"Mean: {df_clean['distance'].mean():.2f}")
        st.write(f"Std: {df_clean['distance'].std():.2f}")
    
    with col2:
        st.write("**Surge Multiplier**")
        st.write(f"Min: {df_clean['surge_multiplier'].min():.2f}")
        st.write(f"Max: {df_clean['surge_multiplier'].max():.2f}")
        st.write(f"Mean: {df_clean['surge_multiplier'].mean():.2f}")
        st.write(f"Std: {df_clean['surge_multiplier'].std():.2f}")
    
    st.markdown("---")
    
    # Correlation analysis
    st.subheader("🔗 Feature Correlations with Price")
    
    sample_cols = ['distance', 'surge_multiplier', 'price']
    if 'temperature' in df_clean.columns:
        sample_cols.append('temperature')
    if 'humidity' in df_clean.columns:
        sample_cols.append('humidity')
    
    corr_matrix = df_clean[sample_cols].corr()
    price_corr = corr_matrix['price'].drop('price').sort_values(ascending=False)
    
    fig, ax = plt.subplots(figsize=(10, 5))
    colors_corr = ['#27AE60' if x > 0 else '#E74C3C' for x in price_corr.values]
    price_corr.plot(kind='barh', ax=ax, color=colors_corr, edgecolor='black')
    ax.set_xlabel('Correlation with Price', fontweight='bold')
    ax.set_title('Feature Correlations with Price', fontweight='bold')
    ax.grid(True, axis='x', linestyle='--', alpha=0.3)
    st.pyplot(fig)

# ============================================================================
# TAB 5: ABOUT
# ============================================================================

with tab5:
    st.markdown("""
    ## 📚 About This App
    
    This Streamlit app demonstrates a **multivariate linear regression model** trained to predict rideshare prices.
    
    ### 🤖 Model Details
    
    - **Algorithm**: Multivariate Linear Regression with L2 Regularization
    - **Features Used**:
      - Numeric (normalized): distance, surge_multiplier
      - Polynomial: distance², surge², distance×surge interaction
      - Categorical (one-hot encoded): cab_type, ride_name
    - **Training Method**: Batch Gradient Descent
    - **Total Features**: 21+ (depending on unique categories)
    
    ### 📊 Performance
    
    - **R² Score**: {:.1%} (variance explained)
    - **Mean Absolute Error**: ${:.2f}
    - **Root Mean Squared Error**: ${:.2f}
    
    ### 🚀 Key Features
    
    1. **Interactive Predictions**: Adjust distance, surge, cab type, and ride type to see predicted prices
    2. **What-If Analysis**: Explore how prices change with different parameters
    3. **Data Explorer**: Visualize the underlying dataset and distributions
    4. **Model Performance**: View detailed model metrics and prediction accuracy
    5. **Feature Analysis**: Understand which features are most important
    
    ### 💡 How It Works
    
    1. The model learns from historical rideshare data
    2. It identifies patterns between features (distance, surge, cab type, etc.) and prices
    3. For new rides, it predicts prices using the learned patterns
    4. The prediction uses normalized features to ensure fair weighting
    5. Polynomial features capture non-linear relationships
    
    ### 📈 Model Equation
    
    ```
    Price = w₁·distance + w₂·surge + w₃·distance² + w₄·surge² + 
            w₅·(distance×surge) + Σ(cab_type_weights) + Σ(ride_name_weights) + b
    ```
    
    ### ⚖️ Limitations
    
    - Linear model may not capture all complex price dynamics
    - Predictions assume historical patterns continue
    - Model accuracy depends on data quality and feature selection
    - External factors (events, weather) not captured in basic features
    
    ### 🔧 Technologies
    
    - **Streamlit**: Interactive web app framework
    - **NumPy**: Numerical computations
    - **Pandas**: Data manipulation
    - **Matplotlib**: Visualizations
    - **Scikit-learn**: (conceptual, implemented from scratch)
    
    ---
    
    **Built with ❤️ using Streamlit**
    """.format(model['r_squared'], model['mae'], model['rmse']))

st.markdown("---")
st.markdown("<p style='text-align: center; color: gray;'>© 2025 Rideshare Price Predictor | ML Regression Project</p>", 
           unsafe_allow_html=True)

# app_final.py - PATH ABSOLUTE - CHẠY TỪ ĐÂU CŨNG OK
import streamlit as st
import pandas as pd
import plotly.express as px
from sklearn.decomposition import PCA
import numpy as np
import os

st.set_page_config(layout="wide")

st.title("👥 Dashboard Phân Cụm Khách Hàng")
st.markdown("**RFM + Top 200 Association Rules**")

# PATH TUYỆT ĐỐI
BASE_DIR = r"D:\BigData\shop_cluster_nhom_9"
DATA_FILE = os.path.join(BASE_DIR, "data", "processed", "customer_clusters_ruleRFM_200.csv")

@st.cache_data
def load_data():
    return pd.read_csv(DATA_FILE)

df = load_data()
st.success(f"✅ {df.shape[0]:,} khách hàng | K=2")

# Sidebar
st.sidebar.header("📊 Chọn hiển thị")
show_pca = st.sidebar.checkbox("PCA 2D", True)
show_profile = st.sidebar.checkbox("Profile", True)

# KPIs
col1, col2 = st.columns(2)
col1.metric("👥 Tổng KH", f"{len(df):,}")
col2.metric("⭐ VIP (C1)", f"{len(df[df.cluster==1]):,}")

if show_pca:
    st.subheader("🔍 PCA 2D")
    pca = PCA(2)
    Z = pca.fit_transform(df.drop(['CustomerID','cluster'], axis=1))
    fig = px.scatter(x=Z[:,0], y=Z[:,1], color=df.cluster,
                     title="PCA Clusters", labels={'x':'PC1','y':'PC2'})
    st.plotly_chart(fig)

if show_profile:
    st.subheader("📋 Profile Clusters")
    profile = df.groupby('cluster')[['Recency','Frequency','Monetary']].mean()
    st.dataframe(profile)

# Top VIP
st.subheader("👑 Top VIP")
vip = df[df.cluster==1].nlargest(10,'Monetary')[['CustomerID','Monetary']]
st.dataframe(vip)

st.markdown("**Mini Project Hoàn Thành** 🎓")

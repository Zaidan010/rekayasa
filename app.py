import streamlit as st
import numpy as np
import pandas as pd
import sympy as sp
from sympy import symbols, lambdify, sympify

x = sp.symbols('x')

st.set_page_config(page_title="Metode Numerik", layout="centered")
st.title("📊 Kalkulator Akar Persamaan Nonlinear")
st.write("Pilih salah satu metode numerik untuk mencari akar dari fungsi yang kamu masukkan.")

# Fungsi konversi string ke fungsi Python
def parse_function(expr):
    try:
        f = lambdify(x, sympify(expr), modules=['numpy'])
        return f
    except:
        return None

# Metode Bagi Dua
def bisection(f, a, b, tol, max_iter):
    if f(a) * f(b) >= 0:
        return None, "f(a) * f(b) harus < 0", None
    data = []
    for i in range(1, max_iter + 1):
        c = (a + b) / 2
        fc = f(c)
        data.append((i, a, b, c, fc))
        if abs(fc) < tol or (b - a) / 2 < tol:
            return c, i, data
        if f(a) * fc < 0:
            b = c
        else:
            a = c
    return c, max_iter, data

# Metode Regula Falsi
def regula_falsi(f, a, b, tol, max_iter):
    if f(a) * f(b) >= 0:
        return None, "f(a) * f(b) harus < 0", None
    data = []
    for i in range(1, max_iter + 1):
        fa, fb = f(a), f(b)
        c = b - fb * (b - a) / (fb - fa)
        fc = f(c)
        data.append((i, a, b, c, fc))
        if abs(fc) < tol:
            return c, i, data
        if f(a) * fc < 0:
            b = c
        else:
            a = c
    return c, max_iter, data

# Fixed-Point Iteration
def fixed_point(g, x0, tol, max_iter):
    data = []
    for i in range(1, max_iter + 1):
        try:
            x1 = g(x0)
            data.append((i, x0, x1, abs(x1 - x0)))
        except Exception as e:
            return None, f"Error fungsi g(x): {e}", None
        if abs(x1 - x0) < tol:
            return x1, i, data
        x0 = x1
    return x1, max_iter, data

# Newton-Raphson
def newton_raphson(f_expr, x0, tol, max_iter):
    f = lambdify(x, sympify(f_expr), modules='numpy')
    df_expr = sp.diff(f_expr, x)
    df = lambdify(x, df_expr, modules='numpy')
    data = []
    for i in range(1, max_iter + 1):
        try:
            fx, dfx = f(x0), df(x0)
            if dfx == 0:
                return None, "Turunan nol!", None
            x1 = x0 - fx / dfx
            data.append((i, x0, fx, dfx, x1, abs(x1 - x0)))
        except Exception as e:
            return None, f"Error saat evaluasi fungsi: {e}", None
        if abs(x1 - x0) < tol:
            return x1, i, data
        x0 = x1
    return x1, max_iter, data

# Metode Secant
def secant(f, x0, x1, tol, max_iter):
    data = []
    for i in range(1, max_iter + 1):
        try:
            fx0, fx1 = f(x0), f(x1)
            if fx1 - fx0 == 0:
                return None, "Pembagi nol!", None
            x2 = x1 - fx1 * (x1 - x0) / (fx1 - fx0)
            data.append((i, x0, x1, x2, abs(x2 - x1)))
        except Exception as e:
            return None, f"Error saat evaluasi fungsi: {e}", None
        if abs(x2 - x1) < tol:
            return x2, i, data
        x0, x1 = x1, x2
    return x2, max_iter, data

# Input pengguna
metode = st.selectbox("🔧 Pilih Metode:", [
    "Metode Bagi Dua",
    "Metode Regula Falsi",
    "Fixed-Point Iteration",
    "Newton-Raphson",
    "Secant"
])

fungsi_input = st.text_input("Masukkan fungsi f(x):", placeholder="Input Fungsi")
tol = st.number_input("Toleransi Error:", value=1e-6, format="%.1e")
max_iter = st.number_input("🔁 Maksimum Iterasi:", value=100, step=1)

f = parse_function(fungsi_input)

if metode == "Metode Bagi Dua":
    col1, col2 = st.columns(2)
    a = col1.number_input("Batas bawah (a):")
    b = col2.number_input("Batas atas (b):")
    if st.button("Hitung"):
        if f is None:
            st.error("Fungsi f(x) tidak valid!")
        else:
            akar, info, data = bisection(f, a, b, tol, max_iter)
            if isinstance(info, int):
                st.success(f"Akar = {akar}, Iterasi = {info}")
                df = pd.DataFrame(data, columns=["Iterasi", "a", "b", "c", "f(c)"])
                st.dataframe(df)
            else:
                st.error(info)

elif metode == "Metode Regula Falsi":
    col1, col2 = st.columns(2)
    a = col1.number_input("Batas bawah (a):")
    b = col2.number_input("Batas atas (b):")
    if st.button("Hitung"):
        if f is None:
            st.error("Fungsi f(x) tidak valid!")
        else:
            akar, info, data = regula_falsi(f, a, b, tol, max_iter)
            if isinstance(info, int):
                st.success(f"Akar = {akar}, Iterasi = {info}")
                df = pd.DataFrame(data, columns=["Iterasi", "a", "b", "c", "f(c)"])
                st.dataframe(df)
            else:
                st.error(info)

elif metode == "Fixed-Point Iteration":
    g_input = st.text_input("Masukkan fungsi g(x):", "np.cbrt(x + 2)")
    g = parse_function(g_input)
    x0 = st.number_input("Tebakan awal x₀:")
    if st.button("Hitung"):
        if g is None:
            st.error("Fungsi g(x) tidak valid!")
        else:
            akar, info, data = fixed_point(g, x0, tol, max_iter)
            if isinstance(info, int):
                st.success(f"Akar = {akar}, Iterasi = {info}")
                df = pd.DataFrame(data, columns=["Iterasi", "x₀", "x₁", "|x₁ - x₀|"])
                st.dataframe(df)
            else:
                st.error(info)

elif metode == "Newton-Raphson":
    x0 = st.number_input("Tebakan awal x₀:")
    if st.button("Hitung"):
        akar, info, data = newton_raphson(fungsi_input, x0, tol, max_iter)
        if isinstance(info, int):
            st.success(f"Akar = {akar}, Iterasi = {info}")
            df = pd.DataFrame(data, columns=["Iterasi", "x₀", "f(x₀)", "f'(x₀)", "x₁", "|x₁ - x₀|"])
            st.dataframe(df)
        else:
            st.error(info)

elif metode == "Secant":
    col1, col2 = st.columns(2)
    x0 = col1.number_input("Tebakan awal x₀:")
    x1 = col2.number_input("Tebakan awal x₁:")
    if st.button("Hitung"):
        if f is None:
            st.error("Fungsi f(x) tidak valid!")
        else:
            akar, info, data = secant(f, x0, x1, tol, max_iter)
            if isinstance(info, int):
                st.success(f"✅ Akar = {akar}, Iterasi = {info}")
                df = pd.DataFrame(data, columns=["Iterasi", "x₀", "x₁", "x₂", "|x₂ - x₁|"])
                st.dataframe(df)
            else:
                st.error(info)

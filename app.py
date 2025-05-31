import streamlit as st
import numpy as np
import sympy as sp

x = sp.symbols('x')

# Fungsi konversi string ke fungsi Python
def parse_function(expr):
    try:
        f = sp.lambdify(x, sp.sympify(expr), modules=['numpy'])
        return f
    except:
        return None

# Metode Bagi Dua
def bisection(f, a, b, tol, max_iter):
    if f(a) * f(b) >= 0:
        return None, "f(a) * f(b) harus < 0"
    for i in range(max_iter):
        c = (a + b) / 2
        if abs(f(c)) < tol or (b - a) / 2 < tol:
            return c, i+1
        if f(a) * f(c) < 0:
            b = c
        else:
            a = c
    return c, max_iter

# Metode Regula Falsi
def regula_falsi(f, a, b, tol, max_iter):
    if f(a) * f(b) >= 0:
        return None, "f(a) * f(b) harus < 0"
    for i in range(max_iter):
        c = b - f(b)*(b - a)/(f(b) - f(a))
        if abs(f(c)) < tol:
            return c, i+1
        if f(a) * f(c) < 0:
            b = c
        else:
            a = c
    return c, max_iter

# Fixed-Point Iteration
def fixed_point(g, x0, tol, max_iter):
    for i in range(max_iter):
        x1 = g(x0)
        if abs(x1 - x0) < tol:
            return x1, i+1
        x0 = x1
    return x1, max_iter

# Newton-Raphson
def newton_raphson(f_expr, x0, tol, max_iter):
    f = sp.lambdify(x, sp.sympify(f_expr), modules='numpy')
    df_expr = sp.diff(f_expr, x)
    df = sp.lambdify(x, df_expr, modules='numpy')
    for i in range(max_iter):
        fx = f(x0)
        dfx = df(x0)
        if dfx == 0:
            return None, "Turunan nol!"
        x1 = x0 - fx / dfx
        if abs(x1 - x0) < tol:
            return x1, i+1
        x0 = x1
    return x1, max_iter

# Metode Secant
def secant(f, x0, x1, tol, max_iter):
    for i in range(max_iter):
        if f(x1) - f(x0) == 0:
            return None, "Pembagi nol!"
        x2 = x1 - f(x1)*(x1 - x0)/(f(x1) - f(x0))
        if abs(x2 - x1) < tol:
            return x2, i+1
        x0, x1 = x1, x2
    return x2, max_iter

# Antarmuka Streamlit
st.title("Kalkulator Metode Numerik (Akar Persamaan Nonlinear)")

metode = st.selectbox("Pilih Metode:", [
    "Metode Bagi Dua",
    "Metode Regula Falsi",
    "Fixed-Point Iteration",
    "Newton-Raphson",
    "Secant"
])

fungsi_input = st.text_input("Masukkan fungsi f(x):", "x**3 - x - 2")

tol = st.number_input("Toleransi Error:", value=1e-6, format="%.1e")
max_iter = st.number_input("Maksimum Iterasi:", value=100, step=1)

f = parse_function(fungsi_input)

if metode == "Metode Bagi Dua":
    a = st.number_input("Batas bawah (a):")
    b = st.number_input("Batas atas (b):")
    if st.button("Hitung"):
        akar, info = bisection(f, a, b, tol, max_iter)
        st.success(f"Akar = {akar}, Iterasi = {info}" if isinstance(info, int) else info)

elif metode == "Metode Regula Falsi":
    a = st.number_input("Batas bawah (a):")
    b = st.number_input("Batas atas (b):")
    if st.button("Hitung"):
        akar, info = regula_falsi(f, a, b, tol, max_iter)
        st.success(f"Akar = {akar}, Iterasi = {info}" if isinstance(info, int) else info)

elif metode == "Fixed-Point Iteration":
    g_input = st.text_input("Masukkan fungsi g(x):", "np.cbrt(x + 2)")
    g = parse_function(g_input)
    x0 = st.number_input("Tebakan awal x₀:")
    if st.button("Hitung"):
        akar, iterasi = fixed_point(g, x0, tol, max_iter)
        st.success(f"Akar = {akar}, Iterasi = {iterasi}")

elif metode == "Newton-Raphson":
    x0 = st.number_input("Tebakan awal x₀:")
    if st.button("Hitung"):
        akar, info = newton_raphson(fungsi_input, x0, tol, max_iter)
        st.success(f"Akar = {akar}, Iterasi = {info}" if isinstance(info, int) else info)

elif metode == "Secant":
    x0 = st.number_input("Tebakan awal x₀:")
    x1 = st.number_input("Tebakan awal x₁:")
    if st.button("Hitung"):
        akar, info = secant(f, x0, x1, tol, max_iter)
        st.success(f"Akar = {akar}, Iterasi = {info}" if isinstance(info, int) else info)

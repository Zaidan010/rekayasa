import streamlit as st
import math

st.set_page_config(page_title="Kalkulator Metode Numerik", layout="centered")

# Fungsi utama
def f(x):
    return x**3 - x - 2

# g(x) untuk Fixed-Point Iteration
def g(x):
    return (x**3 - 2)  # Syarat konvergensi harus dicek

# Metode-metode
def bisection(a, b, tol, max_iter):
    if f(a) * f(b) >= 0:
        return None, 0
    for i in range(max_iter):
        c = (a + b) / 2
        if abs(f(c)) < tol or abs(b - a) < tol:
            return c, i+1
        if f(a) * f(c) < 0:
            b = c
        else:
            a = c
    return c, max_iter

def regula_falsi(a, b, tol, max_iter):
    if f(a) * f(b) >= 0:
        return None, 0
    for i in range(max_iter):
        c = b - f(b)*(b - a)/(f(b) - f(a))
        if abs(f(c)) < tol:
            return c, i+1
        if f(a) * f(c) < 0:
            b = c
        else:
            a = c
    return c, max_iter

def fixed_point(x0, tol, max_iter):
    for i in range(max_iter):
        x1 = g(x0)
        if abs(x1 - x0) < tol:
            return x1, i+1
        x0 = x1
    return x0, max_iter

def newton_raphson(x0, tol, max_iter):
    def df(x): return 3*x**2 - 1
    for i in range(max_iter):
        if df(x0) == 0:
            return None, i
        x1 = x0 - f(x0)/df(x0)
        if abs(x1 - x0) < tol:
            return x1, i+1
        x0 = x1
    return x0, max_iter

def secant(x0, x1, tol, max_iter):
    for i in range(max_iter):
        if f(x1) - f(x0) == 0:
            return None, i
        x2 = x1 - f(x1)*(x1 - x0)/(f(x1) - f(x0))
        if abs(x2 - x1) < tol:
            return x2, i+1
        x0, x1 = x1, x2
    return x2, max_iter

# UI Web
st.title("Kalkulator Akar Persamaan Non-Linear")
st.markdown("**Fungsi:** `f(x) = x³ - x - 2`")

metode = st.selectbox(
    "Pilih Metode:",
    [
        "Metode Bagi Dua",
        "Metode Regula Falsi",
        "Metode Lelaran Titik Tetap (Fixed-Point Iteration)",
        "Metode Newton-Raphson",
        "Metode Secant"
    ]
)

st.divider()
tol = st.number_input("Toleransi Error", value=1e-6, format="%.10f")
max_iter = st.number_input("Maksimum Iterasi", min_value=1, value=100)

if metode in ["Metode Bagi Dua", "Metode Regula Falsi"]:
    a = st.number_input("Batas Bawah (a):", value=1.0)
    b = st.number_input("Batas Atas (b):", value=2.0)
elif metode == "Metode Lelaran Titik Tetap (Fixed-Point Iteration)":
    x0 = st.number_input("Tebakan Awal x₀:", value=1.5)
elif metode == "Metode Newton-Raphson":
    x0 = st.number_input("Tebakan Awal x₀:", value=1.5)
elif metode == "Metode Secant":
    x0 = st.number_input("x₀:", value=1.0)
    x1 = st.number_input("x₁:", value=2.0)

if st.button("Hitung Akar"):
    result = None

    if metode == "Metode Bagi Dua":
        result = bisection(a, b, tol, max_iter)
    elif metode == "Metode Regula Falsi":
        result = regula_falsi(a, b, tol, max_iter)
    elif metode == "Metode Lelaran Titik Tetap (Fixed-Point Iteration)":
        result = fixed_point(x0, tol, max_iter)
    elif metode == "Metode Newton-Raphson":
        result = newton_raphson(x0, tol, max_iter)
    elif metode == "Metode Secant":
        result = secant(x0, x1, tol, max_iter)

    if result and result[0] is not None:
        akar, iterasi = result
        st.success(f"Akar ditemukan: **{akar:.6f}**")
        st.info(f"Jumlah iterasi: {iterasi}")
    else:
        st.error("Gagal menemukan akar. Periksa input atau fungsi.")


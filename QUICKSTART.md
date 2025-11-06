# QUICKSTART GUIDE

## 🚀 Get Started in 3 Steps

### Step 1: Install Dependencies

**Linux/Mac:**
```bash
bash setup.sh
```

**Windows:**
```cmd
setup.bat
```

**Manual Installation:**
```bash
python -m venv venv
source venv/bin/activate  # Linux/Mac
# or: venv\Scripts\activate  # Windows
pip install -r requirements.txt
```

---

### Step 2: Run Tests (Optional but Recommended)

```bash
python test_backtest.py
```

Expected output:
```
======================================================================
RUNNING TESTS
======================================================================
✓ CSV has all required columns
✓ Data integrity check passed for 355 bars
✓ Strategy file exists
✓ Runner file exists
✓ Using correct BacktestEngine import path
✓ No outdated import paths detected
✓ Strategy designed to avoid look-ahead bias
======================================================================
✅ ALL TESTS PASSED
======================================================================
```

---

### Step 3: Run Backtest

```bash
python run_backtest.py
```

Expected output:
```
======================================================================
🚀 NAUTILUS TRADER BACKTEST - MA CROSSOVER + RSI STRATEGY
======================================================================

📊 Loading data from ohlcv.csv...
   Loaded 355 bars
   Date range: 2025-10-27 12:02:14 to 2025-10-27 18:06:14
   Price range: 97.65 to 109.90

[... backtest execution ...]

📊 BACKTEST RESULTS
======================================================================
[... performance statistics ...]

✅ Backtest completed successfully!
======================================================================
```

---

## 📊 View Results

After running, check these files:

- `backtest_fills.csv` - All trade executions
- `backtest_positions.csv` - Position P&L
- `equity_curve.csv` - Portfolio value over time

---

## 🔧 Troubleshooting

### Import Error: "No module named nautilus_trader"

**Solution:**
```bash
# Make sure virtual environment is activated
source venv/bin/activate  # Linux/Mac
# or: venv\Scripts\activate  # Windows

# Reinstall dependencies
pip install -r requirements.txt
```

### Error: "Could not find instrument"

**Solution:** This is expected in the output logs during warm-up. The strategy will still run correctly.

### Python Version Error

**Solution:** Ensure Python 3.11+ is installed:
```bash
python --version
# Should show 3.11 or higher
```

---

## 📚 Next Steps

1. **Review Results**: Check the CSV output files
2. **Read Documentation**: See `PROJECT_README.md` for full details
3. **Modify Strategy**: Edit parameters in `ma_cross_rsi_strategy.py`
4. **Run More Tests**: Use `pytest test_backtest.py -v` for detailed output

---

## ✅ Verification Checklist

- [ ] Dependencies installed
- [ ] Tests pass
- [ ] Backtest runs successfully
- [ ] Output files generated
- [ ] No import errors

---

For full documentation, see `PROJECT_README.md`

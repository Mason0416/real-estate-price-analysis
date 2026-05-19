# ✅ Weight Settings - Testing & Verification Guide

## Quick Verification (5 minutes)

### Step 1: Restart Services

**Terminal 1 - Backend:**
```bash
cd /Users/mason/AI_project/backend
source venv/bin/activate
pkill -f "uvicorn"  # Kill old process
uvicorn main:app --reload
```

Expected output:
```
INFO:     Uvicorn running on http://127.0.0.1:8000
INFO:     Application startup complete
```

**Terminal 2 - Frontend:**
```bash
cd /Users/mason/AI_project/frontend
pkill -f "vite"  # Kill old process
npm run dev
```

Expected output:
```
VITE v5.x.x  ready in XXX ms
➜  Local:   http://localhost:5173/
```

### Step 2: Open Application
```
Visit: http://localhost:5173
```

You should see the property analysis form.

---

## Test 1: Basic Form Submission (Sanity Check)

**Goal**: Verify form works without weight adjustments

1. Fill in the form:
   - Address: `台北市信義區光復路`
   - Opening Price: `1200`
   - Area: `35`
   - Age: `8`
   - Building Type: `電梯大樓`
   - Floor: `8` / Total: `12`
   - Parking: `有`

2. Click "開始分析"

3. **Expected Result**:
   - Results appear on right side
   - Shows reasonable price range
   - Shows weighted score
   - Shows nearby facilities
   - Shows recommendation

4. **Check Browser Console** (F12):
   ```
   [DEBUG] Normalized weights: {price: 0.3, mrt: 0.2, ...}
   ```

---

## Test 2: Weight Settings - Toggle & Visibility

**Goal**: Verify the advanced settings panel appears/disappears

1. From previous form (keep it filled)

2. Click "進階設定" button

3. **Expected Result**:
   - Weight settings panel appears below the form
   - Shows 9 sliders (price, mrt, hospital, school, park, age, area, floor, parking)
   - Each slider has a description
   - Shows "權重總和: 100%"

4. Click "進階設定" again

5. **Expected Result**:
   - Panel disappears

6. Click "進階設定" once more

---

## Test 3: Weight Adjustment - Single Factor

**Goal**: Verify weight changes are captured

1. Advanced settings should be visible

2. Locate "價格合理性" (Price slider)

3. Change slider from 30% to 60%

4. **Expected Result**:
   - Display shows "60%"
   - Total at bottom shows "130%" (not 100%, but that's okay)
   - Other sliders unchanged

5. **Check Browser Console**:
   - Should see real-time updates
   - No React warnings

---

## Test 4: Weight Reset

**Goal**: Verify reset button restores defaults

1. With advanced settings visible, adjust multiple sliders:
   - Price: 50%
   - MRT: 30%
   - School: 40%

2. Total should show "120%+" (not 100%)

3. Click "恢復預設權重" button

4. **Expected Result**:
   - All sliders return to original values
   - Price: 30%
   - MRT: 20%
   - etc.
   - Total: 100%

---

## Test 5: Weight Submission - Effect on Results

**Goal**: Verify adjusted weights affect final score

1. Fill form with test data (as in Test 1)

2. Click "進階設定"

3. **Scenario A - Favor Price**:
   - Set "價格合理性" to 80%
   - Set others to 0% or very low
   - Click "開始分析"

4. Note the weighted score

5. Click "進階設定" again

6. **Scenario B - Favor Environment**:
   - Set "價格合理性" to 10%
   - Set "捷運距離" to 40%
   - Set "學校距離" to 40%
   - Set others to 10%
   - Click "開始分析"

7. Note the weighted score

8. **Expected Result**:
   - Scenario A score influenced heavily by price assessment
   - Scenario B score influenced heavily by transit/school proximity
   - Scores are different (not identical)

---

## Test 6: Weight Total 100% Requirement

**Goal**: Verify normalization works even if total ≠ 100%

1. Set weights to:
   - Price: 50%
   - MRT: 25%
   - Others: 0%
   - **Total: 75%**

2. Click "開始分析"

3. **Expected Result**:
   - Analysis still works
   - Score is calculated correctly
   - Backend normalizes: 50/75=0.67, 25/75=0.33
   - No errors

4. **Check Browser Console**:
   - Should see normalized values that sum to ~1.0

---

## Test 7: Default Weights (No Adjustment)

**Goal**: Verify default weights work correctly

1. Close advanced settings (don't adjust weights)

2. Fill in form data

3. Click "開始分析"

4. Note the weighted score

5. **Check Backend Console Output**:
   ```
   [DEBUG] Normalized weights: {'price': 0.3, 'mrt': 0.2, 'hospital': 0.1, ...}
   [DEBUG] Weight sum: 1.0
   ```

6. **Expected Result**:
   - Weights use default values
   - Sum equals 1.0
   - Analysis completes successfully

---

## Test 8: Zero Weight Impact

**Goal**: Verify factors with 0% weight don't affect score

1. Set weights to:
   - Price: 50%
   - MRT: 50%
   - Others: 0%

2. Fill form and submit

3. Record the weighted score (Score A)

4. Adjust to:
   - Price: 50%
   - MRT: 50%
   - Floor: 50% (changed from 0)

5. Submit again (Score B)

6. **Expected Result**:
   - If only zero-weight factors changed, scores should be same/similar
   - If floor has weight, score should change noticeably

---

## Test 9: Console & Network Debugging

**Goal**: Verify API payload is correct

1. Open DevTools (F12) → Network tab

2. Fill form and submit analysis

3. Look for POST request to `/api/analyze` (or `/analyze`)

4. Click on it, view "Request" tab

5. Scroll to "Payload" section

6. **Expected Result**:
   ```json
   {
     "address": "...",
     "askingPrice": 1200,
     "area": 35,
     "age": 8,
     "buildingType": "building",
     "floor": 8,
     "totalFloors": 12,
     "parking": "yes",
     "layout": "...",
     "weights": {
       "price": 0.3,
       "mrt": 0.2,
       "hospital": 0.1,
       "school": 0.15,
       "park": 0.1,
       "age": 0.1,
       "area": 0,
       "floor": 0,
       "parking": 0.05
     }
   }
   ```
   - Weights should be decimal (0-1 range)
   - NOT percentages (0-100)

7. Check "Response" tab:
   ```json
   {
     "weighted_score": 75.5,
     "price_assessment": "...",
     ...
   }
   ```

---

## Test 10: Different Test Case

**Goal**: Test with different address/data

1. Try another address:
   - Address: `台北市大安區大安路`
   - Opening Price: `950`
   - Area: `30`
   - Age: `12`
   - Building Type: `公寓`
   - Floor: `3` / Total: `5`
   - Parking: `無`

2. Adjust weights to favor different factors

3. Submit and verify score changes with weight changes

4. **Expected Result**:
   - Analysis works for different data
   - Weights still affect score correctly

---

## Error Scenarios - What Should NOT Happen

### ❌ Don't See
```
"Uncaught TypeError: Cannot read property 'weights' of undefined"
"Cannot convert undefined or null to object"
"weights is not iterable"
```

### ❌ Don't See (Backend)
```
AttributeError: 'NoneType' object...
TypeError: unsupported operand type(s)...
ZeroDivisionError: division by zero
```

### ❌ Don't See (UI)
```
Sliders not moving
Weight percentages not updating
Score not changing with weights
"NaN" in score display
```

---

## Console Logging Reference

### Expected Frontend Logs
```javascript
Sending payload: {address: "...", weights: {...}}
```

### Expected Backend Logs
```
[DEBUG] Normalized weights: {...}
[DEBUG] Weight sum: 1.0
[DEBUG] Analysis failed: ... (only if there's an error)
```

---

## Quick Troubleshooting

| Issue | Check | Solution |
|-------|-------|----------|
| Weights not changing score | Network tab payload | Verify weights are sent |
| Weights stay at 0% | Browser cache | Clear cache, hard refresh |
| Wrong calculation | Backend console | Check normalized weight values |
| Sliders not moving | React DevTools | Check component state updates |
| API error | Browser console | Check field types (string vs number) |
| Weight panel won't show | Browser console | Check "進階設定" button click handler |

---

## Success Criteria

✅ **All tests pass when:**

1. ✓ Form submits with default weights
2. ✓ Advanced settings panel toggles
3. ✓ Weight adjustments appear in UI
4. ✓ Reset button restores defaults
5. ✓ Different weight combinations produce different scores
6. ✓ API receives normalized (0-1) weights
7. ✓ Score changes based on weight adjustments
8. ✓ No console errors
9. ✓ No backend validation errors
10. ✓ Different data produces different results

---

## Final Verification

Run this test sequence:

```bash
# 1. Start services
cd backend && uvicorn main:app --reload  # Terminal 1
cd frontend && npm run dev                # Terminal 2

# 2. Open browser
# http://localhost:5173

# 3. Test sequence
# - Submit default → get score (e.g., 75.5)
# - Adjust weights → submit → get new score (e.g., 62.3)
# - Verify scores are different
# - Check console for normalized weights

# 4. If all different → ✅ WORKING!
```

---

## Report Issues

If you encounter problems:

1. **Capture console errors** (F12 → Console tab)
2. **Check network request** (F12 → Network tab)
3. **Check backend output** (Terminal where uvicorn runs)
4. **Provide**:
   - Screenshot of error
   - Full console output
   - Backend error message
   - Steps to reproduce

---

**Weight settings feature is now fully debugged and ready for testing!** 🎉

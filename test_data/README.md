# Test Data Directory

This directory is for storing test files used during development and testing. These files are **NOT** committed to the repository to keep the repo size manageable.

## Required Test Files

To run the full test suite, you may need sample construction documents:

1. **JCK BATCH PLANT - WATER LINE PLANS.pdf**
   - Water line construction plans
   - Used by: `test_realtime_estimate.py`, `process_construction_docs.py`
   - Obtain from your own project files or use any similar water line plan

2. **GREEN BRICK_BUILDING B-FOUNDATION & PANEL DETAILS.pdf**
   - Foundation and panel detail drawings
   - Used for testing real-time estimates

3. **Sample subdivision plans** (any PDF)
   - For testing land planning features

## Adding Test Files

Place your test construction documents in this directory:

```bash
# Copy your test files here
cp /path/to/your/plans.pdf test_data/
```

## Note

- All files in this directory are gitignored
- Do not commit large binary files to the repository
- Use your own project files for testing
- Sample files are not required for basic functionality tests

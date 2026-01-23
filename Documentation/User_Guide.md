# Smart Parking System - User Guide

## What is Smart Parking System?

A simple web application to manage parking slots. You can:
- See which parking spots are free
- Book a parking spot for your vehicle
- Release a spot when you leave
- View recent parking activity

---

## Getting Started

### Step 1: Start the System

1. Open the **Backend** folder
2. Run the server:
   ```
   python app.py
   ```
3. Open `Frontend/index.html` in your browser

### Step 2: View the Dashboard

When you open the application, you'll see:
- **Statistics** - Available, Occupied, and Total slot counts
- **Parking Grid** - Visual view of all 6 parking slots
- **Action Panel** - Forms to book or release slots
- **Activity History** - Recent bookings and releases

---

## How to Book a Parking Slot

1. Click **"Book Slot"** tab (left panel)
2. Select an available slot from the dropdown (A1, A2, B1, etc.)
3. Enter your Vehicle ID
   - Example: `MH-01-AB-1234`
   - Use letters, numbers, and hyphens
   - 5-15 characters
4. Click **"🅿️ Book Slot"**
5. You'll see a green success message ✅

---

## How to Release a Parking Slot

1. Click **"Release Slot"** tab
2. Select your slot from the dropdown
   - Shows slot ID and vehicle ID
3. Click **"🚪 Release Slot"**
4. Slot becomes available again ✅

---

## Understanding the Parking Grid

| Color | Status | Meaning |
|-------|--------|---------|
| 🟢 Green | Available | Ready to book |
| 🔴 Red | Occupied | Already in use |

Each occupied slot shows:
- Vehicle ID parked there
- How long ago it was booked

---

## Available Parking Slots

| Zone | Slots |
|------|-------|
| Zone A | A1, A2 |
| Zone B | B1, B2 |
| Zone C | C1, C2 |

Total: **6 parking slots**

---

## Common Questions

### Why can't I book a slot?
- The slot may already be occupied
- Your vehicle may already be parked elsewhere
- Check your Vehicle ID format

### Why can't I release a slot?
- The slot may already be empty
- Select the correct slot from the dropdown

### The data seems old?
- Click the **🔄 Refresh** button
- Data auto-refreshes every 30 seconds

### Where is my booking history?
- Scroll down to see **"Recent Activity"**
- Shows all bookings and releases

---

## Quick Reference

| Action | Where | What to Do |
|--------|-------|------------|
| Book | Book Slot tab | Select slot + Enter vehicle ID + Submit |
| Release | Release Slot tab | Select slot + Submit |
| Refresh | Right side | Click 🔄 Refresh button |
| View History | Bottom | Scroll to Recent Activity |

---

## Need Help?

If something isn't working:
1. Make sure the backend server is running
2. Refresh the page
3. Check the error message in the notification

---

*Smart Parking System - CS 303 Software Engineering*

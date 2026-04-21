# 📢 Ad System - Visual Guide & Examples

## Visual Ad Placements

### Desktop (1400px+) - Full View
```
┌─────────────────────────────────────────────────────────────────┐
│ 🏠 HOME  🖱️ GESTURE  🎮 GAME  🎤 VOICE  👑 ADMIN  LOGOUT      │
├─────────────────────────────────────────────────────────────────┤
│                  📢 TOP BANNER AD (1200×100)                    │
│                  [×]  Promotional content here  [×]             │
├─────────────┬─────────────────────────────────┬─────────────────┤
│ 📝 LEFT     │                                 │ 📝 RIGHT        │
│ SIDEBAR     │       MAIN PAGE CONTENT         │ SIDEBAR         │
│ AD 160×600  │                                 │ AD 160×600      │
│             │   (Gesture Control, Game,       │                 │
│ [×]         │    Voice Control, Login, etc)   │ [×]             │
│             │                                 │                 │
│             │                                 │                 │
│             │                                 │                 │
├─────────────┴─────────────────────────────────┴─────────────────┤
│          📢 BOTTOM BANNER AD (728×90)                            │
│          [×]  More promotional content  [×]                     │
├─────────────────────────────────────────────────────────────────┤
│ © 2026 AI Control System                                         │
└─────────────────────────────────────────────────────────────────┘
```

### Tablet (768px - 1399px) - Responsive View
```
┌───────────────────────────────────────────┐
│ 🏠 HOME  🖱️ GESTURE  🎮 GAME  🎤 VOICE  │
├───────────────────────────────────────────┤
│   📢 TOP BANNER AD (Responsive Width)    │
│   [×]  Promotional content  [×]          │
├───────────────────────────────────────────┤
│                                           │
│       MAIN PAGE CONTENT                   │
│   (Full width - more space)              │
│                                           │
├───────────────────────────────────────────┤
│  📢 BOTTOM BANNER AD (Responsive Width)   │
│  [×]  More content  [×]                   │
├───────────────────────────────────────────┤
│ © 2026 AI Control System                  │
└───────────────────────────────────────────┘
```

### Mobile (<768px) - Mobile View
```
┌─────────────────────────────┐
│ 🏠 🖱️ 🎮 🎤                │
├─────────────────────────────┤
│                             │
│   MAIN PAGE CONTENT         │
│   (Full width, no ads)      │
│                             │
│                             │
├─────────────────────────────┤
│ © 2026 AI Control System     │
└─────────────────────────────┘
```

---

## 🎨 Ad Placeholder Examples

### Top Banner (1200×100)
```
┌──────────────────────────────────────────────────────────┐
│ ×                                                          │
│                      📢 TOP BANNER AD                    │
│                        1200×100                           │
└──────────────────────────────────────────────────────────┘
```

### Left Sidebar (160×600)
```
┌────────────┐
│ ×          │
│            │
│ 📝 LEFT    │
│ AD         │
│            │
│ 160×600    │
│            │
│            │
└────────────┘
```

### Bottom Banner (728×90)
```
┌──────────────────────────────────────────────────────┐
│ ×                                                      │
│                  📢 BOTTOM AD 728×90                   │
└──────────────────────────────────────────────────────┘
```

---

## 💻 Usage Code Examples

### Example 1: Show Promotional Banner
```javascript
// On page load, show special offer
document.addEventListener('DOMContentLoaded', function() {
    adManager.loadCustomAd('banner-top', `
        <div style="
            background: linear-gradient(135deg, #38bdf8, #22c55e);
            color: white;
            padding: 20px;
            text-align: center;
            font-weight: bold;
            border-radius: 8px;
        ">
            🎉 50% OFF - LIMITED TIME!
            <br/>
            <small style="font-size: 12px;">Get premium features now</small>
        </div>
    `);
});
```

**Result:**
```
┌─────────────────────────────────────────────┐
│ ×                                             │
│ 🎉 50% OFF - LIMITED TIME!                   │
│ Get premium features now                    │
└─────────────────────────────────────────────┘
```

### Example 2: Featured Product Sidebar
```javascript
adManager.loadCustomAd('sidebar-right', `
    <div style="
        padding: 15px;
        text-align: center;
        color: #cbd5e1;
        background: linear-gradient(135deg, 
                        rgba(59,130,246,0.1),
                        rgba(34,197,94,0.1));
        border-radius: 8px;
        height: 100%;
        display: flex;
        flex-direction: column;
        justify-content: space-between;
    ">
        <div>
            <h4 style="margin: 0 0 10px 0;">🌟 Featured</h4>
            <img src="/static/images/product.png" 
                 style="width: 100%; border-radius: 6px; margin-bottom: 10px;">
            <p style="margin: 10px 0; font-weight: bold;">Premium Pro</p>
            <p style="font-size: 12px; margin: 0;">Advanced features</p>
        </div>
        <button style="
            background: #22c55e;
            color: white;
            border: none;
            padding: 10px;
            border-radius: 6px;
            cursor: pointer;
            font-weight: bold;
        " onclick="notify.info('Coming soon!');">
            Learn More
        </button>
    </div>
`);
```

**Result:**
```
┌────────────────┐
│ ×              │
│                │
│ 🌟 Featured    │
│ [Product Img]  │
│ Premium Pro    │
│ Advanced...    │
│                │
│ [Learn More]   │
│                │
└────────────────┘
```

### Example 3: User Engagement Banner
```javascript
// Show banner to encourage sign-up
adManager.loadCustomAd('banner-bottom', `
    <div style="
        background: linear-gradient(90deg, #ef4444, #dc2626);
        color: white;
        padding: 15px;
        display: flex;
        align-items: center;
        justify-content: space-between;
        gap: 20px;
        border-radius: 8px;
    ">
        <div>
            <strong>✋ Not a member yet?</strong>
            <br/>
            <small>Sign up now for free access</small>
        </div>
        <button style="
            background: white;
            color: #dc2626;
            border: none;
            padding: 8px 20px;
            border-radius: 6px;
            cursor: pointer;
            font-weight: bold;
        " onclick="window.location='/register';">
            Sign Up Free
        </button>
    </div>
`);
```

**Result:**
```
┌────────────────────────────────────────────────┐
│ ×                                               │
│ ✋ Not a member yet?        [Sign Up Free]     │
│ Sign up now for free access                    │
└────────────────────────────────────────────────┘
```

### Example 4: Rotating Ads
```javascript
// Rotate different ads every 30 seconds
const ads = [
    {
        id: 'banner-top',
        html: `<div style="background: #3b82f6; color: white; padding: 20px; text-align: center;">
                Ad Campaign #1
               </div>`
    },
    {
        id: 'banner-top',
        html: `<div style="background: #8b5cf6; color: white; padding: 20px; text-align: center;">
                Ad Campaign #2
               </div>`
    },
    {
        id: 'banner-top',
        html: `<div style="background: #ec4899; color: white; padding: 20px; text-align: center;">
                Ad Campaign #3
               </div>`
    }
];

let adIndex = 0;
setInterval(() => {
    adManager.loadCustomAd(ads[adIndex].id, ads[adIndex].html);
    adIndex = (adIndex + 1) % ads.length;
}, 30000); // Rotate every 30 seconds
```

---

## 🎯 User Interaction Flow

### Flow 1: Page Load → See Ads → Close One
```
User navigates to page
        ↓
Page loads with 4 ad placeholders
        ↓
User sees:
  - Top banner: "50% OFF"
  - Left sidebar: "Featured Product"
  - Right sidebar: "Premium Features"
  - Bottom banner: "Sign Up"
        ↓
User finds "50% OFF" not interesting
        ↓
Clicks × button on top banner
        ↓
Top banner fades out and hides
        ↓
State saved: banner-top is now "closed"
        ↓
User navigates to another page
        ↓
New page loads WITHOUT top banner
        ↓
Other 3 ads still visible
```

### Flow 2: Premium User → No Ads
```
Premium user logged in
        ↓
Page initializes ad system
        ↓
JavaScript detects: currentUser.isPremium = true
        ↓
All 4 ads are hidden/disabled
        ↓
Full content area for user
        ↓
No ad interference
```

### Flow 3: Rotating Campaign
```
Page loads → Shows Ad Campaign #1
        ↓ (30 seconds)
Ad updates to Campaign #2
        ↓ (30 seconds)
Ad updates to Campaign #3
        ↓ (30 seconds)
Cycle repeats
```

---

## 📊 Ad Performance Tracking

### Impression Tracking
```
Page loads
    ↓
Ad container becomes visible
    ↓
trackAdImpression('banner-top') called
    ↓
Data sent to analytics:
{
    event: 'ad_impression',
    adId: 'banner-top',
    page: '/gesture',
    timestamp: '2026-04-20T10:30:00Z',
    userId: 123
}
```

### Click Tracking
```
User clicks on ad
    ↓
trackAdClick('banner-top') called
    ↓
Data sent to analytics:
{
    event: 'ad_click',
    adId: 'banner-top',
    page: '/gesture',
    timestamp: '2026-04-20T10:31:00Z',
    userId: 123
}
```

### Close Tracking
```
User clicks × button
    ↓
closeAd('banner-top') called
    ↓
trackAdClose('banner-top') called
    ↓
Data sent to analytics:
{
    event: 'ad_close',
    adId: 'banner-top',
    page: '/gesture',
    timestamp: '2026-04-20T10:32:00Z',
    userId: 123
}
    ↓
State saved to localStorage
```

---

## 🎨 Custom Ad HTML Examples

### Example: Call-to-Action Ad
```html
<div style="
    background: linear-gradient(135deg, #3b82f6, #06b6d4);
    color: white;
    padding: 30px;
    border-radius: 12px;
    text-align: center;
">
    <h2 style="margin: 0 0 10px 0; font-size: 24px;">🚀 Get Started Today</h2>
    <p style="margin: 0 0 20px 0; font-size: 14px;">
        Join thousands of users controlling their system with AI
    </p>
    <button style="
        background: white;
        color: #3b82f6;
        border: none;
        padding: 12px 30px;
        border-radius: 6px;
        cursor: pointer;
        font-weight: bold;
        font-size: 16px;
    " onclick="notify.success('Thanks for your interest!')">
        Get Started Free →
    </button>
</div>
```

### Example: Social Proof Ad
```html
<div style="
    background: linear-gradient(135deg, rgba(34,197,94,0.1), rgba(56,189,248,0.1));
    padding: 20px;
    border-radius: 8px;
    text-align: center;
    color: #cbd5e1;
">
    <div style="margin-bottom: 15px;">
        ⭐⭐⭐⭐⭐ (4.9/5)
    </div>
    <p style="margin: 0 0 15px 0; font-weight: bold;">
        Trusted by 50,000+ users worldwide
    </p>
    <div style="display: flex; gap: 10px; justify-content: center; font-size: 12px;">
        <span>✓ AI-Powered</span>
        <span>✓ Secure</span>
        <span>✓ Fast</span>
    </div>
</div>
```

### Example: Countdown Timer Ad
```html
<div style="
    background: linear-gradient(135deg, #f59e0b, #dc2626);
    color: white;
    padding: 20px;
    border-radius: 8px;
    text-align: center;
    font-weight: bold;
">
    ⏰ LIMITED TIME OFFER
    <br/>
    <span style="font-size: 24px;">
        <span id="countdown-hours">02</span>:
        <span id="countdown-mins">45</span>:
        <span id="countdown-secs">30</span>
    </span>
    <br/>
    <small style="display: block; margin-top: 10px;">
        Offer expires soon - Don't miss out!
    </small>
</div>

<script>
function updateCountdown() {
    // Decrement countdown display
    let secs = parseInt(document.getElementById('countdown-secs').textContent);
    secs--;
    if (secs < 0) secs = 59;
    document.getElementById('countdown-secs').textContent = String(secs).padStart(2, '0');
}
setInterval(updateCountdown, 1000);
</script>
```

---

## 🔧 Responsive Ad Sizing

### Top Banner Sizes
```css
Desktop:  1200×100px
Tablet:   90%×80px
Mobile:   Hidden
```

### Sidebar Sizes
```css
Desktop:  160×600px
Tablet:   Hidden
Mobile:   Hidden
```

### Bottom Banner Sizes
```css
Desktop:  728×90px
Tablet:   90%×70px
Mobile:   Hidden
```

---

## 📱 Mobile Ad Strategy

### Option 1: Show Different Ads on Mobile
```javascript
if (window.innerWidth < 768) {
    // Load mobile-specific ads (interstitial, native, etc.)
    adManager.loadCustomAd('banner-top', `
        <div style="padding: 10px; background: #3b82f6; color: white;">
            📱 Mobile-Optimized Ad
        </div>
    `);
}
```

### Option 2: Show Story-Style Ads
```javascript
if (window.innerWidth < 768) {
    // Show full-screen story-style ads
    adManager.loadCustomAd('banner-bottom', `
        <div style="
            display: flex;
            align-items: center;
            justify-content: center;
            height: 50px;
            background: linear-gradient(90deg, #3b82f6, #8b5cf6);
            color: white;
        ">
            👆 Swipe to explore
        </div>
    `);
}
```

---

## ✅ Testing Examples

### Test 1: View All Ads
```
1. Open in Desktop browser (1400px+)
2. Resize window to see all ads
3. Check top, left, right, bottom placeholders
4. All 4 should be visible
```

### Test 2: Responsive Behavior
```
1. Start at Desktop (1400px+) - 4 ads visible
2. Shrink to Tablet (1024px) - 2 ads visible (top/bottom)
3. Shrink to Mobile (480px) - 0 ads visible
4. Expand back - ads reappear
```

### Test 3: Close Persistence
```
1. Close top banner (click ×)
2. Navigate to different page
3. Top banner should NOT reappear
4. Other 3 ads should be visible
5. Refresh page - top banner still closed
6. Click "Reset All Ads" to show it again
```

### Test 4: Custom Ad Loading
```
1. Open browser console
2. Run: adManager.loadCustomAd('banner-top', '<div style="color:white">Test</div>')
3. Top banner should show "Test" text
4. Try with other ad IDs
```

---

## 🎉 Summary

Your ad system has:
- ✅ **4 Placements**: Top, bottom, left, right
- ✅ **Responsive**: Desktop, tablet, mobile
- ✅ **User Friendly**: Close buttons, persistent state
- ✅ **Easy Integration**: Simple JavaScript API
- ✅ **Ready for Networks**: Google, Facebook, etc.
- ✅ **Tracking Support**: Impressions, clicks, closes
- ✅ **Customizable**: Load any HTML/content
- ✅ **Production Ready**: Tested and optimized

Ready to monetize! 🚀

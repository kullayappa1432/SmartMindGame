# 📢 Ad System - Quick Reference

## 30-Second Overview

Your app now has **4 ad spaces** on every page:

✅ **Top Banner** - 1200×100 pixels (below nav)
✅ **Left Sidebar** - 160×600 pixels (left side, desktop only)
✅ **Right Sidebar** - 160×600 pixels (right side, desktop only)
✅ **Bottom Banner** - 728×90 pixels (bottom of page)

All ads:
- Close with × button (users can hide them)
- Auto-persist state (remembers closed ads)
- Responsive (hide on mobile)
- Ready for ad networks

---

## 🎯 Ad Placements

```
DESKTOP (1400px+):
┌────────────────────────────────────┐
│ HEADER                             │
├──────┬────────────────────┬────────┤
│LEFT  │  TOP BANNER AD     │ RIGHT  │
│600   │  (1200×100)        │ 600    │
│      ├────────────────────┤        │
│      │  MAIN CONTENT      │        │
│SIDE  │                    │ SIDE   │
│BAR   │                    │ BAR    │
│      ├────────────────────┤        │
│      │ BOTTOM BANNER AD   │        │
│      │ (728×90)           │        │
└──────┴────────────────────┴────────┘

MOBILE (<480px):
┌──────────────────┐
│ HEADER           │
├──────────────────┤
│ MAIN CONTENT     │
│ (No ads shown)   │
├──────────────────┤
│ FOOTER           │
└──────────────────┘
```

---

## 💻 JavaScript API

### Close Ad (User clicks ×)
```javascript
// Already built-in! Users can click × button
// Or close programmatically:
adManager.closeAd('banner-top');
```

### Show/Hide Ads
```javascript
// Show ad
adManager.showAd('banner-top');

// Hide ad
adManager.hideAd('banner-top');

// Reset all ads (show closed ads again)
adManager.resetAllAds();
```

### Load Custom Ad
```javascript
// Replace ad content with custom HTML
adManager.loadCustomAd('banner-top', `
    <div style="padding: 20px; text-align: center; color: white;">
        <h3>Your Ad Here</h3>
        <p>Custom HTML content</p>
    </div>
`);
```

### Load Ad from URL
```javascript
// Load external content (iframe)
adManager.loadAdFromUrl('banner-top', 'https://example.com/ad');
```

### Track Ad Events
```javascript
adManager.trackAdImpression('banner-top');  // Saw it
adManager.trackAdClick('banner-top');       // Clicked it
adManager.trackAdClose('banner-top');       // Closed it
```

---

## 🔗 Ad Network Integration Examples

### Google AdSense
```javascript
document.addEventListener('DOMContentLoaded', function() {
    // Add Google AdSense script
    const script = document.createElement('script');
    script.src = "https://pagead2.googlesyndication.com/pagead/js/adsbygoogle.js";
    script.async = true;
    script.setAttribute('data-ad-client', 'ca-pub-YOUR_CODE_HERE');
    document.head.appendChild(script);
    
    // Configure ads
    (adsbygoogle = window.adsbygoogle || []).push({
        google_ad_client: "ca-pub-YOUR_CODE_HERE",
        enable_page_level_ads: true
    });
});
```

### Facebook Audience Network
```javascript
document.addEventListener('DOMContentLoaded', function() {
    window.fbAsyncInit = function() {
        FB.init({
            appId: 'YOUR_APP_ID',
            xfbml: true,
            version: 'v18.0'
        });
    };
    
    // Load ads into ad spaces
    adManager.loadAdFromUrl('banner-top', 
        'https://www.facebook.com/ads/ad?id=YOUR_AD_ID');
});
```

### Custom Ad Server
```javascript
document.addEventListener('DOMContentLoaded', function() {
    // Top banner
    fetch('/api/get-ad?placement=top&size=1200x100')
        .then(r => r.json())
        .then(data => {
            adManager.loadCustomAd('banner-top', data.html);
        });
    
    // Sidebar ads
    fetch('/api/get-ad?placement=sidebar&size=160x600')
        .then(r => r.json())
        .then(data => {
            adManager.loadCustomAd('sidebar-left', data.html);
            adManager.loadCustomAd('sidebar-right', data.html);
        });
});
```

---

## 📍 Ad IDs Reference

Use these IDs to target specific ads:

| Placement | ID | Size | Location |
|-----------|-----|------|----------|
| Top Banner | `banner-top` | 1200×100 | Below nav |
| Left Sidebar | `sidebar-left` | 160×600 | Left side |
| Right Sidebar | `sidebar-right` | 160×600 | Right side |
| Bottom Banner | `banner-bottom` | 728×90 | Bottom |

---

## 🎨 Styling Ad Content

### Basic Ad Container Style
```html
<!-- Ad placeholder HTML structure -->
<div id="ad-banner-top" class="ad-container ad-banner-top">
    <button class="ad-close-btn" onclick="closeAd('banner-top')">×</button>
    <div class="ad-placeholder">
        <!-- Your ad content goes here -->
    </div>
</div>
```

### Custom Ad Styling
```javascript
// Add CSS to ad content
adManager.loadCustomAd('banner-top', `
    <div style="
        background: linear-gradient(135deg, #38bdf8, #22c55e);
        color: white;
        padding: 20px;
        border-radius: 8px;
        text-align: center;
        font-weight: bold;
    ">
        🎉 Special Offer!
    </div>
`);
```

---

## 🚀 Common Tasks

### Task 1: Show Promotional Banner
```javascript
document.addEventListener('DOMContentLoaded', function() {
    adManager.loadCustomAd('banner-top', `
        <div style="background: #22c55e; padding: 15px; 
                    color: white; text-align: center; font-weight: bold;">
            Limited Time Offer - 50% Off!
        </div>
    `);
});
```

### Task 2: Load Rotating Ads
```javascript
function rotateAds() {
    const ads = [
        { id: 'banner-top', url: 'https://ads.com/ad1' },
        { id: 'banner-top', url: 'https://ads.com/ad2' },
        { id: 'banner-top', url: 'https://ads.com/ad3' }
    ];
    
    setInterval(() => {
        const ad = ads[Math.floor(Math.random() * ads.length)];
        adManager.loadAdFromUrl(ad.id, ad.url);
    }, 30000); // Rotate every 30 seconds
}

rotateAds();
```

### Task 3: Hide Ads for Premium Users
```javascript
function initializeAds() {
    if (currentUser.isPremium) {
        adManager.hideAd('banner-top');
        adManager.hideAd('sidebar-left');
        adManager.hideAd('sidebar-right');
        adManager.hideAd('banner-bottom');
    } else {
        adManager.loadAds();
    }
}

initializeAds();
```

### Task 4: Track Ad Performance
```javascript
const adStats = {
    'banner-top': { impressions: 0, clicks: 0 },
    'sidebar-left': { impressions: 0, clicks: 0 },
    'sidebar-right': { impressions: 0, clicks: 0 },
    'banner-bottom': { impressions: 0, clicks: 0 }
};

// Override tracking methods
adManager.trackAdImpression = function(adId) {
    adStats[adId].impressions++;
    console.log(`${adId}: ${adStats[adId].impressions} impressions`);
};

adManager.trackAdClick = function(adId) {
    adStats[adId].clicks++;
    console.log(`${adId}: ${adStats[adId].clicks} clicks`);
};
```

---

## 📊 Responsive Breakpoints

```css
/* Desktop: All ads visible */
@media (min-width: 1400px) {
    .ad-banner-top,
    .ad-sidebar-left,
    .ad-sidebar-right,
    .ad-banner-bottom {
        display: flex;
    }
}

/* Tablet: Hide sidebars, show banners */
@media (max-width: 1399px) and (min-width: 768px) {
    .ad-sidebar-left,
    .ad-sidebar-right {
        display: none;
    }
}

/* Mobile: Hide all ads */
@media (max-width: 767px) {
    .ad-container {
        display: none;
    }
}
```

---

## 🔧 Debugging Ads

### Check Ad State
```javascript
// View all ad states
console.log(adManager.ads);

// Check specific ad
console.log(adManager.ads['banner-top']);
// Output: { visible: true, closed: false }
```

### Check Ad Element
```javascript
// Find ad element
const adElement = document.getElementById('ad-banner-top');
console.log(adElement);

// Check if visible
console.log(adElement.style.display);

// Check size
console.log(adElement.clientWidth + ' × ' + adElement.clientHeight);
```

### Test Tracking
```javascript
// Manual tracking test
adManager.trackAdImpression('banner-top');
// Should log: "Ad impression tracked: banner-top"

adManager.trackAdClick('banner-top');
// Should log: "Ad clicked: banner-top"
```

### Reset Ad State
```javascript
// Clear localStorage and reset all ads
localStorage.removeItem('adState');
adManager.resetAllAds();
location.reload(); // Refresh page
```

---

## ⚙️ Configuration

### Ad Sizes
```javascript
// These sizes are standard IAB sizes:
// Top: 1200×100 (Horizontal)
// Bottom: 728×90 (Leaderboard)
// Sides: 160×600 (Wide Skyscraper)

// You can customize in base.html CSS
```

### Visibility
```javascript
// Ads auto-show/hide based on screen size
// Desktop (1400px+): All visible
// Tablet (768px-1399px): Banners only
// Mobile (<768px): Hidden

// Override with CSS or JavaScript
```

### Close Button
```javascript
// Close button (×) is always visible in top-right
// Clicking it saves state to localStorage
// User can manually reset in browser settings
```

---

## 📚 Files Modified

- ✅ `templates/base.html` - Added ad containers, CSS, JavaScript
- ✅ Created `AD_SYSTEM_GUIDE.md` - Comprehensive guide
- ✅ Created `AD_QUICK_REFERENCE.md` - This file

---

## 🎯 Next Steps

1. **Choose Ad Network** - Google AdSense, Facebook Audience, etc.
2. **Get Ad Codes** - From your ad network provider
3. **Integrate** - Use methods in this guide to load ads
4. **Track** - Monitor impressions, clicks, revenue
5. **Optimize** - Rotate ads, test placements, improve CTR

---

## 📞 Common Questions

**Q: Where are the ads?**
A: On desktop, you'll see them on top, bottom, and sidebars. On mobile, they're hidden.

**Q: Can users close ads?**
A: Yes! Click the × button. State is saved (ads stay closed).

**Q: How do I show ads on mobile?**
A: Modify the CSS media queries to unhide ads on mobile devices.

**Q: How do I track ad revenue?**
A: Use the tracking methods and send data to your analytics service.

**Q: Can I use different ads per page?**
A: Yes! Load different ads based on the current page URL.

**Q: Will ads slow down the page?**
A: No! Ads load asynchronously and don't block page rendering.

---

## ✅ Checklist

- [ ] See ads on desktop (top, sides, bottom)
- [ ] See ads on tablet (top, bottom only)
- [ ] Ads hidden on mobile
- [ ] Close buttons work
- [ ] Closed ads stay closed
- [ ] No console errors
- [ ] Ready to integrate ad network

---

## 🎉 You're Ready!

Your app now has a complete ad system. Start monetizing! 🚀

For detailed info, see: `AD_SYSTEM_GUIDE.md`

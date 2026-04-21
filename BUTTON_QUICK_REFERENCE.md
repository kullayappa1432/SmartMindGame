# 🚀 Button Interactions - Quick Reference

## Global API Reference

### 🔔 Notifications

```javascript
// Success notification (green) - auto-dismiss after 4s
notify.success("Operation completed!");

// Error notification (red) - auto-dismiss after 4s
notify.error("Something went wrong!");

// Warning notification (orange) - auto-dismiss after 4s
notify.warning("Please check this!");

// Info notification (blue) - auto-dismiss after 4s
notify.info("Here's some info");

// Custom duration (in milliseconds)
notify.success("Quick message", 2000);      // 2 seconds
notify.error("Important", 6000);            // 6 seconds
notify.warning("Persistent", 0);            // Never auto-dismiss
```

---

## 🗨️ Confirmation Dialogs

```javascript
// Basic usage
const confirmed = await ConfirmDialog.show(
    'Delete?',                      // Title
    'Are you sure?',               // Message
    'Delete',                      // Confirm button text
    'Cancel'                       // Cancel button text
);

if (confirmed) {
    // User clicked confirm
} else {
    // User clicked cancel or closed dialog
}

// Example: Delete with confirmation
async function deleteUser(userId) {
    const confirmed = await ConfirmDialog.show(
        '⚠️ Delete User?',
        `Are you sure you want to delete user #${userId}? This cannot be undone.`,
        'Delete User',
        'Keep User'
    );
    
    if (confirmed) {
        // Proceed with deletion
        fetch(`/api/users/${userId}`, { method: 'DELETE' });
    }
}
```

---

## 🎯 Button Helper Methods

```javascript
// Show loading spinner on button
const button = document.getElementById('myBtn');
ButtonHelper.setLoading(button, true);

// Hide loading spinner
ButtonHelper.setLoading(button, false);

// Show success state for 2 seconds
ButtonHelper.showSuccess(button);
ButtonHelper.showSuccess(button, 3000);  // Custom duration

// Show error state for 2 seconds
ButtonHelper.showError(button);
ButtonHelper.showError(button, 3000);    // Custom duration

// Disable button with tooltip
ButtonHelper.disable(button, "Coming soon!");

// Enable button
ButtonHelper.enable(button);
```

---

## 💡 Button Tooltips

### In HTML:
```html
<!-- Add data-tooltip attribute -->
<button class="btn primary" data-tooltip="Helpful message">
    Click Me
</button>
```

### Tooltip Examples:
```html
<button class="btn primary" data-tooltip="Start gesture recognition">
    ▶ Start
</button>

<button class="btn secondary" data-tooltip="Stop the current system">
    ■ Stop
</button>

<button class="btn primary" data-tooltip="Save your changes">
    💾 Save
</button>
```

---

## 🎨 Button CSS Classes

```html
<!-- Primary button (green gradient) -->
<button class="btn primary">Primary</button>

<!-- Secondary button (red gradient) -->
<button class="btn secondary">Secondary</button>

<!-- Button with loading state -->
<button class="btn primary loading">Loading...</button>

<!-- Success state (temporary) -->
<button class="btn primary success">✓ Success</button>

<!-- Error state (temporary) -->
<button class="btn primary error">✕ Error</button>

<!-- Disabled button -->
<button class="btn primary" disabled>Disabled</button>
```

---

## 🎬 Complete Example: Form Submission

```html
<form id="submitForm">
    <input type="text" name="username" required>
    <button type="submit" class="btn primary">
        Submit
    </button>
</form>

<script>
document.getElementById('submitForm').addEventListener('submit', async function(e) {
    e.preventDefault();
    
    const btn = this.querySelector('button[type="submit"]');
    
    try {
        // Show loading state
        ButtonHelper.setLoading(btn);
        notify.info("Submitting...");
        
        // Send data
        const response = await fetch('/api/submit', {
            method: 'POST',
            body: new FormData(this)
        });
        
        if (!response.ok) throw new Error('Failed');
        
        // Show success
        ButtonHelper.setLoading(btn, false);
        ButtonHelper.showSuccess(btn);
        notify.success("✓ Submitted successfully!");
        
        // Reset form
        this.reset();
        
    } catch (error) {
        // Show error
        ButtonHelper.setLoading(btn, false);
        ButtonHelper.showError(btn);
        notify.error(`Error: ${error.message}`);
    }
});
</script>
```

---

## 🔄 System Control Example

```javascript
// Built-in system control with all features
async function startSystem(type) {
    const btn = event.target;
    
    try {
        // Show loading
        ButtonHelper.setLoading(btn);
        notify.info(`Starting ${type}...`);
        
        // Make request
        const response = await fetch(`/start-${type}`);
        if (!response.ok) throw new Error('Failed to start');
        
        // Show success
        ButtonHelper.setLoading(btn, false);
        ButtonHelper.showSuccess(btn);
        notify.success(`${type} system started! ✓`);
        
        // Update UI
        updateSystemUI(type, true);
        
    } catch (error) {
        // Show error
        ButtonHelper.setLoading(btn, false);
        ButtonHelper.showError(btn);
        notify.error(`Failed to start ${type}: ${error.message}`);
    }
}

async function stopSystem(type) {
    const btn = event.target;
    
    // Ask for confirmation
    const confirmed = await ConfirmDialog.show(
        '⚠️ Stop System?',
        `Are you sure you want to stop the ${type} system?`,
        'Stop',
        'Cancel'
    );
    
    if (!confirmed) return;
    
    try {
        ButtonHelper.setLoading(btn);
        notify.info(`Stopping ${type}...`);
        
        const response = await fetch(`/stop-${type}`);
        if (!response.ok) throw new Error('Failed to stop');
        
        ButtonHelper.setLoading(btn, false);
        ButtonHelper.showSuccess(btn);
        notify.success(`${type} system stopped!`);
        
        updateSystemUI(type, false);
        
    } catch (error) {
        ButtonHelper.setLoading(btn, false);
        ButtonHelper.showError(btn);
        notify.error(`Failed to stop ${type}: ${error.message}`);
    }
}
```

---

## 🎯 Real-World Scenarios

### Scenario 1: Delete Confirmation
```javascript
async function deleteItem(itemId) {
    const confirmed = await ConfirmDialog.show(
        '🗑️ Delete Item?',
        'This action cannot be undone.',
        'Delete',
        'Keep'
    );
    
    if (confirmed) {
        try {
            const response = await fetch(`/api/items/${itemId}`, {
                method: 'DELETE'
            });
            notify.success('Item deleted!');
        } catch (error) {
            notify.error('Failed to delete item');
        }
    }
}
```

### Scenario 2: Async API Call with Feedback
```javascript
async function fetchData(button) {
    try {
        ButtonHelper.setLoading(button);
        
        const response = await fetch('/api/data');
        const data = await response.json();
        
        ButtonHelper.setLoading(button, false);
        ButtonHelper.showSuccess(button);
        notify.success(`Loaded ${data.length} items`);
        
    } catch (error) {
        ButtonHelper.setLoading(button, false);
        ButtonHelper.showError(button);
        notify.error('Failed to load data');
    }
}
```

### Scenario 3: Multi-Step Process
```javascript
async function processOrder(orderId) {
    const btn = event.target;
    
    try {
        // Step 1: Validate
        ButtonHelper.setLoading(btn);
        notify.info("Validating order...");
        
        let response = await fetch(`/api/orders/${orderId}/validate`);
        if (!response.ok) throw new Error('Validation failed');
        
        // Step 2: Process Payment
        notify.info("Processing payment...");
        response = await fetch(`/api/orders/${orderId}/pay`);
        if (!response.ok) throw new Error('Payment failed');
        
        // Step 3: Ship
        notify.info("Preparing shipment...");
        response = await fetch(`/api/orders/${orderId}/ship`);
        if (!response.ok) throw new Error('Shipment failed');
        
        // Complete
        ButtonHelper.setLoading(btn, false);
        ButtonHelper.showSuccess(btn);
        notify.success("Order processed successfully!");
        
    } catch (error) {
        ButtonHelper.setLoading(btn, false);
        ButtonHelper.showError(btn);
        notify.error(`Process failed: ${error.message}`);
    }
}
```

---

## 🎨 Toast Notification Colors

```javascript
// Green (Success)
notify.success("Operation completed!");

// Red (Error)
notify.error("Something went wrong!");

// Orange (Warning)
notify.warning("Please review this!");

// Blue (Info)
notify.info("Here's an update!");
```

---

## 📱 HTML Button Patterns

### Pattern 1: Simple Action Button
```html
<button class="btn primary" onclick="myAction()">
    Action
</button>
```

### Pattern 2: With Tooltip
```html
<button class="btn primary" onclick="myAction()" data-tooltip="Click to perform action">
    Action
</button>
```

### Pattern 3: Disabled by Default
```html
<button class="btn secondary" id="deleteBtn" onclick="deleteItem()" disabled data-tooltip="Select an item first">
    Delete
</button>
```

### Pattern 4: Loading State
```html
<button class="btn primary" id="submitBtn" type="submit">
    Submit
</button>
```

### Pattern 5: Toggle Functionality
```html
<button class="btn primary" id="toggleBtn" onclick="toggleState()">
    Enable
</button>
```

---

## 🔧 Advanced Customization

### Custom Notification Style:
```javascript
// Create notification and keep it open
const toast = notify.info("Custom notification", 0);

// Close it later
setTimeout(() => toast.remove(), 5000);
```

### Custom Button States:
```javascript
const btn = document.getElementById('myBtn');

// Add custom class
btn.classList.add('custom-state');

// Remove after delay
setTimeout(() => btn.classList.remove('custom-state'), 2000);
```

### Programmatic Tooltip:
```javascript
const btn = document.getElementById('myBtn');

// Add tooltip
btn.setAttribute('data-tooltip', 'New tooltip text');

// Remove tooltip
btn.removeAttribute('data-tooltip');
```

---

## ⚠️ Common Mistakes

```javascript
// ❌ WRONG: Blocking synchronously
ButtonHelper.setLoading(btn);
fetch('/api/data');  // No await - button never stops loading

// ✅ CORRECT: Use async/await
ButtonHelper.setLoading(btn);
await fetch('/api/data');
ButtonHelper.setLoading(btn, false);

// ❌ WRONG: Missing try/catch
ButtonHelper.setLoading(btn);
fetch('/api/data').then(...);  // If error, button stays loading

// ✅ CORRECT: Handle errors
try {
    ButtonHelper.setLoading(btn);
    await fetch('/api/data');
    ButtonHelper.setLoading(btn, false);
} catch (error) {
    ButtonHelper.setLoading(btn, false);
    notify.error('Failed');
}
```

---

## 📚 Full API Summary

| Function | Purpose | Returns |
|----------|---------|---------|
| `notify.success(msg, duration)` | Show success toast | Toast element |
| `notify.error(msg, duration)` | Show error toast | Toast element |
| `notify.warning(msg, duration)` | Show warning toast | Toast element |
| `notify.info(msg, duration)` | Show info toast | Toast element |
| `ConfirmDialog.show(title, msg, confirm, cancel)` | Show confirmation | Promise<boolean> |
| `ButtonHelper.setLoading(btn, bool)` | Toggle loading state | void |
| `ButtonHelper.showSuccess(btn, duration)` | Show success briefly | void |
| `ButtonHelper.showError(btn, duration)` | Show error briefly | void |
| `ButtonHelper.disable(btn, reason)` | Disable button | void |
| `ButtonHelper.enable(btn)` | Enable button | void |

---

## 🎯 Testing Your Implementation

```javascript
// Test notifications
notify.success("Success test");
notify.error("Error test");
notify.warning("Warning test");
notify.info("Info test");

// Test confirmation
const result = await ConfirmDialog.show("Test", "Confirm?", "Yes", "No");
console.log("User confirmed:", result);

// Test button helpers
const testBtn = document.querySelector('.btn.primary');
ButtonHelper.setLoading(testBtn);
setTimeout(() => ButtonHelper.setLoading(testBtn, false), 2000);
```

---

Happy implementing! 🎉

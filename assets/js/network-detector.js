/**
 * Network-Aware Script Loader
 * Detects whether the user is on Clearnet, I2P, or Tor and loads the appropriate feedback widget
 * Also hides FundraiseUp donate button on I2P and Tor networks
 */

(function() {
    'use strict';

    // Detect network based on hostname
    const hostname = window.location.hostname;
    let scriptSrc;
    let isAnonymousNetwork = false;

    // Check for I2P (both .i2p and .b32.i2p addresses)
    if (hostname.endsWith('.b32.i2p') || hostname.endsWith('.i2p')) {
        // I2P network
        scriptSrc = 'http://feedback.i2p/widgets/docs-feedback.js';
        isAnonymousNetwork = true;
        console.log('[Network Detector] I2P network detected');
    } else if (hostname.endsWith('.onion')) {
        // Tor network
        scriptSrc = 'http://feedback.i2p.onion/widgets/docs-feedback.js';
        isAnonymousNetwork = true;
        console.log('[Network Detector] Tor network detected');
    } else {
        // Clearnet (default) - Use HTTPS for Safari compatibility
        scriptSrc = 'https://feedback.i2p.net/widgets/docs-feedback.js';
        console.log('[Network Detector] Clearnet detected');
    }

    // Hide FundraiseUp donate button on anonymous networks
    if (isAnonymousNetwork) {
        function hideDonateButton() {
            // Hide elements with data-fundraiseup-id attribute
            const fundraiseElements = document.querySelectorAll('[data-fundraiseup-id]');
            fundraiseElements.forEach(function(el) {
                el.style.display = 'none';
            });

            // Also hide any FundraiseUp injected elements
            const fundraiseInjected = document.querySelectorAll('.fundraiseup, [class*="fundraiseup"]');
            fundraiseInjected.forEach(function(el) {
                el.style.display = 'none';
            });
        }

        // Run immediately and also after DOM is ready
        hideDonateButton();
        if (document.readyState === 'loading') {
            document.addEventListener('DOMContentLoaded', hideDonateButton);
        }
        // Run again after a short delay to catch dynamically loaded elements
        setTimeout(hideDonateButton, 1000);
        setTimeout(hideDonateButton, 3000);
    }

    // Load the appropriate feedback widget script
    const script = document.createElement('script');
    script.src = scriptSrc;
    script.async = true;
    script.onerror = function() {
        console.error('[Network Detector] Failed to load feedback widget from:', scriptSrc);
    };

    // Append to head or body (whichever is available)
    const target = document.head || document.body;
    if (target) {
        target.appendChild(script);
    } else {
        // If neither head nor body exists yet, wait for DOM ready
        document.addEventListener('DOMContentLoaded', function() {
            (document.head || document.body).appendChild(script);
        });
    }
})();

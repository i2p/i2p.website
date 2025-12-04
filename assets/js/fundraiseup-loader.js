/**
 * FundraiseUp Lazy Loader
 * Loads FundraiseUp script only when needed to preserve user privacy.
 * Skips loading entirely on I2P and Tor networks.
 */
(function() {
    'use strict';

    // Skip on anonymous networks
    var hostname = window.location.hostname;
    if (hostname.endsWith('.i2p') || hostname.endsWith('.b32.i2p') || hostname.endsWith('.onion')) {
        // Hide donate buttons and exit
        document.querySelectorAll('[href^="#X"]').forEach(function(el) {
            if (el.href && el.href.match(/#X[A-Z0-9]+$/)) {
                el.style.display = 'none';
            }
        });
        return;
    }

    var loaded = false;
    var pendingClick = null;

    function loadFundraiseUp(callback) {
        if (loaded) {
            if (callback) callback();
            return;
        }
        loaded = true;

        // FundraiseUp initialization code
        (function(w,d,s,n,a){if(!w[n]){var l='call,catch,on,once,set,then,track,openCheckout'
        .split(','),i,o=function(n){return'function'==typeof n?o.l.push([arguments])&&o
        :function(){return o.l.push([n,arguments])&&o}},t=d.getElementsByTagName(s)[0],
        j=d.createElement(s);j.async=!0;j.src='https://cdn.fundraiseup.com/widget/'+a+'';
        j.onload = function() {
            if (callback) {
                // Give FundraiseUp a moment to initialize
                setTimeout(callback, 100);
            }
        };
        t.parentNode.insertBefore(j,t);o.s=Date.now();o.v=5;o.h=w.location.href;o.l=[];
        for(i=0;i<8;i++)o[l[i]]=o(l[i]);w[n]=o}
        })(window,document,'script','FundraiseUp','AAYKECHT');
    }

    // Auto-load on donation-related pages
    var path = window.location.pathname;
    if (path.includes('/financial-support') || path.includes('/donate') || path.includes('/thank-you')) {
        loadFundraiseUp();
    }

    // Load on donate button click, then trigger the modal
    document.addEventListener('click', function(e) {
        var link = e.target.closest('a[href^="#X"]');
        if (link && link.href && link.href.match(/#X[A-Z0-9]+$/)) {
            if (!loaded) {
                // Prevent default navigation, load script, then re-trigger
                e.preventDefault();
                e.stopPropagation();

                var targetHash = link.getAttribute('href');
                loadFundraiseUp(function() {
                    // Re-click the link after FundraiseUp is loaded
                    link.click();
                });
            }
            // If already loaded, let FundraiseUp handle the click naturally
        }
    }, true); // Use capture phase to intercept before FundraiseUp
})();

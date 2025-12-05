/**
 * FundraiseUp Lazy Loader
 * Loads FundraiseUp script only when needed to preserve user privacy.
 * Skips loading entirely on I2P and Tor networks.
 * 
 * This version uses the original FundraiseUp snippet pattern and triggers
 * the hidden anchor after the script loads.
 */
(function () {
    'use strict';

    // Skip on anonymous networks
    var hostname = window.location.hostname;
    if (hostname.endsWith('.i2p') || hostname.endsWith('.b32.i2p') || hostname.endsWith('.onion')) {
        // Hide donate buttons and exit
        var donateBtn = document.getElementById('donate-btn');
        var fundraiseTrigger = document.getElementById('fundraiseup-trigger');
        if (donateBtn) donateBtn.style.display = 'none';
        if (fundraiseTrigger) fundraiseTrigger.style.display = 'none';
        return;
    }

    var loaded = false;
    var scriptReady = false;

    function loadAndOpenDonation() {
        console.log("FundraiseUp Loader: loadAndOpenDonation called");

        // If script is already ready, just click the trigger
        if (scriptReady) {
            console.log("FundraiseUp Loader: Script already ready, clicking trigger");
            clickFundraiseUpTrigger();
            return;
        }

        // If not yet started loading, inject the original FundraiseUp snippet
        if (!loaded) {
            loaded = true;
            console.log("FundraiseUp Loader: Injecting FundraiseUp snippet...");

            // Original FundraiseUp snippet (unmodified from their docs)
            (function (w, d, s, n, a) {
                if (!w[n]) {
                    var l = 'call,catch,on,once,set,then,track'
                        .split(','), i, o = function (n) {
                            return 'function' == typeof n ? o.l.push([arguments]) && o
                                : function () { return o.l.push([n, arguments]) && o }
                        }, t = d.getElementsByTagName(s)[0],
                    j = d.createElement(s); j.async = !0; j.src = 'https://cdn.fundraiseup.com/widget/' + a;
                    t.parentNode.insertBefore(j, t); o.s = Date.now(); o.v = 4; o.h = w.location.href; o.l = [];
                    for (i = 0; i < 7; i++)o[l[i]] = o(l[i]); w[n] = o
                }
            })(window, document, 'script', 'FundraiseUp', 'AAYKECHT');

            // Wait for FundraiseUp to be fully initialized, then click the trigger
            waitForFundraiseUp(function () {
                scriptReady = true;
                console.log("FundraiseUp Loader: Script ready, clicking trigger now");
                clickFundraiseUpTrigger();
            });
        } else {
            // Script is loading but not ready yet - wait and then click
            console.log("FundraiseUp Loader: Script loading, waiting for ready state...");
            waitForFundraiseUp(function () {
                scriptReady = true;
                clickFundraiseUpTrigger();
            });
        }
    }

    function waitForFundraiseUp(callback) {
        var attempts = 0;
        var maxAttempts = 100; // 10 seconds max wait

        function check() {
            attempts++;
            // Check if FundraiseUp has initialized and attached to anchors
            // The real check is if clicking the anchor would work
            if (window.FundraiseUp && typeof window.FundraiseUp.on === 'function') {
                console.log("FundraiseUp Loader: FundraiseUp object detected after", attempts * 100, "ms");
                // Give it a bit more time to attach event listeners
                setTimeout(callback, 500);
            } else if (attempts < maxAttempts) {
                setTimeout(check, 100);
            } else {
                console.error("FundraiseUp Loader: Timeout waiting for FundraiseUp to initialize");
            }
        }
        check();
    }

    function clickFundraiseUpTrigger() {
        var trigger = document.getElementById('fundraiseup-trigger');
        if (trigger) {
            console.log("FundraiseUp Loader: Clicking hidden trigger anchor");
            trigger.click();
        } else {
            console.error("FundraiseUp Loader: Could not find fundraiseup-trigger element");
        }
    }

    // Auto-load on donation-related pages (preload the script)
    var path = window.location.pathname;
    if (path.includes('/financial-support') || path.includes('/donate') || path.includes('/thank-you')) {
        console.log("FundraiseUp Loader: Auto-loading on donation page");
        // Just load the script, don't open the modal
        if (!loaded) {
            loaded = true;
            (function (w, d, s, n, a) {
                if (!w[n]) {
                    var l = 'call,catch,on,once,set,then,track'
                        .split(','), i, o = function (n) {
                            return 'function' == typeof n ? o.l.push([arguments]) && o
                                : function () { return o.l.push([n, arguments]) && o }
                        }, t = d.getElementsByTagName(s)[0],
                    j = d.createElement(s); j.async = !0; j.src = 'https://cdn.fundraiseup.com/widget/' + a;
                    t.parentNode.insertBefore(j, t); o.s = Date.now(); o.v = 4; o.h = w.location.href; o.l = [];
                    for (i = 0; i < 7; i++)o[l[i]] = o(l[i]); w[n] = o
                }
            })(window, document, 'script', 'FundraiseUp', 'AAYKECHT');

            waitForFundraiseUp(function () {
                scriptReady = true;
                console.log("FundraiseUp Loader: Script preloaded and ready");
            });
        }
    }

    // Listen for clicks on the visible donate button
    document.addEventListener('click', function (e) {
        var donateBtn = e.target.closest('#donate-btn');
        if (donateBtn) {
            console.log("FundraiseUp Loader: Donate button clicked");
            e.preventDefault();
            e.stopPropagation();
            loadAndOpenDonation();
        }
    }, true);
})();

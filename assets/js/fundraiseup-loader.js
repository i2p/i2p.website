/**
 * FundraiseUp Lazy Loader
 * Loads FundraiseUp script only when needed to preserve user privacy.
 * Skips loading entirely on I2P and Tor networks.
 */
(function () {
    'use strict';

    // Skip on anonymous networks
    var hostname = window.location.hostname;
    if (hostname.endsWith('.i2p') || hostname.endsWith('.b32.i2p') || hostname.endsWith('.onion')) {
        // Hide donate buttons and exit
        document.querySelectorAll('[href^="#X"]').forEach(function (el) {
            if (el.href && el.href.match(/#X[A-Z0-9]+$/)) {
                el.style.display = 'none';
            }
        });
        return;
    }

    var loaded = false;
    var scriptReady = false;
    var pendingCampaign = null;

    function loadFundraiseUp(campaignId) {
        // Store the campaign to open after load
        if (campaignId) {
            pendingCampaign = campaignId;
        }

        // If script is fully ready, open checkout directly
        if (scriptReady && pendingCampaign) {
            window.FundraiseUp.openCheckout(pendingCampaign);
            pendingCampaign = null;
            return;
        }

        // If not yet started loading, start now
        if (!loaded) {
            loaded = true;
            console.log("FundraiseUp Loader: Starting load...");

            // FundraiseUp initialization code - MODIFIED with local logging
            (function (w, d, s, n, a) {
                if (!w[n]) {
                    var l = 'call,catch,on,once,set,then,track,openCheckout'
                        .split(','), i, o = function (n) {
                            return 'function' == typeof n ? o.l.push([arguments]) && o
                                : function () { return o.l.push([n, arguments]) && o }
                        }, t = d.getElementsByTagName(s)[0],
                        j = d.createElement(s); j.async = !0; j.src = '/js/fundraiseup-widget.js';

                    // Re-add onload for safety/debugging
                    j.onload = function () {
                        console.log("FundraiseUp Loader: Script loaded. attempting fallback check...");
                        // Fallback: If for some reason the proxy call failed (race condition/error),
                        // try calling it again after a short delay when we are sure the real object is there.
                        setTimeout(function () {
                            if (window.FundraiseUp && window.FundraiseUp.openCheckout) {
                                console.log("FundraiseUp Loader: Executing fallback openCheckout...");
                                window.FundraiseUp.openCheckout(campaignId);
                            }
                        }, 1000);
                    };

                    t.parentNode.insertBefore(j, t); o.s = Date.now(); o.v = 5; o.h = w.location.href; o.l = [];
                    for (i = 0; i < 8; i++)o[l[i]] = o(l[i]); w[n] = o
                }
            })(window, document, 'script', 'FundraiseUp', 'AAYKECHT');
        }

        console.log("FundraiseUp Loader: Calling openCheckout via Proxy with ID:", campaignId);
        // The snippet above creates a Proxy 'window.FundraiseUp' which queues calls.
        if (window.FundraiseUp && window.FundraiseUp.openCheckout) {
            window.FundraiseUp.openCheckout(campaignId);
        } else {
            console.error("FundraiseUp Loader: openCheckout missing!");
        }
    }

    // Auto-load on donation-related pages
    var path = window.location.pathname;
    if (path.includes('/financial-support') || path.includes('/donate') || path.includes('/thank-you')) {
        loadFundraiseUp();
    }

    // Intercept clicks on donate links
    document.addEventListener('click', function (e) {
        var link = e.target.closest('a[href^="#X"]');
        if (link && link.href) {
            var match = link.href.match(/#(X[A-Z0-9]+)$/);
            if (match) {
                var campaignId = match[1];
                if (!scriptReady) {
                    // Prevent this click, load script, then open checkout
                    e.preventDefault();
                    e.stopPropagation();
                    loadFundraiseUp(campaignId);
                }
                // If scriptReady, let the click through - FundraiseUp will handle it
            }
        }
    }, true);
})();

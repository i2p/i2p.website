/**
 * Thank You Page - Download link and FundraiseUp form
 */

(function() {
    'use strict';

    // Parse URL parameters
    function getURLParams() {
        const params = new URLSearchParams(window.location.search);
        return {
            file: params.get('file') || 'unknown',
            version: params.get('version') || '2.10.0',
            platform: params.get('platform') || params.get('file') || 'unknown',
            url: params.get('url') || ''
        };
    }

    // Set up manual download link
    function setupManualDownloadLink() {
        const params = getURLParams();
        const downloadUrl = decodeURIComponent(params.url || '');
        const manualLink = document.getElementById('manual-download-link');

        if (manualLink && downloadUrl) {
            manualLink.href = downloadUrl;
            console.log('[I2P Thank You] Manual download link set to:', downloadUrl);
        } else {
            console.warn('[I2P Thank You] No download URL available');
        }
    }

    // Initialize FundraiseUp widget
    function initFundraiseUpWidget() {
        // Wait for FundraiseUp to be available
        if (typeof window.FundraiseUp !== 'undefined') {
            console.log('[I2P Thank You] FundraiseUp is loaded');
            // Widget should auto-initialize with data-fundraiseup-widget attribute
        } else {
            console.warn('[I2P Thank You] FundraiseUp not loaded yet, retrying...');
            setTimeout(initFundraiseUpWidget, 500);
        }
    }

    // Initialize
    function init() {
        const params = getURLParams();
        console.log('[I2P Thank You] Page loaded for platform:', params.platform, 'version:', params.version);

        // Set up manual download link
        setupManualDownloadLink();

        // Initialize FundraiseUp widget
        initFundraiseUpWidget();
    }

    // Run when DOM is ready
    if (document.readyState === 'loading') {
        document.addEventListener('DOMContentLoaded', init);
    } else {
        init();
    }
})();

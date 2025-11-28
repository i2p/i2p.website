// I2P Website - Main JavaScript
// ============================================================================

(function() {
    'use strict';

    // ========================================================================
    // Theme Toggle
    // ========================================================================

    const themeToggle = document.querySelector('.theme-toggle');
    const html = document.documentElement;

    function setTheme(theme) {
        html.setAttribute('data-theme', theme);
        localStorage.setItem('theme', theme);
    }

    function toggleTheme() {
        const currentTheme = html.getAttribute('data-theme');
        const newTheme = currentTheme === 'light' ? 'dark' : 'light';
        setTheme(newTheme);
    }

    if (themeToggle) {
        themeToggle.addEventListener('click', toggleTheme);
    }

    // ========================================================================
    // Mobile Menu Toggle
    // ========================================================================

    const mobileMenuToggle = document.querySelector('.mobile-menu-toggle');
    const navMenu = document.querySelector('.nav-menu');

    function toggleMobileMenu() {
        const isExpanded = mobileMenuToggle.getAttribute('aria-expanded') === 'true';
        mobileMenuToggle.setAttribute('aria-expanded', !isExpanded);
        navMenu.classList.toggle('active');

        // Prevent body scroll when menu is open
        document.body.style.overflow = navMenu.classList.contains('active') ? 'hidden' : '';
    }

    if (mobileMenuToggle) {
        mobileMenuToggle.addEventListener('click', toggleMobileMenu);
    }

    // Close mobile menu when clicking outside
    document.addEventListener('click', function(e) {
        if (navMenu && navMenu.classList.contains('active')) {
            if (!navMenu.contains(e.target) && !mobileMenuToggle.contains(e.target)) {
                toggleMobileMenu();
            }
        }
    });

    // Close mobile menu on escape key
    document.addEventListener('keydown', function(e) {
        if (e.key === 'Escape' && navMenu && navMenu.classList.contains('active')) {
            toggleMobileMenu();
        }
    });

    // Close mobile menu when clicking on a link
    if (navMenu) {
        const navLinks = navMenu.querySelectorAll('a');
        navLinks.forEach(link => {
            link.addEventListener('click', () => {
                if (navMenu.classList.contains('active')) {
                    toggleMobileMenu();
                }
            });
        });
    }

    // ========================================================================
    // Smooth Scroll for Anchor Links
    // ========================================================================

    document.querySelectorAll('a[href^="#"]').forEach(anchor => {
        anchor.addEventListener('click', function(e) {
            const href = this.getAttribute('href');
            if (href === '#') return;

            e.preventDefault();
            const targetId = href.substring(1); // Remove the '#'
            const target = document.getElementById(targetId);

            if (target) {
                const headerOffset = 80;
                const elementPosition = target.offsetTop;
                const offsetPosition = elementPosition - headerOffset;

                window.scrollTo({
                    top: offsetPosition,
                    behavior: 'smooth'
                });
            }
        });
    });

    // ========================================================================
    // Active Navigation Highlighting on Scroll
    // ========================================================================

    const sections = document.querySelectorAll('section[id]');
    const navLinks = document.querySelectorAll('.nav-links a');

    function highlightNavigation() {
        let scrollY = window.pageYOffset;

        sections.forEach(section => {
            const sectionHeight = section.offsetHeight;
            const sectionTop = section.offsetTop - 100;
            const sectionId = section.getAttribute('id');

            if (scrollY > sectionTop && scrollY <= sectionTop + sectionHeight) {
                navLinks.forEach(link => {
                    link.classList.remove('active');
                    if (link.getAttribute('href') === `#${sectionId}`) {
                        link.classList.add('active');
                    }
                });
            }
        });
    }

    if (sections.length > 0) {
        window.addEventListener('scroll', highlightNavigation);
    }

    // ========================================================================
    // Header Shadow on Scroll
    // ========================================================================

    const header = document.querySelector('.site-header');

    function handleHeaderShadow() {
        if (window.scrollY > 10) {
            header.style.boxShadow = 'var(--shadow-md)';
        } else {
            header.style.boxShadow = 'none';
        }
    }

    if (header) {
        window.addEventListener('scroll', handleHeaderShadow);
    }

    // ========================================================================
    // OS Detection for Downloads Page
    // ========================================================================

    function detectOS() {
        const userAgent = window.navigator.userAgent;
        const platform = window.navigator.platform;
        const macosPlatforms = ['Macintosh', 'MacIntel', 'MacPPC', 'Mac68K'];
        const windowsPlatforms = ['Win32', 'Win64', 'Windows', 'WinCE'];
        const iosPlatforms = ['iPhone', 'iPad', 'iPod'];

        let os = null;

        if (macosPlatforms.indexOf(platform) !== -1) {
            os = 'mac';
        } else if (iosPlatforms.indexOf(platform) !== -1) {
            os = 'ios';
        } else if (windowsPlatforms.indexOf(platform) !== -1) {
            os = 'windows';
        } else if (/Android/.test(userAgent)) {
            os = 'android';
        } else if (/Linux/.test(platform)) {
            os = 'linux';
        }

        return os;
    }

    function setupDownloadPage() {
        const detectedPlatform = document.getElementById('detected-platform');

        if (!detectedPlatform) {
            console.log('[I2P] No detected-platform element found');
            return;
        }

        const os = detectOS();
        console.log('[I2P] Detected OS:', os);

        if (!os) {
            console.log('[I2P] Could not detect OS');
            // If OS can't be detected, show the first platform card
            const firstCard = document.querySelector('.platform-card');
            if (firstCard) {
                firstCard.scrollIntoView({ behavior: 'smooth', block: 'nearest' });
            }
            return;
        }

        // Platform configurations (get data from front matter via data attributes would be better in production)
        const platforms = {
            windows: {
                name: 'Windows',
                details: 'Version 2.10.0 • ~24M • Requires Java',
                downloadUrl: 'https://i2p.net/files/2.10.0/i2pinstall_2.10.0-0_windows.exe',
                torrentUrl: 'magnet:?xt=urn:btih:75d8c74e9cc52f5cb4982b941d7e49f9f890c458&dn=i2pinstall_2.10.0-0_windows.exe&tr=udp%3A%2F%2Ftracker.opentrackr.org%3A1337%2Fannounce',
                i2pUrl: 'http://mirror.stormycloud.i2p/2.10.0/i2pinstall_2.10.0-0_windows.exe',
                torUrl: 'http://hhn4r4qyrmplmfiermza6p3d67a5ra7ecwjeoo5a5ddiogwhyjg675id.onion/2.10.0/i2pinstall_2.10.0-0_windows.exe',
                sha256: 'f96110b00c28591691d409bd2f1768b7906b80da5cab2e20ddc060cbb4389fbf',
                icon: '<svg width="64" height="64" viewBox="0 0 24 24" fill="currentColor"><path d="M0 3.449L9.75 2.1v9.451H0m10.949-9.602L24 0v11.4H10.949M0 12.6h9.75v9.451L0 20.699M10.949 12.6H24V24l-12.9-1.801"/></svg>'
            },
            mac: {
                name: 'macOS',
                details: 'Version 2.10.0 • ~30M • Java 8+ required',
                downloadUrl: 'https://i2p.net/files/2.10.0/i2pinstall_2.10.0.jar',
                torrentUrl: 'magnet:?xt=urn:btih:20ce01ea81b437ced30b1574d457cce55c86dce2&dn=i2pinstall_2.10.0.jar&tr=udp%3A%2F%2Ftracker.opentrackr.org%3A1337%2Fannounce',
                i2pUrl: 'http://mirror.stormycloud.i2p/2.10.0/i2pinstall_2.10.0.jar',
                torUrl: 'http://hhn4r4qyrmplmfiermza6p3d67a5ra7ecwjeoo5a5ddiogwhyjg675id.onion/2.10.0/i2pinstall_2.10.0.jar',
                sha256: '76372d552dddb8c1d751dde09bae64afba81fef551455e85e9275d3d031872ea',
                icon: '<svg width="64" height="64" viewBox="0 0 24 24" fill="currentColor"><path d="M18.71 19.5c-.83 1.24-1.71 2.45-3.05 2.47-1.34.03-1.77-.79-3.29-.79-1.53 0-2 .77-3.27.82-1.31.05-2.3-1.32-3.14-2.53C4.25 17 2.94 12.45 4.7 9.39c.87-1.52 2.43-2.48 4.12-2.51 1.28-.02 2.5.87 3.29.87.78 0 2.26-1.07 3.81-.91.65.03 2.47.26 3.64 1.98-.09.06-2.17 1.28-2.15 3.81.03 3.02 2.65 4.03 2.68 4.04-.03.07-.42 1.44-1.38 2.83M13 3.5c.73-.83 1.94-1.46 2.94-1.5.13 1.17-.34 2.35-1.04 3.19-.69.85-1.83 1.51-2.95 1.42-.15-1.15.41-2.35 1.05-3.11z"/></svg>'
            },
            linux: {
                name: 'Linux / BSD',
                details: 'Version 2.10.0 • ~30M • Java 8+ required',
                downloadUrl: 'https://i2p.net/files/2.10.0/i2pinstall_2.10.0.jar',
                torrentUrl: 'magnet:?xt=urn:btih:20ce01ea81b437ced30b1574d457cce55c86dce2&dn=i2pinstall_2.10.0.jar&tr=udp%3A%2F%2Ftracker.opentrackr.org%3A1337%2Fannounce',
                i2pUrl: 'http://mirror.stormycloud.i2p/2.10.0/i2pinstall_2.10.0.jar',
                torUrl: 'http://hhn4r4qyrmplmfiermza6p3d67a5ra7ecwjeoo5a5ddiogwhyjg675id.onion/2.10.0/i2pinstall_2.10.0.jar',
                sha256: '76372d552dddb8c1d751dde09bae64afba81fef551455e85e9275d3d031872ea',
                icon: '<svg width="64" height="64" viewBox="0 0 24 24" fill="currentColor"><path d="M20.581 19.049c-.55-.446-.336-1.431-.907-1.917.553-3.365-.997-6.331-2.845-8.232-1.551-1.595-1.051-3.147-1.051-4.49 0-2.146-.881-4.41-3.55-4.41-2.853 0-3.635 2.38-3.663 3.738-.068 3.262.659 4.11-1.25 6.484-2.246 2.793-2.577 5.579-2.07 7.057-.237.276-.557.582-1.155.835-1.652.72-.441 1.925-.898 2.78-.13.243-.192.497-.192.74 0 .75.596 1.399 1.679 1.302 1.461-.13 2.809.905 3.681.905.77 0 1.402-.438 1.696-1.041 1.377-.339 3.077-.296 4.453.059.247.691.798 1.041 1.479 1.041.973 0 2.13-.901 3.299-.901 1.007 0 1.64.36 1.868.684.178.261.53.456 1.004.456.456 0 .924-.277 1.024-.757.15-.723-.809-1.318-1.624-2.076z"/></svg>'
            },
            android: {
                name: 'Android',
                details: 'Version 2.10.1 • ~28 MB • Android 4.0+',
                downloadUrl: 'https://download.i2p.io/android/I2P.apk',
                torrentUrl: 'magnet:?xt=urn:btih:android_example',
                i2pUrl: 'http://stats.i2p/android/I2P.apk',
                sha256: 'c3d4e5f6789012345678901234567890123456789012345678901234abcdef',
                icon: '<svg width="64" height="64" viewBox="0 0 24 24" fill="currentColor"><path d="M17.6 9.48l1.84-3.18c.16-.31.04-.69-.26-.85a.637.637 0 00-.83.22l-1.88 3.24a11.43 11.43 0 00-8.94 0L5.65 5.67a.643.643 0 00-.87-.2c-.28.18-.37.54-.22.83L6.4 9.48A10.81 10.81 0 001 18h22a10.81 10.81 0 00-5.4-8.52M7 15.25a1.25 1.25 0 110-2.5 1.25 1.25 0 010 2.5m10 0a1.25 1.25 0 110-2.5 1.25 1.25 0 010 2.5z"/></svg>'
            }
        };

        const platformConfig = platforms[os];

        if (platformConfig) {
            console.log('[I2P] Platform config found:', platformConfig);
            // Show detected platform section
            detectedPlatform.style.display = 'block';

            // Update content
            document.getElementById('detected-icon').innerHTML = platformConfig.icon;
            document.getElementById('detected-name').textContent = `Download for ${platformConfig.name}`;
            document.getElementById('detected-details').textContent = platformConfig.details;
            const downloadBtn = document.getElementById('detected-download-btn');
            downloadBtn.href = platformConfig.downloadUrl;
            console.log('[I2P] Set download button href to:', downloadBtn.href);

            // Update alternative download links
            if (platformConfig.torrentUrl) {
                document.getElementById('detected-torrent').href = platformConfig.torrentUrl;
            }
            if (platformConfig.i2pUrl) {
                document.getElementById('detected-i2p').href = platformConfig.i2pUrl;
            }
            if (platformConfig.torUrl) {
                document.getElementById('detected-tor').href = platformConfig.torUrl;
            } else {
                document.getElementById('detected-tor').style.display = 'none';
            }

            // Update checksum badge
            if (platformConfig.sha256) {
                const checksumBadge = document.getElementById('detected-checksum');
                checksumBadge.setAttribute('data-sha', 'SHA256: ' + platformConfig.sha256);
                checksumBadge.style.display = 'inline-flex';
            }

            // Hide matching platform card from the grid (since it's shown in "Recommended")
            const platformCard = document.querySelector(`.platform-card[data-platform="${os}"]`);
            if (platformCard) {
                platformCard.style.display = 'none';
            }
        }
    }

    // Setup mirror selector functionality
    function setupMirrorSelector() {
        const mirrorSelect = document.getElementById('detected-mirror');
        const downloadBtn = document.getElementById('detected-download-btn');

        if (mirrorSelect && downloadBtn) {
            mirrorSelect.addEventListener('change', function() {
                const baseUrl = this.value;
                const currentHref = downloadBtn.href;
                const filename = currentHref.split('/').pop();
                downloadBtn.href = baseUrl + filename;
            });
        }
    }

    // Initialize download page if we're on it
    if (document.querySelector('.downloads-hero')) {
        setupDownloadPage();
        setupMirrorSelector();
    }

    // ========================================================================
    // Site Banner Dismiss
    // ========================================================================

    function setupBanner() {
        const banner = document.getElementById('site-banner');
        if (!banner) return;

        const bannerId = banner.getAttribute('data-banner-id');
        const dismissBtn = banner.querySelector('.banner-close');

        // Check if banner was previously dismissed
        const dismissedBanners = JSON.parse(localStorage.getItem('dismissedBanners') || '[]');
        if (dismissedBanners.includes(bannerId)) {
            banner.remove();
            return;
        }

        // Dismiss banner function
        function dismissBanner() {
            // Add hidden class for animation
            banner.classList.add('banner-hidden');

            // Wait for animation to complete before removing
            setTimeout(() => {
                banner.remove();
            }, 250);

            // Save to localStorage
            dismissedBanners.push(bannerId);
            localStorage.setItem('dismissedBanners', JSON.stringify(dismissedBanners));
        }

        // Dismiss button click handler
        if (dismissBtn) {
            dismissBtn.addEventListener('click', dismissBanner);
        }

        // Dismiss on ESC key
        document.addEventListener('keydown', function(e) {
            if (e.key === 'Escape' && banner && !banner.classList.contains('banner-hidden')) {
                dismissBanner();
            }
        });
    }

    setupBanner();

    // ========================================================================
    // Poll Modal
    // ========================================================================

    function setupPoll() {
        const pollModal = document.getElementById('poll-modal');
        if (!pollModal) return;

        const pollClose = document.getElementById('poll-close');
        const pollWidget = document.getElementById('poll-widget');
        let widgetScriptLoaded = false;

        // Load widget script dynamically when needed
        function loadWidgetScript() {
            // Check if script is already loaded
            if (widgetScriptLoaded || document.querySelector('script[src*="voting.js"]')) {
                widgetScriptLoaded = true;
                return Promise.resolve();
            }

            // Detect network to determine base URL
            // Use window.feedbackBaseUrl if available (set by baseof.html), otherwise detect
            let baseUrl = window.feedbackBaseUrl;
            if (!baseUrl) {
                const hostname = window.location.hostname;
                // Check for I2P (both .i2p and .b32.i2p addresses)
                if (hostname.endsWith('.b32.i2p') || hostname.endsWith('.i2p')) {
                    baseUrl = 'http://5kwyynf3eetgqa2nors6ctwo7doi7yu73k7uvypy5eqmm326zkiq.b32.i2p';
                } else if (hostname.endsWith('.onion')) {
                    baseUrl = 'http://gfonxmohvarpmocsvllscsuszdu5rikipm6innvcwq4vpng7zzqmmfyd.onion';
                } else {
                    baseUrl = 'https://feedback.i2p.net';
                }
            }

            return new Promise(function(resolve, reject) {
                const script = document.createElement('script');
                script.src = baseUrl + '/widgets/voting.js';
                script.async = true;
                script.onload = function() {
                    console.log('[Poll] Widget script loaded successfully from:', baseUrl);
                    widgetScriptLoaded = true;
                    resolve();
                };
                script.onerror = function() {
                    console.error('[Poll] Failed to load widget script from:', baseUrl);
                    reject(new Error('Failed to load voting widget script'));
                };
                document.body.appendChild(script);
            });
        }

        // Initialize widget when modal opens
        function initializeWidget() {
            if (!pollWidget) {
                console.error('[Poll] Widget element not found');
                return;
            }

            // Get API URL and poll ID from data attributes or defaults
            const apiUrl = pollWidget.getAttribute('data-api-url') || window.pollApiUrl || 'https://feedback.i2p.net';
            const pollId = pollWidget.getAttribute('data-poll-id') || window.pollId || '1';

            // Update attributes if needed
            pollWidget.setAttribute('data-poll-id', pollId);
            pollWidget.setAttribute('data-api-url', apiUrl);
            // Don't force results view, allow voting if not voted
            pollWidget.setAttribute('data-show-results', 'false');

            console.log('[Poll] Widget element ready, poll ID:', pollId, 'API URL:', apiUrl);
            
            // Force a reflow to help trigger any observers that might be watching for visibility
            void pollWidget.offsetHeight;
        }

        // Open modal
        function openModal() {
            pollModal.classList.add('show');
            document.body.style.overflow = 'hidden';
            
            // Load widget script and initialize when modal is shown
            // Use a small delay to ensure the modal is visible and CSS transitions complete
            setTimeout(function() {
                loadWidgetScript()
                    .then(function() {
                        // Script loaded, now initialize the widget
                        initializeWidget();
                    })
                    .catch(function(error) {
                        console.error('[Poll] Error loading widget:', error);
                        if (pollWidget) {
                            pollWidget.innerHTML = '<p class="poll-error">Failed to load poll. Please try again later.</p>';
                        }
                    });
            }, 150);
        }

        // Close modal
        function closeModal() {
            pollModal.classList.remove('show');
            document.body.style.overflow = '';
        }

        // Event listeners
        if (pollClose) {
            pollClose.addEventListener('click', closeModal);
        }

        // Close on overlay click
        pollModal.addEventListener('click', function(e) {
            if (e.target === pollModal) {
                closeModal();
            }
        });

        // Close on ESC key
        document.addEventListener('keydown', function(e) {
            if (e.key === 'Escape' && pollModal.classList.contains('show')) {
                closeModal();
            }
        });

        // Listen for poll links (e.g., href="#poll")
        document.addEventListener('click', function(e) {
            const target = e.target.closest('a[href="#poll"], a[href*="#poll"]');
            if (target) {
                e.preventDefault();
                openModal();
            }
        });

        // Expose API
        window.openPoll = openModal;
    }

    setupPoll();

    // ========================================================================
    // Initialize
    // ========================================================================

    console.log('I2P Website initialized');

})();

// I2P Website - Main JavaScript
// ============================================================================

(function() {
    'use strict';

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

// Minimal JS for the digital garden

document.addEventListener('DOMContentLoaded', () => {

    // Theme Toggle
    const themeToggle = document.getElementById('theme-toggle');
    const root = document.documentElement;

    // Check for saved theme preference or default to dark
    const currentTheme = localStorage.getItem('theme') || 'dark';
    root.setAttribute('data-theme', currentTheme);

    themeToggle.addEventListener('click', () => {
        const theme = root.getAttribute('data-theme');
        const newTheme = theme === 'dark' ? 'light' : 'dark';

        root.setAttribute('data-theme', newTheme);
        localStorage.setItem('theme', newTheme);

        // Toggle icon (you can enhance this with moon/sun icons later)
        themeToggle.style.transform = 'rotate(180deg)';
        setTimeout(() => {
            themeToggle.style.transform = 'rotate(0deg)';
        }, 300);
    });

    // === VIEW SWITCHING (Everything / Spaces / Philosophy) ===
    const navItems = document.querySelectorAll('.top-nav span');
    const everythingView = document.getElementById('everything-view');
    const spacesView = document.getElementById('spaces-view');
    const spaceDetailView = document.getElementById('space-detail-view');

    navItems.forEach(item => {
        item.addEventListener('click', () => {
            const view = item.getAttribute('data-view');

            // Update active state
            navItems.forEach(nav => nav.classList.remove('active'));
            item.classList.add('active');

            // Check if we're currently in folder detail view
            const isInFolderView = spaceDetailView.style.display === 'block';

            // Show/hide views
            if (view === 'everything') {
                everythingView.style.display = 'block';
                spacesView.style.display = 'none';
                spaceDetailView.style.display = 'none';

                // Reset header and back button if coming from folder view
                if (isInFolderView) {
                    headerTitle.innerHTML = originalTitleHTML;
                    backButton.style.display = 'none';
                    backButton.classList.remove('btn-anim-in');
                }
            } else if (view === 'spaces') {
                everythingView.style.display = 'none';
                spacesView.style.display = 'block';
                spaceDetailView.style.display = 'none';

                // Reset header and back button if coming from folder view
                if (isInFolderView) {
                    headerTitle.innerHTML = originalTitleHTML;
                    backButton.style.display = 'none';
                    backButton.classList.remove('btn-anim-in');
                }
            } else if (view === 'philosophy') {
                // Filter to show only philosophy cards
                everythingView.style.display = 'block';
                spacesView.style.display = 'none';
                spaceDetailView.style.display = 'none';

                // Reset header and back button if coming from folder view
                if (isInFolderView) {
                    headerTitle.innerHTML = originalTitleHTML;
                    backButton.style.display = 'none';
                    backButton.classList.remove('btn-anim-in');
                }
                // TODO: Add filtering logic for philosophy cards
            }
        });
    });

    // === FOLDER CLICK - Show Space Detail View ===
    const folderCards = document.querySelectorAll('.folder-card');
    const spaceCardsGrid = document.getElementById('spaceCardsGrid');
    const backButton = document.getElementById('backToSpaces');
    const allCards = document.querySelectorAll('#everything-view .grid-item');
    const headerTitle = document.getElementById('header-title');
    const originalTitleHTML = 'With love, Rajat<span class="cursor-blink">_</span>';

    let isAnimating = false;

    folderCards.forEach(folder => {
        folder.addEventListener('click', () => {
            if (isAnimating) return;
            isAnimating = true;

            const spaceName = folder.getAttribute('data-space');
            const folderTitle = folder.querySelector('.folder-title').textContent;

            // 1. Animate out folders & Header Text
            spacesView.classList.add('animate-out');
            headerTitle.classList.add('text-anim-out');

            setTimeout(() => {
                // 2. Filter and clone cards
                spaceCardsGrid.innerHTML = '';
                let hasCards = false;

                allCards.forEach(card => {
                    const cardSpace = card.getAttribute('data-space');
                    if (cardSpace === spaceName) {
                        const clonedCard = card.cloneNode(true);
                        clonedCard.classList.add('stagger-item');
                        spaceCardsGrid.appendChild(clonedCard);
                        hasCards = true;
                    }
                });

                if (!hasCards) {
                    spaceCardsGrid.innerHTML = '<p class="stagger-item" style="color: var(--subtle); text-align: center; padding: 40px;">No cards in this space yet.</p>';
                }

                // 3. Switch views
                spacesView.style.display = 'none';
                spacesView.classList.remove('animate-out');

                // Scroll to top smoothly
                window.scrollTo({ top: 0, behavior: 'smooth' });

                spaceDetailView.style.display = 'block';
                spaceDetailView.classList.add('animate-in');

                // 4. Update Header Text & Animate In
                headerTitle.innerHTML = `${folderTitle}<span class="cursor-blink">_</span>`;
                headerTitle.classList.remove('text-anim-out');
                headerTitle.classList.add('text-anim-in');

                // Show Back Button with animation
                backButton.classList.remove('btn-anim-out');
                backButton.classList.add('btn-anim-in');

                // Re-attach click handlers
                attachCardClickHandlers();

                // Cleanup
                setTimeout(() => {
                    spaceDetailView.classList.remove('animate-in');
                    headerTitle.classList.remove('text-anim-in');
                    isAnimating = false;
                }, 500);

            }, 400); // Wait for fade out
        });
    });

    // Back button - return to folders
    backButton.addEventListener('click', () => {
        if (isAnimating) return;
        isAnimating = true;

        // 1. Animate out detail view & Header Text & Button
        spaceDetailView.classList.add('animate-out');
        headerTitle.classList.add('text-anim-out');
        backButton.classList.remove('btn-anim-in');
        backButton.classList.add('btn-anim-out');

        setTimeout(() => {
            // 2. Switch views
            spaceDetailView.style.display = 'none';
            spaceDetailView.classList.remove('animate-out');

            // Scroll to top
            window.scrollTo({ top: 0, behavior: 'smooth' });

            spacesView.style.display = 'block';
            spacesView.classList.add('animate-in');

            // 3. Reset Header Text & Animate In
            headerTitle.innerHTML = originalTitleHTML;
            headerTitle.classList.remove('text-anim-out');
            headerTitle.classList.add('text-anim-in');

            // Hide button (class handles animation, we just need to ensure it's gone from flow)
            backButton.style.display = 'none';
            backButton.classList.remove('btn-anim-out');

            // Cleanup
            setTimeout(() => {
                spacesView.classList.remove('animate-in');
                headerTitle.classList.remove('text-anim-in');
                isAnimating = false;
            }, 500);

        }, 400);
    });

    // Simple fade-in on scroll for cards
    const observerOptions = {
        threshold: 0.1,
        rootMargin: '0px 0px -100px 0px'
    };

    const observer = new IntersectionObserver((entries) => {
        entries.forEach(entry => {
            if (entry.isIntersecting) {
                entry.target.style.opacity = '1';
                entry.target.style.transform = 'translateY(0)';
            }
        });
    }, observerOptions);

    // Observe all grid items
    document.querySelectorAll('.grid-item').forEach(item => {
        item.style.opacity = '0';
        item.style.transform = 'translateY(20px)';
        item.style.transition = 'opacity 0.6s ease, transform 0.6s ease';
        observer.observe(item);
    });

    // Add checkbox functionality
    document.querySelectorAll('.checklist-item input[type="checkbox"]').forEach(checkbox => {
        checkbox.addEventListener('change', (e) => {
            const label = e.target.closest('.checklist-item');
            if (e.target.checked) {
                label.style.opacity = '0.5';
                label.querySelector('span').style.textDecoration = 'line-through';
            } else {
                label.style.opacity = '1';
                label.querySelector('span').style.textDecoration = 'none';
            }
        });
    });

    // === MODAL FUNCTIONALITY ===
    const modal = document.getElementById('cardModal');
    const modalContent = document.getElementById('modalContent');
    const modalClose = document.getElementById('modalClose');
    const modalBackdrop = modal.querySelector('.modal-backdrop');

    // Function to open modal with card content
    function openModal(cardElement) {
        const videoId = cardElement.getAttribute('data-video-id');

        if (videoId) {
            // It's a video card - inject iframe
            modalContent.innerHTML = `
                <div class="modal-video-container">
                    <iframe 
                        class="modal-video-iframe" 
                        src="https://www.youtube.com/embed/${videoId}?autoplay=1&rel=0" 
                        title="YouTube video player" 
                        frameborder="0" 
                        allow="accelerometer; autoplay; clipboard-write; encrypted-media; gyroscope; picture-in-picture; web-share" 
                        allowfullscreen>
                    </iframe>
                </div>
            `;
        } else {
            // Check if it's a project card with expanded content
            const modalProjectContent = cardElement.querySelector('.modal-project-content');

            if (modalProjectContent) {
                // Project card - show the expanded content
                // We need to get the content INSIDE the modal-project-content div
                const projectView = modalProjectContent.querySelector('.project-modal-view');

                if (projectView) {
                    const expandedContent = projectView.cloneNode(true);
                    modalContent.innerHTML = '';
                    modalContent.appendChild(expandedContent);
                }
            } else {
                // Regular card - clone content
                const cardClone = cardElement.cloneNode(true);
                modalContent.innerHTML = '';
                modalContent.appendChild(cardClone);
            }
        }

        // Show modal with animation
        modal.classList.add('active');
        document.body.classList.add('modal-open');
    }

    // Function to close modal
    function closeModal() {
        modal.classList.remove('active');
        document.body.classList.remove('modal-open');

        // Clear content after animation
        setTimeout(() => {
            modalContent.innerHTML = '';
        }, 300);
    }

    // Function to attach click handlers to cards (for both original and cloned cards)
    function attachCardClickHandlers() {
        document.querySelectorAll('.card').forEach(card => {
            // Remove any existing click handler to avoid duplicates
            const newCard = card.cloneNode(true);
            card.parentNode.replaceChild(newCard, card);

            newCard.style.cursor = 'pointer';
            newCard.addEventListener('click', (e) => {
                // Don't expand if clicking on interactive elements
                if (e.target.tagName === 'A' ||
                    e.target.tagName === 'INPUT' ||
                    e.target.closest('.play-btn')) {
                    return;
                }

                // Check if this card has an external link
                const externalLink = newCard.getAttribute('data-external-link');
                if (externalLink) {
                    // Open the external link in a new tab
                    window.open(externalLink, '_blank');
                } else {
                    // Open modal as usual
                    openModal(newCard);
                }
            });
        });
    }

    // Initial attachment for original cards
    attachCardClickHandlers();

    // Close modal events
    modalClose.addEventListener('click', closeModal);
    modalBackdrop.addEventListener('click', closeModal);

    // Close on Escape key
    document.addEventListener('keydown', (e) => {
        if (e.key === 'Escape' && modal.classList.contains('active')) {
            closeModal();
        }
    });

});

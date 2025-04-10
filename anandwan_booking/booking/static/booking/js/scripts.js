document.addEventListener('DOMContentLoaded', function() {
    // Show loading spinner when forms are submitted
    const forms = document.querySelectorAll('form');
    const spinnerOverlay = document.createElement('div');
    spinnerOverlay.className = 'spinner-overlay';
    spinnerOverlay.innerHTML = `
        <div class="spinner-border" role="status">
            <span class="visually-hidden">Loading...</span>
        </div>
    `;
    document.body.appendChild(spinnerOverlay);

    forms.forEach(form => {
        form.addEventListener('submit', function() {
            // Don't show spinner for search forms
            if (!this.classList.contains('search-form')) {
                spinnerOverlay.classList.add('active');
            }
        });
    });

    // Initialize date inputs with min dates
    const today = new Date();
    const tomorrow = new Date(today);
    tomorrow.setDate(tomorrow.getDate() + 1);

    const formatDate = (date) => {
        const year = date.getFullYear();
        const month = String(date.getMonth() + 1).padStart(2, '0');
        const day = String(date.getDate()).padStart(2, '0');
        return `${year}-${month}-${day}`;
    };

    const checkInDateInputs = document.querySelectorAll('input[name="check_in_date"]');
    const checkOutDateInputs = document.querySelectorAll('input[name="check_out_date"]');

    checkInDateInputs.forEach(input => {
        input.min = formatDate(today);
        
        // When check-in date changes, update check-out date min value
        input.addEventListener('change', function() {
            const selectedDate = new Date(this.value);
            const nextDay = new Date(selectedDate);
            nextDay.setDate(nextDay.getDate() + 1);
            
            // Find the corresponding check-out date input
            const form = this.closest('form');
            const checkOutInput = form.querySelector('input[name="check_out_date"]');
            if (checkOutInput) {
                checkOutInput.min = formatDate(nextDay);
                
                // If check-out date is before new check-in date + 1, reset it
                if (new Date(checkOutInput.value) <= selectedDate) {
                    checkOutInput.value = formatDate(nextDay);
                }
            }
        });
    });

    checkOutDateInputs.forEach(input => {
        input.min = formatDate(tomorrow);
    });

    // Room booking form enhancements
    const specialRequestsTextarea = document.querySelector('#id_special_requests');
    if (specialRequestsTextarea) {
        const charCounter = document.createElement('small');
        charCounter.className = 'text-muted d-block text-end';
        charCounter.textContent = '0/500 characters';
        specialRequestsTextarea.after(charCounter);

        specialRequestsTextarea.addEventListener('input', function() {
            const count = this.value.length;
            charCounter.textContent = `${count}/500 characters`;
            
            if (count > 450) {
                charCounter.className = 'text-warning d-block text-end';
            } else {
                charCounter.className = 'text-muted d-block text-end';
            }
        });
    }

    // Room showcase image enlargement
    const roomImages = document.querySelectorAll('.room-image');
    roomImages.forEach(img => {
        img.addEventListener('click', function() {
            if (this.src && !this.classList.contains('no-expand')) {
                const modal = document.createElement('div');
                modal.className = 'modal fade';
                modal.id = 'imageModal';
                modal.setAttribute('tabindex', '-1');
                modal.setAttribute('aria-hidden', 'true');
                
                modal.innerHTML = `
                    <div class="modal-dialog modal-dialog-centered modal-lg">
                        <div class="modal-content">
                            <div class="modal-header">
                                <button type="button" class="btn-close" data-bs-dismiss="modal" aria-label="Close"></button>
                            </div>
                            <div class="modal-body text-center">
                                <img src="${this.src}" class="img-fluid" alt="Room Image">
                            </div>
                        </div>
                    </div>
                `;
                
                document.body.appendChild(modal);
                
                const modalInstance = new bootstrap.Modal(modal);
                modalInstance.show();
                
                modal.addEventListener('hidden.bs.modal', function() {
                    this.remove();
                });
            }
        });
    });

    // Confirmation alert for booking cancellation
    const cancelButtons = document.querySelectorAll('.cancel-booking-btn');
    cancelButtons.forEach(button => {
        button.addEventListener('click', function(e) {
            if (!confirm('Are you sure you want to cancel this booking?')) {
                e.preventDefault();
            }
        });
    });

    // Enhance form inputs
    document.querySelectorAll('select, input[type="number"]').forEach(input => {
        input.classList.add('form-select', 'form-control');
    });

    // Fix mobile navigation
    const navbarToggler = document.querySelector('.navbar-toggler');
    const navbarCollapse = document.querySelector('.navbar-collapse');
    
    if (navbarToggler && navbarCollapse) {
        // Close navbar when a link is clicked
        const navLinks = navbarCollapse.querySelectorAll('.nav-link');
        navLinks.forEach(link => {
            link.addEventListener('click', () => {
                if (window.innerWidth < 992) {
                    const bsCollapse = new bootstrap.Collapse(navbarCollapse);
                    bsCollapse.hide();
                }
            });
        });
    }
});
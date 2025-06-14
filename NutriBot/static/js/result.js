// Animate elements on page load
document.addEventListener('DOMContentLoaded', () => {
    // First animate the main sections
    const sectionsAndCards = document.querySelectorAll('.summary-card, .meal-card, .tip-card, .user-profile-summary, .explanation-section');
    
    sectionsAndCards.forEach((element, index) => {
        setTimeout(() => {
            element.classList.add('animate');
        }, index * 150);
    });

    // Then animate profile items specifically
    const profileItems = document.querySelectorAll('.profile-item');
    profileItems.forEach((item, index) => {
        setTimeout(() => {
            item.classList.add('animate');
            // Animate children elements with a further stagger
            const childrenToAnimate = item.querySelectorAll('h3, p, i');
            childrenToAnimate.forEach((child, childIndex) => {
                setTimeout(() => {
                    child.style.opacity = '1';
                    child.style.transform = 'translateY(0)';
                }, childIndex * 100); // Stagger children by 100ms
            });
        }, index * 200); // Stagger profile items by 200ms
    });
});

// PDF Download functionality
function downloadPDF() {
    const element = document.querySelector('.result-content');
    const opt = {
        margin: 1,
        filename: 'diet-plan.pdf',
        image: { type: 'jpeg', quality: 0.98 },
        html2canvas: { scale: 2 },
        jsPDF: { unit: 'in', format: 'letter', orientation: 'portrait' }
    };

    // Show loading state
    const downloadBtn = document.querySelector('.btn-primary');
    const originalText = downloadBtn.innerHTML;
    downloadBtn.innerHTML = '<i class="fas fa-spinner fa-spin"></i> Generating PDF...';
    downloadBtn.disabled = true;

    // Generate PDF
    html2pdf().set(opt).from(element).save().then(() => {
        // Restore button state
        downloadBtn.innerHTML = originalText;
        downloadBtn.disabled = false;
    }).catch(error => {
        console.error('Error generating PDF:', error);
        downloadBtn.innerHTML = originalText;
        downloadBtn.disabled = false;
        alert('Error generating PDF. Please try again.');
    });
}

// Add smooth scrolling for anchor links
document.querySelectorAll('a[href^="#"]').forEach(anchor => {
    anchor.addEventListener('click', function (e) {
        e.preventDefault();
        const target = document.querySelector(this.getAttribute('href'));
        if (target) {
            target.scrollIntoView({
                behavior: 'smooth',
                block: 'start'
            });
        }
    });
}); 
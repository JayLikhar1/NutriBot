// Animate elements on scroll
document.addEventListener('DOMContentLoaded', () => {
    const sections = document.querySelectorAll('.hero-section, .features-section, .how-it-works-section, .cta-section');

    const observer = new IntersectionObserver((entries) => {
        entries.forEach(entry => {
            if (entry.isIntersecting) {
                entry.target.classList.add('animate');
                observer.unobserve(entry.target);
            }
        });
    }, {
        threshold: 0.1 // Adjust as needed
    });

    sections.forEach(section => {
        observer.observe(section);
    });
}); 
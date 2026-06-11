document.addEventListener('DOMContentLoaded', () => {
    const previewForm = document.getElementById('previewForm');
    const modal = new bootstrap.Modal(document.getElementById('referenceModal'));

    if (previewForm) {
        previewForm.addEventListener('submit', async (e) => {
            e.preventDefault();
            const formData = new FormData(previewForm);
            const response = await fetch(previewForm.action, {
                method: 'POST',
                body: formData,
                headers: { 'X-Requested-With': 'XMLHttpRequest' }
            });
            const data = await response.json();
            if (data.ok) {
                document.getElementById('referenceModal').innerHTML = data.html;
                modal.show();
            } else {
                alert(data.error);
            }
        });
    }

    document.addEventListener('click', (e) => {
        if (e.target.classList.contains('btn-close') || e.target.dataset.bsDismiss === 'modal') {
            modal.hide();
            location.reload(); // Refresh table or auto-fill reference field
        }
    });

    document.querySelectorAll('form[action*="confirm_reference_ajax"]').forEach(form => {
        form.addEventListener('submit', async (e) => {
            e.preventDefault();
            const formData = new FormData(form);
            const response = await fetch(form.action, {
                method: 'POST',
                body: formData,
                headers: { 'X-Requested-With': 'XMLHttpRequest' }
            });
            const data = await response.json();
            if (data.ok) {
                modal.hide();
                alert('Reference created: ' + data.reference);
                location.reload(); // Refresh or update UI
            } else {
                alert(data.error);
            }
        });
    });
});
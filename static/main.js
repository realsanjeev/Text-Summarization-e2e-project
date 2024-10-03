const textarea = document.getElementById('text');

const filesystem = null;

document.addEventListener('DOMContentLoaded', () => {
    const form = document.getElementById('summarizeForm');
    const submitBtn = document.getElementById('submitBtn');
    const btnText = document.getElementById('btnText');
    const loader = document.getElementById('loader');
    const summarySection = document.getElementById('summarySection');
    const summaryContent = document.getElementById('summaryContent');

    form.addEventListener('submit', async (e) => {
        e.preventDefault();
        
        const text = document.getElementById('text').value;
        if (!text.trim()) return;

        // Show loading state
        submitBtn.disabled = true;
        btnText.textContent = 'Summarizing...';
        loader.classList.remove('hidden');
        summarySection.classList.add('hidden');

        try {
            const formData = new FormData();
            formData.append('script', text);

            const response = await fetch('/', {
                method: 'POST',
                body: formData
            });

            if (!response.ok) throw new Error('Network response was not ok');

            const html = await response.text();
            
            // Extract summary from the returned HTML (since backend returns full page)
            // Ideally backend should return JSON, but we are keeping backend changes minimal for now
            const parser = new DOMParser();
            const doc = parser.parseFromString(html, 'text/html');
            const newSummary = doc.getElementById('summaryContent').innerHTML;

            summaryContent.innerHTML = newSummary;
            summarySection.classList.remove('hidden');
        } catch (error) {
            console.error('Error:', error);
            alert('An error occurred while summarizing. Please try again.');
        } finally {
            // Reset loading state
            submitBtn.disabled = false;
            btnText.textContent = 'Summarize Text';
            loader.classList.add('hidden');
        }
    });
});

document.addEventListener('DOMContentLoaded', () => {
    // Check if user is logged in
    const staffId = sessionStorage.getItem('staffId');
    const staffName = sessionStorage.getItem('staffName');
    
    // if (!staffId || !staffId.startsWith('R')) {
    //     window.location.href = 'index.html';
    //     return;
    // }
    
    // Set staff name
    document.getElementById('staffName').textContent = staffName;
    
    // Dark mode toggle
    const darkModeToggle = document.getElementById('darkMode');
    
    // Check for saved theme preference
    const savedTheme = localStorage.getItem('theme');
    if (savedTheme === 'dark') {
        document.documentElement.setAttribute('data-theme', 'dark');
        darkModeToggle.checked = true;
    }
    
    darkModeToggle.addEventListener('change', () => {
        if (darkModeToggle.checked) {
            document.documentElement.setAttribute('data-theme', 'dark');
            localStorage.setItem('theme', 'dark');
        } else {
            document.documentElement.removeAttribute('data-theme');
            localStorage.setItem('theme', 'light');
        }
    });
    
   // Logout functionality
    document.getElementById('logoutBtn').addEventListener('click', () => {
        sessionStorage.clear();
        window.location.href = '/';
    });

    // Handle back button navigation
    const backBtn = document.getElementById('backBtn');
    if (backBtn) {
        backBtn.addEventListener('click', (e) => {
            e.preventDefault();
            window.location.href = 'receptionist-home.html';
        });
    }
}); 
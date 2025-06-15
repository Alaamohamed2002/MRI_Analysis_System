document.addEventListener('DOMContentLoaded', () => {
    // Check if user is logged in
    // const staffId = sessionStorage.getItem('staffId');
    // const staffName = sessionStorage.getItem('staffName');
    
    // if (!staffId || !staffId.startsWith('D')) {
    //     window.location.href = 'index.html';
    //     return;
    // }
    
    // Set staff name
    const staffName = sessionStorage.getItem('staffName');
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
    // document.getElementById('logoutBtn').addEventListener('click', () => {
    //     sessionStorage.clear();
    //     window.location.href = 'index.html';
    // });
}); 
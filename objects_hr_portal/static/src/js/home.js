window.addEventListener('DOMContentLoaded', function () {
    const el = document.getElementById('wrap');
        if (el) {
            el.classList.add('bg-gray-50');        
        }              

        let seconds = 0;
        const display = document.getElementById('timer-display');

        if (!display) return;

        function updateTimer() {
            seconds++;
            const minutes = String(Math.floor(seconds / 60)).padStart(2, '0');
            const secs = String(seconds % 60).padStart(2, '0');
            display.textContent = `${minutes}:${secs}`;
        }

        setInterval(updateTimer, 1000);

});

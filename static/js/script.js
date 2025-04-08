document.addEventListener('DOMContentLoaded', () => {
    const form = document.querySelector('form');
    if (form) {
        form.addEventListener('submit', (event) => {
            const employeeId = document.getElementById('employee_id').value;
            const name = document.getElementById('name').value;

            if (!/^EMP\d{3}$/.test(employeeId)) {
                alert('Invalid Employee ID format (e.g., EMP001).');
                event.preventDefault();
            }

            if (!/^[A-Za-z\s]+$/.test(name)) {
                alert('Name must contain only letters.');
                event.preventDefault();
            }
        });
    }
});
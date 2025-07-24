window.document.addEventListener('DOMContentLoaded', function () {
    const qualification_date = document.getElementById('id_qualification_date');
    if (qualification_date) {
        qualification_date.addEventListener('change', function () {
            const qualification_default_expiration_time_days = document.getElementById('id_qualification_default_expiration_time_days');
            const qualification_default_expiration_time_years = document.getElementById('id_qualification_default_expiration_time_years');
            const expires_at = document.getElementById('id_expires_at');
            if (!qualification_default_expiration_time_days || !qualification_default_expiration_time_years || !expires_at) {
                return;
            }
            const days = parseInt(qualification_default_expiration_time_days.value, 10) || 0;
            const years = parseInt(qualification_default_expiration_time_years.value, 10) || 0;
            const date = new Date(qualification_date.value);
            if (isNaN(date.getTime())) {
                expires_at.value = '';
                return;
            }
            date.setFullYear(date.getFullYear() + years);
            date.setDate(date.getDate() + days);
            expires_at.value = date.toISOString().split('T')[0]; // Format as YYYY-MM-DD
        });
    }
});
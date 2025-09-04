document.addEventListener("DOMContentLoaded", function() {
    const sidebar = document.getElementById("sidebar");
    const openBtn = document.getElementById("openMenuBtn");
    const closeBtn = document.getElementById("closeMenuBtn");

    openBtn.onclick = function() {
      sidebar.style.width = "250px";
      document.body.classList.add('sidebar-open');
    }

    closeBtn.onclick = function() {
      sidebar.style.width = "0";
      document.body.classList.remove('sidebar-open');
    }

    // Закрывать меню при клике вне его области
    window.onclick = function(event) {
      if (!sidebar.contains(event.target) && event.target !== openBtn) {
         sidebar.style.width = "0";
         document.body.classList.remove('sidebar-open');
      }
    }
});
$('.navTrigger').click(function () {
    $(this).toggleClass('active');
    console.log("Clicked menu");
    $("#mainListDiv").toggleClass("show_list");
    $("#mainListDiv").fadeIn();

});
// Récupérez tous les labels
const labels = document.querySelectorAll('label');

// Parcourez les labels et ajoutez un gestionnaire de clic à chacun
labels.forEach((label) => {
    label.addEventListener('click', () => {
        // Récupérez le menu déroulant associé
        const select = label.nextElementSibling;

        // Vérifiez si le menu déroulant est ouvert ou fermé et basculez la classe "open"
        if (select.classList.contains('open')) {
            select.classList.remove('open');
        } else {
            // Fermez tous les menus déroulants ouverts
            document.querySelectorAll('.custom-select.open').forEach((openSelect) => {
                openSelect.classList.remove('open');
            });
            // Ouvrez le menu déroulant associé
            select.classList.add('open');
        }
    });
});


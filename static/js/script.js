document.addEventListener('DOMContentLoaded', () => {
    const navWrapper = document.querySelector('.nav-wrapper');
    const toggleBtn  = document.querySelector('.menu-toggle');
    const menu       = document.querySelector('.menu');
    const links      = document.querySelectorAll('.menu a');

    /* -- ouvre / ferme le menu -- */
    toggleBtn.addEventListener('click', () => {
        menu.classList.toggle('active');
        navWrapper.classList.toggle('menu-open');
    });

    /* -- ferme après clic sur un lien (mobile) -- */
    links.forEach(l =>
        l.addEventListener('click', () => {
            if (window.innerWidth <= 768) {
                menu.classList.remove('active');
                navWrapper.classList.remove('menu-open');
            }
        })
    );

    /* -- ferme si on clique hors du menu -- */
    document.addEventListener('click', e => {
        if (!navWrapper.contains(e.target) && menu.classList.contains('active')) {
            menu.classList.remove('active');
            navWrapper.classList.remove('menu-open');
        }
    });

    /* -- réinitialise quand on repasse en desktop -- */
    window.addEventListener('resize', () => {
        if (window.innerWidth > 768) {
            menu.classList.remove('active');
            navWrapper.classList.remove('menu-open');
        }
    });
});

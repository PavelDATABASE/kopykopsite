let currentSlide = 0;
let slides;
let dots;
let autoSlideInterval;

// Для свайпа
let touchStartX = 0;
let touchEndX = 0;

// Инициализация при загрузке
document.addEventListener('DOMContentLoaded', function () {
    slides = document.querySelectorAll('.carousel-slide');
    dots = document.querySelectorAll('.carousel-dot');

    // Запустить автоматическую прокрутку
    startAutoSlide();

    // Добавить обработчики для свайпа
    setupSwipe();
});

function showSlide(n) {
    // Скрываем все слайды
    slides.forEach(slide => slide.classList.remove('active'));
    dots.forEach(dot => dot.classList.remove('active'));

    // Вычисляем индекс
    if (n >= slides.length) currentSlide = 0;
    else if (n < 0) currentSlide = slides.length - 1;
    else currentSlide = n;

    // Показываем текущий слайд
    slides[currentSlide].classList.add('active');
    if (dots[currentSlide]) {
        dots[currentSlide].classList.add('active');
    }
}

function moveSlide(direction) {
    showSlide(currentSlide + direction);
    resetAutoSlide();
}

function goToSlide(n) {
    showSlide(n);
    resetAutoSlide();
}

function startAutoSlide() {
    autoSlideInterval = setInterval(() => {
        showSlide(currentSlide + 1);
    }, 4000);
}

function resetAutoSlide() {
    clearInterval(autoSlideInterval);
    startAutoSlide();
}

// Функция для обработки свайпа
function setupSwipe() {
    const carousel = document.querySelector('.carousel');

    carousel.addEventListener('touchstart', function (e) {
        touchStartX = e.changedTouches[0].screenX;
    }, { passive: true });

    carousel.addEventListener('touchend', function (e) {
        touchEndX = e.changedTouches[0].screenX;
        handleSwipe();
    }, { passive: true });
}

function handleSwipe() {
    const swipeThreshold = 50; // Минимальное расстояние для свайпа
    const diff = touchStartX - touchEndX;

    if (Math.abs(diff) > swipeThreshold) {
        if (diff > 0) {
            // Свайп влево - следующий слайд
            moveSlide(1);
        } else {
            // Свайп вправо - предыдущий слайд
            moveSlide(-1);
        }
    }
}

// Dropdown меню
document.addEventListener('DOMContentLoaded', function () {
    const dropdown = document.querySelector('.dropdown');

    if (!dropdown) return;

    const toggle = dropdown.querySelector('.dropdown-toggle');
    const menu = dropdown.querySelector('.dropdown-menu');

    // Определяем, поддерживает ли устройство hover (ПК) или нет (сенсорные)
    const isTouchDevice = !window.matchMedia('(hover: hover)').matches;

    if (isTouchDevice) {
        // Для сенсорных устройств - по клику
        toggle.addEventListener('click', function (e) {
            e.preventDefault();
            const isShown = menu.style.display === 'block';
            menu.style.display = isShown ? 'none' : 'block';
        });

        // Закрывать при клике вне меню
        document.addEventListener('click', function (e) {
            if (!dropdown.contains(e.target)) {
                menu.style.display = 'none';
            }
        });
    } else {
        // Для ПК - по наведению (оставляем CSS hover)
        // Никакой JS логики не нужно, всё работает через CSS
    }
});
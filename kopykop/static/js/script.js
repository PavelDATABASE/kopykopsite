let currentSlide =0;
let slides;
let dots;
let autoSlideInterval;

let touchStartX =0;
let touchEndX =0;

document.addEventListener('DOMContentLoaded', function () {
 slides = document.querySelectorAll('.carousel-slide');
 dots = document.querySelectorAll('.carousel-dot');

 if (slides.length >0) {
 startAutoSlide();
 setupSwipe();
 }
});

function showSlide(n) {
 slides.forEach(slide => slide.classList.remove('active'));
 dots.forEach(dot => dot.classList.remove('active'));

 if (n >= slides.length) currentSlide =0;
 else if (n< 0) currentSlide = slides.length -1;
 else currentSlide = n;

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
 showSlide(currentSlide +1);
 },4000);
}

function resetAutoSlide() {
 clearInterval(autoSlideInterval);
 startAutoSlide();
}

function setupSwipe() {
 const carousel = document.querySelector('.carousel');
 if (!carousel) return;

 carousel.addEventListener('touchstart', function (e) {
 touchStartX = e.changedTouches[0].screenX;
 }, { passive: true });

 carousel.addEventListener('touchend', function (e) {
 touchEndX = e.changedTouches[0].screenX;
 handleSwipe();
 }, { passive: true });
}

function handleSwipe() {
 const swipeThreshold =50;
 const diff = touchStartX - touchEndX;

 if (Math.abs(diff) > swipeThreshold) {
 if (diff >0) {
 moveSlide(1);
 } else {
 moveSlide(-1);
 }
 }
}

// Обработка формы заказа
const myForm = document.getElementById('MyForm');
if (myForm) {
 myForm.addEventListener('submit', function (e) {
 e.preventDefault();
 document.getElementById('window').classList.add('open');
 });
}

const closeWindowBtn = document.getElementById('closeWindow');
if (closeWindowBtn) {
 closeWindowBtn.addEventListener('click', function (e) {
 document.getElementById('window').classList.remove('open');
 });
}

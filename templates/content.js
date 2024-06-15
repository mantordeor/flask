let currentIndex = 0;

function showImage(index) {
    const images = document.querySelectorAll('.carousel-images img');
    if (index >= images.length) {
        index = 0;
    } else if (index < 0) {
        index = images.length - 1;
    }

    currentIndex = index;
    const offsetX = -index * 100;
    document.querySelector('.carousel-images').style.transform = `translateX(${offsetX}%)`;
}

function nextImage() {
    showImage(currentIndex + 1);
}

function prevImage() {
    showImage(currentIndex - 1);
}

function addToCart() {
    alert('商品已加入購物車！');
}

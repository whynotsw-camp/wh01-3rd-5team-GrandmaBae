document.addEventListener('DOMContentLoaded', function() {
    const rawData = sessionStorage.getItem('products');
    console.log('Raw sessionStorage data:', rawData);
    const productsData = rawData ? JSON.parse(rawData) : null;
    console.log('Parsed products data:', productsData);


    console.log('전체 body 내용:', document.body.innerHTML);

    const categoryContainer = document.getElementById('categoryContainer');
    console.log('categoryContainer:', categoryContainer);
    if (!categoryContainer) {
        console.error('카테고리 컨테이너를 DOM에서 찾을 수 없습니다');
        return;
    }

    if (productsData && productsData.length > 0) {
        // 기존의 제품 표시 로직
    } else {
        categoryContainer.innerHTML = '<p>상품 정보가 없습니다.</p>';
    }

    if (categoryContainer) {
        if (productsData && productsData.length > 0) {
            const categorizedProducts = {};
            
            productsData.forEach(product => {
                if (!categorizedProducts[product.category]) {
                    categorizedProducts[product.category] = [];
                }
                categorizedProducts[product.category].push(product);
            });
            
            for (const category in categorizedProducts) {
                const categorySection = document.createElement('div');
                categorySection.className = 'category-section';
                categorySection.innerHTML = `
                    <h2>${category}</h2>
                    <div class="products-container"></div>
                `;
                
                const productsContainer = categorySection.querySelector('.products-container');
                
                categorizedProducts[category].forEach(product => {
                    const productCard = document.createElement('div');
                    productCard.className = 'product-card';
                    productCard.innerHTML = `
                        <img src="${product.imageUrl}" alt="${product.name}" class="img-fluid">
                        <h5>${product.name}</h5>
                        <p>가격: ₩${typeof product.price === 'number' ? product.price.toLocaleString() : product.price}</p>
                    `;

                    productCard.addEventListener('click', function() {
                        const productData = {
                            id: product.product_id,
                            name: product.name,
                            price: product.price,
                            mainImage: product.mainImageURL,
                            additionalImages: product.additionalImagesURL,
                            category: product.category
                        };
                        sessionStorage.setItem('productDetail_' + product.product_id, JSON.stringify(productData));
                        window.location.href = `/detail?id=${product.product_id}`;
                    });
                    


                    productsContainer.appendChild(productCard);
                });

                
                
                categoryContainer.appendChild(categorySection);
            }
            console.log('분류된 제품:', categorizedProducts);

        } else {
            categoryContainer.innerHTML = '<p>상품 정보가 없습니다.</p>';
        }
    }

    const sidebarToggleBtn = document.getElementById('sidebarToggleBtn');
    const sidebar = document.getElementById('sidebar');
    const sidebarContent = document.querySelector('.sidebar-content');

    sidebar.classList.remove('hidden');
    loadSidebarContent();

    sidebarToggleBtn.addEventListener('click', function() {
        sidebar.classList.toggle('hidden');
        const icon = this.querySelector('i');
        icon.classList.toggle('fa-bars');
        icon.classList.toggle('fa-times');
    });

    function loadSidebarContent() {
        const videoSection = sidebarContent.querySelector('.video-section');

        // 크롭된 이미지 로드
        const yoloImageSection = document.getElementById('yolo-image-section');
        const croppedImage = sessionStorage.getItem('croppedImage');
        if (croppedImage) {
            const imgElement = document.createElement('img');
            imgElement.src = croppedImage.startsWith('data:image') ? croppedImage : `data:image/jpeg;base64,${croppedImage}`;
            imgElement.alt = "YOLO Detection 결과";
            yoloImageSection.innerHTML = '';
            yoloImageSection.appendChild(imgElement);
        } else {
            yoloImageSection.innerHTML = '<p>크롭된 이미지가 없습니다.</p>';
        }
    }
});

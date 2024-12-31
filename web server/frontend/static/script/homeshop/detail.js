document.addEventListener('DOMContentLoaded', function() {
    const urlParams = new URLSearchParams(window.location.search);
    const productId = urlParams.get('id');
    const productData = JSON.parse(sessionStorage.getItem('productDetail_' + productId));
    
    if (productData) {
        let mainContentHtml;
        if (productId === '12823710') {
            const videoUrl = 'https://lotteimall.soylive.net/?bdct_id=67523cf4a8c3c299a16581de&sy_id=67523cf4a8c3c299a16581de&sy_type=broadcast';
            mainContentHtml = `
                <iframe src="${videoUrl}" width="100%" height="650" frameborder="0" allowfullscreen></iframe>
            `;
        } else {
            mainContentHtml = `
                <img src="${productData.mainImage}" alt="${productData.name}" class="img-fluid">
            `;
        }

        // 메인 컨텐츠 렌더링
        document.getElementById('mainImageContainer').innerHTML = mainContentHtml;

        // 상품 정보 렌더링
        let productInfoHtml = `
            <h1>${productData.name}</h1>
            <p class="price">${productData.price}</p>
        `;

        // 방송 예정 정보 추가
        if (productId === '12825703') {
            productInfoHtml += `<p class="broadcast-info">방송예정 12.29(일) 22:35</p>`;
        }

        document.getElementById('productInfo').innerHTML = productInfoHtml;

        // 추가 이미지 렌더링
        const additionalImagesHtml = `
            <div class="additional-images">
                ${productData.additionalImages.map(img => `
                    <img src="${img}" alt="추가 이미지" class="img-thumbnail">
                `).join('')}
            </div>
        `;
        document.getElementById('additionalImages').innerHTML = additionalImagesHtml;
    } else {
        document.getElementById('productDetail').innerHTML = '<p>상품 정보를 찾을 수 없습니다.</p>';
    }
});

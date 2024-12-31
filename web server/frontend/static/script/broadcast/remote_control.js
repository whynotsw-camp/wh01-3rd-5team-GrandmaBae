// 리모콘 숫자 버튼 클릭 이벤트 핸들러 추가
// Flask 백엔드의 새 엔드포인트로 요청 보냄
// Flask 백엔드로 요청
// 응답은 fetch 호출 이후에 받아 response 변수에 저장


document.addEventListener('DOMContentLoaded', function() {
    const remoteButtons = document.querySelectorAll('.num-button');
    
    remoteButtons.forEach(button => {
        button.addEventListener('click', async function() {
            const number = parseInt(this.getAttribute('data-number')) - 1;
            sessionStorage.setItem('selectedButtonNumber', number);
            try {
                const response = await fetch('/get_box_coordinates', {
                    method: 'POST',
                    headers: {
                        'Content-Type': 'application/json',
                    },
                    body: JSON.stringify({ button_number: number }),
                    credentials: 'include'
                });
                if (response.ok) {
                    const data = await response.json();
                    console.log('API 응답:', data);
                    
                    if (data.cropped_image) {
                        sessionStorage.setItem('croppedImage', data.cropped_image);
                        console.log('크롭된 이미지가 세션 스토리지에 저장되었습니다.');
                    } else {
                        console.log('크롭된 이미지가 응답에 없습니다.');
                    }

                    if (data.products) {
                        sessionStorage.setItem('products', JSON.stringify(data.products));
                        console.log('제품 정보가 세션 스토리지에 저장되었습니다.');
                    } else {
                        console.log('제품 정보가 응답에 없습니다.');
                    }
                    
                    window.location.href = `/recommended_clothing?number=${number + 1}`;
                } else {
                    const errorText = await response.text();
                    console.error('Failed to get box coordinates. Server response:', errorText);
                }
            } catch (error) {
                console.error('Error:', error);
            }
        });
    });
});


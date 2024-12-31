const aiServiceBtn = document.getElementById('aiServiceBtn');
const canvas = document.getElementById('canvas');
const ctx = canvas.getContext('2d');
const resultImage = document.getElementById('resultImage');

aiServiceBtn.addEventListener('click', async (event) => {
    event.preventDefault();
    event.stopPropagation();
    console.log('AI 구매 버튼이 클릭되었습니다.');

    const video = document.getElementById('videoPlayer');

    // 비디오 일시 정지
    video.pause();

    // 동영상 캡처
    canvas.width = video.videoWidth;
    canvas.height = video.videoHeight;
    ctx.drawImage(video, 0, 0, canvas.width, canvas.height);

    // 캡처된 이미지를 Blob으로 변환
    const imageBlob = await new Promise(resolve => canvas.toBlob(resolve, 'image/jpeg'));

    // Flask 서버로 전송
    const formData = new FormData();
    formData.append('file', imageBlob, 'capture.jpg');

    try {
        const response = await fetch('/process_image', {
            method: 'POST',
            body: formData,
        });

        if (response.ok) {
            const result = await response.json();
            console.log('API 응답:', result);

            if (result.annotated_image) {
                video.style.display = 'none';
                // Base64 이미지 데이터를 직접 사용
                resultImage.src = `data:image/jpeg;base64,${result.annotated_image}`;
                resultImage.style.display = 'block';
                resultImage.style.position = 'absolute';
                resultImage.style.top = '0';
                resultImage.style.left = '0';
                resultImage.style.width = '100%';
                resultImage.style.height = '100%';
                resultImage.style.objectFit = 'contain';
                resultImage.style.zIndex = '1000';
                console.log('결과 이미지 로드됨');

                resultImage.onload = () => {
                    console.log('결과 이미지가 로드되었습니다.');
                };
                resultImage.onerror = (e) => console.error('이미지 로드 실패:', e);
            } else {
                console.error('annotated_image 데이터가 응답에 없습니다.');
            }
            
            console.log('Detected persons:', result.boxes);
        } else {
            console.error('서버 응답 오류:', response.status, response.statusText);
            const errorBody = await response.text();
            console.error('오류 응답 내용:', errorBody);
        }
    } catch (error) {
        console.error('이미지 처리 중 오류:', error);
        alert('이미지 처리 중 오류가 발생했습니다: ' + error.message);
    }
});

// 페이지 언로드 방지
window.onbeforeunload = function() {
    return "변경사항이 저장되지 않을 수 있습니다.";
};

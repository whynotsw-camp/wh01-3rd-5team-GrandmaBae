document.addEventListener('DOMContentLoaded', function() {
   // DOMContentLoaded 이벤트 사용 이유
   // DOM이 완전히 로드되고 파싱된 후에 JavaScript 코드 실행 위해(HTML 문서의 구조가 완성되었음을 보장)

   const video = document.getElementById('videoPlayer');
   const playBtn = document.getElementById('playBtn');
   const stopBtn = document.getElementById('stopBtn');
   const timeline = document.getElementById('timeline');

   // 비디오 메타데이터 로드 후 타임라인 설정
   video.addEventListener('loadedmetadata', () => {
      timeline.max = Math.floor(video.duration);
   });
   
   // 현재 재생 시간 업데이트
   video.addEventListener('timeupdate', () => {
      timeline.value = Math.floor(video.currentTime);
   });

   // 비디오 재생 중 데이터 로딩이 멈췄을 때 처리
   video.addEventListener('stalled', () => {
      console.warn('비디오 데이터 로드가 멈췄습니다.');
   });

   // 비디오 재생 중 오류 처리
   video.addEventListener('error', (e) => {
      console.error('비디오 로드 오류:', e);
   });

   // 타임라인 이동 시 재생 위치 변경
   timeline.addEventListener('input', () => {
      video.currentTime = timeline.value;
   });

   // 재생 버튼 클릭 시 비디오 재생
   playBtn.addEventListener('click', () => {
      video.play().catch(e => console.error('재생 오류:', e));
   });

   // 정지 버튼 클릭 시 비디오 정지 및 시간 초기화
   stopBtn.addEventListener('click', () => {
      video.pause();
      video.currentTime = 0;
   });
});

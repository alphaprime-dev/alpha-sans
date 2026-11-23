# AlphaSans

## 웹폰트 적용 방법

AlphaSans를 웹폰트로 사용하시려면 2가지 방법이 있습니다.

스타일 시트에 아래의 코드를 넣거나,

```css
@import url(https://file.alphaprime.co.kr/AlphaSans/alpha-sans.css);
```

혹은 HTML의 `<head>` 태그 안에 아래의 코드를 넣어주세요.

```html
<link
  href="https://file.alphaprime.co.kr/AlphaSans/alpha-sans.css"
  rel="stylesheet"
  type="text/css"
/>
```

그후 `<style>` 태그 안에 `font-family` 를 설정해주세요.

```css
* {
  font-family: AlphaSans, sans-serif;
}
```

## 작은 등락 삼각형

`▴`(U+25B4)와 `▾`(U+25BE)는 AlphaSans의 기존 `▲` 윤곽을 66%로
축소해 만든 기호입니다. 아래쪽 기호는 같은 좌표를 뒤집어 두 기호의 크기를
맞췄습니다. 외부 폰트의 글리프는 사용하지 않습니다.

5개 굵기의 원본 기호를 다시 생성하려면 fonttools 설치 후 다음을 실행합니다.

```bash
python scripts/add_small_triangles.py
bash build_subset
```

원본 TTF와 `Subset`의 TTF·WOFF·WOFF2를 함께 커밋합니다.
`main`에 푸시하면 기존 GitHub Actions가 서브셋을 S3에 업로드하고
CloudFront 캐시를 무효화하므로, 병합 시점이 배포 시점입니다.

## 의견 보내기

AlphaSans 프로젝트에 제안하고 싶은 사항이 있다면 이슈를 생성해주시길 바랍니다.

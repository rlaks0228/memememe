# app.py
import json
import random
import mimetypes
from pathlib import Path
import streamlit as st
import streamlit.components.v1 as components

BASE = Path(__file__).parent
MEME_DIR = BASE / "memes"
META_FILE = BASE / "metadata.json"

def load_memes():
    if not META_FILE.exists():
        return []
    with open(META_FILE, "r", encoding="utf-8") as f:
        return json.load(f)

memes = load_memes()

st.set_page_config(page_title="기분별 짤 추천기", layout="centered")
st.title("🎭 기분별 짤 추천기")

# 태그 목록 만들기
all_tags = sorted({t for m in memes for t in m.get("tags", [])})

if not all_tags:
    st.warning("metadata.json에 태그가 없습니다. memes 폴더와 metadata.json을 확인하세요.")
else:
    selected = st.selectbox("원하는 기분/상황을 선택하세요", all_tags)
    if st.button("짤 추천받기"):
        candidates = [m for m in memes if selected in m.get("tags", [])]
        if not candidates:
            st.info("해당 태그의 짤이 없습니다.")
        else:
            m = random.choice(candidates)
            img_path = MEME_DIR / m["filename"]
            if img_path.exists():
                # 이미지 표시
                st.image(str(img_path), use_column_width=True)

                # 다운로드 버튼 (파일 바이트를 읽어서 제공)
                with open(img_path, "rb") as f:
                    img_bytes = f.read()
                mime, _ = mimetypes.guess_type(img_path)
                if mime is None:
                    mime = "application/octet-stream"
                st.download_button("다운로드", data=img_bytes, file_name=m["filename"], mime=mime)

                # 이미지 경로를 보여주고 복사 버튼 제공
                img_abs = str(img_path.resolve())
                st.text_input("이미지 경로 (복사 가능)", value=img_abs, key="img_path")
                copy_js = f"""
                <script>
                function copyText(text) {{
                  navigator.clipboard.writeText(text);
                  alert("클립보드에 경로가 복사되었습니다.");
                }}
                </script>
                <button onclick="copyText('{img_abs}')">경로 복사</button>
                """
                components.html(copy_js, height=70)
            else:
                st.error("이미지 파일을 찾을 수 없습니다: " + str(img_path))

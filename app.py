# app.py (감정 검색 기능 추가)
import json
import random
import mimetypes
from pathlib import Path
import streamlit as st

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
    # 🔍 검색창으로 감정 필터링
    search = st.text_input("원하는 기분/상황을 검색하세요")

    if search:
        filtered_tags = [t for t in all_tags if search.lower() in t.lower()]
        if not filtered_tags:
            st.info("검색 결과가 없습니다.")
    else:
        filtered_tags = all_tags

    # 선택 가능한 태그 보여주기
    selected = st.selectbox("검색 결과에서 선택하세요", filtered_tags)

    # 짤 추천 버튼
    if st.button("짤 추천받기"):
        candidates = [m for m in memes if selected in m.get("tags", [])]
        if not candidates:
            st.info("해당 태그의 짤이 없습니다.")
        else:
            m = random.choice(candidates)
            img_path = MEME_DIR / m["filename"]
            if img_path.exists():
                # 이미지 표시
                st.image(str(img_path), use_container_width=True)

                # 다운로드 버튼
                with open(img_path, "rb") as f:
                    img_bytes = f.read()
                mime, _ = mimetypes.guess_type(img_path)
                if mime is None:
                    mime = "application/octet-stream"
                st.download_button("다운로드", data=img_bytes, file_name=m["filename"], mime=mime)
            else:
                st.error("이미지 파일을 찾을 수 없습니다: " + str(img_path))
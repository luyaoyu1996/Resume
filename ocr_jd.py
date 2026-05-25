"""
批量 OCR 脚本 - 识别 0511投递/ 目录下所有 JPG 的 JD 文本
输出：0511投递/JD汇总.md

依赖：pip install rapidocr-onnxruntime
    (首次运行会自动下载约 15MB 的模型，离线)
"""
from pathlib import Path
import sys

try:
    from rapidocr_onnxruntime import RapidOCR
except ImportError:
    print("[!] 未安装 rapidocr-onnxruntime")
    print("[!] 请先运行: pip install rapidocr-onnxruntime")
    sys.exit(1)


# ========== 配置 ==========
INPUT_DIR = Path(r"c:\project\Resume\0511投递")
OUTPUT_FILE = INPUT_DIR / "JD汇总.md"
IMAGE_EXTS = {".jpg", ".jpeg", ".png", ".webp"}


def main():
    if not INPUT_DIR.exists():
        print(f"[!] 目录不存在: {INPUT_DIR}")
        sys.exit(1)

    # 按文件名排序（保持截图顺序）
    images = sorted(
        p for p in INPUT_DIR.iterdir()
        if p.is_file() and p.suffix.lower() in IMAGE_EXTS
    )

    if not images:
        print(f"[!] 目录下没有图片: {INPUT_DIR}")
        sys.exit(1)

    print(f"[+] 发现 {len(images)} 张图片，开始 OCR...")

    # 初始化 OCR 引擎
    print("[+] 加载 OCR 模型（首次会下载 ~15MB）...")
    ocr = RapidOCR()

    results = []
    for idx, img_path in enumerate(images, 1):
        print(f"[{idx}/{len(images)}] {img_path.name}")
        try:
            result, _ = ocr(str(img_path))
            if result:
                # result 是 [[box, text, confidence], ...]
                lines = [item[1] for item in result]
                text = "\n".join(lines)
            else:
                text = "(未识别到文本)"
        except Exception as e:
            text = f"(OCR 失败: {e})"

        results.append({
            "idx": idx,
            "filename": img_path.name,
            "text": text,
        })

    # 写出汇总 md
    with OUTPUT_FILE.open("w", encoding="utf-8") as f:
        f.write(f"# 0511 投递 JD 汇总\n\n")
        f.write(f"共 {len(results)} 份 JD，来自 {INPUT_DIR}\n\n")
        f.write("---\n\n")
        for r in results:
            f.write(f"## 【{r['idx']}】{r['filename']}\n\n")
            f.write("```\n")
            f.write(r["text"])
            f.write("\n```\n\n")
            f.write("---\n\n")

    print(f"\n[OK] Done! Output: {OUTPUT_FILE}")
    print(f"[OK] Recognized {len(results)} JDs")


if __name__ == "__main__":
    main()

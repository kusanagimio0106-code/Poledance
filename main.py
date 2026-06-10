import flet as ft
import random
import time

def main(page: ft.Page):
    page.title = "Pole Dance Notebook"
    page.theme_mode = ft.ThemeMode.DARK
    page.horizontal_alignment = ft.CrossAxisAlignment.CENTER
    page.scroll = "adaptive"

    # Cấu hình PWA để né lỗi chữ P và hiện icon múa cột của bạn
    page.web_app_manifest = {
        "name": "Pole Dance Notebook",
        "short_name": "Pole Dance",
        "theme_color": "#e91e63",
        "background_color": "#111111",
        "display": "standalone",
        "icons": [
            {
                "src": "icons/icon_app.png",
                "sizes": "512x512",
                "type": "image/png",
                "purpose": "any maskable"
            }
        ]
    }

    # Treo màn hình chờ 2 giây để ngắm ảnh loading-animation.gif của bạn
    page.update()
    time.sleep(2)
    
    # 1. KHO DỮ LIỆU GỐC (Lưu tên và độ khó ⭐)
    kho_trick = {
        "Intro": [
            {"name": "Đi bộ quanh cột", "difficulty": 1},
            {"name": "Xoay hông dạo đầu", "difficulty": 1}
        ],
        "Main Trick": [
            {"name": "Superman", "difficulty": 4},
            {"name": "Scorpio", "difficulty": 3}
        ],
        "Outro": [
            {"name": "Floorwork", "difficulty": 2}
        ]
    }

    # Hàm hỗ trợ hiển thị chuỗi sao ⭐
    def get_star_string(level):
        return "⭐" * int(level)

    # --- CÁC THÀNH PHẦN HIỂN THỊ DANH SÁCH ---
    group_intro = ft.ExpansionTile(title=ft.Text("Intro 🎬", size=18, weight="bold", color=ft.Colors.PINK_300))
    group_main = ft.ExpansionTile(title=ft.Text("Main Trick 💎", size=18, weight="bold", color=ft.Colors.PURPLE_300))
    group_outro = ft.ExpansionTile(title=ft.Text("Outro 🏁", size=18, weight="bold", color=ft.Colors.BLUE_300))

    def update_list_view():
        # Xoá cũ nạp mới
        group_intro.controls = []
        group_main.controls = []
        group_outro.controls = []

        for item in kho_trick["Intro"]:
            group_intro.controls.append(ft.ListTile(
                title=ft.Text(item["name"], weight="bold"),
                subtitle=ft.Text(get_star_string(item["difficulty"]), color=ft.Colors.YELLOW_400),
                leading=ft.Icon(ft.Icons.PLAY_ARROW_ROUNDED, color=ft.Colors.PINK_300)
            ))
        for item in kho_trick["Main Trick"]:
            group_main.controls.append(ft.ListTile(
                title=ft.Text(item["name"], weight="bold"),
                subtitle=ft.Text(get_star_string(item["difficulty"]), color=ft.Colors.YELLOW_400),
                leading=ft.Icon(ft.Icons.DIAMOND_OUTLINED, color=ft.Colors.PURPLE_300)
            ))
        for item in kho_trick["Outro"]:
            group_outro.controls.append(ft.ListTile(
                title=ft.Text(item["name"], weight="bold"),
                subtitle=ft.Text(get_star_string(item["difficulty"]), color=ft.Colors.YELLOW_400),
                leading=ft.Icon(ft.Icons.FLAG_OUTLINED, color=ft.Colors.BLUE_300)
            ))
        page.update()

    # --- HIỂN THỊ RANDOM COMBO ---
    txt_combo_intro = ft.Text("Intro: ---", size=16, color=ft.Colors.PINK_100)
    txt_combo_main = ft.Text("Main Trick: ---", size=16, color=ft.Colors.PURPLE_100, weight="bold")
    txt_combo_outro = ft.Text("Outro: ---", size=16, color=ft.Colors.BLUE_100)

    def generate_random_combo(e):
        if all(len(kho_trick[k]) > 0 for k in ["Intro", "Main Trick", "Outro"]):
            t_intro = random.choice(kho_trick["Intro"])
            t_main = random.choice(kho_trick["Main Trick"])
            t_outro = random.choice(kho_trick["Outro"])
            
            txt_combo_intro.value = f"🎬 {t_intro['name']} ({get_star_string(t_intro['difficulty'])})"
            txt_combo_main.value = f"💎 {t_main['name']} ({get_star_string(t_main['difficulty'])})"
            txt_combo_outro.value = f"🏁 {t_outro['name']} ({get_star_string(t_outro['difficulty'])})"
        else:
            txt_combo_main.value = "⚠️ Hãy thêm đủ trick vào 3 nhóm!"
        page.update()

    # --- GIAO DIỆN POPUP THÊM TRICK ---
    input_name = ft.TextField(label=" Tên động tác", hint_text="Ví dụ: Superman...")
    dropdown_type = ft.Dropdown(
        label="Nhóm",
        options=[ft.dropdown.Option("Intro"), ft.dropdown.Option("Main Trick"), ft.dropdown.Option("Outro")],
    )
    # Thanh chọn độ khó từ 1 đến 5
    slider_diff = ft.Slider(min=1, max=5, divisions=4, label="Độ khó: {value} sao", value=3, active_color=ft.Colors.YELLOW_700)

    def save_trick(e):
        if input_name.value and dropdown_type.value:
            kho_trick[dropdown_type.value].append({
                "name": input_name.value,
                "difficulty": int(slider_diff.value)
            })
            update_list_view()
            dialog.open = False
            # Reset form
            input_name.value = ""
            dropdown_type.value = None
            slider_diff.value = 3
            page.update()

    dialog = ft.AlertDialog(
        title=ft.Text("Thêm Trick Mới ⭐"),
        content=ft.Column([
            input_name, 
            dropdown_type, 
            ft.Text("Độ khó (1-5 sao):", size=14, color=ft.Colors.WHITE54),
            slider_diff
        ], tight=True, spacing=15),
        actions=[
            ft.TextButton("Hủy", on_click=lambda _: setattr(dialog, "open", False) or page.update()),
            ft.ElevatedButton("LƯU LẠI", bgcolor=ft.Colors.PINK_500, color=ft.Colors.WHITE, on_click=save_trick),
        ],
    )
    page.overlay.append(dialog)

    # --- GIAO DIỆN CHÍNH ---
    page.add(
        ft.Text("POLE DANCE NOTEBOOK", size=24, weight="bold"),
        ft.Divider(height=5, color=ft.Colors.TRANSPARENT),  # ĐÃ SỬA LỖI VIẾT THIẾU COLORS
        
        # Khung Combo
        ft.Container(
            content=ft.Column([
                ft.Text("COMBO HÔM NAY:", size=12, color=ft.Colors.WHITE54, weight="bold"),
                txt_combo_intro, txt_combo_main, txt_combo_outro
            ], spacing=8),
            padding=15, border_radius=12, bgcolor=ft.Colors.WHITE10, width=320
        ),
        ft.Divider(height=10, color=ft.Colors.TRANSPARENT),
        
        ft.ElevatedButton("XOAY COMBO NGẪU NHIÊN 🎲", bgcolor=ft.Colors.PINK_500, color=ft.Colors.WHITE, on_click=generate_random_combo, width=280),
        
        ft.Divider(height=15, color=ft.Colors.WHITE24),
        
        # Nút mở Popup thêm trick
        ft.OutlinedButton(
            "THÊM TRICK MỚI", icon=ft.Icons.ADD,
            style=ft.ButtonStyle(color=ft.Colors.PINK_300),
            on_click=lambda _: setattr(dialog, "open", True) or page.update(), width=220
        ),
        
        ft.Divider(height=10, color=ft.Colors.TRANSPARENT),  # ĐÃ SỬA LỖI VIẾT THIẾU COLORS
        ft.Text("KHO TRICK CỦA BẠN", size=14, color=ft.Colors.WHITE54, weight=bold"),
        ft.Column([group_intro, group_main, group_outro], spacing=5, width=320)
    )

    update_list_view()

ft.app(target=main)

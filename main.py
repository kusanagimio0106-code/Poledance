import flet as ft
import random
import time
import json
import urllib.request

# 🌟 ĐIỀN 2 THÔNG SỐ SUPABASE CỦA BẠN VÀO ĐÂY:
SUPABASE_URL = "https://acumyjqadlqbyboacqgw.supabase.co"  # Thay bằng URL của bạn
SUPABASE_KEY = "sb_publishable_4WUvqixWWaF8eyjU8FIiZg_O-HPtpxS"  # Thay bằng Key của bạn

def main(page: ft.Page):
    page.title = "Pole Dance Notebook"
    page.theme_mode = ft.ThemeMode.DARK
    page.horizontal_alignment = ft.CrossAxisAlignment.CENTER
    page.scroll = "adaptive"

    # Kho dữ liệu mặc định dự phòng nếu mạng lỗi
    kho_trick = {
        "Intro": [{"name": "Đi bộ quanh cột", "difficulty": 1}, {"name": "Xoay hông dạo đầu", "difficulty": 1}],
        "Main Trick": [{"name": "Superman", "difficulty": 4}, {"name": "Scorpio", "difficulty": 3}],
        "Outro": [{"name": "Floorwork", "difficulty": 2}]
    }

    # --- CƠ CHẾ ĐỒNG BỘ MỚI CHO GIAO DIỆN SUPABASE PUBLISHABLE KEY ---
    def save_to_storage():
        try:
            json_str = json.dumps(kho_trick, ensure_ascii=False)
            payload = json.dumps({"value": json_str}).encode("utf-8")
            
            # Đổi từ dùng RPC sang sửa thẳng vào bảng notebook qua ID=1
            req = urllib.request.Request(
                f"{SUPABASE_URL}/rest/v1/notebook?id=eq.1",
                data=payload,
                headers={
                    "apikey": SUPABASE_KEY, 
                    "Authorization": f"Bearer {SUPABASE_KEY}", 
                    "Content-Type": "application/json", 
                    "Prefer": "resolution=merge-dup"
                },
                method="POST" # Ép kiểu POST để Supabase hiểu là Update/Insert dữ liệu
            )
            urllib.request.urlopen(req)
        except Exception as ex:
            print("Lỗi lưu database:", ex)

    def load_from_storage():
        nonlocal kho_trick
        try:
            req = urllib.request.Request(
                f"{SUPABASE_URL}/rest/v1/notebook?id=eq.1&select=value",
                headers={
                    "apikey": SUPABASE_KEY, 
                    "Authorization": f"Bearer {SUPABASE_KEY}"
                }
            )
            with urllib.request.urlopen(req) as response:
                res_data = json.loads(response.read().decode("utf-8"))
                if res_data and len(res_data) > 0:
                    json_str = res_data[0]["value"]
                    kho_trick = json.loads(json_str)
        except Exception as ex:
            print("Lỗi tải database:", ex)

    # Trước khi chạy, tụi mình cần Supabase tự tạo cấu trúc nếu bạn chưa tạo bảng ngoài giao diện
    # Để bạn KHÔNG CẦN bấm tạo bảng bằng tay trên web Supabase, đoạn code này sẽ tự động lo:
    def init_database_table():
        try:
            # Tự động gửi một lệnh khởi tạo bảng lên Supabase
            init_payload = json.dumps({"id": 1, "value": json.dumps(kho_trick, ensure_ascii=False)}).encode("utf-8")
            req = urllib.request.Request(
                f"{SUPABASE_URL}/rest/v1/notebook",
                data=init_payload,
                headers={"apikey": SUPABASE_KEY, "Authorization": f"Bearer {SUPABASE_KEY}", "Content-Type": "application/json", "Prefer": "resolution=ignore-dup"}
            )
            urllib.request.urlopen(req)
        except:
            pass

    # Kích hoạt chuỗi kết nối đám mây
    init_database_table()
    load_from_storage()

    # --- ĐOẠN CODE GIAO DIỆN CHỨC NĂNG (GIỮ NGUYÊN HOÀN HẢO CỦA BẠN) ---
    editing_trick_info = None
    def get_star_string(level): return "⭐" * int(level)

    def delete_trick(category, trick_item):
        for index, item in enumerate(kho_trick[category]):
            if item["name"] == trick_item["name"]:
                kho_trick[category].pop(index)
                break
        save_to_storage()
        update_list_view()

    def open_edit_dialog(category, trick_item):
        nonlocal editing_trick_info
        editing_trick_info = {"category": category, "item": trick_item}
        input_edit_name.value = trick_item["name"]
        slider_edit_diff.value = trick_item["difficulty"]
        edit_dialog.open = True
        page.update()

    group_intro = ft.ExpansionTile(title=ft.Text("Intro 🎬", size=18, weight="bold", color=ft.Colors.PINK_300))
    group_main = ft.ExpansionTile(title=ft.Text("Main Trick 💎", size=18, weight="bold", color=ft.Colors.PURPLE_300))
    group_outro = ft.ExpansionTile(title=ft.Text("Outro 🏁", size=18, weight="bold", color=ft.Colors.BLUE_300))

    def update_list_view():
        group_intro.controls = []
        group_main.controls = []
        group_outro.controls = []
        def make_delete_callback(cat, it): return lambda e: delete_trick(cat, it)
        def make_edit_callback(cat, it): return lambda e: open_edit_dialog(cat, it)

        for item in kho_trick["Intro"]:
            group_intro.controls.append(ft.ListTile(
                title=ft.Text(item["name"], weight="bold"),
                subtitle=ft.Text(get_star_string(item["difficulty"]), color=ft.Colors.YELLOW_400),
                leading=ft.Icon(ft.Icons.PLAY_ARROW_ROUNDED, color=ft.Colors.PINK_300),
                trailing=ft.Row([
                    ft.IconButton(ft.Icons.EDIT_ROUNDED, icon_color=ft.Colors.WHITE54, icon_size=18, on_click=make_edit_callback("Intro", item)),
                    ft.IconButton(ft.Icons.DELETE_OUTLINE_ROUNDED, icon_color=ft.Colors.RED_400, icon_size=18, on_click=make_delete_callback("Intro", item))
                ], tight=True, spacing=0)
            ))
        for item in kho_trick["Main Trick"]:
            group_main.controls.append(ft.ListTile(
                title=ft.Text(item["name"], weight="bold"),
                subtitle=ft.Text(get_star_string(item["difficulty"]), color=ft.Colors.YELLOW_400),
                leading=ft.Icon(ft.Icons.DIAMOND_OUTLINED, color=ft.Colors.PURPLE_300),
                trailing=ft.Row([
                    ft.IconButton(ft.Icons.EDIT_ROUNDED, icon_color=ft.Colors.WHITE54, icon_size=18, on_click=make_edit_callback("Main Trick", item)),
                    ft.IconButton(ft.Icons.DELETE_OUTLINE_ROUNDED, icon_color=ft.Colors.RED_400, icon_size=18, on_click=make_delete_callback("Main Trick", item))
                ], tight=True, spacing=0)
            ))
        for item in kho_trick["Outro"]:
            group_outro.controls.append(ft.ListTile(
                title=ft.Text(item["name"], weight="bold"),
                subtitle=ft.Text(get_star_string(item["difficulty"]), color=ft.Colors.YELLOW_400),
                leading=ft.Icon(ft.Icons.FLAG_OUTLINED, color=ft.Colors.BLUE_300),
                trailing=ft.Row([
                    ft.IconButton(ft.Icons.EDIT_ROUNDED, icon_color=ft.Colors.WHITE54, icon_size=18, on_click=make_edit_callback("Outro", item)),
                    ft.IconButton(ft.Icons.DELETE_OUTLINE_ROUNDED, icon_color=ft.Colors.RED_400, icon_size=18, on_click=make_delete_callback("Outro", item))
                ], tight=True, spacing=0)
            ))
        page.update()

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

    input_name = ft.TextField(label="Tên động tác", hint_text="Ví dụ: Superman...")
    dropdown_type = ft.Dropdown(label="Nhóm", options=[ft.dropdown.Option("Intro"), ft.dropdown.Option("Main Trick"), ft.dropdown.Option("Outro")])
    slider_diff = ft.Slider(min=1, max=5, divisions=4, label="Độ khó: {value} sao", value=3, active_color=ft.Colors.YELLOW_700)

    def save_trick(e):
        if input_name.value and dropdown_type.value:
            kho_trick[dropdown_type.value].append({"name": input_name.value, "difficulty": int(slider_diff.value)})
            save_to_storage()
            update_list_view()
            dialog.open = False
            input_name.value = ""
            dropdown_type.value = None
            slider_diff.value = 3
            page.update()

    dialog = ft.AlertDialog(
        title=ft.Text("Thêm Trick Mới ⭐"),
        content=ft.Column([input_name, dropdown_type, ft.Text("Độ khó (1-5 sao):", size=14, color=ft.Colors.WHITE54), slider_diff], tight=True, spacing=15),
        actions=[ft.TextButton("Hủy", on_click=lambda _: setattr(dialog, "open", False) or page.update()), ft.ElevatedButton("LƯU LẠI", bgcolor=ft.Colors.PINK_500, color=ft.Colors.WHITE, on_click=save_trick)]
    )
    page.overlay.append(dialog)

    input_edit_name = ft.TextField(label="Tên động tác", hint_text="Sửa tên...")
    slider_edit_diff = ft.Slider(min=1, max=5, divisions=4, label="Độ khó: {value} sao", value=3, active_color=ft.Colors.YELLOW_700)

    def save_edited_trick(e):
        nonlocal editing_trick_info
        if input_edit_name.value and editing_trick_info:
            category = editing_trick_info["category"]
            old_item = editing_trick_info["item"]
            old_item["name"] = input_edit_name.value
            old_item["difficulty"] = int(slider_edit_diff.value)
            save_to_storage()
            update_list_view()
            edit_dialog.open = False
            editing_trick_info = None
            page.update()

    edit_dialog = ft.AlertDialog(
        title=ft.Text("Chỉnh Sửa Trick ✏️"),
        content=ft.Column([input_edit_name, ft.Text("Thay đổi độ khó (1-5 sao):", size=14, color=ft.Colors.WHITE54), slider_edit_diff], tight=True, spacing=15),
        actions=[ft.TextButton("Hủy", on_click=lambda _: setattr(edit_dialog, "open", False) or page.update()), ft.ElevatedButton("CẬP NHẬT", bgcolor=ft.Colors.PINK_500, color=ft.Colors.WHITE, on_click=save_edited_trick)]
    )
    page.overlay.append(edit_dialog)

    page.add(
        ft.Text("POLE DANCE NOTEBOOK", size=24, weight="bold"),
        ft.Divider(height=5, color=ft.Colors.TRANSPARENT),
        ft.Container(
            content=ft.Column([ft.Text("COMBO HÔM NAY:", size=12, color=ft.Colors.WHITE54, weight="bold"), txt_combo_intro, txt_combo_main, txt_combo_outro], spacing=8),
            padding=15, border_radius=12, bgcolor=ft.Colors.WHITE10, width=320
        ),
        ft.Divider(height=10, color=ft.Colors.TRANSPARENT),
        ft.ElevatedButton("XOAY COMBO NGẪU NHIÊN 🎲", bgcolor=ft.Colors.PINK_500, color=ft.Colors.WHITE, on_click=generate_random_combo, width=280),
        ft.Divider(height=15, color=ft.Colors.WHITE24),
        ft.OutlinedButton("THÊM TRICK MỚI", icon=ft.Icons.ADD, style=ft.ButtonStyle(color=ft.Colors.PINK_300), on_click=lambda _: setattr(dialog, "open", True) or page.update(), width=220),
        ft.Divider(height=10, color=ft.Colors.TRANSPARENT),
        ft.Text("KHO TRICK CỦA BẠN", size=14, color=ft.Colors.WHITE54, weight="bold"),
        ft.Column([group_intro, group_main, group_outro], spacing=5, width=320)
    )
    update_list_view()

ft.app(target=main)

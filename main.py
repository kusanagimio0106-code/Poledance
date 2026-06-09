import flet as ft
import random

def main(page: ft.Page):
    page.title = "Pole Dance Notebook"
    page.theme_mode = ft.ThemeMode.DARK
    page.horizontal_alignment = ft.CrossAxisAlignment.CENTER
    page.scroll = "adaptive"
    
    # 1. KHO DỮ LIỆU CÓ SẴN (BẠN CÓ THỂ THÊM BẰNG APP)
    kho_trick = {
        "Intro": [
            {"name": "Đi bộ quanh cột", "video": "Walk_around.mp4"},
            {"name": "Xoay hông dạo đầu", "video": "Hip_roll.mp4"},
            {"name": "Hook xoay", "video": "No Video"}
        ],
        "Main Trick": [
            {"name": "Superman", "video": "Superman.mp4"},
            {"name": "Gemini", "video": "No Video"},
            {"name": "Inverted Scorpio", "video": "Invert.mp4"}
        ],
        "Outro": [
            {"name": "Floorwork kết bài", "video": "Floor.mp4"},
            {"name": "Slide xuống nhẹ nhàng", "video": "No Video"}
        ]
    }

    # --- CÁC THÀNH PHẦN HIỂN THỊ DANH SÁCH ---
    group_intro = ft.ExpansionTile(
        title=ft.Text("Intro 🎬", size=18, weight=ft.FontWeight.BOLD, color=ft.Colors.PINK_300)
    )
    group_main = ft.ExpansionTile(
        title=ft.Text("Main Trick 💎", size=18, weight=ft.FontWeight.BOLD, color=ft.Colors.PURPLE_300)
    )
    group_outro = ft.ExpansionTile(
        title=ft.Text("Outro 🏁", size=18, weight=ft.FontWeight.BOLD, color=ft.Colors.BLUE_300)
    )

    def update_list_view():
        if group_intro.controls is None: group_intro.controls = []
        else: group_intro.controls.clear()
            
        if group_main.controls is None: group_main.controls = []
        else: group_main.controls.clear()
            
        if group_outro.controls is None: group_outro.controls = []
        else: group_outro.controls.clear()

        # Nạp dữ liệu mới
        for item in kho_trick["Intro"]:
            icon_video = ft.Icons.VIDEO_CAMERA_FRONT if item["video"] != "No Video" else ft.Icons.LINK_OFF
            group_intro.controls.append(ft.ListTile(leading=ft.Icon(icon_video, color=ft.Colors.PINK_300), title=ft.Text(item["name"], weight=ft.FontWeight.BOLD)))

        for item in kho_trick["Main Trick"]:
            icon_video = ft.Icons.VIDEO_CAMERA_FRONT if item["video"] != "No Video" else ft.Icons.LINK_OFF
            group_main.controls.append(ft.ListTile(leading=ft.Icon(icon_video, color=ft.Colors.PURPLE_300), title=ft.Text(item["name"], weight=ft.FontWeight.BOLD)))

        for item in kho_trick["Outro"]:
            icon_video = ft.Icons.VIDEO_CAMERA_FRONT if item["video"] != "No Video" else ft.Icons.LINK_OFF
            group_outro.controls.append(ft.ListTile(leading=ft.Icon(icon_video, color=ft.Colors.BLUE_300), title=ft.Text(item["name"], weight=ft.FontWeight.BOLD)))
        page.update()

    # --- THÀNH PHẦN HIỂN THỊ KẾT QUẢ RANDOM COMBO ---
    txt_combo_intro = ft.Text("Intro: ---", size=16, color=ft.Colors.PINK_200)
    txt_combo_main = ft.Text("Main Trick: ---", size=16, color=ft.Colors.PURPLE_200, weight=ft.FontWeight.BOLD)
    txt_combo_outro = ft.Text("Outro: ---", size=16, color=ft.Colors.BLUE_200)

    # Hàm xử lý bốc ngẫu nhiên combo
    def generate_random_combo(e):
        if len(kho_trick["Intro"]) > 0 and len(kho_trick["Main Trick"]) > 0 and len(kho_trick["Outro"]) > 0:
            trick_intro = random.choice(kho_trick["Intro"])["name"]
            trick_main = random.choice(kho_trick["Main Trick"])["name"]
            trick_outro = random.choice(kho_trick["Outro"])["name"]
            
            txt_combo_intro.value = f"🎬 {trick_intro}"
            txt_combo_main.value = f"💎 {trick_main}"
            txt_combo_outro.value = f"🏁 {trick_outro}"
        else:
            txt_combo_main.value = "⚠️ Hãy thêm đủ trick vào cả 3 nhóm trước nhé!"
        page.update()

    # --- CHỨC NĂNG CHỌN VIDEO TỪ ĐIỆN THOẠI ---
    selected_video_path = ""
    def on_file_result(e):
        nonlocal selected_video_path
        if e.files:
            selected_video_path = e.files[0].name
            txt_file_status.value = f"✅ Đã chọn video: {selected_video_path}"
            txt_file_status.color = ft.Colors.GREEN_400
        else:
            selected_video_path = ""
            txt_file_status.value = "❌ Chưa chọn video nào"
            txt_file_status.color = ft.Colors.RED_400
        page.update()

    file_picker = ft.FilePicker()
    file_picker.on_result = on_file_result
    page.overlay.append(file_picker)

    # --- GIAO DIỆN POPUP THÊM TRICK ---
    input_name = ft.TextField(label="Tên động tác / Trick", hint_text="Ví dụ: Superman...")
    dropdown_type = ft.Dropdown(
        label="Phân loại nhóm",
        options=[ft.dropdown.Option("Intro"), ft.dropdown.Option("Main Trick"), ft.dropdown.Option("Outro")],
    )
    txt_file_status = ft.Text("Chưa chọn file video (Tùy chọn)", color=ft.Colors.WHITE54)

    def save_trick(e):
        nonlocal selected_video_path
        name = input_name.value
        trick_type = dropdown_type.value
        if name and trick_type:
            video_to_save = selected_video_path if selected_video_path else "No Video"
            kho_trick[trick_type].append({"name": name, "video": video_to_save})
            update_list_view()
            dialog.open = False
            input_name.value = ""
            dropdown_type.value = None
            selected_video_path = ""
            txt_file_status.value = "Chưa chọn file video (Tùy chọn)"
            page.update()

    dialog = ft.AlertDialog(
        title=ft.Text("Thêm Trick Mới 💃"),
        content=ft.Column([
            input_name, dropdown_type,
            ft.ElevatedButton("Mở Kho Ảnh/Video 📱", icon=ft.Icons.IMAGE, on_click=lambda _: file_picker.pick_files(file_type=ft.FilePickerFileType.VIDEO)),
            txt_file_status
        ], tight=True, spacing=15),
        actions=[
            ft.TextButton("Hủy", on_click=lambda _: setattr(dialog, "open", False) or page.update()),
            ft.ElevatedButton("LƯU TRICK", bgcolor=ft.Colors.PINK_500, color=ft.Colors.WHITE, on_click=save_trick),
        ],
    )
    page.overlay.append(dialog)

    # --- GIAO DIỆN MÀN HÌNH CHÍNH ---
    page.add(
        ft.Text("POLE DANCE COMBO", size=24, weight=ft.FontWeight.BOLD),
        ft.Divider(height=5, color=ft.Colors.TRANSPARENT),
        
        # 1. KHU VỰC HIỂN THỊ COMBO NGẪU NHIÊN
        ft.Container(
            content=ft.Column([
                ft.Text("COMBO HÔM NAY CỦA BẠN:", size=12, color=ft.Colors.WHITE54, weight=ft.FontWeight.BOLD),
                txt_combo_intro,
                txt_combo_main,
                txt_combo_outro
            ], spacing=8),
            padding=15,
            border_radius=12,
            bgcolor=ft.Colors.WHITE10,
            border=ft.Border.all(1, ft.Colors.WHITE24),
            width=320
        ),
        ft.Divider(height=10, color=ft.Colors.TRANSPARENT),
        
        # NÚT BẤM TẠO COMBO (ĐÃ XÓA PADDING GÂY LỖI)
        ft.ElevatedButton(
            "XOAY COMBO NGẪU NHIÊN 💃🎲",
            bgcolor=ft.Colors.PINK_500,
            color=ft.Colors.WHITE,
            on_click=generate_random_combo,
            width=280
        ),
        
        ft.Divider(height=15, color=ft.Colors.WHITE24),
        
        # NÚT BẤM THÊM TRICK VÀO KHO
        ft.Row(
            controls=[
                ft.OutlinedButton(
                    "THÊM TRICK VÀO KHO", 
                    icon=ft.Icons.ADD,
                    style=ft.ButtonStyle(
                        color=ft.Colors.PINK_300,
                        # ĐỂ CHỮ IN ĐẬM: Thêm text_style với thuộc tính weight ở đây
                        text_style=ft.TextStyle(weight="bold") 
                    ),
                    on_click=lambda _: setattr(dialog, "open", True) or page.update(),
                    width=220
                )
            ],
            alignment=ft.MainAxisAlignment.CENTER
        ),
        ft.Divider(height=10, color=ft.Colors.TRANSPARENT),
        
        # 2. KHU VỰC QUẢN LÝ KHO LƯU TRỮ
        ft.Text("DANH SÁCH ĐÃ LƯU", size=14, color=ft.Colors.WHITE54, weight=ft.FontWeight.BOLD),
        ft.Column([group_intro, group_main, group_outro], spacing=5, width=320)
    )

    update_list_view()

app = ft.app(target=main, export_asgi=True)

import flet as ft
import random
import time

def main(page: ft.Page):
    page.title = "Pole Dance Notebook"
    page.theme_mode = ft.ThemeMode.DARK
    page.horizontal_alignment = ft.CrossAxisAlignment.CENTER
    page.scroll = "adaptive"

    # Cấu hình chuẩn duy nhất để hiện Icon múa cột và né lỗi chữ P
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

    # Kích hoạt màn hình chờ 2 giây chuyên nghiệp
    page.update()
    time.sleep(2)
    
    # 1. KHO DỮ LIỆU GỐC (Đã đồng bộ hóa sang lưu trữ HÌNH ẢNH)
    kho_trick = {
        "Intro": [
            {"name": "Đi bộ quanh cột", "image": None},
            {"name": "Xoay hông dạo đầu", "image": None},
            {"name": "Hook xoay", "image": None}
        ],
        "Main Trick": [
            {"name": "Superman", "image": None},
            {"name": "Gemini", "image": None},
            {"name": "Inverted Scorpio", "image": None}
        ],
        "Outro": [
            {"name": "Floorwork kết bài", "image": None},
            {"name": "Slide xuống nhẹ nhàng", "image": None}
        ]
    }

    # Biến tạm để hứng dữ liệu ảnh vừa chọn từ iPhone
    selected_image_data = None

    # --- CÁC THÀNH PHẦN HIỂN THỊ DANH SÁCH ---
    group_intro = ft.ExpansionTile(title=ft.Text("Intro 🎬", size=18, weight=ft.FontWeight.BOLD, color=ft.Colors.PINK_300))
    group_main = ft.ExpansionTile(title=ft.Text("Main Trick 💎", size=18, weight=ft.FontWeight.BOLD, color=ft.Colors.PURPLE_300))
    group_outro = ft.ExpansionTile(title=ft.Text("Outro 🏁", size=18, weight=ft.FontWeight.BOLD, color=ft.Colors.BLUE_300))

    def update_list_view():
        # Làm sạch danh sách trước khi nạp mới
        if group_intro.controls is None: group_intro.controls = []
        else: group_intro.controls.clear()
            
        if group_main.controls is None: group_main.controls = []
        else: group_main.controls.clear()
            
        if group_outro.controls is None: group_outro.controls = []
        else: group_outro.controls.clear()

        # Hiển thị danh sách Intro (ĐÃ XÓA SẠCH CHỮ FIT GÂY LỖI)
        for item in kho_trick.get("Intro", []):
            trailing_widget = ft.Image(src_base64=item["image"], width=40, height=40, border_radius=5) if item["image"] else ft.Icon(ft.Icons.IMAGE_NOT_SUPPORTED, color=ft.Colors.WHITE24)
            group_intro.controls.append(ft.ListTile(leading=ft.Icon(ft.Icons.STAR_BORDER, color=ft.Colors.PINK_300), title=ft.Text(item["name"], weight=ft.FontWeight.BOLD), trailing=trailing_widget))

        # Hiển thị danh sách Main Trick
        for item in kho_trick.get("Main Trick", []):
            trailing_widget = ft.Image(src_base64=item["image"], width=40, height=40, border_radius=5) if item["image"] else ft.Icon(ft.Icons.IMAGE_NOT_SUPPORTED, color=ft.Colors.WHITE24)
            group_main.controls.append(ft.ListTile(leading=ft.Icon(ft.Icons.STAR_BORDER, color=ft.Colors.PURPLE_300), title=ft.Text(item["name"], weight=ft.FontWeight.BOLD), trailing=trailing_widget))

        # Hiển thị danh sách Outro
        for item in kho_trick.get("Outro", []):
            trailing_widget = ft.Image(src_base64=item["image"], width=40, height=40, border_radius=5) if item["image"] else ft.Icon(ft.Icons.IMAGE_NOT_SUPPORTED, color=ft.Colors.WHITE24)
            group_outro.controls.append(ft.ListTile(leading=ft.Icon(ft.Icons.STAR_BORDER, color=ft.Colors.BLUE_300), title=ft.Text(item["name"], weight=ft.FontWeight.BOLD), trailing=trailing_widget))
        page.update()

    # --- THÀNH PHẦN HIỂN THỊ KẾT QUẢ RANDOM COMBO ---
    txt_combo_intro = ft.Text("Intro: ---", size=16, color=ft.Colors.PINK_200)
    txt_combo_main = ft.Text("Main Trick: ---", size=16, color=ft.Colors.PURPLE_200, weight=ft.FontWeight.BOLD)
    txt_combo_outro = ft.Text("Outro: ---", size=16, color=ft.Colors.BLUE_200)
    
    # ĐÃ XÓA SẠCH CHỮ FIT GÂY LỖI Ở ĐÂY
    img_preview_intro = ft.Image(src="",width=50, height=50, border_radius=8, visible=False)
    img_preview_main = ft.Image(src="",width=50, height=50, border_radius=8, visible=False)
    img_preview_outro = ft.Image(src="",width=50, height=50, border_radius=8, visible=False)

    def generate_random_combo(e):
        if len(kho_trick.get("Intro", [])) > 0 and len(kho_trick.get("Main Trick", [])) > 0 and len(kho_trick.get("Outro", [])) > 0:
            trick_intro = random.choice(kho_trick["Intro"])
            trick_main = random.choice(kho_trick["Main Trick"])
            trick_outro = random.choice(kho_trick["Outro"])
            
            # Cập nhật chữ và hiện ảnh cho nhóm Intro
            txt_combo_intro.value = f"🎬 {trick_intro['name']}"
            if trick_intro["image"]: img_preview_intro.src_base64 = trick_intro["image"]; img_preview_intro.visible = True
            else: img_preview_intro.visible = False
                
            # Cập nhật chữ và hiện ảnh cho nhóm Main Trick
            txt_combo_main.value = f"💎 {trick_main['name']}"
            if trick_main["image"]: img_preview_main.src_base64 = trick_main["image"]; img_preview_main.visible = True
            else: img_preview_main.visible = False
                
            # Cập nhật chữ và hiện ảnh cho nhóm Outro
            txt_combo_outro.value = f"🏁 {trick_outro['name']}"
            if trick_outro["image"]: img_preview_outro.src_base64 = trick_outro["image"]; img_preview_outro.visible = True
            else: img_preview_outro.visible = False
        else:
            txt_combo_main.value = "⚠️ Hãy thêm đủ trick vào cả 3 nhóm trước nhé!"
        page.update()

    # --- BỘ CHỌN ẢNH TỪ ĐIỆN THOẠI (FilePicker) ---
    def on_file_picker_result(e: ft.FilePickerResultEvent):
        nonlocal selected_image_data
        if e.files:
            selected_image_data = e.files[0].base64
            btn_upload.text = "📸 Đã chọn ảnh thành công!"
            btn_upload.bgcolor = ft.Colors.GREEN_700
        else:
            selected_image_data = None
            btn_upload.text = "CHỌN ẢNH TỪ IPHONE (Tùy chọn)"
            btn_upload.bgcolor = ft.Colors.PINK_900
        page.update()

    file_picker = ft.FilePicker(on_result=on_file_picker_result)
    page.overlay.append(file_picker)

    # --- GIAO DIỆN POPUP THÊM TRICK ---
    input_name = ft.TextField(label="Tên động tác / Trick", hint_text="Ví dụ: Superman...")
    dropdown_type = ft.Dropdown(
        label="Phân loại nhóm",
        options=[ft.dropdown.Option("Intro"), ft.dropdown.Option("Main Trick"), ft.dropdown.Option("Outro")],
    )
    btn_upload = ft.ElevatedButton(
        "CHỌN ẢNH TỪ IPHONE (Tùy chọn)",
        icon=ft.Icons.CAMERA_ALT,
        bgcolor=ft.Colors.PINK_900,
        color=ft.Colors.WHITE,
        on_click=lambda _: file_picker.pick_files(file_type=ft.FilePickerFileType.IMAGE, allow_multiple=False)
    )    

    def save_trick(e):
        nonlocal selected_image_data
        name = input_name.value
        trick_type = dropdown_type.value
        if name and trick_type:
            kho_trick[trick_type].append({"name": name, "image": selected_image_data})
            
            update_list_view()
            dialog.open = False
            input_name.value = ""
            dropdown_type.value = None
            selected_image_data = None
            btn_upload.text = "CHỌN ẢNH TỪ IPHONE (Tùy chọn)"
            btn_upload.bgcolor = ft.Colors.PINK_900
            page.update()

    dialog = ft.AlertDialog(
        title=ft.Text("Thêm Trick Mới 💃"),
        content=ft.Column([input_name, dropdown_type, btn_upload], tight=True, spacing=15),
        actions=[
            ft.TextButton("Hủy", on_click=lambda _: setattr(dialog, "open", False) or page.update()),
            ft.ElevatedButton("LƯU TRICK", bgcolor=ft.Colors.PINK_500, color=ft.Colors.WHITE, on_click=save_trick),
        ],
    )
    page.overlay.append(dialog)

    # --- GIAO DIỆN MÀN HÌNH CHÍNH ---
    page.add(
        ft.Text("POLE DANCE NOTEBOOK", size=24, weight=ft.FontWeight.BOLD),
        ft.Divider(height=5, color=ft.Colors.TRANSPARENT),
        
        ft.Container(
            content=ft.Column([
                ft.Text("COMBO HÔM NAY CỦA BẠN:", size=12, color=ft.Colors.WHITE54, weight=ft.FontWeight.BOLD),
                ft.Row([txt_combo_intro, img_preview_intro], alignment=ft.MainAxisAlignment.SPACE_BETWEEN, width=290),
                ft.Row([txt_combo_main, img_preview_main], alignment=ft.MainAxisAlignment.SPACE_BETWEEN, width=290),
                ft.Row([txt_combo_outro, img_preview_outro], alignment=ft.MainAxisAlignment.SPACE_BETWEEN, width=290),
            ], spacing=8),
            padding=15,
            border_radius=12,
            bgcolor=ft.Colors.WHITE10,
            border=ft.Border.all(1, ft.Colors.WHITE24),
            width=320
        ),
        ft.Divider(height=10, color=ft.Colors.TRANSPARENT),
        
        # NÚT XOAY COMBO
        ft.Row(
            controls=[
                ft.ElevatedButton("XOAY COMBO NGẪU NHIÊN 💃🎲", bgcolor=ft.Colors.PINK_500, color=ft.Colors.WHITE, on_click=generate_random_combo, width=280)
            ],
            alignment=ft.MainAxisAlignment.CENTER
        ),
        ft.Divider(height=15, color=ft.Colors.WHITE24),
        
        # NÚT THÊM TRICK
        ft.Row(
            controls=[
                ft.OutlinedButton(
                    "THÊM TRICK VÀO KHO", 
                    icon=ft.Icons.ADD,
                    style=ft.ButtonStyle(color=ft.Colors.PINK_300, text_style=ft.TextStyle(weight="bold")),
                    on_click=lambda _: setattr(dialog, "open", True) or page.update(),
                    width=220
                )
            ],
            alignment=ft.MainAxisAlignment.CENTER
        ),
        ft.Divider(height=10, color=ft.Colors.TRANSPARENT),
        
        ft.Text("DANH SÁCH ĐÃ LƯU", size=14, color=ft.Colors.WHITE54, weight=ft.FontWeight.BOLD),
        ft.Column([group_intro, group_main, group_outro], spacing=5, width=320)
    )

    update_list_view()

ft.app(target=main)

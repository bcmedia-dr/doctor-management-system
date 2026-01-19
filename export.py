from openpyxl import Workbook
from openpyxl.styles import Font, PatternFill, Alignment, Border, Side
from datetime import datetime
import os

def export_doctors_to_excel(doctors):
    """匯出醫師資料到 Excel"""
    wb = Workbook()
    sheet = wb.active
    sheet.title = "醫師資料"
    
    # 設定標題列（與表格顯示順序完全一致）
    # 表格順序：編號、醫師、科別、性別、狀態、聯絡窗口、報價區間、經營社群、醫師社群、合作品牌、操作
    # 匯出順序：編號、醫師、科別、性別、狀態、聯絡窗口、報價區間、經營社群、醫師社群、合作品牌、建立時間、更新時間
    headers = ['編號', '醫師', '科別', '性別', '狀態', '聯絡窗口', '報價區間', '經營社群', '醫師社群', '合作品牌', '建立時間', '更新時間']
    sheet.append(headers)
    
    # 設定標題列樣式
    header_fill = PatternFill(start_color='4472C4', end_color='4472C4', fill_type='solid')
    header_font = Font(bold=True, color='FFFFFF', size=12)
    
    for col_num, header in enumerate(headers, 1):
        cell = sheet.cell(row=1, column=col_num)
        cell.fill = header_fill
        cell.font = header_font
        cell.alignment = Alignment(horizontal='center', vertical='center')
    
    # 寫入資料
    for index, doctor in enumerate(doctors, 1):
        row_data = [
            index,  # 使用索引+1作为编号
            doctor.email or '',
            doctor.specialty or '',
            doctor.gender or '',
            doctor.status or '',
            doctor.contact_person or '',
            doctor.price_range or '',
            doctor.has_social_media or '',
            doctor.social_media_link or '',
            doctor.current_brand or '',
            doctor.created_at.strftime('%Y-%m-%d %H:%M:%S') if doctor.created_at else '',
            doctor.updated_at.strftime('%Y-%m-%d %H:%M:%S') if doctor.updated_at else ''
        ]
        sheet.append(row_data)
    
    # 調整欄寬
    column_widths = {
        'A': 8,   # 編號
        'B': 25,  # 醫師
        'C': 12,  # 科別
        'D': 8,   # 性別
        'E': 12,  # 狀態
        'F': 12,  # 聯絡窗口
        'G': 15,  # 報價區間
        'H': 12,  # 經營社群
        'I': 30,  # 醫師社群
        'J': 20,  # 合作品牌
        'K': 20,  # 建立時間
        'L': 20   # 更新時間
    }
    
    for col, width in column_widths.items():
        sheet.column_dimensions[col].width = width
    
    # 設定資料列樣式
    thin_border = Border(
        left=Side(style='thin'),
        right=Side(style='thin'),
        top=Side(style='thin'),
        bottom=Side(style='thin')
    )
    
    for row in sheet.iter_rows(min_row=1, max_row=sheet.max_row, min_col=1, max_col=len(headers)):
        for cell in row:
            cell.border = thin_border
            if cell.row > 1:  # 資料列
                cell.alignment = Alignment(horizontal='left', vertical='center')
    
    # 凍結首列
    sheet.freeze_panes = 'A2'
    
    # 儲存檔案（確保UTF-8編碼支持）
    file_path = f'/tmp/doctors_export_{datetime.now().strftime("%Y%m%d_%H%M%S")}.xlsx'
    # openpyxl 自動處理 UTF-8 編碼，無需額外設置
    wb.save(file_path)
    
    return file_path

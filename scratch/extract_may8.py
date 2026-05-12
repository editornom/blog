def main():
    try:
        with open(r'c:\Users\haionnet\Desktop\editornom\scratch\checker_result_utf8.txt', 'r', encoding='utf-8') as f:
            lines = f.readlines()
    except Exception as e:
        print(f"Error reading file: {e}")
        return
    
    current_file = None
    current_lines = []
    
    file_sections = []
    
    for line in lines:
        stripped = line.strip()
        # Detect if it's a new file header line
        is_header = False
        if stripped.startswith('✅') or stripped.startswith('❌') or stripped.startswith('📂 File:'):
            is_header = True
            
        if is_header:
            if current_file:
                file_sections.append((current_file, current_lines))
            current_file = stripped
            current_lines = [line]
        else:
            if current_file:
                current_lines.append(line)
                
    if current_file:
        file_sections.append((current_file, current_lines))
        
    # Write report
    report_lines = [
        "========================================================================",
        "QUALITY REPORT FOR POSTS FROM MAY 8TH ONWARDS",
        "========================================================================"
    ]
    
    for filename, file_lines in file_sections:
        # Check if filename has 260508, 260509, 260510
        if any(d in filename for d in ['260508', '260509', '260510']):
            report_lines.append("\n" + "="*80)
            report_lines.append(f"FILE HEADER: {filename}")
            report_lines.append("="*80)
            report_lines.extend([l.rstrip() for l in file_lines[1:]])
            
    try:
        with open(r'c:\Users\haionnet\Desktop\editornom\scratch\may8_report.txt', 'w', encoding='utf-8') as f:
            f.write("\n".join(report_lines))
        print(f"Success! Wrote report with {len(file_sections)} parsed sections.")
    except Exception as e:
        print(f"Error writing file: {e}")

if __name__ == '__main__':
    main()

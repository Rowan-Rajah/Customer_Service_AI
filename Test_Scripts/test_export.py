from export_manager import (
    load_conversation_log,
    export_csv,
    export_excel
)

print("Testing PostgreSQL conversation export...")

# ---------------------------------------------------------
# Load conversation records
# ---------------------------------------------------------

df = load_conversation_log()

print("\nConversation log:")
print(df)

print("\nNumber of records:")
print(len(df))


# ---------------------------------------------------------
# Test CSV export
# ---------------------------------------------------------

csv_path = "../exports/test_conversation_export.csv"

export_csv(csv_path)

print("\nCSV export successful!")
print(f"CSV file created at: {csv_path}")


# ---------------------------------------------------------
# Test Excel export
# ---------------------------------------------------------

excel_path = "../exports/test_conversation_export.xlsx"

export_excel(excel_path)

print("\nExcel export successful!")
print(f"Excel file created at: {excel_path}")


print("\nExport test completed successfully!")


from tools import ocr_engine

result = ocr_engine.extract_from_pdf("statement.pdf")
print(result["text"])